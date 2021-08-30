import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyxlsb import convert_date
import datetime
import random

# Functions to Add More Information to the Data
def add_test_summary(x):
    x['Total Antigen'] = x[' Antigen Positive'] + x[' Antigen Negative']
    x['Total RTPCR'] = x[' Positive'] + x[' Negative']
    x['Antigen TPR'] = x[' Antigen Positive'] / x['Total Antigen']
    x['RTPCR TPR'] = x[' Positive'] / x['Total RTPCR']
    return x

def get_age_bracket(row):
    age = int(row)
    if age<=20:
        return '0-20'
    elif age<=40:
        return '21-40'
    elif age<=60:
        return '41-60'
    elif age<=80:
        return '61-80'
    else:
        return '80+'


def get_ward(x):
    pin_to_ward_df = pd.read_excel('../data/pincode_to_ward.xlsx',dtype=str)
    pin_to_ward = pin_to_ward_df.set_index(' Pin Code')['WARD'].to_dict()
    if x in pin_to_ward.keys():
        wards = pin_to_ward[x].split(',')
        n_wards = len(wards)
        i = random.randint(0,n_wards-1)
        return wards[i].strip(' ')
    else:
        return "Not Available"

def add_info(x):
    x['age bracket'] = x.apply(lambda row: get_age_bracket(row['age']),axis=1)
    x['ward'] = x.apply(lambda row: get_ward(row['pin code']),axis=1)
    return x

# Filters
def remove_outofMumbai(x):
    labs = []
    # Labs include those in Mumbai, Thane, Mira Bhayander, and Worli
    for i in x['laboratory name'].value_counts().index:
        if ('Mumbai' in i) or ('Thane' in i) or ('Bhayandar' in i) or ('Worli' in i):
            labs.append(i)
    labs.append(' Tata Memorial Centre Advanced Centre for Treatment  Research and Education in Cancer')
    labs.append(' INHS Asvini')
    labs.append(' Krsnaa Diagnostics Pvt Ltd  Pune')
    labs.append(' Maa Sasheb Meenatai Thakre')

    mumbai_data = x[x['laboratory name'].isin(labs)]
    print("Length of original dataframe : ", len(x))
    print("Length of Mumbai samples only : ", len(mumbai_data))
    return mumbai_data

def remove_repeat_samples(x):
    return x[x['repeat sample'] == ' No']

def remove_invalidpin(x):
    valid_pinvals = [str(i) for i in range(400001,400106)]
    return x[x['pin code'].isin(valid_pinvals)]

def remove_backdated(x, cutoff_date = datetime.date(2020,3,1)):
    return x[x['date of sample tested'] >= cutoff_date]

def filter_date(x, start_date, end_date=datetime.date.today()):
    x =  x[x['date of sample tested'] >= start_date]
    x =  x[x['date of sample tested'] <= end_date]
    return x

def filter_age(x, age_range):
    x =  x[x['age'] >= age_range[0]]
    x =  x[x['age'] <= age_range[1]]
    return x

def get_valid_gender(x):
    valid_vals = [' F', ' M']
    return x[x['gender'].isin(valid_vals)]

def remove_untested(x):
    good_data_vals = [' Negative', ' Positive', ' Antigen Positive',' Antigen Negative']
    return x[x['final result sample'].isin(good_data_vals)]

# def rtpcr_res(row):
#     if(row['Total RTPCR'] == 0):
#         return "NA"
#     elif(row[' Positive'] > 0):
#         return 'Positive'
#     else:
#         return 'Negative'

# def antigen_res(row):
#     if(row['Total Antigen'] == 0):
#         return "NA"
#     elif(row[' Antigen Positive'] > 0):
#         return 'Positive'
#     else:
#         return 'Negative'