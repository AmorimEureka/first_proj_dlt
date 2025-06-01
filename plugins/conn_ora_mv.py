import os
import oracledb as ora
import dlt
from dlt.sources import incremental
from datetime import datetime, timezone

# Inicializa modo thick
ora.init_oracle_client(lib_dir="/.oracle/instantclient_19_23")


def ora_source(table_name: str):

    # Carrega configuracoes de extracao do config.toml.
    confi_campos_tabelas = dlt.config.get(f"sources.sql_database.{table_name}.included_columns")
    config_cursor_campo_incremental = dlt.config.get(f"sources.sql_database.{table_name}.incremental_column")
    config_chave_primaria = dlt.config.get(f"sources.sql_database.{table_name}.primary_key")
    config_data_inicial = dlt.config.get(f"sources.sql_database.{table_name}.initial_value")

    valor_inicial = datetime.strptime(config_data_inicial, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    campos_consulta = ", ".join(confi_campos_tabelas)

    @dlt.resource(name=table_name, write_disposition="merge", primary_key=config_chave_primaria)
    def resource_dinamico_ora(**kwargs):

        cursor_campo_incremental = kwargs.get(config_cursor_campo_incremental, valor_inicial)

        conn = None

        try:
            conn = ora.connect(
                user=os.getenv("ORACLE_USER"),
                password=os.getenv("ORACLE_PASSWORD"),
                dsn=f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"
            )

            with conn.cursor() as cursor:

                # Variavel c/ data inicial ou mais rescente.
                bind_last_value = cursor.var(ora.DATETIME)                              # [doc_ora .var()]-Bind Variable OUT-Para setar tipo, tamanho do dado retornado.
                bind_last_value.setvalue(0, cursor_campo_incremental or valor_inicial)  # [doc_ora .setvalue()]-Bind Variable IN/OUT-Para setar valor inicial
                                                                                        # e retornar dados.

                query = f"""
                    SELECT {campos_consulta}
                    FROM DBAMV.{table_name}
                    WHERE {config_cursor_campo_incremental} > :last_value
                    ORDER BY {config_cursor_campo_incremental} ASC
                """

                cursor.execute(query, last_value=bind_last_value)

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
