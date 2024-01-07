/*
Now we need to update the last table for the card details.

Make the associated changes after finding out what the lengths of each variable should be:

+------------------------+-------------------+--------------------+
|    dim_card_details    | current data type | required data type |
+------------------------+-------------------+--------------------+
| card_number            | TEXT              | VARCHAR(?)         |
| expiry_date            | TEXT              | VARCHAR(?)         |
| date_payment_confirmed | TEXT              | DATE               |
+------------------------+-------------------+--------------------+

*/


SELECT * FROM dim_card_details;

ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(19);

ALTER TABLE dim_card_details
ALTER COLUMN expiry_date TYPE VARCHAR(19);

ALTER TABLE dim_card_details
ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::date;


SELECT 
TABLE_CATALOG,
TABLE_SCHEMA,
TABLE_NAME, 
COLUMN_NAME, 
DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME = 'dim_card_details' 



ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);