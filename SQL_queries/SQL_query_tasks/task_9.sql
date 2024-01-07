
WITH sales_date AS (
    SELECT 
        year,
        TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', timestamp), 'YYYY-MM-DD HH24:MI:SS') AS sales_date_column,
        LEAD(TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', timestamp), 'YYYY-MM-DD HH24:MI:SS')) OVER (PARTITION BY year ORDER BY TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', timestamp), 'YYYY-MM-DD HH24:MI:SS')) AS next_sale_date
    FROM 
        dim_date_times
)
SELECT 
    year,
    '{"hours": ' || EXTRACT(HOUR FROM AVG(next_sale_date - sales_date_column)) || ', "minutes": ' || EXTRACT(MINUTE FROM AVG(next_sale_date - sales_date_column)) || ', "seconds": ' || EXTRACT(SECOND FROM AVG(next_sale_date - sales_date_column)) || ', "milliseconds": ' || EXTRACT(MILLISECOND FROM AVG(next_sale_date - sales_date_column)) || '}' AS actual_time_taken
FROM 
    sales_date
WHERE 
    next_sale_date IS NOT NULL
GROUP BY 
    year
ORDER BY 
    AVG(next_sale_date - sales_date_column) DESC
LIMIT 5;