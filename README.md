# Multinational Retail Data Centralisation 

## Project Description 

You work for a multinational company that sells various goods across the globe.

Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team.

In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location.

Your first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data.

You will then query the database to get up-to-date metrics for the business.

Over the course of this project we shall create a series of python scripts containing class objects that will conduct the initial extraction, cleaning and uploading of the requisite data. 
The data will be drawn from a number of sources, including json files, CSV files and S3 buckets. The data is then thoroughly cleaned, taking care to remove NULL values, incorrectly entered values and 
duplicate inputs. The clean dataframes are then uploaded to a seperate database. 

Within this PGAdmin4 based database, a star-based schema is implemented, ensuring consistency across the columns with regard to datatype, thus allowing for a clear idea of how they relate and therefore greater interoperability. This is achieved by changing column datatypes to be consistent across tables, then linking the aforementioned dim_xxxx table to the main orders_table via sets of primary and foreign keys. 

Finally, with this all inplace, the data base will be queried using SQL and the relevant data extracted as a final proof of proficiency. 
    

## Installation Instructions 

1. Clone the repository

2. Install the required modules (eg sqlalchemy, yaml, pandas, etc)

3. Use the python scripts to replicate the process of downloading, extracting and cleaning the various data sets
    
## Usage Instructions 

1. Connect to the database using the DatabaseConnector Class in `database_utils.py`.
2. Extract the information from the various data sources using the DatabaseExtractor Class in `data_extraction.py`.
3. Clean the extracted data using the DatabaseCleaner Class in `data_cleaning.py`.
4. Upload the cleaned data to your database using the DatabaseConnector class.
5. Use the SQL queries within the schema folder to set the column data types and creat the primary/foreign name keys. 
6. Query database as you please.
    

## File Structure 

The project contains the following files: 

- README.md
    - Documentation for the project. 

- /Class_scripts
    - database_utils.py: Script defining DatabaseConnector Class that runs database connections. 
    - data_extractor.py: Script defining DataExtractor Class that extracts data from assorted sources.
    - data_cleaning.py: Script defining DataCleaner class which cleans extracted data.

- /schema
    - dim_card_details.sql
    - dim_date_times.sql
    - dim_users.sql
    - orders.sql
    - products.sql
    - store_details.sql

- /SQL_queries
    - /SQL_query_tasks
    - /SQL_query_results
    
    
## License Information

No License
