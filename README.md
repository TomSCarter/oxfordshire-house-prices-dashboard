# Oxfordshire house prices dashboard

An interactive dashboard of residential sales in Oxfordshire from 2015 to 2025, for property investors, built with Plotly and Streamlit.

**Live dashboard:** [link]

The data comes from my [Land Registry cleaning pipeline](https://github.com/TomSCarter/land-registry-cleaning-pipeline), which links HM Land Registry Price Paid Data to Energy Performance Certificates. That link adds floor area and energy rating to each sale, which makes measures such as price per square metre possible.

## Questions

The dashboard is aimed at a property investor, and answers four questions:

1. Where is space cheapest in Oxfordshire?
2. How have prices and sales volumes changed since 2015, and how did tax changes affect them?
3. Do prices or sales volumes vary through the year?
4. Do homes with poor energy efficiency sell at a discount per m²?

## Findings

**1. Space is cheapest in Cherwell.** Flats there cost about £3,100 per m², against about £6,300 for detached houses in Oxford. Flats are the cheapest type per m² in every district.
*Recommendation:* for the most floor area per pound, look at flats in Cherwell, Vale of White Horse and West Oxfordshire. These are district-wide medians, so prices vary by location within each district.

**2. Tax deadlines shift sales earlier, but not prices.** Sales spike in the months before a tax increase and drop afterwards, while prices show no clear change. Separately, median price per m² rose about 15% from 2020 to 2022, during the stamp duty holiday and the COVID-19 lockdowns, and has been flat in cash terms since.
*Recommendation:* buyers push to complete before a tax increase, but there's no sign of paying more per m² to do so.

**3. Sales are lowest in winter.** January is the quietest month (about 73% of an average month) and June the busiest (about 118%), with the second half of the year above average. Prices show no reliable seasonal pattern.
*Recommendation:* winter brings fewer competing buyers, though not lower prices.

**4. The most efficient homes sell for the least per m².** Among existing homes, those rated A/B have the lowest median price per m² for every property type, roughly 8–15% below D-rated homes. Though this is just an association, building age and location are likely to factor in the trend.
*Recommendation:* sale prices show no premium for ratings above D, so any case for upgrades rests on running costs and letting requirements.

## Limitations

- Standard market sales (category A) only
- Only sales that could be matched to an Energy Performance Certificate
- Prices are not adjusted for inflation
- No rental data, so returns for investors can't be assessed
- Energy ratings come from certificates that may predate the sale up to 10 years, and some predate the 2015 change in rating method

## Running it

The aggregated tables the dashboard uses are included in `data/aggregated/`, so it runs without the raw data:

    pip install -r requirements.txt
    streamlit run app.py

To rebuild the aggregated tables, run the [cleaning pipeline](https://github.com/TomSCarter/land-registry-cleaning-pipeline), copy its output Parquet file into `data/raw/`, then run:

    python prepare_data.py

## Structure

    ├── app.py               # Streamlit dashboard
    ├── charts.py            # chart functions
    ├── prepare_data.py      # builds the aggregated tables from the cleaned data
    ├── requirements.txt
    ├── .streamlit/config.toml
    ├── data/aggregated/     # small summary tables used by the app (tracked)
    ├── data/raw/            # cleaned sales data (not tracked)
    ├── notebooks/           # exploration and chart development
    └── logs/                # daily notes and decisions

## Data and licences

Only district-level and county-level summary tables are published here, with no addresses, postcodes or individual sales.

Contains HM Land Registry data © Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.

Energy Performance of Buildings Data: England and Wales, Ministry of Housing, Communities and Local Government. Contains public sector information licensed under the Open Government Licence v3.0.

Address data in both datasets is subject to separate Royal Mail and Ordnance Survey terms, and isn't included.

Code is MIT licensed.