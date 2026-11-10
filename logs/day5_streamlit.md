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

## app.py

### Structure
- Loads the aggregated Parquet files, never the full sales table
- Data loading wrapped in a function decorated with @st.cache_data, so files aren't reread on every rerun (As Streamlit reruns the whole script on each interaction)
- Page settings (st.set_page_config) first, wide layout
- Charts and config=HIDE_BAR (passed into the charts to hide the toolbar) imported from charts.py

### Layout
- Dashboard title and description
- One section per question: question as subheading, then Findings and Recommendations, then the chart for reference
- Placeholders for the three remaining questions (energy rating, new builds, seasonality)
- Footer: how the data was built (with link to the cleaning pipeline repo), limitations (category A only, EPC-matched sales only, not adjusted for inflation, no rental data), and both attribution statements

### Design decisions
- Tried st.metric figures beside the charts, but removed them: most repeated what the charts already show, and one (2025 median price) sat beside an unrelated chart (the relevant one was hidden by the dropdown). All made more sense once I focused on writing the findings and recommendations, which are more important anyway
- Split the volume/price dropdown chart into two separate charts. The dropdown hid the price view, and the two views answer different questions (tax effects on volume vs. long-term price trend). A shame after the work I did building the dropdown, but hopefully the familiarity will still be useful in the future.
- Added the tax event dates to the price chart as labelled dotted lines, to allow the reader to cross-reference the charts.

### Display fixes
- Light theme forced with .streamlit/config.toml, as the charts are designed for a white background (dark mode made gridlines obscure the annotation text)
- theme=None in st.plotly_chart, plus explicit white plot backgrounds in charts.py, because Streamlit was still showing grey plot areas
- Charts rendered at a different size in Streamlit than in the notebook (though depending on laptop vs monitor), which moved pixel-based positions:
    - Subtitle overlapping chart 1: added a top margin
    - Annotation pushed above chart 2: annotation positions changed from pixel offsets to y-axis values, and a fixed pixel chart height set
- Price chart range slider extended past the data because the last vline label ran beyond the axis range: fixed by adding rangeslider_range to update_xaxes

