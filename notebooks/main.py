import streamlit as st
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import datetime
import plotly.express as px

from functions import *
from dataloader import *

# x = st.slider('x')
# st.write(x, 'squared is', x * x)

ward_population = pd.read_excel('../data/ward_population.xlsx')
wards = list(ward_population['Ward Name'])

# Add a slider to the sidebar:
st.sidebar.markdown('Filters')
age_range = st.sidebar.slider(
    'Select a range of age',
    0, 110, (0, 110)
)

start_date = datetime.date(2020,3,1)
end_date = datetime.date.today()
# tomorrow = today + datetime.timedelta(days=1)
start_date = st.sidebar.date_input('Start date',start_date)
end_date = st.sidebar.date_input('End date', end_date)


st.sidebar.markdown('Filters')
pop_to_col = {'Age': 'age bracket', 'Gender':'gender', 'Symptomatic Status': 'symptoms status'}
out_to_col = {'Total RTPCR': 'Total RTPCR', 'Total Antigen':'Total Antigen', 'RTPCR Positive': ' Positive', 'RTPCR Negative': ' Negative', 'Antigen Positive' : ' Antigen Positive', 'Antigen Negative': ' Antigen Negative', 'RTPCR TPR':'RTPCR TPR', 'Antigen TPR': 'Antigen TPR'}

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

# Add a selectbox to the sidebar:
pop1 = st.sidebar.selectbox(
    'Population Group 1?',
    ('Age', 'Gender', 'Symptomatic Status')
)

pop2 = st.sidebar.selectbox(
    'Population Group 2?',
    ('Age', 'Gender', 'Symptomatic Status')
)

out1 = st.sidebar.selectbox(
    'Outcome 1? (X Axis)',
    ('Total RTPCR', 'Total Antigen', 'RTPCR Positive', 'RTPCR Negative', 'Antigen Positive','Antigen Negative', 'RTPCR TPR', 'Antigen TPR')
)

out2 = st.sidebar.selectbox(
    'Outcome 2 (Y Axis)',
    ('Total RTPCR', 'Total Antigen', 'RTPCR Positive', 'RTPCR Negative', 'Antigen Positive','Antigen Negative', 'RTPCR TPR', 'Antigen TPR')
)

out3 = st.sidebar.selectbox(
    'Outcome 3 (Size of Bubble)?',
    ('Total RTPCR', 'Total Antigen', 'RTPCR Positive', 'RTPCR Negative', 'Antigen Positive','Antigen Negative', 'RTPCR TPR', 'Antigen TPR')
)


@st.cache
def prepare_data():
    all_data = load_data(['Mumbai'],source='local')
    print (len(all_data))
    mumbai_data = remove_outofMumbai(all_data)
    mumbai_data = add_info(mumbai_data)
    return mumbai_data

mumbai_data = prepare_data()
print("LOOKATME")
print(len(mumbai_data))
input_data = filter_date(mumbai_data,start_date,end_date)
input_data = filter_age(input_data,age_range)
print("LOOKATME")
print(len(input_data))
df = two_pop_groups(input_data, pop_to_col[pop1], pop_to_col[pop2])
st.write(df.head())
# # print(df.head())

# st.write("Hello")


fig = px.scatter(df, x=out_to_col[out1], y=out_to_col[out2],
	         size=out_to_col[out3], color=pop_to_col[pop2], text=pop_to_col[pop1],
                 hover_name=pop_to_col[pop1],size_max=60)
# fig.show()
st.plotly_chart(fig, use_container_width=True)