# This Python File Contains the Data Functions (Group By, Aggregate, etc) for Use with the Streamlit Dashboard

# Import Pool
import streamlit as st
import pandas as pd
import base64

import matplotlib.pyplot as plt
import plotly.express as px


# Helper Function - Converting Icon Images to Base64 Encoding for Dash-Display
@st.cache_data
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

@st.cache_data
def total_generated(df):

    total_gen = df['Daily Value Imputed'].sum()
    return total_gen


@st.cache_data
def eco_impacts(df, eco_select):
   
    if eco_select == 'co2_avoided':
        total_co2_avoided = df['co2_avoided'].sum()
        return total_co2_avoided

@st.cache_data
def matplot_vis(df, x_var, y_var, vis_kind, fig_size, color, edgecolor):
    
    df.plot(kind=vis_kind, x=x_var, y=y_var,figsize=fig_size, color=color, edgecolor=edgecolor)

    plt.title('Total Energy Yield by Month')
    plt.ylabel('Total Yield (kWh)')
    plt.xlabel('Month')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(plt)

    return plt.show()


# 
@st.cache_data
def plotly_vis(df, x_var, y_var, vis_kind, color=None, df_select="", data_action=""):
    
    if vis_kind.lower() == "line":
        fig = px.line(df, x=x_var, y=y_var, color_discrete_sequence=[color] if color else None)

    elif vis_kind.lower() == "bar":
        fig = px.bar(df, x=x_var, y=y_var, color_discrete_sequence=[color] if color else None)

    elif vis_kind.lower() == "area":
        fig = px.area(df, x=x_var, y=y_var, color_discrete_sequence=[color] if color else None)

    elif vis_kind.lower() == "scatter":
        fig = px.scatter(df, x=x_var, y=y_var, color_discrete_sequence=[color] if color else None)

    elif vis_kind == "histogram":
        fig = px.histogram(df, x=x_var, y=y_var, color_discrete_sequence=[color] if color else None)
    
    elif vis_kind == "box":
        fig = px.box(df, x=x_var, y=y_var, color_discrete_sequence=[color] if color else None)
    
    elif vis_kind == "violin":
        fig = px.violin(df, x=x_var, y=y_var, color_discrete_sequence=[color] if color else None)
    
    elif vis_kind == "ecdf":
        fig = px.ecdf(df, x=y_var)
    
    elif vis_kind == "matrix":
        
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        corr = df.corr()
        fig = px.imshow(corr)

    elif vis_kind == "pie":
        fig = px.pie(df, values=y_var, names=x_var)

        fig.update_layout(
            title=f"{data_action} for {df_select}",
            template="presentation",  # or "plotly_white"
            paper_bgcolor="rgba(0,0,0,0)",   # transparent background
            plot_bgcolor="rgba(56,196,1,0)"
        )

        fig.update_traces(
            pull=[0.1, 0.1, 0.1, 0.1, 0.1]  # adjust per slice
        )

    elif vis_kind == "tree":
        # Melt the dataset into long format
        site_name = df_select
        df_long = df.melt(
            value_vars=['co2_avoided', 'coal_tonnage_avoided', 'homes_powered', 'cars_offroad'],
            var_name='metric',
            value_name='value'
            )

        # Create treemap
        fig = px.treemap(
            df_long,
            path=[px.Constant(site_name), 'metric'],  # top level is the site
            values='value',
            color='metric',
            color_discrete_map={
                'co2_avoided': '#38c401',
                'coal_tonnage_avoided': '#3170de',
                'homes_powered': '#DE482B',
                'cars_offroad': '#EED842',
                site_name: 'rgba(0,0,0,0)'
            }
        )

        # Layout tweaks for transparent background
        fig.update_layout(
            title=f"{data_action} for {df_select}",
            margin=dict(t=30, l=10, r=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        
    
    else:
        fig = px.line(df, x=x_var, y=y_var)  # fallback


    if vis_kind == "pie":
        
        fig.update_layout(
            title=f"{data_action} for {df_select}",
            template="presentation",  # or "plotly_white"
            paper_bgcolor="rgba(0,0,0,0)",   # transparent background
            plot_bgcolor="rgba(56,196,1,0)"
        )

        fig.update_traces(
            pull=[0.1, 0.1, 0.1, 0.1, 0.1]  # adjust per slice
        )
        fig.update_traces(marker=dict(line=dict(color='#d1d1d1', width=2)))

    else:
        # Layout styling (replaces all your plt.* calls)
        fig.update_layout(
            title=f"{data_action} for {df_select}",
            xaxis_title=x_var,
            yaxis_title=y_var,
            template="presentation",  # or "plotly_white"
            paper_bgcolor="rgba(0,0,0,0)",   # transparent background
            plot_bgcolor="rgba(56,196,1,0)"
        )

    st.plotly_chart(fig)



def aeso_yearly_agg(df, datetime_col="DateTime"):
    df = df.copy()

    # Ensure datetime format
    df[datetime_col] = pd.to_datetime(df[datetime_col])

    # Set as index
    df.set_index(datetime_col, inplace=True)

    # Resample yearly (sum for numeric columns)
    df_yearly = df.resample("Y").sum(numeric_only=True)

    # Reset index
    df_yearly.reset_index(inplace=True)

    return df_yearly



def monthly_agg(df, data_col):
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    
    df_agg = (
        df.groupby(df['time'].dt.to_period('M'))[data_col]
        .sum()
        .reset_index()
    )
    
    #FORCE correct column name
    df_agg.columns = ['time', data_col]
    
    df_agg['time'] = df_agg['time'].dt.to_timestamp()
    
    return df_agg






def weekly_agg(df, data_col):

    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    
    df_agg = (
        df.groupby(df['time'].dt.to_period('W'))[data_col]
        .sum()
        .reset_index()
    )
    
    #FORCE correct column name
    df_agg.columns = ['time', data_col]
    
    df_agg['time'] = df_agg['time'].dt.to_timestamp()
    
    return df_agg





# CHAT GPT HELPER FUNCTION -- WARNING! --- URL Link Builder Helper Function ------------------------
import urllib.parse

def build_url(**kwargs):
    # Start with what is CURRENTLY in session state
    params = {
        'dataset': st.session_state.get('dataset'),
        'graph': st.session_state.get('graph_type'),
        'x_var': st.session_state.get('x_var'),
        'y_var': st.session_state.get('y_var'),
    }
    # Overwrite only the specific change (e.g., changing just the dataset)
    params.update(kwargs)
    
    # Clean out None values and encode for URL safety
    query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return f"?{query_string}"


# THIS FUNCTION IS SPECIFICALLY FOR THE ML PAGE SO THAT THE VARIABLES DONT CONFLICT WITH ANALYTICS PAGE...

def build_url_ml(**kwargs):
    # Start with what is CURRENTLY in session state
    params = {
        'dataset': st.session_state.get('dataset'),
        'graph': st.session_state.get('graph_type'),
        'x': st.session_state.get('x'),
        'y_test': st.session_state.get('y_test'),
        'view_type': st.session_state.get('view_type')
    }
    # Overwrite only the specific change (e.g., changing just the dataset)
    params.update(kwargs)
    
    # Clean out None values and encode for URL safety
    query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return f"?{query_string}"


def build_impact_url(toggle_var):
    """
    Adds the variable to the list if it's not there, 
    or removes it if it is (toggling).
    """
    current_vars = st.session_state.get('selected_impacts', [])
    
    if toggle_var in current_vars:
        new_vars = [v for v in current_vars if v != toggle_var]
    else:
        new_vars = current_vars + [toggle_var]
        
    # Join list into a comma-separated string for the URL: ?impacts=carbon,trees
    params = dict(st.query_params)
    params['impacts'] = ",".join(new_vars)
    return "?" + urllib.parse.urlencode(params)

    # Sample toggle handler
def toggle_impact(impact_name):
    current = st.session_state.selected_impacts
    if impact_name in current:
        current.remove(impact_name)
    else:
        current.append(impact_name)
    st.session_state.selected_impacts = current


def build_treemap(df, site_name):
    # Melt the dataset into long format
    df_long = df.melt(
        value_vars=['co2_avoided', 'coal_tonnage_avoided', 'homes_powered', 'cars_offroad'],
        var_name='metric',
        value_name='value'
    )

    # Create treemap
    fig = px.treemap(
        df_long,
        path=[px.Constant(site_name), 'metric'],  # top level is the site
        values='value',
        color='metric',
        color_discrete_map={
            'co2_avoided': '#38c401',
            'coal_tonnage_avoided': '#3170de',
            'homes_powered': '#DE482B',
            'cars_offroad': '#EED842',
        },
        bordercolor='#d1d1d1'
    )

    # Layout tweaks for transparent background
    fig.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)


@st.cache_data
def load_data_aeso():
    aeso = pd.read_csv("data/aeso_pool_genv2.csv")
    return aeso


@st.cache_data    
def aeso_daily_agg(df, datetime_col="DateTime"):
    df = df.copy()

    # Ensure datetime format
    df[datetime_col] = pd.to_datetime(df[datetime_col])

    # Set as index
    df.set_index(datetime_col, inplace=True)

    # Aggregate to daily (sum for numeric columns)
    df_daily = df.resample("D").sum(numeric_only=True)

    # Reset index so DateTime comes back as a column
    df_daily.reset_index(inplace=True)

    return df_daily