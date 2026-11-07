import pandas as pd
from pathlib import Path

# SETTINGS
DATA_FILE = "data/pp_epc_oxfordshire_2015_2025_v2.parquet"
OUT_PATH = "data/aggregated/"

# LOAD FUNCTION

def load_data(data_file):
    """Reads parquet of merged cleaned data"""

    file_in = Path(data_file)


# PREPARE DATA FUNCTION
def prepare_data():
    """Prepares the base table of data with filters that apply to both downstream aggregated tables"""

# AGGREGATED MEDIAN PRICE BY DISTRICT TABLE
def price_district_table():
    """Prepares the aggregated table with median £ per m2 by district and property type"""

# AGGREGATED MEDIAN PRICE AND VOLUME TABLE
def median_volume_table():
    """Prepares the aggregated median £ per m2 and sales volume per month table"""


# SAVE OUTPUT
def save_output(out_path, out_name):
    """Checks for licensing restricted columns then saves the final table as parquet"""


# MAIN()
def main():

# STANDARD GUARD
if __name__ == "__main__":
    main()
