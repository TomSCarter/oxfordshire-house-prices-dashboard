import streamlit as st
from charts import district_price_chart, volume_price_chart
import pandas as pd

@st.cache_data
def load_table(path):
    return pd.read_parquet(path)

price_district_table = load_table('data/aggregated/price_district_table.parquet')
med_vol_table = load_table('data/aggregated/median_volume_table.parquet')

st.set_page_config(page_title='Land registry dashboard', layout='wide')
st.title('Headline')
st.markdown('body text')

st.plotly_chart(district_price_chart(price_district_table), theme=None)
st.plotly_chart(volume_price_chart(med_vol_table), theme=None)

