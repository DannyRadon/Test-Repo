# ---------------------------------------- Test File for Side-Bar Navigation  --------------------------------------------------------

# Import Pool
import urllib.parse
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from st_click_detector import click_detector
from helpers.data_load import load_data
from helpers.data_funcs import *


# Loading in the Data (If Not Cached)
df_visser, df_bissell, df_aeso = load_data()

range_select = "Daily"

params = st.query_params

## --- SYNC URL TO SESSION STATE ---
for url_key, state_key in [
    ("dataset", "dataset"), 
    ("graph", "graph_type"), 
    ("x_var", "x_var"), 
    ("y_var", "y_var"),
]:
    if url_key in st.query_params:
        st.session_state[state_key] = st.query_params[url_key]


# --- SETTING DEFAULTS --- If the app is opened for the first time (no URL params)

if "dataset" not in st.session_state:
    st.session_state.dataset = "New Jubilee"

if "graph_type" not in st.session_state:
    st.session_state.graph_type = "Line"

if "x_var" not in st.session_state:
    st.session_state.x_var = "month"

if "y_var" not in st.session_state:
    st.session_state.y_var = "co2_avoided"


if "dataflow" not in st.session_state:
    st.session_state.dataflow = "None"



# --- GENERATING DYNAMIC URL LINKS ---

# Dataset URLs
url_bissell = build_url(dataset="Bissell Thrift")
url_jubilee = build_url(dataset="New Jubilee")

# Import & Export URLs
url_export = build_url(dataflow="Export")

# Graph Visualization URLs
url_pie = build_url(graph="Pie")
url_tree = build_url(graph="Tree")


# X Variable URLs
url_month = build_url(x_var="month")
url_projects = build_url(x_var="projects")

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
                                    

data_action = "Carbon Avoided"

# Global Variables to Use for State Session Updates & Calls
df_selection = st.session_state.dataset
    
vis_type = st.session_state.graph_type
if vis_type not in ["Pie", "Tree"]:
    vis_type = "Pie"

x_new = st.session_state.x_var

if x_new not in ['month', 'projects']:
    x_new = "month"
    
y_new = st.session_state.y_var
dataflow = st.session_state.dataflow

# State Session Checks for Current Dataset(s)
if df_selection == "Bissell Thrift":
    df = df_bissell
    df_select = "Bissell Thrift Shop"
    
else:
    df = df_visser
    df_select = "New Jubilee"



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


# Loading in the Icons
icon_sys_info = get_base64_image("static/icon_sysinfo.png")
icon_analytics_info = get_base64_image("static/icon_analytics.png")
icon_ml_info = get_base64_image("static/icon_ml.png")
icon_home = get_base64_image("static/icon_home.png")

# Title for the Page
st.title("Environmental Impacts")


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
        <img src="data:image/png;base64,{icon_analytics_info}">
        <div class="card-text">Analytics</div>
    </div>
    <div class="icon-card">
        <img src="data:image/png;base64,{icon_ml_info}">
        <div class="card-text">M-Learning</div>
    </div>
</div>
''', unsafe_allow_html=True)


# Clickable-Icon Navigation Area -- Routing to Other Pages -- this is what allows interactivity 

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button(" ", key="home_btn"):
        st.switch_page("home.py")

with col2:
    if st.button(" ", key="sys_info_btn"):
        st.switch_page("pages/system_info.py")

with col3:
    if st.button(" ", key="imp_info_btn"):
        st.switch_page("pages/analytics.py")

with col4:
    if st.button(" ", key="ml_info_btn"):
        st.switch_page("pages/ml.py")


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
                <div class>Gen Market</div>
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
        Format
        <div class="dropdown">
            <div class="dropdown-item">
                Visualization
                <div class="submenu">
                    <a href="{url_pie}" target="_self">Pie</a>
                    <a href="{url_tree}" target="_self">Tree Map</a> 
                </div>
            </div>
            <div class="dropdown-item">
                Variables
                <div class="submenu">
                    <div class="dropdown-item">
                        Comparisons 
                        <div class="submenu">
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




# ------------------------------------------------ CODE & DATA AREA -------------------------------------------------------------------
if y_new not in ["output", "ratio", "carbon", "trees", "cars", "homes", "coal_e", "coal_t", "gas"]:
    y_new = "output"

if y_new == "output":
    y_new = "Daily Value Imputed"
    data_action = "Generation"

if y_new == "ratio":
    y_new = "PR_Daily"
    data_action = "Perf. Ratio"

if y_new == "carbon":
    y_new = "co2_avoided"
    data_action = "CO2 Avoided"

if y_new == "trees":
    y_new = "trees_saved"
    data_action = "Trees Saved"

if y_new == "cars":
    y_new = "cars_offroad"
    data_action = "Cars Neutralized"

if y_new == "homes":
    y_new = "homes_powered"
    data_action = "Homes Powered"

if y_new == "coal_e":
    y_new = "coal_emission_avoided"
    data_action = "Coal Avoided (Emissive)"

if y_new == "coal_t":
    y_new = "coal_tonnage_avoided"
    data_action = "Coal Avoided (Tonnage)"

if y_new == "gas":
    y_new = "gas_saved"
    data_action = "Gasoline Saved"

# ------------------- This Branch will handle the X-Variable Handling -------------
if x_new == "month":
    x_new = "Month"


plotly_vis(df, x_new, y_new, vis_type.lower(), data_action=data_action, df_select=df_select)
st.divider()
st.header("All Impacts by Projects")

impact_cols = [
"co2_avoided", "cars_offroad",
"homes_powered", "coal_tonnage_avoided", 
"coal_emission_avoided"
]

bissell_totals = df_bissell[impact_cols].sum()
jubilee_totals = df_visser[impact_cols].sum()

df_compare = pd.DataFrame({
"Metric": impact_cols,
"Bissell": bissell_totals.values,
"Jubilee": jubilee_totals.values
})

fig = px.bar(
df_compare,
x="Metric",
y=["Bissell", "Jubilee"],
barmode="group",
color_discrete_map={
    "Bissell": "#A5BEE0",   # green
    "Jubilee": "#0058EE"    # blue
    }
)

    
fig.update_layout(
paper_bgcolor="rgba(0,0,0,0)",   # whole canvas
plot_bgcolor="rgba(0,0,0,0)",     # plotting area
)

st.plotly_chart(fig)


st.divider()



df = df_visser if st.session_state.dataset == "New Jubilee" else df_bissell

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
