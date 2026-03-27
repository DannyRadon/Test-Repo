# This File Contains the Code for Loading Data

# Import Pool
import streamlit as st
import pandas as pd
import numpy as np


# Defining Function -- Data Loader

@st.cache_data
def load_data():

    # This is just a placeholder for dev purposes, the true data link will probably be cloud
    file_visser = 'data/visser_data_imputed.csv'
    file_bissell = 'data/bissell_data_imputed.csv'
    file_aeso = 'data/aeso_pool_genv2.csv'

   
    df_visser = pd.read_csv(file_visser)
    df_bissell = pd.read_csv(file_bissell)
    df_aeso = pd.read_csv(file_aeso)
    


    return df_visser, df_bissell, df_aeso
