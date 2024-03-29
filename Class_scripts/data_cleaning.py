from database_utils import DatabaseConnector
from data_extraction import DataExtractor
import numpy as np
import pandas as pd


class DataCleaning():
    """
    This class contains methods to clean data from various sources.
    """

    def __init__(self):
        """
        Initializes the DataCleaning instance.
        """
        self.db_connector = DatabaseConnector(".../db_creds.yaml")
        self.db_extractor = DataExtractor()

    def _clean_country_code(self, df):
            """
            Cleans country_code column:
            - Removes incorrect codes by setting len
            - Sets to string type

            Parameters:
            - df (pd.DataFrame): dataframe containing country_code column.
            """
            df.loc[df.country_code.str.len() > 2, 'country_code'] = np.nan
            df.country_code = df.country_code.astype('string')

    def _clean_dates(self, df, columns):
        """
        Cleans date data by  putting it in the Year-Month-Day format.
        
        Parameters:
        - df (pd.DataFrame): dataframe containing columns.
        - columns (arr): array of column names.
        """
        for column_name in columns:
            df[column_name] = pd.to_datetime(df[column_name], format='mixed', errors='coerce')
            df[column_name] = df[column_name].dt.strftime('%Y-%m-%d')

    def _clean_phone_numbers(self, df):
        """
        Clean and validate phone numbers in a DataFrame based on country codes using regular expressions (regex).

        Parameters:
        - df (pandas DataFrame): The DataFrame containing 'country_code' and 'phone_number' columns.
        """

        uk_regex = r"^(?:(?:\+44\s?\(0\)\s?\d{2,4}|\(?\d{2,5}\)?)\s?\d{3,4}\s?\d{3,4}$|\d{10,11}|\+44\s?\d{2,5}\s?\d{3,4}\s?\d{3,4})$"
        de_regex = r"(\(?([\d \-\)\–\+\/\(]+){6,}\)?([ .\-–\/]?)([\d]+))"
        us_regex = r"\(?\d{3}\)?-? *\d{3}-? *-?\d{4}"

        df.loc[
            (df["country_code"] == "GB")
            & (~df["phone_number"].astype(str).str.match(uk_regex)),
            "phone_number",
        ] = np.nan
        df.loc[
            (df["country_code"] == "DE")
            & (~df["phone_number"].astype(str).str.match(de_regex)),
            "phone_number",
        ] = np.nan
        df.loc[
            (df["country_code"] == "US")
            & (~df["phone_number"].astype(str).str.match(us_regex)),
            "phone_number",
        ] = np.nan

    def _clean_uuids(self, df, columns):
        """
        Removes incorrect uuid entries.

        Parameters:
        - df (pd.DataFrame): dataframe containing columns.
        - columns (arr): array of columns containing uuids.
        """
        for column_name in columns:    
            uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            df.loc[:,column_name] = df[column_name].astype('string')
            df.loc[~df[column_name].str.match(uuid_pattern), column_name] = np.nan

    def _clean_card_providers(self, df, column_name, categories):
        """
        Cleans column_name by filtering out values not in the provided categories.
        
        Parameters:
        - df (pd.DataFrame): dataframe containing column_name.
        - column_name (str): column containing categories.
        - categories (arr): categories that are valid in the column.
        """
        df.loc[~df[column_name].isin(categories), column_name] = np.nan
        df[column_name] = df[column_name].astype('string')


    def _clean_card_numbers(self, df):
        """
        Clean card_number by setting to string, replacing '?', and removing strings containing letters.

        Parameters:
        - df (pd.DataFrame): dataframe containing card_number column.
        """
        df['card_number']=df['card_number'].astype('string')
        df['card_number'] = df['card_number'].str.replace('?', '')
        df['card_number'] = df['card_number'].where(df['card_number'].str.contains(r'^\d+$'), np.nan)
        
        # Can't get this to work, return to it later
        '''
    def _ensure_correct_card_number_length(self, card_data):
        card_provider_length_mapping = {
            'JCB 16 digit': 16,
            'VISA 16 digit': 16,
            'Mastercard': 16,
            'Discover': 16,
            'Diners Club / Carte Blanche': 14,
            'American Express': 15,
            'JCB 15 digit': 15,
            'Maestro': 12,
            'VISA 19 digit': 19,
            'VISA 13 digit': 13
        }

        # Map the correct length for each card provider
        card_data['correct_length'] = card_data['card_provider'].map(card_provider_length_mapping)

        # Filter rows where the card_number length matches the correct_length
        card_data = card_data[card_data['card_number'].astype(str).apply(len) == card_data['correct_length']]

        # Drop the temporary 'correct_length' column
        card_data = card_data.drop(columns=['correct_length'])
        '''

    def _clean_lat_and_long(self, store_data, columns):
        """
        Cleans number data by removing letters and setting to string.

        Parameters:
        - df (pd.DataFrame): dataframe containing required columns.
        - columns (arr): array containing columns with number data from which letters will be removed.
        """
        for column in columns:
            store_data[column] = pd.to_numeric(store_data[column], errors='coerce')
            store_data[column] = store_data[column].astype('string')

    def _convert_product_weights(self, products_data):
        """
        Clean and convert the 'weight' column in the provided DataFrame to kilograms.

        Parameters:
        - products_data (pandas DataFrame): The DataFrame containing the 'weight' column to be cleaned and converted.
        """
        products_data['weight'] = products_data['weight'].apply(self._clean_and_convert_weight)

        return products_data

    def _clean_and_convert_weight(self, weight):
        """
        Clean and convert a weight string to kilograms.

        Parameters:
        - weight (str): The string representing the weight, possibly including a quantity.
        """
        try:
            
            quantity, weight_str = self._extract_quantity_and_weight(weight)

            cleaned_weight = ''.join(char for char in str(weight_str) if char.isdigit() or char in ['.', ','])

            cleaned_weight = float(cleaned_weight.replace(',', '.'))

            original_unit = str(weight_str).lower()
            if 'kg' in original_unit:
                cleaned_weight_kg = float(cleaned_weight)  
            elif 'g' in original_unit:
                cleaned_weight_kg = float(cleaned_weight / 1000)  
            elif 'oz' in original_unit:
                cleaned_weight_kg = float(cleaned_weight / 35.274)  
            elif 'ml' in original_unit:
                cleaned_weight_kg = float(cleaned_weight / 1000)
            else:
                cleaned_weight_kg = float(cleaned_weight)  

            if quantity:
                cleaned_weight_kg *= float(quantity)

            return cleaned_weight_kg
        except (ValueError, TypeError):
            print('error with converting to kg')
            return None


    def _extract_quantity_and_weight(self, weight):
        """
        Extract quantity and weight parts from a given weight string.

        Parameters:
        - weight (str): The string representing the weight, possibly including a quantity.
        """
        parts = weight.split('x', 1)
        quantity = parts[0].strip() if len(parts) > 1 else None
        weight_str = parts[-1].strip()
        return quantity, weight_str
    
    def _clean_date_numbers(self, sales_data, columns):
        """
        Clean and convert columns containing date numbers in the provided DataFrame.

        Parameters:
        - sales_data (pandas DataFrame): The DataFrame containing columns with date numbers to be cleaned.
        - columns (list): List of column names to be processed.
        """
        for column in columns:
         sales_data[column] = pd.to_numeric(sales_data[column], errors='coerce', downcast='integer')
         sales_data[column] = sales_data[column].astype('Int64').astype('string')


    def clean_user_data(self, user_data):
        """
        Cleans the provided user_data DataFrame and returns the cleaned DataFrame.
        """
        user_data = user_data.dropna().drop_duplicates()

        self._clean_country_code(user_data)
        self._clean_dates(user_data, ['join_date', 'date_of_birth']) 
        self._clean_phone_numbers(user_data)
        self._clean_uuids(user_data, ['user_uuid'])
        return user_data

    def clean_card_data(self, card_data):
        """
        Clean and process credit card data in the provided DataFrame.

        Parameters:
        - card_data (pandas DataFrame): The DataFrame containing credit card data.
        """
        self._clean_card_providers(card_data, 'card_provider', 
                               categories = ['Diners Club / Carte Blanche', 'American Express', 'JCB 16 digit',
        'JCB 15 digit', 'Maestro', 'Mastercard', 'Discover',
       'VISA 19 digit', 'VISA 16 digit', 'VISA 13 digit'])
        self._clean_card_numbers(card_data)
        #self._ensure_correct_card_number_length(card_data)
        card_data["date_payment_confirmed"] = pd.to_datetime(
            card_data["date_payment_confirmed"], format="mixed", errors="coerce"
        ).dt.date
        card_data["expiry_date"] = pd.to_datetime(
            card_data["expiry_date"], format="%m/%y", errors='coerce'
        )
        card_data = card_data.dropna().drop_duplicates()

        return card_data
    
    def clean_store_data(self, store_data):
        """
        Clean and process store data in the provided DataFrame.

        Parameters:
        - store_data (pandas DataFrame): The DataFrame containing store-related data.
        """
        store_data = store_data.drop(columns=['index','lat'])
        store_data = store_data.drop_duplicates()
        store_data.iloc[0] = store_data.iloc[0].fillna("N/A")
        store_data.loc[~store_data["country_code"].isin(["DE", "US", "GB"]), "country_code"] = np.nan

        store_data.loc[store_data["continent"] == "eeEurope", "continent"] = "Europe"
        store_data.loc[store_data["continent"] == "eeAmerica", "continent"] = "America"

        store_data['staff_numbers'] = pd.to_numeric(store_data['staff_numbers'], errors='coerce').fillna(0).astype(int)
        self._clean_dates(store_data, ['opening_date'])
        self._clean_lat_and_long(store_data, ['longitude', 'latitude'])
        self._clean_card_providers(store_data, 'store_type', categories = ['Web Portal', 'Local', 'Super Store', 'Mall Kiosk', 'Outlet'])

        return store_data
    
    def clean_products_data(self, products_data):
       """
       Clean and process product data in the provided DataFrame.

        Parameters:
        - products_data (pandas DataFrame): The DataFrame containing product-related data.
       """
       products_data = products_data.dropna().drop_duplicates()

       self._clean_dates(products_data, ['date_added'])
       self._convert_product_weights(products_data)
       self._clean_uuids(products_data, ['uuid'])
       self._clean_card_providers(products_data, 'category', categories = ['toys-and-games', 'sports-and-leisure', 'pets', 'homeware', 'health-and-beauty',
                            'food-and-drink', 'diy'])
       products_data = products_data.rename(columns={'removed': 'availabilty'})
       products_data.availabilty = products_data.availabilty.replace('Still_avaliable', 'Still_available')
       self._clean_card_providers(products_data, 'availabilty', categories= ['Still_available', 'Removed'])

       return products_data

    def clean_orders_data(self, orders_table):
        """
        Cleans the provided orders_data DataFrame and returns the cleaned DataFrame.
        """
        
        orders_table = orders_table.drop(columns=['level_0', 'first_name', 'last_name', '1'])
        orders_table = orders_table.drop_duplicates().dropna()

        
        
        orders_table.product_quantity = pd.to_numeric(orders_table.product_quantity, errors='coerce', downcast='integer')
        self._clean_uuids(orders_table, ['date_uuid', 'user_uuid'])

        orders_table.dropna(inplace=True)
        return orders_table
    
    def clean_date_times(self, sales_data):
        """
         Clean and process date and time data in the provided DataFrame.

        Parameters:
        - sales_data (pandas DataFrame): The DataFrame containing date and time-related data.
        """
        sales_data = sales_data.dropna().drop_duplicates()
        sales_data.timestamp = pd.to_datetime(sales_data.timestamp, format='%H:%M:%S', errors='coerce').dt.time
        self._clean_card_providers(sales_data, 'time_period', categories=['Evening', 'Morning', 'Midday', 'Late_Hours'])
        self._clean_uuids(sales_data, ['date_uuid'])
        self._clean_date_numbers(sales_data, ['month', 'year', 'day'])

        return sales_data
    
if __name__ == "__main__":
    pass