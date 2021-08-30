'''
Table of Contents:
Import CSV or XLSX - Load in Side Bar
Make import file accessible
Make a graph to visualize the data  #Code this first
'''
import streamlit as st
import pandas as pd
import altair as alt

@st.cache
def load_data():
    data = pd.read_csv('/mnt/c/Users/shrey/Desktop/WadAI/data/data/test_line_list.csv')
    return data

csv_data = load_data()


def main():
    df = load_data()
    st.title("Line List Data Exploration")
    x_axis = st.selectbox("Choose a variable for the x-axis", df.columns, index=3)
    #x_axis = st.select_slider("Choose a variable for the x-axis", df['Weight_in_lbs'].tolist())
    y_axis = st.selectbox("Choose a variable for the y-axis", df.columns, index=4)
    visualize_data(df, x_axis, y_axis)


def visualize_data(df, x_axis, y_axis):
    graph = alt.Chart(df).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        #color='Origin',
        #tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    ).interactive()

    st.write(graph)

if __name__ == "__main__":
    main()