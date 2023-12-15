class DataCleaning:

    def clean_user_data(user_df):
            # Add your data cleaning logic here
            # Example: Removing rows with NULL values
            cleaned_df = user_df.dropna()

            # Additional cleaning steps can be added based on your specific requirements

            return cleaned_df