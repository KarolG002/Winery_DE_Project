{% macro price_category(price_column) %}
    CASE
        WHEN {{ price_column }} < 10 THEN 'Cheap'
        WHEN {{ price_column }} BETWEEN 10 AND 20 THEN 'Moderate'
        WHEN {{ price_column }} BETWEEN 20 AND 50 THEN 'Expensive'
        ELSE 'Luxury'
    END
{% endmacro %}
