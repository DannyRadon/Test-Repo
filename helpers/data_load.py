# This File Contains the Code for Loading Data

# Import Pool
import streamlit as st
import pandas as pd
import numpy as np


# Defining Function -- Data Loader

@st.cache_data
def load_data():

    file = '/workspaces/Test-Repo/data/bv_merged.csv'   # This is just a placeholder for dev purposes, the true data link will probably be cloud

    file_visser = '/workspaces/Test-Repo/data/visser_data_imputed.csv'
    file_bissell = '/workspaces/Test-Repo/data/bissell_data_imputed.csv'

    df = pd.read_csv(file)
    df_visser = pd.read_csv(file_visser)
    df_bissell = pd.read_csv(file_bissell)

    return df_visser, df_bissell