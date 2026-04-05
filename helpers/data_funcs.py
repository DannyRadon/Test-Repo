# This Python File Contains the Data Functions (Group By, Aggregate, etc) for Use with the Streamlit Dashboard

# Import Pool
import streamlit as st
import pandas as pd
import numpy as np
import base64

import pvlib

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

import streamlit.components.v1 as stc

from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


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





# Helper to avoid repetitive code
@st.cache_data
def get_scoped_metrics(actual, pred):
    return {
        "RMSE": np.sqrt(mean_squared_error(actual, pred)),
        "MAE": mean_absolute_error(actual, pred),
        "R2": r2_score(actual, pred),
        "MAPE": np.mean(np.abs((actual - pred) / actual)) * 100
    } 

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







# CODE SECTION FOR UTILITIES / TOOLS -----------------------------------

def calculator(width=350, height=450):
    
    with open("utils/calculator.html", "r") as calc_file:
        page = calc_file.read()
        stc.html(page, width=width, height=height, scrolling=False)
    
    # Encode it so the IFrame can read it as a source
    b64_calc = base64.b64encode(calc_html.encode()).decode()
    calc_src = f"data:text/html;base64,{b64_calc}"    







# Data Cleaning Function for AESO
@st.cache_data
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








# Function for Feature Engineering Cleaned AESO Dataset
@st.cache_data
def fe(aeso_clean):
    
    EMISSIONS_FACTOR = 0.52
    
    monthly = (
        aeso_clean.groupby(['year', 'month'], as_index=False)
        .agg({
            'total_generation__solar': 'sum',
            'maximum_capacity__solar': 'mean',
            'system_available__solar': 'mean',
            'pool_price': 'mean',
            'total_gen_all': 'sum',
            'emissions_avoided': 'sum'
        })
    )

    monthly['time'] = pd.to_datetime(
        monthly[['year', 'month']].assign(day=1)
    )
    monthly = monthly.sort_values('time').reset_index(drop=True)

    monthly['solar_generation_per_capacity'] = (
        monthly['total_generation__solar'] / monthly['maximum_capacity__solar']
    )

    monthly['solar_market_share'] = (
        monthly['total_generation__solar'] / monthly['total_gen_all']
    )

    target = 'solar_generation_per_capacity'

    monthly['time_index'] = np.arange(len(monthly))
    monthly['month_num'] = monthly['time'].dt.month

    for k in range(1, 5):
        monthly[f'sin_year_{k}'] = np.sin(2 * np.pi * k * monthly['month_num'] / 12)
        monthly[f'cos_year_{k}'] = np.cos(2 * np.pi * k * monthly['month_num'] / 12)

    monthly['availability_ratio'] = (
        monthly['system_available__solar'] / monthly['maximum_capacity__solar']
    )

    monthly['gen_per_cap_lag_1'] = monthly[target].shift(1)
    monthly['gen_per_cap_lag_12'] = monthly[target].shift(12)

    monthly['pool_price_roll_3'] = monthly['pool_price'].shift(1).rolling(3).mean()
    monthly['pool_price_roll_6'] = monthly['pool_price'].shift(1).rolling(6).mean()

    monthly = (
        monthly.replace([np.inf, -np.inf], np.nan)
        .dropna()
        .reset_index(drop=True)
    )

    return monthly






# Data Processing Function for Model 3
@st.cache_data
def ProcessDataM3(aeso_fe, selected_target):
    
    target = selected_target
    
    # monthly df
    monthly_gen = (
        aeso_fe.groupby(['year', 'month'], as_index=False)
        .agg({
            'total_generation__solar': 'sum',
            'maximum_capacity__solar': 'mean',
            'system_available__solar': 'mean',
            'pool_price': 'mean',
            'total_gen_all': 'sum',
            'emissions_avoided': 'sum'  ############# new -- forgot to add emissions data ealier
        })
    )
    
    monthly_gen['time'] = pd.to_datetime(
        monthly_gen[['year', 'month']].assign(day=1)
    )
    monthly_gen = monthly_gen.sort_values('time').reset_index(drop=True)
    
    monthly_gen['solar_generation_per_capacity'] = (
        monthly_gen['total_generation__solar'] / monthly_gen['maximum_capacity__solar']
    )
    
    monthly_gen['solar_market_share'] = (
        monthly_gen['total_generation__solar'] / monthly_gen['total_gen_all']
    )
    
    monthly_gen = (
        monthly_gen.replace([np.inf, -np.inf], np.nan)
        .dropna()
        .reset_index(drop=True)
    )
    
    target = 'solar_generation_per_capacity'
    
    # build features
    df = monthly_gen.copy()
    
    # linear trend
    df['time_index'] = np.arange(len(df))
    
    # month number
    df['month_num'] = df['time'].dt.month
    
    # Fourier order 4
    for k in range(1, 5):
        df[f'sin_year_{k}'] = np.sin(2 * np.pi * k * df['month_num'] / 12)
        df[f'cos_year_{k}'] = np.cos(2 * np.pi * k * df['month_num'] / 12)
    
    # availability ratio
    df['availability_ratio'] = (
        df['system_available__solar'] / df['maximum_capacity__solar']
    )
    
    # lag set A
    df['gen_per_cap_lag_1'] = df[target].shift(1)
    df['gen_per_cap_lag_12'] = df[target].shift(12)
    
    # pool price rolling
    df['pool_price_roll_3'] = df['pool_price'].shift(1).rolling(3).mean()
    df['pool_price_roll_6'] = df['pool_price'].shift(1).rolling(6).mean()
    
    features = [
        'time_index',
    
        'sin_year_1', 'cos_year_1',
        'sin_year_2', 'cos_year_2',
        'sin_year_3', 'cos_year_3',
        'sin_year_4', 'cos_year_4',
    
        'system_available__solar',
        'availability_ratio',
    
        'pool_price',
        'pool_price_roll_3',
        'pool_price_roll_6',
    
        'gen_per_cap_lag_1',
        'gen_per_cap_lag_12'
    ]
    
    df_model = df.dropna().reset_index(drop=True)    
    
    return df_model, features, selected_target







# Training Function for Model-3

@st.cache_data
def TrainModel3(df_model, features, selected_target, monthly):
    
    EMISSIONS_FACTOR = 0.52
    
    # train/test split
    test_size = int(np.ceil(len(df_model) * 0.20))
    train_df = df_model.iloc[:-test_size].copy()
    test_df  = df_model.iloc[-test_size:].copy()
    
    X_train = train_df[features]
    y_train = train_df[selected_target]
    
    X_test = test_df[features]
    y_test = test_df[selected_target]
    
    
    # train model XGBoost
    model = XGBRegressor(
        max_depth=2,
        learning_rate=0.05,
        n_estimators=300,
        subsample=0.8,
        colsample_bytree=1.0,
        objective='reg:squarederror',
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # predict
    test_pred = model.predict(X_test)
    
    results = test_df[['time']].copy()
    results['actual'] = y_test.values
    results['pred'] = test_pred
    results['error'] = results['actual'] - results['pred']
    results['abs_error'] = np.abs(results['error'])    
    
    # columns needed for conversions
    results['maximum_capacity__solar'] = test_df['maximum_capacity__solar'].values
    results['total_gen_all'] = test_df['total_gen_all'].values

    # Scale Conversions 
    # Total Generation
    results['actual_total_generation__solar'] = results['actual']
    results['pred_total_generation__solar'] = results['pred']
    
    # Market Share
    results['actual_solar_market_share'] = results['actual_total_generation__solar'] / results['total_gen_all']
    results['pred_solar_market_share'] = results['pred_total_generation__solar'] / results['total_gen_all']
    
    # Emissions Avoided
    results['actual_emissions_avoided'] = results['actual_total_generation__solar'] * EMISSIONS_FACTOR
    results['pred_emissions_avoided'] = results['pred_total_generation__solar'] * EMISSIONS_FACTOR
    
    metrics = {
         "solar_generation_per_capacity": get_scoped_metrics(results['actual'], results['pred']),
         "total_generation__solar": get_scoped_metrics(results['actual_total_generation__solar'], results['pred_total_generation__solar']),
         "solar_market_share": get_scoped_metrics(results['actual_solar_market_share'], results['pred_solar_market_share']),
         "emissions_avoided": get_scoped_metrics(results['actual_emissions_avoided'], results['pred_emissions_avoided'])
     }        
    return y_test, test_pred, results, test_df, model, X_train, train_df, metrics






# Evaluation Function for Model 3

def EvaluateModel3(y_test, test_pred, results, test_df, model, features, X_train, selected_target, page_tab, g_type):
    
    # evaluate main selected_target
    rmse = np.sqrt(mean_squared_error(y_test, test_pred)) 
    mae = mean_absolute_error(y_test, test_pred)
    r2 = r2_score(y_test, test_pred) 
    mape = np.mean(np.abs((y_test - test_pred) / y_test)) * 100
    
    # optional: compare against your original aggregated emissions_avoided column
    results['actual_emissions_avoided_from_source'] = test_df['emissions_avoided'].values
    
    # evaluation for converted outputs
    rmse_gen = np.sqrt(mean_squared_error(
        results['actual_total_generation__solar'],
        results['pred_total_generation__solar']
    ))
    mae_gen = mean_absolute_error(
        results['actual_total_generation__solar'],
        results['pred_total_generation__solar']
    )
    r2_gen = r2_score(
        results['actual_total_generation__solar'],
        results['pred_total_generation__solar']
    )
    
    rmse_share = np.sqrt(mean_squared_error(
        results['actual_solar_market_share'],
        results['pred_solar_market_share']
    ))
    mae_share = mean_absolute_error(
        results['actual_solar_market_share'],
        results['pred_solar_market_share']
    )
    r2_share = r2_score(
        results['actual_solar_market_share'],
        results['pred_solar_market_share']
    )
    
    rmse_emissions = np.sqrt(mean_squared_error(
        results['actual_emissions_avoided'],
        results['pred_emissions_avoided']
    ))
    mae_emissions = mean_absolute_error(
        results['actual_emissions_avoided'],
        results['pred_emissions_avoided']
    )
    r2_emissions = r2_score(
        results['actual_emissions_avoided'],
        results['pred_emissions_avoided']
    )
    
    if page_tab == 2:
        col1, col2 = st.columns(2)
    
        with col1:
    
            st.subheader("**Model Name:** ")
            st.write(f"**{type(model).__name__}**")
            st.subheader("**Target Variable:**")
            st.write(f"**{selected_target}**")
    
        with col2:
            st.subheader("**Model Parameters:** ")
            st.write("**Learning Rate:** ", model.get_params()['learning_rate'])
            st.write("**Max. Depth:** ", model.get_params()['max_depth'])
            st.write("**n_estimators:** ", model.get_params()['n_estimators'])
            st.write("**Sub-Sample:** ", model.get_params()['subsample'])
    
        st.divider()
    
        col1, col2, col3 = st.columns(3)
    
        with col1:
            st.header("RMSE:")
            st.subheader(str(int(rmse)) + " MW")
    
        with col2:
            st.header("MAE:")
            st.subheader(str(int(mae)) + " MW")
    
        with col3:
            st.header("R²:")
            st.subheader( str(int(r2 * 100)) + " %")
    
        st.divider()
    
    elif page_tab == 3:
        
        st.header(f"Feat. Importance for - {selected_target}")
        st.divider()
        
        # feature importance
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        top_val = feature_importance['importance'].iloc[0]
        total_val = feature_importance['importance'].sum()
        dominance_pct = (top_val / total_val) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Total Features:** ", model.n_features_in_)
            st.write("**Top Feature Influence:** ", f"{int(dominance_pct)}%")
        
        with col2:
            st.write("Total of 'Zero-Impact' Features: ", (feature_importance['importance'] == 0).sum())
            st.write("Top Feature: ", f'"{feature_importance['feature'].iloc[0]}"')
            
        plt.figure(figsize=(10, 6))
        plt.barh(feature_importance['feature'], feature_importance['importance'])
        plt.gca().invert_yaxis()
        plt.title('Feature Importance')
        plt.xlabel('Importance')
        st.pyplot(plt.gcf())   
        
        st.divider()
        st.write("This Section is Experimental...")
        selected_to_drop = st.multiselect("Select features to 'lose':", feature_importance['feature'])
        lost_importance = feature_importance[feature_importance['feature'].isin(selected_to_drop)]['importance'].sum()
        
        st.warning(f"Removing these would lose **{lost_importance*100:.1f}%** of the model's predictive power.")  
        
        # Create the cumulative column
        feature_importance['c_sum'] = feature_importance['importance'].cumsum()
        
        fig = px.area(feature_importance, x=range(len(feature_importance)), y='c_sum', 
                      title="Cumulative Logic Coverage",
                      labels={'x': 'Number of Features', 'y': 'Total Importance'})
        st.plotly_chart(fig)        
    
    elif page_tab == 4:
        
        res = y_test - test_pred
        res_mean = res.mean()
        res_max = res.max()
        res_min = res.min()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**Average Residual:** {res_mean:.2f}")
        
        with col2:
            st.write(f"**Max Residual:** {res_max:.2f}")
        
        with col3:
            st.write(f"**Min Residual:** {res_min:.2f}")
        
        # Residual Analysis Plot Figure Created
        fig = go.Figure()
        
        # These Branches Handle the Different Rendering Outputs for Visualizations Based Upon User's Selection 
        
        # Line Graph Selected
        if g_type == "Line":
            # Residual line
            fig.add_trace(go.Scatter(
                x=results['time'],
                y=results['error'],
                mode='lines+markers',
                name='Residuals'
            ))
        
            # Zero line
            fig.add_hline(
                y=0,
                line_dash="dash",
                line_color="white",
                annotation_text="Zero Error",
                annotation_position="top left",
            )
        
            # Layout
            fig.update_layout(
                title=f"Residuals: {selected_target}",
                xaxis_title="Time",
                yaxis_title="Residual (Actual - Predicted)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"            
            )
        
        # Scatter Plot Selected
        elif g_type == "Scatter":
            # Residual Scatter
            fig.add_trace(go.Scatter(
                x=results['time'],
                y=results['error'],
                mode='markers',
                name='Residuals'
            ))
        
            # Zero line
            fig.add_hline(
                y=0,
                line_dash="dash",
                line_color="white",
                annotation_text="Zero Error",
                annotation_position="top left",
            )
        
            # Layout
            fig.update_layout(
                title=f"Residuals: {selected_target}",
                xaxis_title="Time",
                yaxis_title="Residual (Actual - Predicted)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"            
            )            
        
        # Bar Graph Seleted
        elif g_type == "Bar":
            
            # Residual Bar
            fig.add_trace(go.Bar(
                x=results['time'],
                y=results['error'],
                name='Residuals'
            ))
        
            # Zero line
            fig.add_hline(
                y=0,
                line_dash="dash",
                line_color="white",
                annotation_text="Zero Error",
                annotation_position="top left",
            )
        
            # Layout
            fig.update_layout(
                title=f"Residuals: {selected_target}",
                xaxis_title="Time",
                yaxis_title="Residual (Actual - Predicted)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"            
            )  
        
        # Box Plot Selected
        elif g_type == "Box":
            # Residual Box
            fig.add_trace(go.Box(
                x=results['time'],
                y=results['error'],
                name='Residuals'
            ))
        
            # Zero line
            fig.add_hline(
                y=0,
                line_dash="dash",
                line_color="white",
                annotation_text="Zero Error",
                annotation_position="top left",
            )
        
            # Layout
            fig.update_layout(
                title=f"Residuals: {selected_target}",
                xaxis_title="Time",
                yaxis_title="Residual (Actual - Predicted)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"            
            )              
            
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution of Residuals
        plt.figure(figsize=(10, 6))
        
        # Note: sns.histplot returns an Axes object, not a Figure object
        sns.histplot(results['error'], kde=True, bins=30)
        
        plt.title('Distribution of Residuals')
        plt.xlabel('Residual (Actual - Predicted)')
        plt.ylabel('Frequency')
        plt.grid(True)
        
        # Use this to send the current figure to the Streamlit app
        st.pyplot(plt.gcf())
    
    
    elif page_tab == 5:
        
        import shap
        
        # Using X_train as the background dataset for the explainer
        explainer = shap.TreeExplainer(model, X_train)
        
        # Define the months and year for analysis
        target_months = {3: 'March', 7: 'July', 8: 'August'}
        target_year = 2025
        
        for month_num, month_name in target_months.items():
            # Filter the test data for the specific month and year
            month_data = test_df[(test_df['time'].dt.month == month_num) & (test_df['time'].dt.year == target_year)]
        
            if not month_data.empty:
                # Assuming we want to explain the first instance found for that month
                # If there are multiple instances, you might want to pick a specific one
                data_to_explain = month_data.iloc[0]
                X_data_to_explain = data_to_explain[features].to_frame().T
        
                # Calculate SHAP values for the selected data point
                shap_values = explainer(X_data_to_explain)
                shap.plots.waterfall(shap_values[0], show=False)
        
                st.write(f"\n--- SHAP Analysis for {month_name} {target_year} | **Selected:** {selected_target} ---")
                
                # Plotting the SHAP waterfall plot for a single prediction
                
                st.pyplot(plt.gcf())
                plt.clf()
                
            else:
                print(f"\nNo data found for {month_name} {target_year} in the test set.")



# ------ This Section Handles PVLib Simulation Code -----------------------------------------------


def RunSimulation(df, cap, tilt, az, df_select):
    
    # This Branch Sets Up the Fixed Coordinates for Either Solar Site
    if df_select == "New Jubilee":
        
        visser_lat = 53.665690
        visser_long = -113.289641  
        
        latitude = visser_lat
        longitude = visser_long        
        
    else:
        
        bissell_lat = 53.6028
        bissell_long = -113.4483
        
        latitude = bissell_lat
        longitude = bissell_long
        
        """ Remember to put in the Bissell Coords here..."""
        pass
    
    
    df_project = df.copy()
    df_project['time'] = pd.to_datetime(df_project['time']).dt.normalize() + pd.Timedelta(hours=12)
    
    # 2. Set it as the index (Crucial for PVLib!)
    df_project = df_project.set_index('time')    
    
    # Loss Factor  
    loss_factor = 0.75             
    
    
    # Calculating Solar Position - Derived by PVLib's Astronomy Engine
    solpos = pvlib.solarposition.get_solarposition(df_project.index, latitude, longitude) # Calculates Exact Position of Sun in Sky for Every Day
    dni_extra = pvlib.irradiance.get_extra_radiation(df_project.index)                    # Calculates 'Extra-Terrestrial' Radiation (Energy hitting atmosphere before absorption)    
    
    
    # Converting GHI to POA (Plane of Attack - Insolation Angles) | Calcuating Total Irradiation
    poa = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,           # Inputting Solar Generation System Panel Tilt
        surface_azimuth=az,     # Inputting Solar Generation System Panel Azimuth (Direction)
        solar_zenith=solpos['zenith'],    # Attaining Solar 'Zenith' - Angle of Sun Height Relative to Overhead
        solar_azimuth=solpos['azimuth'],  # Attaining Solar 'Azimuth' - Like the Compass Direction of the Sun
        dni=df_project['dni'],     # Inputting Direct Normal Irradiance Values from Open-Meteo
        ghi=df_project['ghi'],     # Inputting Global Horizontal Irradiance Values from Open-Meteo
        dhi=df_project['dhi'],     # Inputting Direct Horizontal Irradiance Values from Open-Meteo
        dni_extra=dni_extra,
        model='isotropic'
    )
    
    # Extracting the Plane-of-Attack Values Calculated and Storing it in Joined Dataset
    df_project['poa_global'] = poa['poa_global']
    
    # ------------------ THEORETICAL OUTPUT ------------------
    df_project['theoretical_kwh'] = (
        df_project['poa_global'] / 1000
    ) * cap * loss_factor

    return df_project



# Evaluating & Projecting New Eco-Impact Projection Values
def ProjectNewImpacts(df_project):
    
    # Constant Pool
    tree_var = 0.022
    car_var = 4.6
    co2_factor = 0.54
    home_var = 10
    coal_var = 2.5
    gas_var = 0.0023
    
    # Calcuting the Annual CO2 Saved & 10-Year & 25-Year
    df_project['co2_avoided'] = (df_project['theoretical_kwh'] * co2_factor)
    df_project['co2_avoided_10'] =  (df_project['theoretical_kwh'] * co2_factor * 10 * 0.97)
    df_project['co2_avoided_25'] = (df_project['theoretical_kwh'] * co2_factor * 25 * 0.94)
    
    # Calculating the Trees Saved
    df_project['trees_saved'] = (df_project['co2_avoided'] / tree_var)
    df_project['trees_saved_10'] = ((df_project['co2_avoided'] / tree_var) * 10 * 0.97)
    df_project['trees_saved_25'] = ((df_project['co2_avoided'] / tree_var) * 25 * 0.94)
    
    
    df_project['cars_offroad'] = (df_project['co2_avoided'] / car_var)
    df_project['cars_offroad_10'] = ((df_project['co2_avoided'] / car_var) * 10 * 0.97)
    df_project['cars_offroad_25'] = ((df_project['co2_avoided'] / car_var) * 25 * 0.94)
    
    df_project['homes_powered'] = (df_project['theoretical_kwh'] / home_var)
    df_project['homes_powered_10'] = ((df_project['theoretical_kwh'] / home_var) * 10 * 0.97)
    df_project['homes_powered_25'] = ((df_project['theoretical_kwh'] / home_var) * 25 * 0.94)
    
    df_project['coal_tonnage_avoided'] = ((df_project['theoretical_kwh'] * 0.9) / coal_var)
    df_project['coal_tonnage_avoided_10'] = (((df_project['theoretical_kwh'] * 0.9) / coal_var) * 10 * 0.97)
    df_project['coal_tonnage_avoided_25'] = (((df_project['theoretical_kwh'] * 0.9) / coal_var) * 25 * 0.94)
    
    df_project['gas_saved'] = (df_project['co2_avoided'] / gas_var)
    df_project['gas_saved_10'] = ((df_project['co2_avoided'] / gas_var) * 10 * 0.97)
    df_project['gas_saved_25'] = ((df_project['co2_avoided'] / gas_var) * 25 * 0.94)    
    
    
    return df_project




def render_comparison_table(df, df_project, og_size, capacity, tilt, azimuth):
    
    # ---------- ORIGINAL VALUES ----------
    orig = {
        "Capacity (kW)": og_size,
        "Tilt (°)": 30,  # your assumed default
        "Azimuth (°)": 180,  # your assumed default
        "Output (kWh)": df['theoretical_kwh'].sum().round(2),
        "CO₂ Saved (t)": df['co2_avoided'].sum().round(2),
        "Trees Saved": df['trees_saved'].sum().round(),
        "Homes Powered": df['homes_powered'].sum().round(2),
        "Cars Off Road": df['cars_offroad'].sum().round(2)
    }

    # ---------- SIMULATED VALUES ----------
    sim = {
        "Capacity (kW)": capacity,
        "Tilt (°)": tilt,
        "Azimuth (°)": azimuth,
        "Output (kWh)": df_project['theoretical_kwh'].sum().round(2),
        "CO₂ Saved (t)": df_project['co2_avoided'].sum().round(2),
        "Trees Saved": df_project['trees_saved'].sum().round(),
        "Homes Powered": df_project['homes_powered'].sum().round(2),
        "Cars Off Road": df_project['cars_offroad'].sum().round(2)
    }

    # ---------- BUILD ROWS ----------
    rows_html = ""

    for key in orig.keys():
        o = orig[key]
        s = sim[key]

        # Handle numeric vs non-numeric safely
        try:
            diff = s - o
            pct = (diff / o * 100) if o != 0 else 0

            # Color logic
            if diff > 0:
                color = "#00ff73"   # green
                sign = "+"
            elif diff < 0:
                color = "#FF4B4B"   # red
                sign = ""
            else:
                color = "#FFFFFF"
                sign = ""

            diff_display = f"{sign}{diff:.2f} ({sign}{pct:.1f}%)"
        except:
            color = "#FFFFFF"
            diff_display = "—"

        rows_html += f"""
        <tr>
            <td>{key}</td>
            <td>{o}</td>
            <td>{s}</td>
            <td style="color:{color}; font-weight:bold;">{diff_display}</td>
        </tr>
        """

    # ---------- FINAL HTML ----------
    html = f"""
    <div style="
        background-color: rgba(0,0,0,0);
        border: 2px solid #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    ">
        <table style="
            width:100%;
            color:white;
            border-collapse: collapse;
            text-align:center;
        ">
            <thead>
                <tr style="border-bottom:1px solid white;">
                    <th style="padding:10px;">Metric</th>
                    <th>Original</th>
                    <th>Simulated</th>
                    <th>Difference</th>
                </tr>
            </thead>
            <tbody>
    {rows_html}
            </tbody>
    
        </table>
    </div>
    """

    st.components.v1.html(html, height=400, scrolling=False)
    
    
def render_graphic_comparison(df, df_project, og_size, cap, tilt, az):
    
    impact_cols = [
        "co2_avoided", "cars_offroad",
        "homes_powered", "coal_tonnage_avoided", 
        "coal_emission_avoided"
    ]

    og_totals = df[impact_cols].sum()
    sim_totals = df_project[impact_cols].sum()

    df_compare = pd.DataFrame({
        "Metric": impact_cols,
        "Original": og_totals.values,
        "Simulated": sim_totals.values
    })

    fig = px.bar(
    df_compare,
    x="Metric",
    y=["Original", "Simulated"],
    barmode="group",
    color_discrete_map={
        "Original": "#0058EE",   # green
        "Simulated": "#A5BEE0"    # blue
        }   
    )

    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",   # whole canvas
        plot_bgcolor="rgba(0,0,0,0)",     # plotting area
    )

    st.plotly_chart(fig)    
    
