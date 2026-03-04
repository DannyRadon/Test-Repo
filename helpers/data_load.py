# This File Contains the Code for Loading Data

# Import Pool
import streamlit as st
import pandas as pd
import numpy as np


# Defining Function -- Data Loader

@st.cache_data
def load_data():

    file = '/workspaces/Test-Repo/data/bv_merged.csv'
    df = pd.read_csv(file)

    return df