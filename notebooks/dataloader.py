import pandas as pd
import numpy as np
import sys
import streamlit as st
import datetime

from pyathena.connection import Connection
from pyathena.pandas_cursor import PandasCursor

@st.cache
def load_athena(location):
  sql = "SELECT * FROM test_linelist where partition_0='"+location+"' limit 10000"
  cursor = Connection(schema_name='covid-linelist').cursor(PandasCursor)
  df = cursor.execute(sql).as_pandas()
  print(df.head)
  print(df.shape)
  print(df.columns)
  return df

@st.cache
def load_local(path):
    if 'xlsb' in path:
        x = pd.read_excel(path,engine='pyxlsb',header=None)
    elif 'xlsx' in path :
        x = pd.read_excel(path,header=None)
    elif 'csv' in path : 
        x = pd.read_csv(path,header=None)
    else:
        print("Wrong file format")
        return pd.DataFrame()
    
    x = x.dropna(how='all')
    x.columns = x.iloc[0]
    x = x[1:]
    x.columns = ['nan'] + [i.strip().lower() for i in x.columns if str(i)!="nan"] + ['nan']
    print (x.columns, len(x.columns))
    return x

def clean_data(x):
    columns_to_keep = ['icmr id', 'laboratory name', 'patient id', 'age', 'age in', 'gender',
       'state of residence', 'district of residence','pin code',
       'patient category', 'was the patient quarantined',
       'did you travel to foreign country in last 14 days',
       'respiratory infection sari',
       'respiratory infection influenza like illness',
       'are you a healthcare worker involved in managing covid-19 patient',
       'date of sample collection', 'date of sample received',
       'entry date', 'sample type', 'sample id',
       'underlying medical condition', 'hospitalized', 'hospital name',
       'symptoms status', 'symptoms', 'testing kit used', 'egene', 'rdrp',
       'orf1b', 'repeat sample',
       'date of sample tested', 'confirmation date', 'final result sample']
    
    x = x[columns_to_keep]
    # Removes unnecessary serial no. index column
    if len(x.columns)==58:
        x = x.drop(x.columns[-1],axis=1)
    x = x.reset_index()
    x = x.drop('index',axis=1)
    
    # Drop rows that have invalid date fields for date of sample tested
    index_errors = []
    for i in range(len(x)):
        a = x['date of sample tested'].iloc[i]
        b = x['date of sample collection'].iloc[i]
        c = x['date of sample received'].iloc[i]
        d = x['entry date'].iloc[i]
        try:
            date = pd.to_datetime(a)
            date = pd.to_datetime(b)
            date = pd.to_datetime(c)
            date = pd.to_datetime(d)
        except Exception as e:
            index_errors.append(i)
            
    x = x.drop(index_errors)
    print("Dropping %d rows due to invalid dates"%(len(index_errors)))
    
    x['age'] = pd.to_numeric(x['age'], errors='coerce')
    x['date of sample tested'] = pd.to_datetime(x['date of sample tested'])
    x['date of sample tested']  = x['date of sample tested'].dt.date
    x['date of sample collection'] = pd.to_datetime(x['date of sample collection'])
    x['date of sample collection']  = x['date of sample collection'].dt.date
    x['date of sample received'] = pd.to_datetime(x['date of sample received'])
    x['date of sample received']  = x['date of sample received'].dt.date
    x['entry date'] = pd.to_datetime(x['entry date'])
    x['entry date']  = x['entry date'].dt.date
    
    print("Shape of new df is ",x.shape)
    return x

def load_data(locations, source='local'):
    location_data = []
    for location in locations:
        if source=='local':
            data_dir = "../data/Compiled/"
            file_name = 'all_data_urban.csv'
            if(location == ' Mumbai Suburban'):
                file_name = 'Mumbai Suburban.csv'
            df = load_local(data_dir + file_name)

        elif source=='s3':
            df = load_athena(location)

        df = clean_data(df)
        df['source'] = location
        location_data.append(df)
    all_data = pd.concat(location_data)
    print (len(all_data))
    return all_data[:20]