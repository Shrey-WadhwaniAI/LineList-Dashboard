import streamlit as st
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import datetime
import plotly.express as px

from functions import *
from dataloader import *

wards = ["F/N","F/S","K/E","H/E","G/N","K/W","G/S","A","B","D","M/W","M/E","S","N","E","R/S","H/W","P/S","P/N","T","R/C","L","R/N","C"]

st.sidebar.markdown('Filters')
start_date = datetime.date(2020,3,1)
end_date = datetime.date.today()
start_date = st.sidebar.date_input('Start date',start_date)
end_date = st.sidebar.date_input('End date', end_date)

st.sidebar.markdown('Wards')
ward_selection = st.sidebar.selectbox(
    'Ward Selection Type',
    ('All','Choose Custom','Conditional')
)

selected_wards = []
if ward_selection=='Choose Custom':
    selected_wards = st.sidebar.multiselect('Select wards',wards,default=wards)

if ward_selection=='All':
    selected_wards = wards

out = st.sidebar.selectbox(
    'Outcome (Y Axis)',
    ('Positive RTPCR', 'Total RTPCR Tests', 'RTPCR TPR')
)

@st.cache
def prepare_data():
    all_data = load_data(['Mumbai'],source='s3')
    mumbai_data = remove_outofMumbai(all_data)
    mumbai_data = add_info(mumbai_data)
    return mumbai_data

mumbai_data = prepare_data()
input_data = filter_date(mumbai_data,start_date,end_date)
df = time_series(input_data, out, selected_wards)
st.write(df.head())

df_long = pd.melt(df, id_vars=['date of sample collection'], value_vars=df.columns[1:])
fig = px.line(df_long, x='date of sample collection', y='value', color='ward')
st.plotly_chart(fig, use_container_width=True)