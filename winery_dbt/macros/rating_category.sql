{% macro rating_category(rating_column) %}
    CASE
        WHEN {{ rating_column }} < 3 THEN 'Low'
        WHEN {{ rating_column }} BETWEEN 3 AND 4 THEN 'Medium'
        ELSE 'High'
    END
{% endmacro %}
