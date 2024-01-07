SELECT 
    country_code,
    COUNT(*) AS total_no_stores
FROM 
    dim_store_details
GROUP BY 
    country_code;

