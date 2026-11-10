import pandas as pd
import streamlit as st
from charts import district_price_chart, historical_volume_chart, historical_price_chart, HIDE_BAR

st.set_page_config(page_title='Oxfordshire house prices dashboard', layout='wide')

@st.cache_data
def load_table(path):
    return pd.read_parquet(path)

price_district_table = load_table('data/aggregated/price_district_table.parquet')
med_vol_table = load_table('data/aggregated/median_volume_table.parquet')
yearly_table = load_table('data/aggregated/yearly_median_table.parquet')

st.title('Oxfordshire house prices dashboard')
st.markdown("""An interactive dashboard of residential sales in Oxfordshire from 2015 to 2025, focused on sales volume and £ per m² floor area.\n\n\n\n
""")


# col1, col2, col3 = st.columns([4, 1, 1], vertical_alignment="center")

# with col1:
#     st.header("""Where is space cheapest in Oxfordshire?""")
#     st.markdown("""Finding: Cherwell has the lowest median price per floor area, with flats in Cherwell cheaper than expected relative to other districts. 
#     Across all districts Flats are cheapest and Detached houses most expensive but the order of Terraced vs Semi-detached houses changes in the more expensive districts. 
#     Oxford is most expensive with terraced houses siginificantly more expensive than semi-detatched, this may reflect town centre properties vs suburbs.""")
#     st.markdown("""Recomendation: The apparently lower price of flats in Cherwell and semi-detached houses in Oxford and South Oxfordshire warrants further investigation. Is this a result of location within the district?""")
# with col2:
#     st.metric("Cherwell", f"£{price_district_table.iloc[0, 4]:,.0f}/m²", border=True)
# with col3:
#     st.metric("Oxford", f"£{price_district_table.iloc[-1, 4]:,.0f}/m²", f"{100 * (price_district_table.iloc[-1, 4] - price_district_table.iloc[0, 4]) / price_district_table.iloc[0, 4]:,.0f} % vs Cherwell", border=True)

st.subheader("""Where is space cheapest in Oxfordshire?""")
st.markdown("""**Finding**: Cherwell has the cheapest space, where flats cost just £3,100 per m² compared to £6,300 per m² for detached Oxford properties. 
Across all districts flats are cheapest and detached houses most expensive. In Oxford terraced houses cost about 6% more per m² than semi-detatched, which is the reverse of most other districts, this could reflect town centre terraces vs suburban semis.""")
st.markdown("""**Recommendation**: For the most floor area per £, look at flats in Cherwell, Vale of White Horse and West Oxfordshire. In Oxford semi-detached houses offer more space for the money than terraced. These are district-wide medians, so prices within a district will vary by location.""")
st.plotly_chart(district_price_chart(price_district_table), width='stretch', theme=None, config=HIDE_BAR)

# left, right = st.columns([5,1], vertical_alignment="center")
# with left:
#     st.header("""How have tax changes effected sales volumes and prices?""")
# with right:
#     st.metric("Median £/m² in 2025", f"£{yearly_table.iloc[10, 2]:,.0f}", f"{100 * (yearly_table.iloc[10, 2] - yearly_table.iloc[9, 2]) / yearly_table.iloc[9, 2]:,.1f}% vs 2024", border=True)

# st.subheader("""How have tax changes affected sales volumes?""")
st.subheader("""What has been the overall price/volume trend since 2015?""")
st.markdown("""**Finding**: When a tax increase is implemented sales are brought forward to avoid the change, resulting in a spike in sales volume in the months before followed by a corresponding drop. 
Month-to-month variation of prices (median £ per m²) around these events is typically within noise. Though from 2020 to 2022 there was a 15% increase in prices, which was during the period of COVID-19 lockdowns and a stamp duty holiday. Prices have been flat since in cash terms.""")
st.markdown("""**Recomendation**: Keep up-to-date with any upcoming tax changes. Buyers will be keen to complete before any tax increase takes effect but prices do not appear to increase.""")

st.plotly_chart(historical_volume_chart(med_vol_table), width='stretch', theme=None, config=HIDE_BAR)

# st.subheader("""How have prices changed over time?""")
# st.markdown("""**Finding**: Between 2020 and mid-2022 there was a 15% increase in median £ per m², since then prices have been flat. The period of increasing prices included COVID-19 lockdowns and a stamp duty holiday.""")
# st.markdown("""**Recomendation**: In the current enviroment a properties price cannot be expected to rise without intervention.""")

st.plotly_chart(historical_price_chart(med_vol_table), width='stretch', theme=None, config=HIDE_BAR)


st.markdown("""Built with Plotly and Streamlit.\n
The data comes from my Land Registry cleaning pipeline, which links HM Land Registry Price Paid Data to Energy Performance Certificates. 
That link adds floor area and energy rating to each sale, which makes measures such as price per square metre possible.""")

    # - How does £ per sqm floor_area vary between districts? Where is space cheapest?
    # - Do homes with poor energy efficiency sell at a discount (per m2)?
    #     - Landlords have to meet a minimum energy rating to let, which may be raised
    # - Do prices or sales volume vary throughout the year? When are they lowest/highest?
    #     - Compare months within a year to avoid long term price rise trend
    # - Do new builds cost more per m2?
    # - What has been the overall price/volume trend since 2015?
    #     - Did sales volumes or prices change when tax changes took place?
    #         - Extra stamp duty changes (first in April 2016 for additional properties then increased)