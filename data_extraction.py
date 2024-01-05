from database_utils import DatabaseConnector
import pandas as pd
import tabula 
import requests
import boto3

class DataExtractor():
    """
    This class extracts data from different data sources.
    e.g. CSV fies, API, S3 bucket.
    """
    def __init__(self):
        """
        Initializes the DataExtractor instance.
        """
        self.db_connector = DatabaseConnector("/Users/TheBoss/Desktop/AICore/retail_data_project/db_creds.yaml")
        self.db_engine = self.db_connector.db_engine
        self.db_creds = self.db_connector.db_creds

    def read_rds_table(self, table_name):
        """
        Reads data from a specified table in an RDS database and returns it as a pandas DataFrame.

        Parameters:
        - table_name (str): Name of the table to read from.

        Returns:
        - table_data (pandas DataFrame): Data from the specified table.
        """
        table_data = pd.read_sql_table(table_name, self.db_engine).set_index('index')
        return table_data
    
    def retrieve_pdf_data(self, pdf_link):
        """
        Retrieves pdf file from S3 Bucket and returns a pandas DataFrame.

        Parameters:
        - pdf_link (str): Link to PDF in S3 Bucket.

        Returns: 
        - pdf_data (pandas DataFrame): Data extracted from th PDF.
        """
        try:
            pdf_pages = tabula.read_pdf(pdf_link, pages='all')
            pdf_data = pd.concat(pdf_pages, ignore_index=True)

            if pdf_data.empty:
                raise ValueError("No data found in the PDF.")

            print("PDF data retrieval successful.")
            return pdf_data

        except Exception as e:
            error_message = f"Error retrieving PDF data: {str(e)}"
            print(error_message)

    def list_number_of_stores(self, number_of_stores_endpoint, header):
        """
        Returns the number of stores in the data from the API endpoint.
        
        Parameters:
        - number_of_stores_endpoint (str): Endpoint URL for API.
        - header (dict): Credentials to connect to the API.
        
        Returns:
        - number_of_stores (int): Number of stores in the data.
        """
        response = requests.get(number_of_stores_endpoint, headers=header)
        if response.status_code == 200:
            data = response.json()
            df = pd.json_normalize(data) 
            number_of_stores = df.number_stores[0]
            print(f'Number of stores: {number_of_stores}')
            return number_of_stores
        else:
            print(f'Request failed with status code: {response.status_code}')
            print(f'Response Text: { response.text}')

    def retrieve_stores_data(self, store_endpoint, number_of_stores, header):
        """
        Retrieves data for each store from the API endpoint and returns it as a pandas DataFrame.

        Parameters:
        - store_endpoint (str): Base endpoint URL for individual store data.
        - number_of_stores (int): Number of stores to retrieve data for.
        - header (dict): Credentials to connect to the API.

        Returns:
        - store_data (pandas DataFrame): Combined data for all stores.
        """
        all_store_data = []
        for store_number in range(number_of_stores):
            response = requests.get(f'{store_endpoint}{store_number}', headers=header)
            if response.status_code == 200:
                store_data = response.json()
                all_store_data.append(store_data)
            else:
                print(f"Failed to fetch data for store {store_number}. Status code: {response.status_code}")
        store_data = pd.DataFrame(all_store_data)
        return store_data
    
    def extract_from_s3(self, s3_url):
        """
        Extracts data from an AWS S3 bucket using the provided HTTP S3 URL. This method determines the file type
        (either CSV or JSON) from the URL and reads the data into a DataFrame accordingly.

        Args:
            s3_url (str): HTTP URL to the S3 file.

        Returns:
            pd.DataFrame: DataFrame containing data extracted from the S3 file.

        Raises:
            ValueError: If the file type is neither CSV nor JSON.
        """
        # Parse bucket name and file path from s3_url
        bucket_name = s3_url.split('/')[2].split('.')[0]
        file_path = '/'.join(s3_url.split('/')[3:])

        # Determine file type from the URL
        file_type = file_path.split('.')[-1]

        # Initialise boto3 client
        s3_client = boto3.client("s3")

        # Download file and read into a DataFrame based on file type
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_path)
        if file_type.lower() == 'json':
            df = pd.read_json(obj["Body"])
        elif file_type.lower() == 'csv':
            df = pd.read_csv(obj["Body"])
        else:
            raise ValueError("Unsupported file type. Please provide a CSV or JSON file.")

        return df
    
    def extract_from_json(self, path):
        """
        Extracts a JSON file and returns a pandas DataFrame.

        Parameters:
        - path (str): Path to the JSON file.

        Returns:
        - json_data (pandas DataFrame): Data from the JSON file.
        """
        return pd.read_json(path)
    
if __name__ == "__main__":
    pass

