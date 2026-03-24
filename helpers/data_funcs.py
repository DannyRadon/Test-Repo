# This Python File Contains the Data Functions (Group By, Aggregate, etc) for Use with the Streamlit Dashboard

# Import Pool
import streamlit as st
import pandas as pd
import base64





# Helper Function - Converting Icon Images to Base64 Encoding for Dash-Display
def get_base64_image(image_path):
    import base64
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        # If path is wrong, it won't crash your app
        return None




# Monthly Daily Output Function for EDA Page

@st.cache_data
def monthly_output_sums(df):

    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    monthly_summary = df.groupby(df['time'].dt.to_period('M'))['Daily Value Imputed'].sum().reset_index()

    # Convert Period back to timestamp for plotting
    monthly_summary['time'] = monthly_summary['time'].dt.to_timestamp()
    monthly_summary = monthly_summary.set_index('time')

    return monthly_summary



@st.cache_data
def daily_cumulitive(df):
    
    df_cumulative = df.copy()
    df_cumulative['Cumulative Daily'] = df_cumulative['Daily Value Imputed'].cumsum()

    return df_cumulative



@st.cache_data
def total_load_hours(df, sys_cap):

    df_loadsum = df.copy()
    df_loadsum['time'] = pd.to_datetime(df_loadsum['time'], errors='coerce')

    total_energy_kwh = df_loadsum['Daily Value Imputed'].sum()
    
    flh_total = total_energy_kwh / sys_cap
    return flh_total

st.cache_data
def total_generated(df):

    total_gen = df['Daily Value Imputed'].sum()
    return total_gen


st.cache_data
def eco_impacts(df, eco_select):
   
    if eco_select == 'co2_avoided':
        total_co2_avoided = df['co2_avoided'].sum()
        return total_co2_avoided

            