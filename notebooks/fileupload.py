from enum import Enum
from io import BytesIO, StringIO
from typing import Union
 
import pandas as pd
import streamlit as st
import altair as alt

##except Exception as e:
##    print(e)
 
STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""
 
 
class FileUpload(object):
 
    def __init__(self):
        self.fileTypes = ["csv"]
 
    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        file = st.file_uploader("Upload file", type=self.fileTypes)
        show_file = st.empty()
        if not file:
            show_file.info("Please upload a file of type: " + ", ".join(["csv"]))
            return
        content = file.getvalue()
        data = pd.read_csv(file)
        st.dataframe(data.head(10))
        file.close()
    @st.cache
    def load_data():
        df = pd.read_csv(st.file_uploader("Upload file", type=self.fileTypes))
        return df
    def main():
        df = load_data()
        page = st.sidebar.selectbox("Choose a page", ["Homepage", "Exploration"])

        if page == "Homepage":
            st.header("This is your data explorer.")
            st.write("Please select a page on the left.")
            st.write(df)
        elif page == "Exploration":
            st.title("Data Exploration")
            x_axis = st.selectbox("Choose a variable for the x-axis", df.columns, index=3)
            y_axis = st.selectbox("Choose a variable for the y-axis", df.columns, index=4)
            visualize_data(df, x_axis, y_axis)
    def visualize_data(df, x_axis, y_axis):
        graph = alt.Chart(df).mark_circle(size=60).encode(
            x=x_axis,
            y=y_axis,
            color='Origin',
            tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
        ).interactive()

        st.write(graph)
    







if __name__ ==  "__main__":
    helper = FileUpload()
    helper.run()
    helper.load_data
    helper.main
    helper.visualize_data(pd.read_csv(st.file_uploader("Upload file", type=self.fileTypes)), st.selectbox("Choose a variable for the x-axis", df.columns, index=3), y_axis = st.selectbox("Choose a variable for the y-axis", df.columns, index=4))