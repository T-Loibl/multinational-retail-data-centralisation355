
/*Change the data types to correspond to those seen in the table below.

+------------------+--------------------+--------------------+
|   orders_table   | current data type  | required data type |
+------------------+--------------------+--------------------+
| date_uuid        | TEXT               | UUID               |
| user_uuid        | TEXT               | UUID               |
| card_number      | TEXT               | VARCHAR(?)         |
| store_code       | TEXT               | VARCHAR(?)         |
| product_code     | TEXT               | VARCHAR(?)         |
| product_quantity | BIGINT             | SMALLINT           |
+------------------+--------------------+--------------------+

The ? in VARCHAR should be replaced with an integer representing the maximum length of the values in that column.

*/




ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;

ALTER TABLE orders_table
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID;

ALTER TABLE orders_table
ALTER COLUMN card_number TYPE VARCHAR(19);

ALTER TABLE orders_table
ALTER COLUMN store_code TYPE VARCHAR(12);

ALTER TABLE orders_table
ALTER COLUMN product_code TYPE VARCHAR(11);

ALTER TABLE orders_table
ALTER COLUMN product_quantity TYPE SMALLINT;


SELECT 
TABLE_CATALOG,
TABLE_SCHEMA,
TABLE_NAME, 
COLUMN_NAME, 
DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME = 'orders_table' 



/* Add foreign keys */

ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_user_uuids
FOREIGN KEY (user_uuid)
REFERENCES dim_users (user_uuid);

ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_store_details
FOREIGN KEY (store_code)
REFERENCES dim_store_details (store_code);

ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_product_codes
FOREIGN KEY (product_code)
REFERENCES dim_products (product_code);

ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_date_details
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times (date_uuid);

ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_card_details
FOREIGN KEY (card_number)
REFERENCES dim_card_details (card_number);