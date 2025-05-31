import os
import oracledb as ora
import dlt
from dlt.sources import incremental
from datetime import datetime, timezone

# Inicializa modo thick
ora.init_oracle_client(lib_dir="/.oracle/instantclient_19_23")


def ora_source(table_name: str):

    # Carrega configuracoes de extracao do config.toml
    included_columns = dlt.config.get(f"sources.sql_database.{table_name}.included_columns")
    campo_incremental = dlt.config.get(f"sources.sql_database.{table_name}.incremental_column")
    chave_primaria = dlt.config.get(f"sources.sql_database.{table_name}.primary_key")
    data_inicial = dlt.config.get(f"sources.sql_database.{table_name}.initial_value")

    # Formatação data inicial
    initial_value = datetime.strptime(data_inicial, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    columns_str = ", ".join(included_columns)

    @dlt.resource(name=table_name, write_disposition="merge", primary_key=chave_primaria)
    def resource_dinamico_ora(**kwargs):

        incremental_column_value = kwargs.get(campo_incremental, initial_value)

        conn = None

        try:
            conn = ora.connect(
                user=os.getenv("ORACLE_USER"),
                password=os.getenv("ORACLE_PASSWORD"),
                dsn=f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"
            )

            with conn.cursor() as cursor:

                print(f"[DEBUG] Valor incremental recebido: {incremental_column_value}")
                bind_lv = cursor.var(ora.DATETIME)
                bind_lv.setvalue(0, incremental_column_value or initial_value)

                query = f"""
                    SELECT {columns_str}
                    FROM DBAMV.{table_name}
                    WHERE {campo_incremental} > :last_value
                    ORDER BY {campo_incremental} ASC
                """

                print(f"[DEBUG] Query: {query.strip()}")
                cursor.execute(query, last_value=bind_lv)
                col_names = [col[0] for col in cursor.description]
                for row in cursor:
                    print(f"[DEBUG] Linha extraída: {row}")
                    yield dict(zip(col_names, row))

        except Exception as e:
            print(f"Erro ao conectar ou buscar dados no Oracle:\n {e}")
            raise
        finally:
            if conn:
                conn.close()

    return resource_dinamico_ora
