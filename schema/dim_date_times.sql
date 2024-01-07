/*
Now update the date table with the correct types:

+-----------------+-------------------+--------------------+
| dim_date_times  | current data type | required data type |
+-----------------+-------------------+--------------------+
| month           | TEXT              | VARCHAR(?)         |
| year            | TEXT              | VARCHAR(?)         |
| day             | TEXT              | VARCHAR(?)         |
| time_period     | TEXT              | VARCHAR(?)         |
| date_uuid       | TEXT              | UUID               |
+-----------------+-------------------+--------------------+

*/


SELECT * FROM dim_date_times;


ALTER TABLE dim_date_times
ALTER COLUMN month TYPE VARCHAR(2);

ALTER TABLE dim_date_times
ALTER COLUMN year TYPE VARCHAR(4);

ALTER TABLE dim_date_times
ALTER COLUMN day TYPE VARCHAR(2);

ALTER TABLE dim_date_times
ALTER COLUMN time_period TYPE VARCHAR(10);

ALTER TABLE dim_date_times
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;


SELECT 
TABLE_CATALOG,
TABLE_SCHEMA,
TABLE_NAME, 
COLUMN_NAME, 
DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME = 'dim_date_times' 


DELETE FROM dim_date_times WHERE date_uuid IS NULL;
ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);