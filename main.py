import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Mah Finances", layout="wide")

custom_catagory_file = "custom_categories.json"

#Store categories in session state
if "custom_categories" not in st.session_state:
    st.session_state.custom_categories = {
        "Uncategorized": []
    }

#Load categories from JSON file if it exists
if os.path.exists(custom_catagory_file):
    with open(custom_catagory_file, "r") as f:
        st.session_state.custom_categories = json.load(f)

def save_categories():
    """Save categories to JSON file"""
    with open(custom_catagory_file, "w") as f:
        json.dump(st.session_state.custom_categories, f, indent=4)

def custom_catagorise_transaction(df):
    df["Custom Category"] = "Uncategorized"  # Default category

    for cust_cat, keywords in st.session_state.custom_categories.items():
        if cust_cat == "Uncategorized" or not keywords:
            continue

        lower_keywords = [keyword.lower().strip() for keyword in keywords]

        
        for idx, row in df.iterrows():
            details = row["Merchant Name"].lower().strip() if pd.notna(row["Merchant Name"]) else ""
            # print(details)
            # Check if any rows Mearchant Name already has a category assigned
            if details in lower_keywords:
                df.at[idx, "Custom Category"] = cust_cat

            #If it has no merchant name, take make Custom Category the default, existing category
            elif details == "":
                print(df.at[idx,"Transaction Details"]," No Merchant Name -->    ", df.at[idx, "Category"])
                df.at[idx, "Custom Category"] = df.at[idx, "Category"]

    return df

def add_keyword_to_category(category, keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.custom_categories[category]:
        st.session_state.custom_categories[category].append(keyword)
        save_categories()
        return True
    return False

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
        df.columns = [col.strip() for col in df.columns]  #Strip whitespace from column names
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %y")  #Turn date into pandsa acceptable format
        df["Amount"] = df["Amount"].astype(float)  #Ensure Amount is float
        df["Balance"] = df["Balance"].astype(float) #Ensure Balance is float

        return custom_catagorise_transaction(df)
    
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

        # st.write("Preview of categorized data:")
        # st.dataframe(df[["Merchant Name", "Category", "Custom Category"]])


        #Catagorising data
        if df is not None:
            #Creatinf a new column for in/out transactions
            in_df = df[df["Amount"] > 0].copy()
            out_df = df[df["Amount"] < 0].copy()

            st.session_state.out_df = out_df.copy()

            tab1, tab2 = st.tabs(["Out/Credit", "In/Debit"])
            with tab1:
                new_catagory = st.text_input("New Custom Category name")
                add_button = st.button("Add Custom Category")

                if add_button and new_catagory:
                    if new_catagory not in st.session_state.custom_categories:
                        st.session_state.custom_categories[new_catagory] = []
                        save_categories()
                        st.rerun()

                st.subheader("Your Expenses")
                # Combine manually defined + fallback categories for selectbox options
                all_category_options = list(set(
                    list(st.session_state.custom_categories.keys()) +
                    df["Category"].dropna().unique().tolist()
                ))

                edited_df = st.data_editor(
                    st.session_state.out_df[["Date","Merchant Name", "Transaction Details","Category", "Amount", "Balance", "Custom Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MMM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f"),
                        "Balance": st.column_config.NumberColumn("Balance", format="%.2f"),
                        "Custom Category": st.column_config.SelectboxColumn(
                            "Custom Category",
                            options=all_category_options,
                        )},
                        hide_index=True,
                        use_container_width=True,
                        key="cust_catagory_editor"
                
                )

                save_button = st.button("Save Changes", type="primary")
                if save_button:
                    #check every row in edited_df for changes
                    for idx, row in edited_df.iterrows():
                        new_cust_cat = row["Custom Category"]

                        #If no changes made, continue
                        if new_cust_cat == st.session_state.out_df.at[idx, "Custom Category"]:
                            continue
                        
                        #If a change was made we use the Transaction Details to an identifier
                        #Change this to make use of Merchant Name, 
                        # and in the case of no merchant name, make CUstCat the default catagory the bank assigned to the transaction
                        details = row["Merchant Name"]
                        st.session_state.out_df.at[idx, "Custom Category"] = new_cust_cat
                        # add_keyword_to_category(new_cust_cat, details)
                        if pd.notna(details) and details.strip():
                            add_keyword_to_category(new_cust_cat, details.strip())
                        # print("added")
                       

            with tab2:
                st.write(in_df)
            


main()
    