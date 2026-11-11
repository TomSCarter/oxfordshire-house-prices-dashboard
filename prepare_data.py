import pandas as pd
from pathlib import Path

# SETTINGS
DATA_FILE = "data/raw/pp_epc_oxfordshire_2015_2025_v2.parquet"
OUT_PATH = "data/aggregated/"
RECENT_YEARS = [2023, 2024, 2025]
TAX_CHANGE_YEARS = [2016, 2020, 2021, 2025]

# LOAD FUNCTION

def load_data(data_file):
    """Reads parquet of merged cleaned data"""

    file_in = Path(data_file)
    if not file_in.exists():
        raise FileNotFoundError(f"No file found at {data_file}")
    raw_data = pd.read_parquet(file_in)
    return raw_data


# PREPARE DATA FUNCTION
def prepare_data(raw_data):
    """Prepares the base table of data with filters that apply to all downstream aggregated tables"""

    cat_a_only = raw_data[raw_data['transaction_category'] == 'A'].copy()
    cat_a_only['£/m2'] = cat_a_only['price_paid'] / cat_a_only['total_floor_area']

    labels = {'F': 'Flat', 'T': 'Terraced', 'S': 'Semi-detached', 'D': 'Detached'}
    cat_a_only['property_subtype'] = cat_a_only['property_subtype'].replace(labels)
    cat_a_only['district'] = cat_a_only['district'].str.title().str.replace('Of', 'of')

    return cat_a_only

# AGGREGATED MEDIAN PRICE BY DISTRICT TABLE
def price_district_table(cat_a_only):
    """Prepares the aggregated table with median £ per m2 by district and property type. Adds column for median whole district £ per m2"""
    
    recent_years = cat_a_only[cat_a_only['year'].isin(RECENT_YEARS)].copy()

    recent_years_agg = recent_years.groupby(['district', 'property_subtype'])['£/m2'].agg(['median', 'count']).reset_index()
    recent_years_agg = recent_years_agg.rename(columns = {'property_subtype':'property_type', 'median':'£_per_m²'})
    recent_years_agg['£_per_m²'] = round(recent_years_agg['£_per_m²'], 2)

    overall_medians = recent_years.groupby('district')['£/m2'].median().reset_index()
    overall_medians = overall_medians.rename(columns = {'£/m2':'district_median_£_per_m2'})
    overall_medians['district_median_£_per_m2'] = round(overall_medians['district_median_£_per_m2'], 2)
    combined = recent_years_agg.merge(right= overall_medians, on='district')

    order = ['Detached', 'Semi-detached', 'Terraced', 'Flat']

    combined['property_type'] = pd.Categorical(
        combined['property_type'],
        categories=order,
        ordered=True
    )

    combined = combined.sort_values(['district_median_£_per_m2', 'property_type']).reset_index(drop=True)
    return combined

# AGGREGATED MEDIAN PRICE AND VOLUME TABLE
def median_volume_table(cat_a_only):
    """Prepares the aggregated median £ per m2 and sales volume per month table"""

    med_vol_table = cat_a_only.resample('MS', on='deed_date')[['unique_id', '£/m2']].agg({'unique_id':'count', '£/m2':'median'})
    med_vol_table = med_vol_table.rename(columns={'unique_id':'monthly_sales_count', '£/m2':'median_£_per_m2'}).reset_index()
    return med_vol_table

# YEARLY MEDIAN PRICE TABLE
def yearly_median_table(cat_a_only):
    """Generates a table of yearly median £ per m2 floor area and sales volume"""
    yearly_table = cat_a_only.resample('YS', on='deed_date')[['unique_id', '£/m2']].agg({'unique_id':'count', '£/m2':'median'})
    yearly_table = yearly_table.rename(columns={'unique_id':'monthly_sales_count', '£/m2':'median_£_per_m2'}).reset_index()
    yearly_table['median_£_per_m2'] = round(yearly_table['median_£_per_m2'], 2)
    return yearly_table

# SEASONALITY TABLE
def seasonality_table(cat_a_only):
    monthly = cat_a_only.groupby(['year', 'month'])[['unique_id', '£/m2']].agg({'unique_id':'count', '£/m2':'median'}).reset_index()

    avg_monthly = monthly.groupby(['year'])[['unique_id', '£/m2']].agg({'unique_id':'mean', '£/m2':'mean'}).reset_index()

    merged_monthly = monthly.merge(avg_monthly, on='year').rename(columns={'unique_id_x':'monthly_sales', '£/m2_x':'£/m2', 'unique_id_y':'avg_vol', '£/m2_y':'avg_£/m2'})
    merged_monthly['norm_monthly_sales'] = 100 * merged_monthly['monthly_sales'] / merged_monthly['avg_vol']
    merged_monthly['norm_monthly_£/m2'] = 100 * merged_monthly['£/m2'] / merged_monthly['avg_£/m2']

    normal_years = merged_monthly[~merged_monthly['year'].isin(TAX_CHANGE_YEARS)]
    normal_years_medians = normal_years.groupby('month')['norm_monthly_sales'].agg(['median', 'max', 'min']).reset_index()
    return normal_years_medians

# SAVE OUTPUT
def save_output(df, out_path, out_name):
    """Checks for licensing restricted columns then saves the final table as parquet"""
    not_allowed = ['unique_id', 'address', 'saon', 'paon', 'street', 'postcode', 'uprn']
    cols = df.columns
    if any(cols.isin(not_allowed)):
        raise ValueError(f"Columns in {out_name} contain address items restricted by licensing")
    folder = Path(out_path)
    folder.mkdir(exist_ok=True, parents=True)
    file_out = folder / out_name
    df.to_parquet(file_out)

# MAIN()
def main():
    raw_df = load_data(DATA_FILE)
    cat_a_only = prepare_data(raw_df)

    recent_years_agg = price_district_table(cat_a_only)
    save_output(recent_years_agg, OUT_PATH, 'price_district_table.parquet')
    print(f"Saved aggregated median price by district table, shape: {recent_years_agg.shape}")
    print(recent_years_agg)

    med_vol_table = median_volume_table(cat_a_only)
    save_output(med_vol_table, OUT_PATH, 'median_volume_table.parquet')
    print(f"Saved aggregated median price and volume table, shape: {med_vol_table.shape}")
    print(med_vol_table)

    yearly_table = yearly_median_table(cat_a_only)
    save_output(yearly_table, OUT_PATH, 'yearly_median_table.parquet')
    print(f"Saved aggregated yearly median price and volume table, shape: {yearly_table.shape}")
    print(yearly_table)  

    normal_years_medians = seasonality_table(cat_a_only)
    save_output(normal_years_medians, OUT_PATH, 'normal_years_medians.parquet')
    print(f"Saved normalised monthly volume table, shape: {normal_years_medians.shape}")
    print(yearly_table)  

# STANDARD GUARD
if __name__ == "__main__":
    main()
