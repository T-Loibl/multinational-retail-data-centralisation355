/*
You will need to do some work on the products table before casting the data types correctly.

The product_price column has a £ character which you need to remove using SQL.

The team that handles the deliveries would like a new human-readable column added for the weight so they can quickly make decisions on delivery weights.

Add a new column weight_class which will contain human-readable values based on the weight range of the product.

+--------------------------+-------------------+
| weight_class VARCHAR(?)  | weight range(kg)  |
+--------------------------+-------------------+
| Light                    | < 2               |
| Mid_Sized                | >= 2 - < 40       |
| Heavy                    | >= 40 - < 140     |
| Truck_Required           | => 140            |
+----------------------------+-----------------+

*/

SELECT * FROM dim_products;


UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')
WHERE product_price LIKE '£%';



ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(14);

ALTER TABLE dim_products
ALTER COLUMN weight TYPE FLOAT USING weight::double precision;

UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
	WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
	WHEN weight >= 140 THEN 'Truck_Required'
END;


/*
After all the columns are created and cleaned, change the data types of the products table.

You will want to rename the removed column to still_available before changing its data type.

Make the changes to the columns to cast them to the following data types:

+-----------------+--------------------+--------------------+
|  dim_products   | current data type  | required data type |
+-----------------+--------------------+--------------------+
| product_price   | TEXT               | FLOAT              |
| weight          | TEXT               | FLOAT              |
| EAN             | TEXT               | VARCHAR(?)         |
| product_code    | TEXT               | VARCHAR(?)         |
| date_added      | TEXT               | DATE               |
| uuid            | TEXT               | UUID               |
| still_available | TEXT               | BOOL               |
| weight_class    | TEXT               | VARCHAR(?)         |
+-----------------+--------------------+--------------------+

*/


ALTER TABLE dim_products
RENAME COLUMN availabilty TO still_available;

DELETE FROM dim_products WHERE product_price='ODPMASE7V7'

UPDATE dim_products
SET "EAN" = '3508047190029'
WHERE uuid = '7a446d4e-1f19-477f-bf87-7c35c0111a74'

UPDATE dim_products
SET "EAN" = '5010240729109'
WHERE uuid = 'c268343b-4c76-4080-881e-1e1f5d695d80'

UPDATE dim_products
SET "EAN" = '0472306810827'
WHERE uuid = '0c0c3e2e-8415-4fa4-a4b0-a0250c5727ee'

ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING product_price::double precision;

ALTER TABLE dim_products
ALTER COLUMN weight TYPE FLOAT USING weight::double precision;

ALTER TABLE dim_products
ALTER COLUMN "EAN" TYPE VARCHAR(15);

ALTER TABLE dim_products
ALTER COLUMN product_code TYPE VARCHAR(11);

ALTER TABLE dim_products
ALTER COLUMN date_added TYPE DATE USING date_added::date;

ALTER TABLE dim_products
ALTER COLUMN uuid TYPE UUID USING uuid::uuid;

ALTER TABLE dim_products
ALTER COLUMN still_available TYPE BOOLEAN USING CASE WHEN still_available = 'true' THEN TRUE ELSE FALSE END;

ALTER TABLE dim_products
ALTER COLUMN weight_class TYPE VARCHAR(14);


SELECT 
TABLE_CATALOG,
TABLE_SCHEMA,
TABLE_NAME, 
COLUMN_NAME, 
DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME = 'dim_products' 



ALTER TABLE dim_products
ADD PRIMARY KEY (product_code);