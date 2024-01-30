#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from time import time
import argparse 
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    table_name1 = params.table_name1
    url1 = params.url1
    table_name2 = params.table_name2
    url2 = params.url2

    if url1.endswith('.csv.gz'):
        csv_name1 = 'output1.csv.gz'
    else:
        csv_name1 = 'output1.csv'
    
    if url2.endswith('.csv.gz'):
        csv_name2 = 'output2.csv.gz'
    else:
        csv_name2 = 'output2.csv'

    os.system(f"wget {url1} -O {csv_name1}")
    os.system(f"wget {url2} -O {csv_name2}")

    # download the csv

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    df_total = pd.read_csv(csv_name1, dtype='unicode')

    df = pd.read_csv(csv_name1, nrows = 100)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name = table_name1, con = engine, if_exists = 'replace')

    df_iter = pd.read_csv(csv_name1, iterator=True, chunksize=100000)

    n = 0
    rowcount = len(df_total.index)

    print('%.d rows to be inserted...' % (rowcount))

    for item in df_iter:
        
        chunkcount = len(item.index)
        t_start = time()
        
        item.lpep_pickup_datetime = pd.to_datetime(item.lpep_pickup_datetime)
        item.lpep_dropoff_datetime = pd.to_datetime(item.lpep_dropoff_datetime)
        
        item.to_sql(name = table_name1, con = engine, if_exists = 'append')
        
        t_end = time()
        n = n+1
        
        print('Chunk %.d with %.d rows inserted, took %.3f seconds...' % (n, chunkcount, t_end - t_start))
        
    df_zones = pd.read_csv(csv_name2)
    
    df_zones.head(n=0).to_sql(name = table_name2, con = engine, if_exists = 'replace')
    df_zones.to_sql(name = table_name2, con = engine, if_exists = 'append')

    print('Zones file inserted.') 


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        prog='ingester',
                        description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help= 'username for postgres')
    parser.add_argument('--password', help= 'password for postgres')
    parser.add_argument('--host', help= 'host for postgres')
    parser.add_argument('--port', help= 'port for postgres')
    parser.add_argument('--db_name', help= 'database name for postgres')
    parser.add_argument('--table_name1', help= 'table 1 name where the results will be written')
    parser.add_argument('--url1', help= 'url of csv 1 file')
    parser.add_argument('--table_name2', help= 'table 2 name where the results will be written')
    parser.add_argument('--url2', help= 'url of csv 2 file')

    args = parser.parse_args()

    main(args)



