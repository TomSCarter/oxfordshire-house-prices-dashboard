# Oxfordshire house prices dashboard - Day 5 log - Packaging into a Streamlit dashboard

- Checked restrictions on sharing derived data. 
    - Both datasets are under Open Government License, restrictions relate to address data (inc postcodes) due to Royal Mail and OS rights
    - Safe to share: Aggregated tables with no addresses, postcodes or individual records, such as median price by local authority or EPC band counts by region.
    - Grey area: tables broken down by postcode district or sector. Aggregating to local authority or ONS areas is safer.
    - Avoid: individual sales or certificates, addresses, full postcodes, or EPC rows keyed by UPRN, which may count as personal data.
    - Always include attribution statements
        - 'Contains HM Land Registry data © Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.'
        - 'Energy Performance of Buildings Data: England and Wales, Ministry of Housing, Communities and Local Government. Contains public sector information licensed under the Open Government Licence v3.0.'