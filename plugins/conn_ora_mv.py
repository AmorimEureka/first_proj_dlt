import os
import oracledb as ora
import dlt
from dlt.sources import incremental
from datetime import datetime, timezone

# Inicializa modo thick
ora.init_oracle_client(lib_dir="/.oracle/instantclient_19_23")


@dlt.source
def ora_source(table_name: str):
    # Carrega configurações da tabela via config.toml
    included_columns = dlt.config.get(f"sources.sql_database.{table_name}.included_columns")
    campo_incremental = dlt.config.get(f"sources.sql_database.{table_name}.incremental_column")
    chave_primaria = dlt.config.get(f"sources.sql_database.{table_name}.primary_key")
    data_inicial = dlt.config.get(f"sources.sql_database.{table_name}.initial_value")

    # Formatação inicial
    initial_value = datetime.strptime(data_inicial, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    columns_str = ", ".join(included_columns)

    @dlt.resource(
        name=table_name,
        write_disposition="merge"
    )
    def resource_dinamico_ora(
        last_value=incremental(
            cursor_path=campo_incremental,
            initial_value=initial_value,
            primary_key=chave_primaria,
            row_order="asc"
        )
    ):
        conn = None
        try:
            conn = ora.connect(
                user=os.getenv("ORACLE_USER"),
                password=os.getenv("ORACLE_PASSWORD"),
                dsn=f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"
            )

            with conn.cursor() as cursor:
                for lv in last_value:
                   # print(f"[DEBUG] last_value = {lv} | type = {type(lv)}")

                    # Garante tipo datetime com timezone, ignora placeholder
                    if isinstance(lv, str):
                        try:
                            lv = datetime.fromisoformat(lv).replace(tzinfo=timezone.utc)
                        except ValueError:
                            print(f"[WARN] Ignorando valor inválido para last_value: {lv}")
                            continue

                    bind_lv = cursor.var(ora.DATETIME)
                    bind_lv.setvalue(0, lv)

                    query = f"""
                        SELECT {columns_str}
                        FROM DBAMV.{table_name}
                        WHERE {campo_incremental} > :last_value
                        ORDER BY {campo_incremental} ASC
                    """

                    cursor.execute(query, last_value=bind_lv)
                    col_names = [col[0] for col in cursor.description]
                    for row in cursor:
                        yield dict(zip(col_names, row))

        except Exception as e:
            print(f"Erro ao conectar ou buscar dados no Oracle:\n {e}")
            raise
        finally:
            if conn:
                conn.close()

    return [resource_dinamico_ora()]