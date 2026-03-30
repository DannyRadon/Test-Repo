# This Python File Contains the Data Functions (Group By, Aggregate, etc) for Use with the Streamlit Dashboard

# Import Pool
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import base64

import matplotlib.pyplot as plt
import plotly.express as px

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


def RunModel3(aeso_fe, page_tab):
    
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
    
    print("Modeling dataframe shape:", df_model.shape)
    print("Date range:", df_model['time'].min(), "to", df_model['time'].max())
    
    # train/test split
    test_size = int(np.ceil(len(df_model) * 0.20))
    train_df = df_model.iloc[:-test_size].copy()
    test_df  = df_model.iloc[-test_size:].copy()
    
    X_train = train_df[features]
    y_train = train_df[target]
    
    X_test = test_df[features]
    y_test = test_df[target]
    
    print("\nTrain size:", len(train_df))
    print("Test size :", len(test_df))
    print("Train range:", train_df['time'].min(), "to", train_df['time'].max())
    print("Test range :", test_df['time'].min(), "to", test_df['time'].max())
    
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
    
    # evaluate main target
    rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    mae = mean_absolute_error(y_test, test_pred)
    r2 = r2_score(y_test, test_pred)
    mape = np.mean(np.abs((y_test - test_pred) / y_test)) * 100
    
    print("\nFINAL TEST METRICS")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE : {mae:.4f}")
    print(f"R²  : {r2:.4f}")
    print(f"MAPE: {mape:.2f}%")
    
    # convert predictions into solar gen and market share
    results['maximum_capacity__solar'] = test_df['maximum_capacity__solar'].values
    results['total_gen_all'] = test_df['total_gen_all'].values
    
    # total gen solar = solar gen per capacity times max capacity
    results['actual_total_generation__solar'] = (
        results['actual'] * results['maximum_capacity__solar']
    )
    results['pred_total_generation__solar'] = (
        results['pred'] * results['maximum_capacity__solar']
    )
    # market share = total gen solar/total gen all
    results['actual_solar_market_share'] = (
        results['actual_total_generation__solar'] / results['total_gen_all']
    )
    results['pred_solar_market_share'] = (
        results['pred_total_generation__solar'] / results['total_gen_all']
    )
    
    # ---------------------------------------------------------
    # ADD EMISSIONS AVOIDED
    # derived from total solar generation
    # ---------------------------------------------------------
    EMISSIONS_FACTOR = 0.52
    
    results['actual_emissions_avoided'] = (
        results['actual_total_generation__solar'] * EMISSIONS_FACTOR
    )
    results['pred_emissions_avoided'] = (
        results['pred_total_generation__solar'] * EMISSIONS_FACTOR
    )
    
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
            st.write(type(model).__name__)
    
        with col2:
            st.subheader("**Model Parameters:** ")
            st.write("**Learning Rate:** ", model.get_params()['learning_rate'])
            st.write("**Max. Depth:** ", model.get_params()['max_depth'])
            st.write("**n_estimators:** ", model.get_params()['n_estimators'])
            st.write("**Sub-Sample:** ", model.get_params()['subsample'])
    
        st.divider()
    
        col1, col2, col3 = st.columns(3)
    
        with col1:
            st.metric("RMSE:", int(rmse)) 
    
        with col2:
            st.metric("MAE:" , int(mae))
    
        with col3:
            st.metric("R²:", r2 * 100)
    
        st.divider()
    
    elif page_tab == 3:
        
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
        
        st.subheader("")
        
        # Create the cumulative column
        feature_importance['c_sum'] = feature_importance['importance'].cumsum()
        
        fig = px.area(feature_importance, x=range(len(feature_importance)), y='c_sum', 
                      title="Cumulative Logic Coverage",
                      labels={'x': 'Number of Features', 'y': 'Total Importance'})
        st.plotly_chart(fig)        
    
    elif page_tab == 4:
        
        # Residual Analysis Plot
        plt.figure(figsize=(12, 6))
        plt.plot(results['time'], results['error'], marker='o', linestyle='-')
        plt.axhline(0, color='red', linestyle='--', label='Zero Error')
        plt.title('Residuals: Actual - Predicted Solar Generation per Capacity')
        plt.xlabel('Time')
        plt.ylabel('Residual (Actual - Predicted)')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt.gcf())
        
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
        
                st.write(f"\n--- SHAP Analysis for {month_name} {target_year} ---")
                
                # Plotting the SHAP waterfall plot for a single prediction
                
                st.pyplot(plt.gcf())
                plt.clf()
                
            else:
                print(f"\nNo data found for {month_name} {target_year} in the test set.")
        
