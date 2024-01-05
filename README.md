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

Within this PGAdmin4 based database, a star-based schema is implemented, ensuring consistency across the columns with regard to datatype, thus allowing for a clear idea of how they relate and therefore
greater interoperability. 

Finally, with this all inplace, the data base will be queried using SQL and the relevant data extracted as a final proof of proficiency. 
    

## Installation Instructions 

1. Clone the repository

2. Install the required modules (eg sqlalchemy, yaml, pandas, etc)

3. Use the python scripts to replicate the process of downloading, extracting and cleaning the various data sets
    
## Usage Instructions 

    Usage instructions
    File structure of the project
    License information
