import pandas as pd
import streamlit as st
from charts import district_price_chart, historical_volume_chart, historical_price_chart, HIDE_BAR, seasonality_chart, energy_efficiency_chart

st.set_page_config(page_title='Oxfordshire house prices dashboard', layout='wide')

@st.cache_data
def load_table(path):
    return pd.read_parquet(path)

price_district_table = load_table('data/aggregated/price_district_table.parquet')
med_vol_table = load_table('data/aggregated/median_volume_table.parquet')
seasonality_table = load_table('data/aggregated/normal_years_medians.parquet')
energy_efficiency_table = load_table('data/aggregated/energy_efficiency.parquet')

st.title('Oxfordshire house prices dashboard')
st.caption('Best viewed on a desktop or laptop')
st.markdown("""An interactive dashboard of residential sales in Oxfordshire from 2015 to 2025 for property investors, focused on sales volume and £ per m² floor area.\n\n\n\n
""")

st.subheader("""Where is space cheapest in Oxfordshire?""")
st.markdown("""**Finding**: Cherwell has the cheapest space, where flats cost just £3,100 per m² compared to £6,300 per m² for detached Oxford properties. 
Across all districts flats are cheapest and detached houses most expensive. In Oxford terraced houses cost about 6% more per m² than semi-detached, which is the reverse of most other districts. This could reflect town centre terraces vs suburban semis.""")
st.markdown("""**Recommendation**: For the most floor area per £, look at flats in Cherwell, Vale of White Horse and West Oxfordshire. In Oxford semi-detached houses offer more space for the money than terraced. These are district-wide medians, so prices within a district will vary by location.""")
st.plotly_chart(district_price_chart(price_district_table), width='stretch', theme=None, config=HIDE_BAR)

st.subheader("""What has been the overall price/volume trend since 2015?""")
st.markdown("""**Finding**: When a tax increase is implemented sales are brought forward to avoid the change, resulting in a spike in sales volume in the months before followed by a corresponding drop. 
Month-to-month variation of prices (median £ per m²) around these events is typically within noise. The exception is 2020–22, when prices rose 15% during the stamp duty holiday and the COVID-19 lockdowns. The data can’t separate the two effects. Prices have been flat since in cash terms.""")
st.markdown("""**Recommendation**: Keep up-to-date with any upcoming tax changes. Buyers will be keen to complete before any tax increase takes effect but prices do not appear to increase.""")

st.plotly_chart(historical_volume_chart(med_vol_table), width='stretch', theme=None, config=HIDE_BAR)

st.plotly_chart(historical_price_chart(med_vol_table), width='stretch', theme=None, config=HIDE_BAR)

st.subheader(""" Do prices or sales volume vary throughout the year? When are they lowest/highest?""")
st.markdown("""**Finding**: Sales volumes increase in the first half of the year to a peak in June (118% of an average month) then stay above average for the second half. 
January has the lowest sales (73% of an average month) and there is a small bump in March possibly due to the end of the financial year. 
Prices vary slightly through the year (around 2%) but part of this will be rising year-on-year prices, so there is no reliable seasonal pattern.""")
st.markdown("""**Recommendation**: There may be less demand over winter, giving more choice and fewer competing buyers.""")
st.plotly_chart(seasonality_chart(seasonality_table), width='stretch', theme=None, config=HIDE_BAR)

st.subheader(""" Do homes with poor energy efficiency sell at a discount (per m²)?""")
st.markdown("""
**Finding**: Homes with high (A/B) or low (F/G) energy efficiency sell for a lower price (per m²) than moderate efficiency (C-E). Detached homes are an exception where the least efficient homes share the highest price (E & F/G similar). This could be influenced by old inefficient homes located in expensive locations, efficient newer homes in cheaper locations, or buyers do not value efficiency beyond modest levels.
""")
st.markdown("""**Recommendation**: Prices show no premium for efficiency above D, any case for upgrades would need to be based on other factors (e.g. running costs, letting requirements).""")
st.plotly_chart(energy_efficiency_chart(energy_efficiency_table), width='stretch', theme=None, config=HIDE_BAR)

st.markdown("""Built by Tom Carter with Plotly and Streamlit.
The data comes from my [Land Registry cleaning pipeline](https://github.com/TomSCarter/land-registry-cleaning-pipeline), which links HM Land Registry Price Paid Data to Energy Performance Certificates. 
That link adds floor area and energy rating to each sale, which makes measures such as price per square metre possible.
\nLimitations: 
- Category A sales only
- Only sales that could be matched to an Energy Performance Certificate
- Prices are not adjusted for inflation
- No data on rentals
\n
\nContains HM Land Registry data © Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.
\nEnergy Performance of Buildings Data: England and Wales, Ministry of Housing, Communities and Local Government. Contains public sector information licensed under the Open Government Licence v3.0.
 """)
