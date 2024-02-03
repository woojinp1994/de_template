import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/de-template-bf74bda2d0b3.json"

bucket_name = 'mage-wp'
project_id = 'de-template'

table_name = "nyc_taxi_data_green"
root_path = f'{bucket_name}/{table_name}'


@data_exporter
def export_data_to_google_cloud_storage(data, *args, **kwargs) -> None:

    pq.write_to_dataset(
        pa.Table.from_pandas(data),
        root_path = root_path,
        partition_cols = ['lpep_pickup_date'],
        filesystem = pa.fs.GcsFileSystem()
    )


