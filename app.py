import pandas as pd
import streamlit as st
from charts import district_price_chart, volume_price_chart, HIDE_BAR

st.set_page_config(page_title='Land registry dashboard', layout='wide')

@st.cache_data
def load_table(path):
    return pd.read_parquet(path)

price_district_table = load_table('data/aggregated/price_district_table.parquet')
med_vol_table = load_table('data/aggregated/median_volume_table.parquet')
yearly_table = load_table('data/aggregated/yearly_median_table.parquet')

st.title('Oxfordshire house prices dashboard')
st.markdown("""An interactive dashboard of residential sales in Oxfordshire from 2015 to 2025, focused on sales volume and £ per m² floor area.\n
""")

col1, col2, col3 = st.columns(3)
col1.metric("Cherwell", f"£{price_district_table.iloc[0, 4]:,.0f}/m²")
col2.metric("Oxford", f"£{price_district_table.iloc[-1, 4]:,.0f}/m²")
col3.metric("Median £/m² in 2025", f"£{yearly_table.iloc[10, 2]:,.0f}", f"{100 * (yearly_table.iloc[10, 2] - yearly_table.iloc[9, 2]) / yearly_table.iloc[9, 2]:,.1f}% vs 2024")

st.plotly_chart(district_price_chart(price_district_table), width='stretch', theme=None, config=HIDE_BAR)
st.plotly_chart(volume_price_chart(med_vol_table), width='stretch', theme=None, config=HIDE_BAR)

st.markdown("""Built with Plotly and Streamlit.\n
The data comes from my Land Registry cleaning pipeline, which links HM Land Registry Price Paid Data to Energy Performance Certificates. 
That link adds floor area and energy rating to each sale, which makes measures such as price per square metre possible.""")