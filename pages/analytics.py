# ---------------------------------------- Test File for Side-Bar Navigation  --------------------------------------------------------

# Import Pool
import base64
import urllib.parse

import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from st_click_detector import click_detector

from helpers.data_load import load_data
from helpers.data_funcs import *

import pvlib



# Loading in the Data (If Not Cached)
df_visser, df_bissell, df_aeso = load_data()

range_select = "Daily"

params = st.query_params

# --- SYNC URL TO SESSION STATE ---
for url_key, state_key in [
    ("dataset", "dataset"), 
    ("graph", "graph_type"), 
    ("x_var", "x_var"), 
    ("y_var", "y_var"),
    ("view", "view_mode"),
    ("calc_btn", "calc_btn")
]:
    if url_key in st.query_params:
        st.session_state[state_key] = st.query_params[url_key]


# --- SETTING DEFAULTS --- If the app is opened for the first time (no URL params)

if "dataset" not in st.session_state:
    st.session_state.dataset = "New Jubilee"

if "graph_type" not in st.session_state:
    st.session_state.graph_type = "Line"

if "x_var" not in st.session_state:
    st.session_state.x_var = "time"

if "y_var" not in st.session_state:
    st.session_state.y_var = "Daily Value Imputed"

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "Graphical"

if "dataflow" not in st.session_state:
    st.session_state.dataflow = "None"

if "calc_btn" not in st.session_state:
    st.session_state.calc_btn = False


# --- GENERATING DYNAMIC URL LINKS ---

# Dataset URLs
url_bissell = build_url(dataset="Bissell Thrift")
url_jubilee = build_url(dataset="New Jubilee")
url_aeso = build_url(dataset="AESO")

# Import & Export URLs
url_export = build_url(dataflow="Export")

# View Mode URLs -- Used for Switching Between Descriptive vs Graphical
url_descriptive = build_url(view="Descriptive")
url_graphical = build_url(view="Graphical")

# Graph Visualization URLs
url_bar = build_url(graph="Bar")
url_line = build_url(graph="Line")
url_area = build_url(graph="Area")
url_scatter = build_url(graph="Scatter")
url_histo = build_url(graph="Histogram")
url_box = build_url(graph="Box")
url_violin = build_url(graph="Violin")
url_ecdf = build_url(graph="ecdf")
url_matrix = build_url(graph="matrix")

# X Variable URLs -- Time Series & Weather (Weather is Experimental)
url_hourly = build_url(x_var="hourly")
url_daily = build_url(x_var="daily")
url_weekly = build_url(x_var="weekly")
url_monthly = build_url(x_var="monthly")
url_yearly = build_url(x_var="yearly")

url_cloud = build_url(x_var="cloud")
url_precip = build_url(x_var="precip")
url_temp = build_url(x_var="temp")
url_wind = build_url(x_var="wind")

# Y Variable URLs -- Energy Outputs & Environmental Calculations

url_output = build_url(y_var="output")
url_ratio = build_url(y_var="ratio")

url_carbon = build_url(y_var="carbon")
url_trees = build_url(y_var="trees")
url_cars = build_url(y_var="cars")
url_homes = build_url(y_var="homes")
url_coale = build_url(y_var="coal_e")
url_coalt = build_url(y_var="coal_t")
url_gas = build_url(y_var="gas")
                                    






# Global Variables to Use for State Session Updates & Calls
df_selection = st.session_state.dataset
vis_type = st.session_state.graph_type

if vis_type in ['Pie', 'Tree']:
    vis_type = 'Line'

x_new = st.session_state.x_var

if x_new == "month" or x_new == "projects":
    x_new = "time"
    
y_var = st.session_state.y_var
view_mode = st.session_state.view_mode
dataflow = st.session_state.dataflow



# State Session Checks for Current Dataset(s)
if df_selection == "Bissell Thrift":
    df = df_bissell.copy()
    df_select = "Bissell Thrift Shop"
    
elif df_selection == "New Jubilee":
    df = df_visser.copy()
    df_select = "New Jubilee"

else:
    df = df_aeso.copy()
    df_select = "AESO"
    
    
    
    

# ------------------------------------------ CSS & HTML GRAPHICS HANDLING SECTION ------------------------------------------

# This CSS creates the Gradient Background 
st.markdown("""
<style>
.stApp {
    /* Linear gradient example: top-left blue to bottom-right purple */
    background: linear-gradient(135deg, #2257d6 25%, #3b77bc 50%, #009cde 66%, #d0d0d0 100%);
}
</style>
""", unsafe_allow_html=True)

def function(name):
    pass


# Loading in the Icons
icon_sys_info = get_base64_image("static/icon_sysinfo.png")
icon_impacts_info = get_base64_image("static/icon_impacts.png")
icon_ml_info = get_base64_image("static/icon_ml.png")
icon_home = get_base64_image("static/icon_home.png")
icon_chat = get_base64_image("static/icon_chat.png")

# Title for the Page
st.title("Exploratory Analytics")

# This CSS Handles the Setup for the Canvas for the Icons and Clickable Regions for them...
st.markdown("""
<style>
.icon-card {
    background: linear-gradient(
        135deg,
        #cbcbcb 0%,
        #ec722e 25%,
        #DE482B 100%
    );
    border-radius: 12px;
    width: 150px !important;
    height: 150px !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;  /* icon on top, label at bottom */
    padding: 2px 0;
    border: 2px solid #333;
    margin: 0 auto;
    box-shadow: 0px 4px 12px 2px rgba(0,0,0,0.4);
    transition: transform 0.2s ease;
}
            

.icon-card:hover {
    transform: scale(1.05);
    box-shadow: 0px 6px 18px rgba(0,0,0,0.6);
}

.icon-card img {
    max-width: 150px;    /* Almost fills the width */
    max-height: 115px;   /* Almost fills the height */
    
    
    
}

.card-text {
    font-size: 16px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-top: 0px;
    margin-bottom: 5px;
}

/* Transparent overlay button for click */
.stButton > button {
    position: absolute;
    width: 150px !important;   /* Matches your .icon-card width */
    height: 150px !important;  /* Matches your .icon-card height */
    background: transparent !important;
    border: none !important;
    color: transparent !important;
    margin-top: -205px;        /* This "lifts" the button up to sit ON TOP of the card */
    z-index: 10;
    cursor: pointer;
}

/* Optional: remove the default streamlit button hover effect so it doesn't flicker */
.stButton > button:hover {
    background: transparent !important;
    border: none !important;
    color: transparent !important;
}

/* Tabs background when active */
[role="tablist"] button[aria-selected="true"] {
    background: linear-gradient(135deg, #38c401, #81C046, 0.7); !important; /* highlight color */
    color: white !important;              /* text color */
    border-radius: 8px;                   /* optional rounded corners */
}

/* Optional: hover effect for all tabs */
[role="tablist"] button:hover {
    background-color: rgba(56,196,1,0.3) !important;
    color: white !important;
    border-radius: 8px;
}

/* Top bar background */
header[data-testid="stHeader"] {
    background: linear-gradient(135deg, #0054e3, #3b77bc, #009cde) !important; /* gradient */
    height: 50px;           /* adjust height if needed */
}


/* ===== TASK BAR MAIN CONTAINER ===== */
.menu-bar {
    background: linear-gradient(180deg, #7BA2E7, #357EC7, #3169C6, #7BA2E7);
    padding: 6px 12px;
    display: flex;
    gap: 25px;
    align-items: center;
    border: 4px solid #cecece;
    border-radius: 5px;
    box-shadow: 0px 6px 50px 5px rgba(0,0,0,0.4);
    font-family: Arial, sans-serif;
}


/* ===== MENU ITEMS ===== */
.menu-item {
    position: relative;
    cursor: pointer;
    font-size: 14px;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
}

/* Hover effect like Windows */
.menu-item:hover {
    background-color: #cecece;
    color: black;
}

/* ===== TASK BAR DROP DOWN MENUS CONTAINER ===== */
.menu-bar {
    background: linear-gradient(180deg, #7BA2E7, #357EC7, #3169C6, #7BA2E7);
    padding: 6px 12px;
    display: flex;       /* This makes items stay side-by-side */
    flex-direction: row; /* Explicitly force horizontal layout */
    width: 100%;  /* Prevents the bar from collapsing */
    gap: 25px;
    align-items: center;
    border: 4px solid #cecece;
    border-radius: 5px;
    box-shadow: 0px 6px 50px 5px rgba(0,0,0,0.4);
    font-family: Arial, sans-serif;
}

.dropdown {
    display: none;
    position: absolute;
    top: 100%; /* Sticks it to the bottom of the menu-item */
    left: 0;
    background-color: #f0f0f0;
    min-width: 160px;
    z-index: 9999; /* Ensures it stays on top of other dashboard charts */
    border: 3px solid #3170de;
    border-radius: 8px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
}

/* ===== DROPDOWN ITEMS ===== */
.dropdown div {
    padding: 6px 10px;
    cursor: pointer;
    color: black;
}

/* Hover effect inside dropdown */
.dropdown > div:hover {
    background-color: #0078d7;
    color: white;
}

.menu-leaf > button {
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
    background: transparent;
    border: none;
    cursor: pointer;
    z-index: 10;
}

.menu-leaf:hover {
    background-color: #0078d7;
    color: white;
}

/* SHOW dropdown when hovering parent */
.menu-item:hover .dropdown {
    display: block;
}


/* ===== SUBMENU (nested dropdown) ===== */
.submenu {
    display: none;
    position: absolute;
    top: 0;
    left: 100%; /* pushes it to the right */
    background-color: #f0f0f0;
    min-width: 140px;
    border: 2px solid #3170de;
    border-radius: 8px;
    padding: 0;
    z-index: 1001;
}

/* --- Highlighting Options in Nested Sub-Menu  */
.submenu > .dropdown-item:hover {
    background-color: #0078d7;
    color: white;
}

/* Parent item needs positioning */
.dropdown-item {
    position: relative;
}


/* Only show submenu when hovering DIRECT parent */
.dropdown-item:hover > .submenu {
    display: block;
}

/* Push clock to the right side of the taskbar */
.taskbar-clock {
    margin-left: auto; 
    color: white;
    font-size: 14px;
    font-weight: bold;
    padding: 4px 12px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    border-left: 1px solid rgba(255, 255, 255, 0.3);
    min-width: 100px;
    text-align: center;
}

/* ------------------ Sidebar gradient ------------------ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2257d6, #009cde, #009cde, #dcdcdc);
    color: white;
    border: 4px solid #d7d7d7
}

/* Hover State */
[data-testid="stSidebarNav"] li a:hover {
    background-color: rgba(229, 80, 0, 0.5) !important;
    color: #0068c9 !important;
}

/* Active/Selected Page State */
[data-testid="stSidebarNav"] li a[aria-current="page"] {
    background-color: rgba(56, 196, 1, 0.7) !important;
    color: white !important;
    font-weight: bold;
}
            
/* Sidebar headers */
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #ffffff;
}

/* Target the text within the sidebar navigation */
[data-testid="stSidebarNav"] li a span {
    text-transform: uppercase; /* Options: uppercase, capitalize, lowercase */
    font-family: 'Arial', sans-serif; /* Your preferred font */
    font-size: 20px;
    font-weight: bold;
}

/* Sidebar buttons */
[data-testid="stSidebar"] button {
    background-color: #38c401;
    color: white;
    border-radius: 8px;
    margin-bottom: 5px;
    border: 2px solid #ffffff
}

/* Optional: page title style */
.page-title {
    font-size: 42px;
    font-weight: bold;
    color: #d7d7d7;
    -webkit-text-stroke: 1px #000000;  /* subtle outline */
    text-align: center;
    margin-bottom: 5px;


}

/* 1. Hide the entire radio widget container */
div[data-testid="stRadio"] {
    display: none !important;
    visibility: hidden !important;
    height: 0px !important;
    margin: 0px !important;
    padding: 0px !important;
}

/* 2. Hide the label specifically just in case */
div[data-testid="stWidgetLabel"] {
    display: none !important;
}

/* Remove hyperlink look */
.dropdown a {
    text-decoration: none !important;
    color: black !important;
    display: block;
    padding: 6px 10px;
}

/* Hover effect like real menus */
.dropdown a:hover {
    background-color: #0078d7 !important;
    color: white !important;
}
</style>



""", unsafe_allow_html=True)



# This CSS Handles the Green Background for the Icon Sections - This is setup to be handled by the HTML stuff down below
st.markdown("""
<style>
.green-section {
    background: linear-gradient(
        180deg,
        #A4C76E 0%,
        #7FAE42 50%,
        #38c401 100%
    );
    padding: 30px 10px;
    border-radius: 15px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 20px;
    border: 5px solid #cecece;
    box-shadow: 0px 6px 50px 5px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)



# Render all cards in one row (green section) -- This is the HTML stuff I was talking about above 
st.markdown(f'''
<div class="green-section">
    <div class="icon-card">
        <img src="data:image/png;base64,{icon_home}">
        <div class="card-text">Home</div>
    </div>
    <div class="icon-card">
        <img src="data:image/png;base64,{icon_sys_info}">
        <div class="card-text">System Info</div>
    </div>
    <div class="icon-card">
        <img src="data:image/png;base64,{icon_impacts_info}">
        <div class="card-text">Impacts</div>
    </div>
    <div class="icon-card">
        <img src="data:image/png;base64,{icon_ml_info}">
        <div class="card-text">M-Learning</div>
    </div>
    <div class="icon-card">
        <img src="data:image/png;base64,{icon_chat}">
        <div class="card-text">Chat</div>
    </div>
</div>
''', unsafe_allow_html=True)


# Clickable-Icon Navigation Area -- Routing to Other Pages -- this is what allows interactivity 

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button(" ", key="home_btn"):
        st.switch_page("home.py")

with col2:
    if st.button(" ", key="sys_info_btn"):
        st.switch_page("pages/system_info.py")

with col3:
    if st.button(" ", key="imp_info_btn"):
        st.switch_page("pages/impacts.py")

with col4:
    if st.button(" ", key="ml_info_btn"):
        st.switch_page("pages/ml.py")

with col5:
    if st.button(" ", key="chat_btn"):
        st.switch_page("pages/chat.py")
        






if df_select == "AESO":
    
    
    
    if y_var not in [
        "max_cap", 
        "total_gen",
        "sys_cap",
        "sys_gen",
        "pool_price",
        "pool_forecast",
        "rolling_avg"]:
        
        y_var = "max_cap"
    
    if x_new != "DateTime":
        x_new = "DateTime"
        
        
        
        
    # Creating AESO Specific URL Keys for Variables
    url_max = build_url(y_var="max_cap")
    url_tot = build_url(y_var="total_gen")
    url_sys = build_url(y_var="sys_cap")
    url_gen = build_url(y_var="sys_gen")
    url_pool = build_url(y_var="pool_price")
    url_fpool = build_url(y_var="pool_forecast")
    url_rolling = build_url(y_var="rolling_avg")
    url_monthly_multi = build_url(graph="monthly_multi")
    
    # This HTML File Handles the Task Bar Menu Labelling Control & Drop-Down Menu handling & Drop-Down Sub
    st.markdown(f"""
    <div class="menu-bar">
        <div class="menu-item">
            Data
            <div class="dropdown">
                <div class="dropdown-item">
                <span style="display:flex; justify-content:space-between;">
                    Change Dataset
                </span>
                <div class="submenu">
                    <div class="dropdown-item">
                        <span style="display:flex; justify-content:space-between;">
                            SPICE 
                        </span>
                        <div class="submenu">
                            <a href="{url_jubilee}" target="_self">New Jubilee</a>
                            <a href="{url_bissell}" target="_self">Bissell Thrift</a>
                    </div>
                </div>
                <div class="dropdown-item">
                <span style="display:flex; justify-content:space-between;">
                    AESO
                </span>
                <div class="submenu">
                    <a href="{url_aeso}" target="_self">Generation & Pool Markets</a>
                </div>
            </div>
        </div>
    </div>
                <div>Import Dataset</div>
                <a href="{url_export}" target="_self">Export Dataset</a>
            </div>
        </div>
        <div class="menu-item">
            Edit
            <div class="dropdown">
                <div>Undo Action</div>
                <div>Redo Action</div>
            </div>
        </div>
        <div class="menu-item">
            View
            <div class="dropdown">
                <a href="{url_descriptive}" target="_self">Descriptive</a>
                <a href="{url_graphical}" target="_self">Graphical</a>
            </div>
        </div>
        <div class="menu-item">
            Format
            <div class="dropdown">
                <div class="dropdown-item">
                    Visualization
                    <div class="submenu">
                        <a href="{url_line}" target="_self">Line</a> 
                        <a href="{url_bar}" target="_self">Bar</a>
                        <a href="{url_area}" target="_self">Area</a>
                        <a href="{url_scatter}" target="_self">Scatter</a>
                        <a href="{url_histo}" target="_self">Histogram</a>
                        <a href="{url_box}" target="_self">Box Plot</a>
                        <a href="{url_violin}" target="_self">Violin Plot</a>
                        <a href="{url_ecdf}" target="_self">Cumulative</a>
                        <a href="{url_matrix}" target="_self">Matrix</a>
                    </div>
                </div>
                <div class="dropdown-item">
                    Variables
                    <div class="submenu">
                        <div class="dropdown-item">
                            X Variable 
                            <div class="submenu">
                                <div class="dropdown-item">
                                    Time-Series
                                    <div class="submenu">
                                        <a href="{url_hourly} target="_self">Hourly</a>
                                        <a href="{url_daily}" target="_self">Daily</a>
                                        <a href="{url_weekly}" target="_self">Weekly</a>
                                        <a href="{url_monthly}" target="_self">Monthly</a>
                                        <a href="{url_yearly}" target="_self">Yearly</a>
                                        <a href="{url_monthly_multi}" target="_self">Monthly Multi-Year</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="dropdown-item">
                            Y Variable
                            <div class="submenu">
                                <div class="dropdown-item">
                                    Energy
                                    <div class="submenu">
                                        <a href="{url_max}" target="_self">Max. Cap</a>
                                        <a href="{url_tot}" target="_self">Total Gen</a>
                                        <a href="{url_sys}" target="_self">System Cap</a>
                                        <a href="{url_gen}" target="_self">System Gen</a>
                                    </div>
                                </div>
                                <div class="dropdown-item">
                                    Market
                                    <div class="submenu">
                                        <a href="{url_pool}" target="_self">Pool Price</a>
                                        <a href="{url_fpool}" target="_self">Pool (Forecast)</a>
                                        <a href="{url_rolling} target="_self"> Rolling (30 Day)</a>
                                    </div>
                                </div>
                            </div>  
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="menu-item">
            Utils
            <div class="dropdown">
                <div>Calculator</div>
                <div>Write Pad</div>
            </div>
        </div>
        <div class="menu-item">
            Help
            <div class="dropdown">
                <div>Dashboard Help</div>
                <div>Report a Bug</div>
                <div>About the Dashboard</div>
            </div>
    </div>
    <div class="taskbar-clock" id="taskbar-clock">00:00:00 PM</div>
    <script>
        function updateTaskbarClock() {{
            const now = new Date();
            let hours = now.getHours();
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';
            
            hours = hours % 12;
            hours = hours ? hours : 12;
            const hoursStr = String(hours).padStart(2, '0');
    
            const timeString = hoursStr + ":" + minutes + ":" + seconds + " " + ampm;
            
            // Find the clock element in the parent document
            const clockElement = document.getElementById('taskbar-clock');
            if (clockElement) {{
                clockElement.textContent = timeString;
            }}
        }}
    
        // Update every second
        setInterval(updateTaskbarClock, 1000);
        updateTaskbarClock();
    </script>
    """, unsafe_allow_html=True)
    
    
        
    # ---------------------------------- CODE SECTION FOR GUI USER INPUT to SYSTEM OUTPUTS --------------------------------------------------------------
    
    
    
    # Checking for Import or Export Condition
    
    if dataflow == "Export":
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="exported_dataset.csv", mime="text/csv")
        dataflow = "None"
    
    
    # ------------- This Section Handles the Y-Variables for Visuals --------
 
    
    if y_var == "max_cap":
        y_var = "maximum_capacity__solar"
        data_action = "Max Solar Capacity"
    
    if y_var == "total_gen":
        y_var = "total_generation__solar"
        data_action = "Total Solar Generation"
    
    if y_var == "sys_cap":
        y_var = "system_capacity__solar"
        data_action = "System (Solar) Capacity"
    
    if y_var == "sys_gen":
        y_var = "system_generation__solar"
        data_action = "System (Solar) Generation"
    
    if y_var == "pool_price":
        data_action = "Pool Prices"
    
    if y_var == "pool_forecast":
        y_var = "forecast_pool_price"
        data_action = "Forecasted Pool Prices"
    
    if y_var == "rolling_avg":
        y_var = "rolling_30day_avg"
        data_action = "Rolling 30-Day Average"  
    
    
    # ------------------- This Branch will handle the X-Variable Handling -------------
    if x_new in ["hourly", "daily", "weekly", "monthly", "yearly"]:
        
        if x_new == "hourly":
            df = df
            range_select = "Hourly"
            
        elif x_new == "weekly":
            df = weekly_agg(df, y_new)
            range_select = "Weekly"
    
        elif x_new == "monthly":
            df = monthly_agg(df, y_new)
            range_select = "Monthly"
        
        elif x_new == "daily":
            df = aeso_daily_agg(df)
            range_select = "Daily"
        
        elif x_new == "yearly":
            df = aeso_yearly_agg(df)
            range_select = "Yearly"
    
        x_new = "DateTime"
    
    
    
    # Application of the Changes & Session Save State
    # CHECK CHECK CONDITION FOR LAST MINUTE VISUALS PRE-DEMO
    if vis_type.lower() == "monthly_multi":
    
        df_copy = df.copy()
    
        # Ensure datetime exists
        df_copy["DateTime"] = pd.to_datetime(df_copy["DateTime"])
    
        # Extract year + month
        df_copy["year"] = df_copy["DateTime"].dt.year
        df_copy["month"] = df_copy["DateTime"].dt.month
    
        # Aggregate
        monthly_generation = (
            df_copy
            .groupby(['year', 'month'])[y_var]  # <-- adjust if needed
            .sum()
            .reset_index()
        )
    
        fig = px.line(
            monthly_generation,
            x='month',
            y=y_var,
            color='year',
            title=f'Monthly {y_var} Over Time',
            labels={
                'month': 'Month',
                y_var: '(MWh)',
                'year': 'Year'
            }
        )
    
        fig.update_layout(
            xaxis=dict(tickmode='linear', tick0=1, dtick=1),
            template="presentation",  # or "plotly_white"
            paper_bgcolor="rgba(0,0,0,0)",   # transparent background
            plot_bgcolor="rgba(56,196,1,0)"            
        )    
    
    if view_mode == "Descriptive":
        df_copy = df.copy()
        
        
        st.header(f"Descriptive Analytics for {df_select}")
        st.dataframe(df_copy.describe())
        st.divider()
    
        st.header(f"Data-Types for {df_select}")
        st.dataframe(df_copy.dtypes)
    
        st.header(f"Missing & Invalid Values for {df_select}")
        st.dataframe(df.isnull().sum())
    
        st.header(f"Correlation Matrix for {df_select}")
        st.dataframe(df_copy.corr(numeric_only=True))
    
    else:
        try:
            
            if vis_type.lower() == "monthly_multi":
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                plotly_vis(df, x_new, y_var, vis_type.lower(), df_select=df_select, data_action=data_action)
        except NameError:
            data_action = "Generation"
            plotly_vis(df, x_new, y_var, vis_type.lower(), df_select=df_select, data_action=data_action)
        
    
    tab1, tab2 = st.tabs(['Overview', 'Methodology'])
            
    with tab1:
                
        st.write("Insert KPI Cards Here...")
                
                
    with tab2:
        st.header("Methodology")
                
        s_tab1, s_tab2 = st.tabs(['Imputation', 'External Data'])
                
        with s_tab1:
            st.subheader("Handling Missing Data, Invalid Data, or Corrupted Data:")
            st.write("The method used to logically-impute the missing and/or corrupted data entries found in the New Jubilee Greenhouse & Bissell Thrift Shop Datasets was to utilize the Python library called 'PVLib'.")
            st.write("PVLib (Photo-Voltaic Library) for Python is a 'Solar Generation Simulator' powered by an Astronomy and Weather Engine utilizing a solar site's configuration of panel tilt, azimuth, location coordinates and system capacity along with solar irradiance data to generate theoretical solar output values based on the data fed into the engine.")
            st.write("As the given datasets did not include panel tilt or azimuth, the panel tilt was defaulted to be 30 Degrees as it is an 'Engineering-Safe' baseline for northern latitude operations of solar sites. Additionally, as the panel azimuth was also not included, its direction was observed by the usage of satellite imagery and a protractor.")
            st.write("The imputation operations also involved the incorporation of Weather & Solar Irradiance Data sourced from OpenMeteo on the exact days in conjunction with the given datasets.")
            st.write("PVLib is able to produce a theoretical output based on the Irradiance Data & Site Configuration Data. This value is the best theoretical output possibility and thus required a 'dampening' effect to bring it in-line with a realistic profile exhibited by the solar sites.")
            st.write("This dampenening effect is applied as the form of a 'Performance Ratio' taken as a value from 'What Was Really Produced (Actual) / What Could Have Been Produced (Theoretical). This Performance Ratio (PR) was then applied to the values that were imputed for the missing, invalid or corrupted days. The performance ratio is essentially a rolling average of a couple days before and after the bad data entry.")
            st.write("As a result, the general trend of the system's behavior is well-captured and safely-accurate to enact further Exploratory Analysis and Environmental Impact Calculations.")
                
        with s_tab2:
            st.subheader("Using External Datasets:")
                    
            ss_tab1, ss_tab2 = st.tabs(['AESO', 'OpenMeteo'])
                    
            with ss_tab1:
                st.subheader("AESO - Alberta Electric System Operator")
                st.write("The usage of AESO data allows the incorporation of insights into 'real-time' hourly grid data with features such as total generation by type, system capacities per fuel, amongst others.")
                st.write("Additionally, the use of AESO data also gives data into pool prices (wholesale electricity prices) as well as the grip supply mixes between solar, coal, etc.")
                st.write("This provides market context for solar performance aligning Edmonton communities with the Alberta Market.")
                st.write("Finally, it provides seasonal and daily solar performance as well ass emissions data for the overall Alberta Energy Market which allows the insights into trends over the years.")
        
            with ss_tab2:
                st.subheader("OpenMeteo - Open-Source Weather API")
                st.write("The usage of OpenMeteo's Weather Data allowed for the incorporation of the much needed historical weather records that would be utilized in the engine for PVLib as it simulated the theoretical solar output conditions for the missing and corrupted days residing within the New Jubilee & Bissell Thrift Shop datasets.")
                st.write("The obtained Weather Data also featured Solar Irradiance data by the hourly which was then aggregated to a daily average. The critical components that were required for the PVLib simulation to successfully enact its calculations were GNI, DNI, DHI components of Solar Irradiance.")
                st.write("Additionally, the incorporation of 'Wind Speed' also played a factor in the calculations of PVLib and was easily provided by the dataset obtained from OpenMeteo.")
                st.write("The OpenMeteo Dataset required the use of the Solar Site's Location Coordinates in Lat/Long format in order to achieve best & accurate historical weather records for the time-frame of the given datasets.")
                st.write("This sourced dataset used for imputation was also used for the Eco-Impacts Simulator page, using DNI, GHI, DHI, wind speed and temperature values.")
                        
        
    components.html("""
    <script>
        function updateClock() {
            const now = new Date();
            let hours = now.getHours();
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';
            
            hours = hours % 12;
            hours = hours ? hours : 12;
            const timeString = `${String(hours).padStart(2, '0')}:${minutes}:${seconds} ${ampm}`;
    
            // REACH OUT of the component's iframe into the main page
            const clock = window.parent.document.getElementById('taskbar-clock');
            if (clock) {
                clock.textContent = timeString;
            }
        }
        
        // Update every second
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """, height=0)     
    



# ----------------------------- SECTION FOR SPICE DATA ------------------------------------ SECTIOM FOR SPICE DATA ---------------------------- ###############


else:
    
    
    # This HTML File Handles the Task Bar Menu Labelling Control & Drop-Down Menu handling & Drop-Down Sub
    st.markdown(f"""
    <div class="menu-bar">
        <div class="menu-item">
            Data
            <div class="dropdown">
                <div class="dropdown-item">
                <span style="display:flex; justify-content:space-between;">
                    Change Dataset
                </span>
                <div class="submenu">
                    <div class="dropdown-item">
                        <span style="display:flex; justify-content:space-between;">
                            SPICE 
                        </span>
                        <div class="submenu">
                            <a href="{url_jubilee}" target="_self">New Jubilee</a>
                            <a href="{url_bissell}" target="_self">Bissell Thrift</a>
                    </div>
                </div>
                <div class="dropdown-item">
                <span style="display:flex; justify-content:space-between;">
                    AESO
                </span>
                <div class="submenu">
                    <a href="{url_aeso}" target="_self">Generation & Pool Markets</a>
                </div>
            </div>
        </div>
    </div>
                <div>Import Dataset</div>
                <a href="{url_export}" target="_self">Export Dataset</a>
            </div>
        </div>
        <div class="menu-item">
            Edit
            <div class="dropdown">
                <div>Undo Action</div>
                <div>Redo Action</div>
            </div>
        </div>
        <div class="menu-item">
            View
            <div class="dropdown">
                <a href="{url_descriptive}" target="_self">Descriptive</a>
                <a href="{url_graphical}" target="_self">Graphical</a>
            </div>
        </div>
        <div class="menu-item">
            Format
            <div class="dropdown">
                <div class="dropdown-item">
                    Visualization
                    <div class="submenu">
                        <a href="{url_line}" target="_self">Line</a> 
                        <a href="{url_bar}" target="_self">Bar</a>
                        <a href="{url_area}" target="_self">Area</a>
                        <a href="{url_scatter}" target="_self">Scatter</a>
                        <a href="{url_histo}" target="_self">Histogram</a>
                        <a href="{url_box}" target="_self">Box Plot</a>
                        <a href="{url_violin}" target="_self">Violin Plot</a>
                        <a href="{url_ecdf}" target="_self">Cumulative</a>
                        <a href="{url_matrix}" target="_self">Matrix</a>
                    </div>
                </div>
                <div class="dropdown-item">
                    Variables
                    <div class="submenu">
                        <div class="dropdown-item">
                            X Variable 
                            <div class="submenu">
                                <div class="dropdown-item">
                                    Time-Series
                                    <div class="submenu">
                                        <a href="{url_daily}" target="_self">Daily</a>
                                        <a href="{url_weekly}" target="_self">Weekly</a>
                                        <a href="{url_monthly}" target="_self">Monthly</a>
                                        <a href="{url_yearly}" target="_self">Yearly</a>
                                    </div>
                                </div>
                                <div class="dropdown-item">
                                    Weather
                                    <div class="submenu">
                                        <a href="{url_cloud}" target="_self">Cloud Cover</a>
                                        <a href="{url_precip}" target="_self">Precipitation</a>
                                        <a href="{url_temp}" target="_self">Air Temp</a>
                                        <a href="{url_wind}" target="_self">Wind Speed</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="dropdown-item">
                            Y Variable
                            <div class="submenu">
                                <div class="dropdown-item">
                                    Energy
                                    <div class="submenu">
                                        <a href="{url_output}" target="_self">Solar Output</a>
                                        <a href="{url_ratio}" target="_self">Perf. Ratio</a>
                                    </div>
                                </div>
                                <div class="dropdown-item">
                                    Enviro
                                    <div class="submenu">
                                        <a href="{url_carbon}" target="_self">CO2 Avoided</a>
                                        <a href="{url_trees}" target="_self">Trees Saved</a>
                                        <a href="{url_cars}" target="_self">Cars Equivalent</a>
                                        <a href="{url_homes}" target="_self">Homes Powered</a>
                                        <a href="{url_coale}" target="_self">Coal Emission Avoided</a>
                                        <a href="{url_coalt}" target="_self">Coal Weight Avoided</a>
                                        <a href="{url_gas}" target="_self">Gas Saved</a>
                                    </div>
                                </div>
                            </div>  
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="menu-item">
            Tools
            <div class="dropdown">
                <div onclick="toggleCalculator()" style="cursor:pointer; padding: 5px 10px;">Calculator</div>
                <div>Write Pad</div>
            </div>
        </div>
        <div class="menu-item">
            Help
            <div class="dropdown">
                <div>Dashboard Help</div>
                <div>Report a Bug</div>
                <div>About the Dashboard</div>
            </div>
    </div>
    <div id="calculator-popout" style="display: none; position: fixed; top: 20%; left: 50%; transform: translateX(-50%); background: white; border: 3px solid #3170de; padding: 20px; z-index: 99999; width: 250px; text-align: center; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
        <div style="background: #3170de; color: white; padding: 8px 15px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: bold; font-family: sans-serif;">Calculator</span>
            <button onclick="toggleCalculator()" style="background: none; border: none; color: white; cursor: pointer; font-size: 20px; font-weight: bold;">&times;</button>
        </div>
</div>
    <div class="taskbar-clock" id="taskbar-clock">00:00:00 PM</div>
    <script>
    
    // This JavaScript Portion Handles the System-Clock on the Taskbar
    
        function updateTaskbarClock() {{
            const now = new Date();
            let hours = now.getHours();
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';
            
            hours = hours % 12;
            hours = hours ? hours : 12;
            const hoursStr = String(hours).padStart(2, '0');
    
            const timeString = hoursStr + ":" + minutes + ":" + seconds + " " + ampm;
            
            // Find the clock element in the parent document
            const clockElement = document.getElementById('taskbar-clock');
            if (clockElement) {{
                clockElement.textContent = timeString;
            }}
        }}
    
        // Update every second
        setInterval(updateTaskbarClock, 1000);
        updateTaskbarClock();
    </script>
    """, unsafe_allow_html=True)
    
   
    # ---------------------------------- CODE SECTION FOR GUI USER INPUT to SYSTEM OUTPUTS --------------------------------------------------------------
    

    
    # Checking for Import or Export Condition
    
    if dataflow == "Export":
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="exported_dataset.csv", mime="text/csv")
        dataflow = "None"
    
    
    # ------------- This Section Handles the Y-Variables for Visuals --------
    
    if y_var not in ["output", "ratio", "carbon", "trees", "cars", "homes", "coal_e", "coal_t", "gas"]:
        y_var = "output"
        
    if y_var == "output":
        y_var = "Daily Value Imputed"
        data_action = "Generation"
    
    if y_var == "ratio":
        y_var = "PR_Daily"
        data_action = "Perf. Ratio"
    
    if y_var == "carbon":
        y_var = "co2_avoided"
        data_action = "CO2 Avoided"
    
    if y_var == "trees":
        y_var = "trees_saved"
        data_action = "Trees Saved"
    
    if y_var == "cars":
        y_var = "cars_offroad"
        data_action = "Cars Neutralized"
    
    if y_var == "homes":
        y_var = "homes_powered"
        data_action = "Homes Powered"
    
    if y_var == "coal_e":
        y_var = "coal_emission_avoided"
        data_action = "Coal Avoided (Emissive)"
    
    if y_var == "coal_t":
        y_var = "coal_tonnage_avoided"
        data_action = "Coal Avoided (Tonnage)"
    
    if y_var == "gas":
        y_var = "gas_saved"
        data_action = "Gasoline Saved"
    
    
    
    # ------------------- This Branch will handle the X-Variable Handling -------------
    if x_new in ["daily", "weekly", "monthly", "yearly"]:
    
        if x_new == "weekly":
            df = weekly_agg(df, y_var)
            range_select = "Weekly"
    
        elif x_new == "monthly":
            df = monthly_agg(df, y_var)
            range_select = "Monthly"
        
        elif x_new == "daily":
            df = df
            range_select = "Daily"
    
        x_new = "time"
    
    else:
        if x_new == "cloud":
            x_new = "cloud_cover (%)"
        
        elif x_new == "precip":
            x_new = "precipitation (mm)"
        
        elif x_new == "temp":
            x_new = "temp_air"
        
        elif x_new == "wind":
            x_new = "wind_speed"
    
    
    # Application of the Changes & Session Save State
    
    
    if view_mode == "Descriptive":
        df_copy = df.copy()
        
        st.header("Descriptive Analytics")
        st.dataframe(df_copy.describe())
        st.divider()
    
        st.header("Data-Types")
        st.dataframe(df_copy.dtypes)
    
        st.header("Missing & Invalid Values")
        st.dataframe(df.isnull().sum())
    
        st.header("Correlation Matrix")
        st.dataframe(df_copy.corr(numeric_only=True))
    
    else:
        try:
            plotly_vis(df, x_new, y_var, vis_type.lower(), df_select=df_select, data_action=data_action)
        except NameError:
            data_action = "Generation"
            plotly_vis(df, x_new, y_var, vis_type.lower(), df_select=df_select, data_action=data_action)
        
    
    df = df_visser if st.session_state.dataset == "New Jubilee" else df_bissell
    
    
    tab1, tab2 = st.tabs(['Overview', 'Methodology'])
            
    with tab1:
                
        st.write("In Development...")
                
                
    with tab2:
        st.header("Methodology")
                
        s_tab1, s_tab2 = st.tabs(['Imputation', 'External Data'])
                
        with s_tab1:
            st.subheader("Handling Missing Data, Invalid Data, or Corrupted Data:")
            st.write("The method used to logically-impute the missing and/or corrupted data entries found in the New Jubilee Greenhouse & Bissell Thrift Shop Datasets was to utilize the Python library called 'PVLib'.")
            st.write("PVLib (Photo-Voltaic Library) for Python is a 'Solar Generation Simulator' powered by an Astronomy and Weather Engine utilizing a solar site's configuration of panel tilt, azimuth, location coordinates and system capacity along with solar irradiance data to generate theoretical solar output values based on the data fed into the engine.")
            st.write("As the given datasets did not include panel tilt or azimuth, the panel tilt was defaulted to be 30 Degrees as it is an 'Engineering-Safe' baseline for northern latitude operations of solar sites. Additionally, as the panel azimuth was also not included, its direction was observed by the usage of satellite imagery and a protractor.")
            st.write("The imputation operations also involved the incorporation of Weather & Solar Irradiance Data sourced from OpenMeteo on the exact days in conjunction with the given datasets.")
            st.write("PVLib is able to produce a theoretical output based on the Irradiance Data & Site Configuration Data. This value is the best theoretical output possibility and thus required a 'dampening' effect to bring it in-line with a realistic profile exhibited by the solar sites.")
            st.write("This dampenening effect is applied as the form of a 'Performance Ratio' taken as a value from 'What Was Really Produced (Actual) / What Could Have Been Produced (Theoretical). This Performance Ratio (PR) was then applied to the values that were imputed for the missing, invalid or corrupted days. The performance ratio is essentially a rolling average of a couple days before and after the bad data entry.")
            st.write("As a result, the general trend of the system's behavior is well-captured and safely-accurate to enact further Exploratory Analysis and Environmental Impact Calculations.")
                
        with s_tab2:
            st.subheader("Using External Datasets:")
                    
            ss_tab1, ss_tab2 = st.tabs(['AESO', 'OpenMeteo'])
                    
            with ss_tab1:
                st.subheader("AESO - Alberta Electric System Operator")
                st.write("The usage of AESO data allows the incorporation of insights into 'real-time' hourly grid data with features such as total generation by type, system capacities per fuel, amongst others.")
                st.write("Additionally, the use of AESO data also gives data into pool prices (wholesale electricity prices) as well as the grip supply mixes between solar, coal, etc.")
                st.write("This provides market context for solar performance aligning Edmonton communities with the Alberta Market.")
                st.write("Finally, it provides seasonal and daily solar performance as well ass emissions data for the overall Alberta Energy Market which allows the insights into trends over the years.")
        
            with ss_tab2:
                st.subheader("OpenMeteo - Open-Source Weather API")
                st.write("The usage of OpenMeteo's Weather Data allowed for the incorporation of the much needed historical weather records that would be utilized in the engine for PVLib as it simulated the theoretical solar output conditions for the missing and corrupted days residing within the New Jubilee & Bissell Thrift Shop datasets.")
                st.write("The obtained Weather Data also featured Solar Irradiance data by the hourly which was then aggregated to a daily average. The critical components that were required for the PVLib simulation to successfully enact its calculations were GNI, DNI, DHI components of Solar Irradiance.")
                st.write("Additionally, the incorporation of 'Wind Speed' also played a factor in the calculations of PVLib and was easily provided by the dataset obtained from OpenMeteo.")
                st.write("The OpenMeteo Dataset required the use of the Solar Site's Location Coordinates in Lat/Long format in order to achieve best & accurate historical weather records for the time-frame of the given datasets.")
                st.write("This sourced dataset used for imputation was also used for the Eco-Impacts Simulator page, using DNI, GHI, DHI, wind speed and temperature values.")    
    
    components.html("""
    <script>
        function updateClock() {
            const now = new Date();
            let hours = now.getHours();
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';
            
            hours = hours % 12;
            hours = hours ? hours : 12;
            const timeString = `${String(hours).padStart(2, '0')}:${minutes}:${seconds} ${ampm}`;
    
            // REACH OUT of the component's iframe into the main page
            const clock = window.parent.document.getElementById('taskbar-clock');
            if (clock) {
                clock.textContent = timeString;
            }
        }
        
        // Update every second
        setInterval(updateClock, 1000);
        updateClock();
    </script>
    """, height=0)    

    

