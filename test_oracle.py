import dlt
from conn_ora_mv import ora_source


def multiple_sources():

    table_names = dlt.config.get("sources.sql_database.table_names")

    resources = []

    for tabela in table_names:

        resources.append(ora_source(tabela))

    return resources


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="test_oracle",
        destination="postgres",
        dataset_name="raw_mv"
    )

    load_info = pipeline.run(multiple_sources())
    print("Resultado do pipeline:", load_info)
