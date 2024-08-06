-- models/red_wines.sql

WITH raw_data AS (
    SELECT *
    FROM {{ source('winery_source', 'white') }}
)

SELECT
    id,
    name AS wine_name,
    region AS wine_region,
    winery AS wine_winery,
    rating,
    numberofratings AS num_ratings,
    price,
    cast(replace(year, 'N.V.', '0000') as INT) as year,
    {{ rating_category('Rating') }} AS RatingCategory,
    {{ price_category('Price') }} AS PriceCategory,
    'white' AS WineType
FROM raw_data
