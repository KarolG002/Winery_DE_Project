-- models/red_wines.sql

WITH raw_data AS (
    SELECT *
    FROM {{ source('winery_source', 'sparkling') }}
)

SELECT
    id,
    name AS wine_name,
    country AS country_name,
    region AS wine_region,
    winery AS wine_winery,
    rating,
    numberofratings AS num_ratings,
    price,
    cast(replace(year, 'N.V.', '0000') as INT) as year,
    {{ rating_category('Rating') }} AS RatingCategory,
    {{ price_category('Price') }} AS PriceCategory,
    'sparkling' AS WineType
FROM raw_data
