/*
There are two latitude columns in the store details table. Using SQL, merge one of the columns into the other so you have one latitude column.

Then set the data types for each column as shown below:

+---------------------+-------------------+------------------------+
| store_details_table | current data type |   required data type   |
+---------------------+-------------------+------------------------+
| longitude           | TEXT              | FLOAT                  |
| locality            | TEXT              | VARCHAR(255)           |
| store_code          | TEXT              | VARCHAR(?)             |
| staff_numbers       | TEXT              | SMALLINT               |
| opening_date        | TEXT              | DATE                   |
| store_type          | TEXT              | VARCHAR(255) NULLABLE  |
| latitude            | TEXT              | FLOAT                  |
| country_code        | TEXT              | VARCHAR(?)             |
| continent           | TEXT              | VARCHAR(255)           |
+---------------------+-------------------+------------------------+

There is a row that represents the business's website change the location column values where they're null to N/A.
*/

SELECT * FROM dim_store_details;


ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE FLOAT USING longitude::double precision;

ALTER TABLE dim_store_details
ALTER COLUMN locality TYPE VARCHAR(255);

ALTER TABLE dim_store_details
ALTER COLUMN store_code TYPE VARCHAR(12);

ALTER TABLE dim_store_details
ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT;

ALTER TABLE dim_store_details
ALTER COLUMN opening_date TYPE DATE USING opening_date::date;

ALTER TABLE dim_store_details
ALTER COLUMN store_type TYPE VARCHAR(255);
ALTER TABLE dim_store_details
ALTER COLUMN store_type DROP NOT NULL;

ALTER TABLE dim_store_details
ALTER COLUMN latitude TYPE FLOAT USING latitude::double precision;

ALTER TABLE dim_store_details
ALTER COLUMN country_code TYPE VARCHAR(2);

ALTER TABLE dim_store_details
ALTER COLUMN continent TYPE VARCHAR(255);


SELECT 
TABLE_CATALOG,
TABLE_SCHEMA,
TABLE_NAME, 
COLUMN_NAME, 
DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME = 'dim_store_details' 



ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);