SELECT
    dim_store_details.store_type AS store_type,
    ROUND(SUM(orders_table.product_quantity * dim_products.product_price)::numeric, 2) AS total_sales,
    ROUND((SUM(orders_table.product_quantity * dim_products.product_price) /
        (SELECT 
            SUM(orders_table.product_quantity * dim_products.product_price)
        FROM 
            orders_table
        JOIN dim_products ON orders_table.product_code = dim_products.product_code) * 100)::numeric, 2) 
    AS "percentage_total(%)"
FROM 
    orders_table
JOIN 
    dim_products ON orders_table.product_code = dim_products.product_code
JOIN 
    dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY
    store_type
ORDER BY
    "percentage_total(%)" DESC;