with source as (
    select * from {{ source('staging', 'fhv_tripdata') }}
),

renamed as (
    select
        -- identifiers
        cast(pulocationid as integer) as pickup_location_id,
        cast(dolocationid as integer) as dropoff_location_id,

        -- timestamps
        cast(pickup_datetime as timestamp) as pickup_datetime,  
        cast(dropoff_datetime as timestamp) as dropoff_datetime,

        -- trip info
        cast(dispatching_base_num as string) as dispatch_base_number,
        cast(affiliated_base_number as string) as affiliated_base_number,
        cast(sr_flag as string) as sr_flag
        
    from source

    -- Filter out records with null dispatching_base_number (data quality requirement)
    where dispatching_base_num is not null
)

select * from renamed