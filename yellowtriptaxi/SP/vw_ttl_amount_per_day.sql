ALTER VIEW ttl_amount_per_day AS
WITH cte AS (
    SELECT 
        VendorID,
        CAST(tpep_pickup_datetime AS DATE) AS pickup_date,
        total_amount
    FROM yellow_trip_taxi_data.dbo.yellow_triptaxi_data_raw_retention
)
SELECT 
    VendorID,
    pickup_date,
    SUM(total_amount) AS total_amount_per_day
FROM cte
GROUP BY 
    VendorID,
    pickup_date
