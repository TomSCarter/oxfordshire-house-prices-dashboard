# Oxfordshire house prices dashboard - Day 5 log - Packaging into a Streamlit dashboard

- Checked restrictions on sharing derived data. 
    - Both datasets are under Open Government License, restrictions relate to address data (inc postcodes) due to Royal Mail and OS rights
    - Safe to share: Aggregated tables with no addresses, postcodes or individual records, such as median price by local authority or EPC band counts by region.
    - Grey area: tables broken down by postcode district or sector. Aggregating to local authority or ONS areas is safer.
    - Avoid: individual sales or certificates, addresses, full postcodes, or EPC rows keyed by UPRN, which may count as personal data.
    - Always include attribution statements
        - 'Contains HM Land Registry data © Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.'
        - 'Energy Performance of Buildings Data: England and Wales, Ministry of Housing, Communities and Local Government. Contains public sector information licensed under the Open Government Licence v3.0.'

## prepare_data.py
- Script to build the aggregate tables for the dashboard charts (so no need to load full dataset)
- Structure: Settings, load data, prepare, one function per table, save, main()
- prepare_data() function does the prep requires for all the tables (e.g. category A only, £/m2 etc)
- Tables:
    - price_district_table(): median £/m2 and number of sales by district and property type, for recent years (2023-2025). With an added column containing each districts overall median, which is used to order the table/charts (median of medians wouldn't be accurate)
    - median_volume_table(): monthly sales count and median £/m2, 2015-2025
- save_output()
    - Saved as Parquet to keep datatypes
    - Checks for columns relating to address to avoid licensing issues and allow upload of the aggregate tables
- Aggregated files committed to git. Allowed by licensing and allows app to run without raw data

## charts.py
- Module containing chart functions. To be imported by the app and notebook. Each function takes one of the aggregated tables and returns a figure object (not the displayed graph)
- Structure: Shared style settings, annotations as list of lists (for looping over in chart function), district_price_chart(), volume_price_chart()
- District order now derived from data within the function rather than hard-coded
- go.scatter needs full df['deed_date'] rather than just 'deed_date' as in px.scatter etc
- Files kept in main directory as there are only 3 and it's the typical layout for a Streamlit app