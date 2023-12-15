import yaml
import sqlalchemy
from sqlalchemy import create_engine

class DatabaseConnector: 
    def __init__(self, RDS_HOST, RDS_PASSWORD, RDS_USER, RDS_DATABASE, RDS_PORT):
        self.RDS_HOST = RDS_HOST
        self.RDS_PASSWORD = RDS_PASSWORD
        self.RDS_USER = RDS_USER
        self.RDS_DATABASE = RDS_DATABASE
        self.RDS_PORT = RDS_PORT

    def read_db_creds(cls, file_path = '/Users/TheBoss/Desktop/AICore/retail_data_project/db_creds.yaml'):
        with open(file_path, 'r') as file:
                creds = yaml.safe_load(file)
                return creds
        
    def init_db_engine(cls, file_path = '/Users/TheBoss/Desktop/AICore/retail_data_project/db_creds.yaml'):
        creds = cls.read_db_creds(file_path)

        if creds:
            db_url = sqlalchemy.engine.url.URL(
                drivername = 'mysql',  # Change this to your database type if needed
                username = creds['RDS_USER'],
                password = creds['RDS_PASSWORD'],
                host = creds['RDS_HOST'],
                port = creds['RDS_PORT'],
                database = creds['RDS_DATABASE']
            )

            engine = create_engine(db_url)
            return engine
        
    def list_db_tables(cls, engine):
        with engine.connect() as connection:
            result = connection.execute("SHOW TABLES;")
            tables = [table[0] for table in result.fetchall()]
            return tables
        
    def upload_to_db(cls, df, table_name):
        df.to_sql(name=table_name, con=cls.init_db_engine(), index=False, if_exists='replace')
        print(f"Data uploaded to {table_name} successfully.")