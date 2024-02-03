import io
import pandas as pd
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_'

    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'RatecodeID':pd.Int64Dtype(),
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'ehail_fee':float,
                    'improvement_surcharge':float,
                    'total_amount':float, 
                    'payment_type': pd.Int64Dtype(),
                    'trip_type': pd.Int64Dtype(),
                    'congestion_surcharge':float
                }

    # native date parsing 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    # Change below yrmon block to add more months of green trip data.
    
    yrmon = [
        '2020-10',
        '2020-11',
        '2020-12'
    ]
    

    final_url = [url + s + '.csv.gz' for s in yrmon]

    all_df = []

    for item in final_url:

        df = pd.read_csv(
            item, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates
            )
        
        all_df.append(df)

    return pd.concat(all_df)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'