import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from helpers.data_funcs import load_data_aeso
from src.aeso_cleaning_fe1 import clean_fe1
from src.modeling import run_modeling_pipeline
from helpers.data_funcs import *

import plotly.tools as tls
import plotly.graph_objects as go


@st.cache_data
def load_clean_data():
    aeso = load_data_aeso()
    return clean_fe1(aeso)

@st.cache_resource
def load_model_outputs():
    aeso_clean = load_clean_data()
    return run_modeling_pipeline(aeso_clean)

def plot_prediction_view(outputs, selected_target):
    train_df = outputs["train_df"]
    test_df = outputs["test_df"]
    results = outputs["results"]

    fig, ax = plt.subplots(figsize=(12, 5))

    if selected_target == "solar_generation_per_capacity":
        ax.plot(train_df["time"], train_df["solar_generation_per_capacity"], label="Train")
        ax.plot(test_df["time"], test_df["solar_generation_per_capacity"], label="Test Actual")
        ax.plot(results["time"], results["pred"], label="Test Predicted")
    elif selected_target == "total_generation__solar":
        ax.plot(results["time"], results["actual_total_generation__solar"], label="Actual")
        ax.plot(results["time"], results["pred_total_generation__solar"], label="Predicted")
    elif selected_target == "solar_market_share":
        ax.plot(results["time"], results["actual_solar_market_share"], label="Actual")
        ax.plot(results["time"], results["pred_solar_market_share"], label="Predicted")
    elif selected_target == "emissions_avoided":
        ax.plot(results["time"], results["actual_emissions_avoided"], label="Actual")
        ax.plot(results["time"], results["pred_emissions_avoided"], label="Predicted")

    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.subplots_adjust(
        left=0.1,
        right=0.9,
        top=0.95,
        bottom=0.05
    )       
    st.plotly_chart(fig, use_container_width=True)
@st.cache_data
def plot_xai_view(outputs):
    fi = outputs["feature_importance"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(fi["feature"], fi["importance"])
    ax.invert_yaxis()
    plt.subplots_adjust(
        left=0.01,
        right=0.9,
        top=0.95,
        bottom=0.05
    )       
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def plot_forecast_view(outputs, selected_target):
    monthly = outputs["monthly"]
    forecast_df = outputs["forecast_df"]

    fig, ax = plt.subplots(figsize=(12, 5))
    

    if selected_target == "solar_generation_per_capacity":
        ax.plot(monthly["time"], monthly["solar_generation_per_capacity"], label="Historical")
        for scen in forecast_df["scenario"].unique():
            temp = forecast_df[forecast_df["scenario"] == scen]
            ax.plot(temp["time"], temp["forecast_generation_per_capacity"], linestyle="--", label=scen)

    elif selected_target == "total_generation__solar":
        ax.plot(monthly["time"], monthly["total_generation__solar"], label="Historical")
        for scen in forecast_df["scenario"].unique():
            temp = forecast_df[forecast_df["scenario"] == scen]
            ax.plot(temp["time"], temp["forecast_total_generation__solar"], linestyle="--", label=scen)

    elif selected_target == "solar_market_share":
        ax.plot(monthly["time"], monthly["solar_market_share"], label="Historical")
        for scen in forecast_df["scenario"].unique():
            temp = forecast_df[forecast_df["scenario"] == scen]
            ax.plot(temp["time"], temp["forecast_solar_market_share"], linestyle="--", label=scen)

    elif selected_target == "emissions_avoided":
        ax.plot(monthly["time"], monthly["emissions_avoided"], label="Historical")
        for scen in forecast_df["scenario"].unique():
            temp = forecast_df[forecast_df["scenario"] == scen]
            ax.plot(temp["time"], temp["forecast_emissions_avoided"], linestyle="--", label=scen)
            
            
    plt.subplots_adjust(
        left=0.01,
        right=0.9,
        top=0.95,
        bottom=0.05
    )    
    
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.plotly_chart(fig)


outputs = load_model_outputs()
