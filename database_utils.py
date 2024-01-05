from sqlalchemy import create_engine, inspect
from sqlalchemy.exc  import SQLAlchemyError
import pandas as pd
import psycopg2
import sqlalchemy
import yaml


class DatabaseConnector():
    """
    This class connects to a PostgreSQL database and provides methods to interact with it.
    
    Parameters:
    - file_path (str): Path to the YAML file containing database credentials.
    """

    def __init__(self, file_path):
        """
        Initializes the DatabaseConnector instance.

        Parameters:
        - file_path (str): Path to the YAML file containing database credentials.
        """  
        self.file_path = file_path
        self.db_creds = self.read_db_creds()
        self.db_engine = self.init_db_engine()
        
    def read_db_creds(self):
        """
        Reads and returns the database credentials from the specified YAML file.
        """
        with open(self.file_path, 'r') as file:
            db_creds = yaml.safe_load(file)
        return db_creds
    
    def init_db_engine(self):
        """
        Initializes and returns a SQLAlchemy database engine using the provided credentials.

        Returns:
        - sqlalchemy.engine.base.Engine: Database engine.
        """
        database_url = (
        f"postgresql://{self.db_creds['RDS_USER']}:{self.db_creds['RDS_PASSWORD']}"
        f"@{self.db_creds['RDS_HOST']}:{self.db_creds['RDS_PORT']}/{self.db_creds['RDS_DATABASE']}"
        )
        db_engine = create_engine(database_url)
        return db_engine
    
    def list_db_tables(self):
        """
        Returns a list of table names present in the connected database.
        """
        inspector = inspect(self.db_engine)
        db_table_list = inspector.get_table_names()
        return db_table_list
    
    def upload_to_db(self, clean_dataframe, table_name: str):
        """
        Uploads a DataFrame to a specified table in the database. If the table exists, it is replaced.
        Optionally sets a primary key on the specified column after the upload.

        Parameters:
            df (pd.DataFrame): The DataFrame to upload.
            table_name (str): The name of the target table in the database.
            primary_key (str, optional): The column name to be set as the primary key.
        """
        if not isinstance(clean_dataframe, pd.DataFrame):
            raise ValueError("df must be a pandas DataFrame")

        try:
            engine = self.init_db_engine()
            with engine.begin() as conn:
                clean_dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Data uploaded successfully to table '{table_name}'")
        except SQLAlchemyError as e:
            print("An error occurred while uploading data to the database:", e)
    
if __name__ == "__main__":
    pass