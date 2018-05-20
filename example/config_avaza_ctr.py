
# set the path-to-files
TRAIN_FILE = "/data/avaza-ctr-2015/train.csv"
TEST_FILE = "/data/avaza-ctr-2015/test.csv"

SUB_DIR = "/data/avaza-ctr-2015/data"


NUM_SPLITS = 3
RANDOM_SEED = 2017

# types of columns of the dataset dataframe
CATEGORICAL_COLS = ['hour', 'C1', 'banner_pos', 'site_id', 'site_domain', 'site_category', 
'app_id', 'app_domain', 'app_category', 'device_id', 'device_ip', 'device_model', 'device_type', 'device_conn_type', 
'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']

NUMERIC_COLS = [
]

IGNORE_COLS = [
    "id", "click",
]
