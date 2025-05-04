import os
import dlt
import oracledb
from sqlalchemy import create_engine
from dlt.sources.sql_database import sql_database

oracledb.init_oracle_client(lib_dir="/.oracle/instantclient_19_23")

username = os.getenv("ORACLE_USER")
password = os.getenv("ORACLE_PASSWORD")
host = os.getenv("ORACLE_HOST")
port = os.getenv("ORACLE_PORT")
service_name = os.getenv("ORACLE_SERVICE")

dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))(CONNECT_DATA=(SERVICE_NAME={service_name})))"

engine = create_engine(
    f"oracle+oracledb://{username}:{password}@/?dsn={dsn}"
)


def load_database_data() -> None:
    source_factory = sql_database()
    source = source_factory(engine=engine, table_names=["ATENDIME"])

    pipeline = dlt.pipeline(
        pipeline_name="pipeline_teste_ora_postgres",
        destination="postgres",
        dataset_name="raw_mv_dlt"
    )

    load_info = pipeline.run(source)
    print(load_info)


# Função principal de carga de dados
# def load_database_data() -> None:
#     print("🚀 Iniciando extração da tabela ATENDIME...")

#     # Define a fonte de dados Oracle
#     source_factory = sql_database()
#     source = source_factory(engine=engine, table_names=["ATENDIME"])

#     # (Opcional) Testa leitura de uma linha para verificar acesso
#     for row in source:
#         print("🔍 Amostra de dado:", row)
#         break

#     # Define pipeline dlt
#     pipeline = dlt.pipeline(
#         pipeline_name="pipeline_teste_ora_postgres",
#         destination="postgres",
#         dataset_name="raw_mv_dlt"  # Certifique-se de que esse schema existe no Postgres
#     )

#     # Executa carga
#     load_info = pipeline.run(source)
#     print("✅ Carga finalizada. Detalhes:")
#     print(load_info)


# # Executa a função principal
# if __name__ == "__main__":
#     load_database_data()
