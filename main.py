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
        #try to read the csv file
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]  # Strip whitespace from column names
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %y")  #Turn date into pandsa acceptable format
        df["Amount"] = df["Amount"].astype(float)  #Ensure Amount is float
        df["Balance"] = df["Balance"].astype(float) #Ensure Balance is float

        st.write(df)
        return df
    
    except Exception as e:
        #if cant read the csv, display an error message
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
        #if file is uploaded, process the data
        df = load_transactions(upload_file)

        #Catagorising data
        if df is not None:
            #Creatinf a new column for in/out transactions
            in_df = df[df["Amount"] > 0].copy()
            out_df = df[df["Amount"] < 0].copy()
            


main()
    