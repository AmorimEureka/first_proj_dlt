import dlt

from conn_ora_mv import load_data_ora

if __name__ == "__main__":

    try:

        table_names = dlt.config.get("sources.sql_database.table_names")

        pipeline = dlt.pipeline(
            pipeline_name="test_oracle",
            destination="postgres",
            dataset_name="raw_mv"
        )

        for tabela in table_names:
            load_mv = pipeline.run(load_data_ora(tabela), table_name=tabela)
            print(f"{load_mv}")

    except Exception as e:
        print(f"Error na pipeline:\n {e}")
