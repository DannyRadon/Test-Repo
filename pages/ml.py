import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

# Import Pool
import urllib.parse
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.tools as tls
import matplotlib.pyplot as plt

from st_click_detector import click_detector
from helpers.data_load import load_data
from helpers.data_funcs import *

# Imported ML pieces
from src.aeso_cleaning_fe1 import *
from src.modeling_2 import *



st.title("Machine Learning & Forecasting")

# ----------------------------
# DATA PIPELINE
# ----------------------------

@st.cache_data
def load_clean_data():
    aeso = load_data_aeso()
    return clean_fe1(aeso)

@st.cache_resource
def load_model_outputs():
    aeso_clean = load_clean_data()
    return run_modeling_pipeline(aeso_clean)

outputs = load_model_outputs()


# ------------------------------- THIS SECTION IS TO SETUP & OPERATE THE GUI MENU LOGIC ----------------------------------- |


params = st.query_params

# --- SYNC URL TO SESSION STATE --- |
for url_key, state_key in [
    ("graph", "graph_type"), 
    ("x", "x"), 
    ("y_test", "y_test"),
    ("view_type", "view_type")
]:
    if url_key in st.query_params:
        st.session_state[state_key] = st.query_params[url_key]




# --- SETTING DEFAULTS --- If the app is opened for the first time (no URL params)
        
        
if "graph_type" not in st.session_state:
    st.session_state.graph_type = "Line"
        
if "x" not in st.session_state:
    st.session_state.x = "DateTime"
        
if "y_test" not in st.session_state:
    st.session_state.y_test = "gen_cap"
        
if "view_type" not in st.session_state:
    st.session_state.view_type = "prediction"
        
if "dataflow" not in st.session_state:
    st.session_state.dataflow = "None"



# ----------------------------------------- Initializing & Building HTML URLs --- Used for GUI Click Detection Logic -----------------------|


# Import & Export URLs
url_export = build_url_ml(dataflow="Export")

# Graph Visualization URLs
url_bar = build_url_ml(graph="Bar")
url_line = build_url_ml(graph="Line")
url_area = build_url_ml(graph="Area")
url_scatter = build_url_ml(graph="Scatter")

# View Mode URLs
url_pred = build_url_ml(view_type="prediction")
url_xai = build_url_ml(view_type="insights")
url_fore = build_url_ml(view_type="forecast")


# Output URLs 
url_gencap = build_url_ml(y_test="gen_cap")
url_share = build_url_ml(y_test="share")
url_total = build_url_ml(y_test="gen_total")
url_avoided = build_url_ml(y_test="avoided")


# Global Variables to Use for State Session Updates & Calls
vis_type = st.session_state.graph_type
y_test = st.session_state.y_test
dataflow = st.session_state.dataflow
view_type = st.session_state.view_type


# ----------------------------  This CSS SECTION (MARKDOWN) SETS UP THE CLICKABLE ICONS AND CANVAS (HOME, SYS INFO, ETC) --------------------------------- \




# This CSS creates the Gradient MAIN Background 
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
icon_impacts_info = get_base64_image("static/icon_impacts.png")
icon_analytics_info = get_base64_image("static/icon_analytics.png")
icon_home = get_base64_image("static/icon_home.png")


# THIS MARKDOWN FILE HANDLES THE TOP BAR & SIDE-BAR GUI APPEARANCES
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
        <img src="data:image/png;base64,{icon_analytics_info}">
        <div class="card-text">Analytics</div>
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
        st.switch_page("pages/impacts.py")

with col4:
    if st.button(" ", key="ml_info_btn"):
        st.switch_page("pages/analytics.py")
        
        
        



# ---------------- WARNING! ------------------------------ NASTY HTML SECTION HANDLING THE BRIDGE BETWEEN GUI CLICK & ST ENGINE ----------------------------- WARNING! ----------------------------|


# This HTML File Handles the Task Bar Menu Labelling Control & Drop-Down Menu handling & Drop-Down Sub
st.markdown(f"""
<div class="menu-bar">
    <div class="menu-item">
        Data
        <div class="dropdown">
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
            <a href="{url_pred}" target="_self">Predictions</a>
            <a href="{url_xai}" target="_self">XAI Insights</a>
            <a href="{url_fore}" target="_self">60-Month Forecasts</a>
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
                </div>
            </div>
            <div class="dropdown-item">
                Outputs
                <div class="submenu">
                    <div class="dropdown-item">
                        Types
                        <div class="submenu">
                            <div class="dropdown-item">
                                Energy
                                <div class="submenu">
                                    <a href="{url_gencap}" target="_self">Gen per Cap</a>
                                    <a href="{url_total}" target="_self">Total Generated</a>
                                </div>
                            </div>
                            <div class="dropdown-item">
                                Eco & Market
                                <div class="submenu">
                                    <a href="{url_share}" target="_self">Solar Market Share</a>
                                    <a href="{url_avoided}" target="_self">Emissions Avoided</a>
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



# Checking for Import or Export Condition

if dataflow == "Export":
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="exported_dataset.csv", mime="text/csv")
    dataflow = "None"


# ------------- This Section Handles the Y-Variables for Visuals --------
    
if y_test == "gen_cap":
    selected_target = "solar_generation_per_capacity"
    
if y_test == "share":
    selected_target = "solar_market_share"
    
if y_test == "gen_total":
    selected_target = "total_generation__solar"
    
if y_test == "avoided":
    selected_target = "emissions_avoided"
    




# ------------------------------------------------- ACTUAL PROGRAMMING SECTION WITH DATA AND ENGINE -----------------------------------------------





# ---------------------------- And a Double-Thank You Here...
# RENDER LOGIC
# ----------------------------


if view_type == "prediction":
    plot_prediction_view(outputs, selected_target)
    metrics = outputs["metrics"][selected_target]


elif view_type == "insights":
    st.title("Explainable AI")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Information', 'Metrics', 'Feature Importance', 'Residual Analysis', 'SHAP Analysis', 'Visualizations'])
    
    with tab1:
        st.header("Explainable AI Information") 
        st.divider()
        
        st.subheader("What is Explainable AI?")
        st.write("Explainable AI (XAI) is a set of processes and methods which help human users to observe, comprehend and trust the results created by a Machine Learning Algorithm.")
        st.write("")
        
        st.subheader("How is a Model Explainable?")
        st.write("One part to a Model's Explainability involves Performance Metrics such as:")
        
        sub1, sub2, sub3, sub4 = st.tabs(['RMSE', 'MAE', 'R²', 'Accuracy'])
        
        with sub1:
            st.header("RMSE - Root Mean Square Error")
            st.divider()
            st.write("The Root Mean Square Error (RMSE) is a standard metric used in Machine Learning to measure the accuracy of a model, particularly a 'Regression Model'.") 
            st.write("The computed value represents the average difference between what was predicted and what was actual.")
            st.write("In the context of Explainable AI, the RMSE serves as a crucial quantitative metric to confirm that a 'transparent' Model is performing accurately.")
            st.write("To interpret a calculated RMSE value; a value that is closer to '0' indicates a better fit. A value of '0' indicates a perfect fit.")
            st.write("Units with RMSE is expressed in the same units as the target variable")
            st.subheader("Usage Warning:")
            st.write("RMSE squares the errors before averaging them, allowing higher influence to be given to large errors.")
            st.write("This makes it more sensitive to outliers compared to other Performance Metrics like Mean Absolute Error (MAE).")
        with sub2:
            st.header("MAE - Mean Absolute Error")
    
    with tab2:
        plot_xai_view(outputs)
        st.dataframe(outputs["feature_importance"], use_container_width=True)

elif view_type == "forecast":
    plot_forecast_view(outputs, selected_target)
    st.dataframe(outputs["forecast_df"], use_container_width=True)
    
    
# Update the Taskbar Clock
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
