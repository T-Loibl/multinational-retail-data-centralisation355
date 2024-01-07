SELECT
    locality,
    COUNT(*) AS total_no_of_stores
FROM
    dim_store_details
GROUP BY
    locality
ORDER BY
    total_no_of_stores DESC
LIMIT 7;