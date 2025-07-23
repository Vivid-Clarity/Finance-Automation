import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Mah Finances", layout="wide")

def load_transactions(file):
    """Use pandas to process the csv data from uploaded file

    Args:
        file (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        df = pd.read_csv(file)
        st.write(df)
        return df
    
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def main():
    """
    Main function to run the Streamlit app
    """
    st.title("Mah Finances")
    #streamlit built in file uploader
    upload_file = st.file_uploader("Upload account statement(CSV file)", type=["csv"])

    if upload_file is not None:
        df = load_transactions(upload_file)


main()
    