# Oxfordshire house prices dashboard

An interactive dashboard of residential sales in Oxfordshire from 2015 to 2025, built with Plotly and Streamlit.

The data comes from my [Land Registry cleaning pipeline](https://github.com/TomSCarter/land-registry-cleaning-pipeline), which links HM Land Registry Price Paid Data to Energy Performance Certificates. That link adds floor area and energy rating to each sale, which makes measures such as price per square metre possible.

**Status:** in progress.

## Questions

_To be added: the questions the dashboard answers, and who they're for._

## Findings

_To be added: one headline finding per chart, with a recommendation._

## Data

The data isn't included in this repo. To reproduce it, run the [cleaning pipeline](https://github.com/TomSCarter/land-registry-cleaning-pipeline) and copy its output Parquet file from `data/processed/` into this project's `data/processed/` folder.

The dashboard loads pre-aggregated tables rather than the full sales table, so it stays fast.

Contains HM Land Registry data © Crown copyright and database right 2026. This data is licensed under the Open Government Licence v3.0. EPC data is subject to its own licence terms.

## Running it