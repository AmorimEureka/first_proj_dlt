import oracledb as ora
import os

import dlt

# Inicializa modo thick
ora.init_oracle_client(lib_dir="/.oracle/instantclient_19_23")


def load_data_ora(table_name: str):
    try:

        included_columns = dlt.config.get(f"sources.sql_database.{table_name}.included_columns")
        columns_str = ", ".join(included_columns)

        conn = ora.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"
        )

        print("Conectei no Oracle!")

        with conn.cursor() as cursor:
            consulta = f"""
                WITH ATEND AS (
                    SELECT
                        {columns_str}
                    FROM DBAMV.{table_name}
                    ORDER BY DT_ATENDIMENTO DESC
                )
                SELECT * FROM ATEND WHERE ROWNUM <= 15
            """

            cursor.execute(consulta)

            col_names = [col[0].lower() for col in cursor.description]
            for row in cursor:
                yield dict(zip(col_names, row))

    except Exception as e:
        print(f"Erro ao conectar ou buscar dados no Oracle: {e}")
        raise
    finally:
        if conn:
            conn.close()
