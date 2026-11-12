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
- Structure: Shared style settings, annotations as list of lists (for looping over in chart function), district_price_chart(), historical_volume_chart(), historical_price_chart(), seasonality_chart(), energy_efficiency_chart()
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
- One section per question: question as subheading, then Findings and Recommendations, then the chart for reference (cheapest space, price/sales volume over time, seasonality, energy rating)
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

## Scope change
- Dashboard reduced from 5 questions to 4: £/m² by district, price and volume trend since 2015, seasonality, and the energy-efficiency discount
- New-build premium question dropped: a raw comparison is too confounded (new builds differ in size, location and type). To be answered next week with a regression including a new-build flag, floor area and district

## Seasonality chart
- Each month's sales expressed as an index relative to the year's average month (100 = average), so the long-term trend doesn't hide the seasonal pattern
- Tax-affected years (2016, 2020, 2021, 2025) excluded, so not distorted by the deadline spikes
- Line: median index across the remaining years. Band: min to max across those years, to show how consistent the pattern is
    - Chose a band over one line per year: with seven years, individual lines mostly added clutter
- Reference line at 100 (an average month), month names on the x-axis, line colour matching the volume chart
- Finding: January is quietest (about 73% of an average month), June busiest (about 118%), and the second half of the year stays above average. A smaller March bump remains even with tax years excluded
- Prices: a calendar-year baseline showed about ±2% variation, but part of that reflects prices rising within each year, so the dashboard says there's no reliable seasonal pattern. A rolling baseline would test this properly (in BACKLOG.md)
- Recommendation accounts for completion dates lagging agreed sales by a couple of months, and doesn't claim a winter price discount, since the price data doesn't show one

## Energy efficiency chart
 - Exclude new builds (19485 rows) as they carry a premium and are mostly A/B to give 85561 rows
 - Band A (0.2%) and band G (0.6%) rare and grouped with adjacent to give A/B, C, D, E, and F/G
 - Excluded rows with an expired EPC (982 rows) leaving 84575 rows, as these are most likely to be a poor reflection of the properties energy efficiency at the time of sale
 - Using 2015-2025 means as properties get more efficient and more expensive over time, the trend is distorted (prices rose about 27% over the period while the mix of ratings changed). Limited to recent (2023-2025) records.
    - Efficiency ratings still well populated (min F/G: 557 to max C: 8149)
- Added count to table and tooltip
- Excluded point for Flats rated F/G due to only 18 records, with the reason in the subtitle, so the least reliable value isn't the most prominent
- Main result: A/B-rated homes have the lowest median £/m² for every property type (roughly 8–15% below D). For semi-detached and terraced, F/G is also lower than C–E. Detached is the exception: F/G is about level with E, the highest
- Wording kept to association, not cause: likely confounders are building age and location
- Subtitle notes that some certificates predate the 2015 change in rating method

