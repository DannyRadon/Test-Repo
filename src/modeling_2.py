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

def plot_prediction_view(train_df, test_df, results, target, g_type):

    fig = go.Figure()
    
    # Rendering a Line Graph Visualization per User Selection
    if g_type == "Line":
        
        # Actual
        fig.add_trace(go.Line(
            x=results["time"],
            y=results["actual"],
            mode="lines",
            name=f"Actual"
        ))
        
        # Predicted
        fig.add_trace(go.Line(
            x=results["time"],
            y=results["pred"],
            mode="lines",
            line=dict(dash="dash"),
            line_color="white",
            name=f"Predicted"
        ))
        
        fig.update_layout(
            title=f"Actual vs Predicted ({target})",
            xaxis_title="Time",
            yaxis_title=target,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )        
    
    # Rendering a Scatter Graph Visualization per User Selection 
    elif g_type == "Scatter":
        # Actual
        fig.add_trace(go.Scatter(
            x=results["time"],
            y=results["actual"],
            mode="markers",
            name=f"Actual"
        ))
        
        # Predicted
        fig.add_trace(go.Scatter(
            x=results["time"],
            y=results["pred"],
            mode="markers",
            marker=dict(color="white"),
            name=f"Predicted"
        ))
        
        fig.update_layout(
            title=f"Actual vs Predicted ({target})",
            xaxis_title="Time",
            yaxis_title=target,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )        
    
    # Rendering a Bar Graph Visualization per User Selection
    elif g_type == "Bar":
        # Actual
        fig.add_trace(go.Bar(
            x=results["time"],
            y=results["actual"],
            name=f"Actual"
        ))
        
        # Predicted
        fig.add_trace(go.Bar(
            x=results["time"],
            y=results["pred"],
            name=f"Predicted"
        ))
        
        fig.update_layout(
            title=f"Actual vs Predicted ({target})",
            xaxis_title="Time",
            yaxis_title=target,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
    
    elif g_type == "Box":
        # Actual
        fig.add_trace(go.Box(
            x=results["time"],
            y=results["actual"],
            name=f"Actual"
        ))
        
        # Predicted
        fig.add_trace(go.Box(
            x=results["time"],
            y=results["pred"],
            name=f"Predicted"
        ))
        
        fig.update_layout(
            title=f"Actual vs Predicted ({target})",
            xaxis_title="Time",
            yaxis_title=target,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )        
        
        
    st.plotly_chart(fig, use_container_width=True)
    

    
    

def plot_xai_view(features):
    fi = features["feature_importance"]
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


def plot_forecast_view(outputs, target):
    monthly = outputs["monthly"]
    forecast_df = outputs["forecast_df"]

    fig, ax = plt.subplots(figsize=(12, 5))
    

    if target == "solar_generation_per_capacity":
        ax.plot(monthly["time"], monthly["solar_generation_per_capacity"], label="Historical")
        for scen in forecast_df["scenario"].unique():
            temp = forecast_df[forecast_df["scenario"] == scen]
            ax.plot(temp["time"], temp["forecast_generation_per_capacity"], linestyle="--", label=scen)

    elif target == "total_generation__solar":
        ax.plot(monthly["time"], monthly["total_generation__solar"], label="Historical")
        for scen in forecast_df["scenario"].unique():
            temp = forecast_df[forecast_df["scenario"] == scen]
            ax.plot(temp["time"], temp["forecast_total_generation__solar"], linestyle="--", label=scen)

    elif target == "solar_market_share":
        ax.plot(monthly["time"], monthly["solar_market_share"], label="Historical")
        for scen in forecast_df["scenario"].unique():
            temp = forecast_df[forecast_df["scenario"] == scen]
            ax.plot(temp["time"], temp["forecast_solar_market_share"], linestyle="--", label=scen)

    elif target == "emissions_avoided":
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


