import pandas as pd

class DataExtractor:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def read_rds_table(self, db_connector, table_name):
        with db_connector.db_engine.connect() as connection:
            query = f"SELECT * FROM {table_name};"
            result = connection.execute(query)
            data = [dict(row) for row in result.fetchall()]
            df = pd.DataFrame(data)
            return df
        