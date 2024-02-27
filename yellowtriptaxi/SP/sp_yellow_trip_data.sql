

-- EXEC sp_yellow_trip_data

-- ALTER PROCEDURE sp_yellow_trip_data AS

-- INSERT DATA  IN THE RETENTION TABLE
-- USUALLY THIS TABLE IS USED FOR THE INCREMENTAL PROCESS

WITH  cte as (
SELECT 
		[VendorID]
      ,[tpep_pickup_datetime]
      ,[tpep_dropoff_datetime]
      ,[passenger_count]
      ,[trip_distance]
      ,[RatecodeID]
      ,[store_and_fwd_flag]
      ,[PULocationID]
      ,[DOLocationID]
      ,[payment_type]
      ,[fare_amount]
      ,[extra]
      ,[mta_tax]
      ,[tip_amount]
      ,[tolls_amount]
      ,[improvement_surcharge]
      ,[total_amount]
      ,[congestion_surcharge]
      ,[airport_fee]
  FROM  [yellow_trip_taxi_data].[dbo].[yellow_triptaxi_data_raw] 
  )
   
  INSERT INTO [yellow_trip_taxi_data].[dbo].[yellow_triptaxi_data_raw_retention]
  SELECT  DISTINCT *
  FROM cte
  WHERE passenger_count > 0 
   
  ;

  -- FROM TRASNFORM TO OUTPUT TABLE MAKING SURE WE DONT HAVE DUPES DATA
WITH cte AS (
    SELECT 
        ROW_NUMBER() OVER (PARTITION BY  
                            VendorID
                            ,tpep_pickup_datetime
                            ,tpep_dropoff_datetime
                            ,passenger_count
                            ,trip_distance
                            ,RatecodeID
                            ,store_and_fwd_flag
                            ,PULocationID
                            ,DOLocationID
                            ,payment_type
                            ,fare_amount
                            ,extra
                            ,mta_tax
                            ,tip_amount
                            ,tolls_amount
                            ,improvement_surcharge
                            ,total_amount
                            ,congestion_surcharge
                            ,airport_fee
                        ORDER BY (SELECT NULL)) AS row_num
        ,VendorID
        ,tpep_pickup_datetime
        ,tpep_dropoff_datetime
        ,passenger_count
        ,trip_distance
        ,RatecodeID
        ,store_and_fwd_flag
        ,PULocationID
        ,DOLocationID
        ,payment_type
        ,fare_amount
        ,extra
        ,mta_tax
        ,tip_amount
        ,tolls_amount
        ,improvement_surcharge
        ,total_amount
        ,congestion_surcharge
        ,airport_fee
    FROM yellow_trip_taxi_data.dbo.yellow_triptaxi_data_raw_retention
)
   
INSERT INTO [yellow_trip_taxi_data].[dbo].[yellow_triptaxi_data_output]
SELECT DISTINCT
  VendorID
        ,tpep_pickup_datetime
        ,tpep_dropoff_datetime
        ,passenger_count
        ,trip_distance
        ,RatecodeID
        ,store_and_fwd_flag
        ,PULocationID
        ,DOLocationID
        ,payment_type
        ,fare_amount
        ,extra
        ,mta_tax
        ,tip_amount
        ,tolls_amount
        ,improvement_surcharge
        ,total_amount
        ,congestion_surcharge
        ,airport_fee
FROM cte
WHERE row_num = 1;

