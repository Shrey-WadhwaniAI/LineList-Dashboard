from utils import *
import streamlit as st


def pop_filter(x,pops):
    if 'gender' in pops : 
        x = get_valid_gender(x)
    return x
    

@st.cache
def two_pop_groups(data,pop1,pop2):
    df = remove_untested(data)
    #print("untested filter")
    #print(len(df))
    df = pop_filter(df,[pop1,pop2])
    #print(len(df))
    grouped = df.groupby([pop1, pop2,'final result sample']).agg('size')
    #print("grouped data")
    #print(grouped)
    grouped.to_csv('../data/grouped.csv')
    df2 = grouped.unstack(fill_value=0)
    df2 = add_test_summary(df2)
    df2 = df2.round(4)
    df2 = df2.reset_index()
    # df2.to_csv('../Outputs/agegender_tests.csv')
    return df2