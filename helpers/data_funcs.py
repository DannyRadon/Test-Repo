# This Python File Contains the Data Functions (Group By, Aggregate, etc) for Use with the Streamlit Dashboard

# Import Pool
import streamlit as st
import pandas as pd

# Monthly Daily Output Function for EDA Page

@st.cache_data
def monthly_output_sums(df):

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    monthly_summary = df.groupby(df['Date'].dt.to_period('M'))['Daily Value (kWh)'].sum().reset_index()

    # Convert Period back to timestamp for plotting
    monthly_summary['Date'] = monthly_summary['Date'].dt.to_timestamp()

    return monthly_summary



@st.cache_data
def daily_cumulitive(df):
    
    df_cumulative = df.copy()
    df_cumulative['Cumulative Daily'] = df_cumulative['Daily Value (kWh)'].cumsum()

    return df_cumulative



@st.cache_data
def total_load_hours(df):

    df_loadsum = df.copy()
    df_loadsum['Date'] = pd.to_datetime(df_loadsum['Date'], errors='coerce')

    df_loadsum = (
        df_loadsum
        .groupby(df_loadsum['Date'].dt.to_period('M'))['Full Load Hours (Monthly)']
        .first()       
    )
    
    return df_loadsum.sum()