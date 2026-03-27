import streamlit as st
import pandas as pd
import numpy as np



# COMBINE CLEANING AND FE SO YOU CAN USE IT FOR EDA VISUALS AND ML  *note this is not all the FE, its only the newly created features for the EDA visuals, the full ml fe will be another function


def clean_fe1(aeso):
    # CLEANINg
    aeso_clean = aeso.copy()
    aeso__clean = aeso.drop(columns=['Unnamed: 0', 'forecast_pool_price'])
    # Transform datetime into cols
    aeso__clean['DateTime'] = pd.to_datetime(aeso__clean['DateTime'], format="%Y-%m-%d %H:%M")
    aeso__clean['year'] = aeso__clean['DateTime'].dt.year
    aeso__clean['month'] = aeso__clean['DateTime'].dt.month
    aeso__clean['day'] = aeso__clean['DateTime'].dt.day
    aeso__clean['hour'] = aeso__clean['DateTime'].dt.hour

    # sort values by datetime
    aeso__clean = aeso__clean.sort_values('DateTime').reset_index(drop=True)

    # impute negative values of total generation solar to 0
    aeso__clean['total_generation__solar'] = aeso__clean['total_generation__solar'].apply(lambda x: 0 if x < 0 else x)


    # New feature: total generation summed for all fuel types over each row (ie. hour)
    aeso__clean['total_gen_all'] = aeso__clean[[col for col in aeso__clean.columns if 'total_generation__' in col]].sum(axis=1)

    # new feature: solar market share  ---> target feature
    aeso__clean['solar_market_share_total_gen'] = np.where(
      aeso__clean['total_gen_all'] > 0,
    aeso__clean['total_generation__solar'] / aeso__clean['total_gen_all'],
    np.nan
)

    # New feature: emissions avoided with solar (0.52tonnes CO2/MWh)
    aeso__clean['emissions_avoided'] = aeso__clean['total_generation__solar'] * 0.52

    ## modeling target feature :solar_generation_per_capacity ----> use these predicted values to calucalte actual target of solar market share
    aeso__clean['solar_generation_per_capacity'] = (
      aeso__clean['total_generation__solar'] / aeso__clean['maximum_capacity__solar']
  )

    return aeso__clean



