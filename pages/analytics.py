# ---------------------------------------- Test File for Side-Bar Navigation  --------------------------------------------------------

# Import Pool
import streamlit as st
import plotly.express as px

from helpers.data_load import load_data
from helpers.data_funcs import *



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



# Loading in the Data (If Not Cached)
df_visser, df_bissell = load_data()

# Loading in the Icons
icon_sys_info = get_base64_image("static/icons/icon_sysinfo.png")
icon_impacts_info = get_base64_image("static/icons/icon_impacts.png")
icon_ml_info = get_base64_image("static/icons/icon_ml.png")
icon_home = get_base64_image("static/icons/icon_home.png")

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
</div>
''', unsafe_allow_html=True)



# ------------------------------------------------ CODE & DATA AREA -------------------------------------------------------------------
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
        st.switch_page("pages/ml.py")



# DataFrame Selection for Solar Site
df_select = st.radio("Select Solar Site:", ['Bissell Thrift Shop', 'New Jubilee Greenhouse'])

if df_select == 'Bissell Thrift Shop':
    df = df_bissell

elif df_select == 'New Jubilee Greenhouse':
    df = df_visser


st.divider()


filt_col_1, filt_col_2 = st.columns(2)

with filt_col_1:
    range_select = st.radio("Select Interval Type:", ['Daily', 'Weekly', 'Monthly'], horizontal=True)

with filt_col_2:
    year_select = st.selectbox("Select a Year:", (2025, 2026))

if year_select:
 
    df['time'] = pd.to_datetime(df['time'])
    df_filtered = df[df['time'].dt.year == year_select]

st.header(f"{range_select} Generation (kWh) for {df_select}")
tab_1, tab_2 = st.tabs(['Graph Data', 'Sheet Data'])

if range_select == 'Daily':

    with tab_1:
        if year_select:
            st.bar_chart(df_filtered['Daily Value Imputed'])

        else:
            df['time'] = pd.to_datetime(df['time'])
            df = df.set_index('time')

            st.bar_chart(df['Daily Value Imputed'])

    with tab_2:
        if year_select:
            
            st.dataframe(df_filtered[['time', 'Daily Value Imputed']])

        else:    
            st.dataframe(df[['time', 'Daily Value Imputed']])
    

    

elif range_select == 'Weekly':

    if year_select:
        df_filtered['time'] = pd.to_datetime(df_filtered['time'])
        df_filtered = df_filtered.set_index('time')

        df_weekly = df_filtered.resample('W').agg({
        'Daily Value Imputed': 'sum'
        })

    
    else:
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')

        df_weekly = df.resample('W').agg({
        'Daily Value Imputed': 'sum'
        })

    with tab_1:
        st.dataframe(df_weekly)
    
    with tab_2:
        st.line_chart(df_weekly)
    

elif range_select == 'Monthly':

    if year_select:
        monthly_summary = monthly_output_sums(df_filtered)
    
    else:
        monthly_summary = monthly_output_sums(df)

    with tab_1:
        st.dataframe(monthly_summary)
    
    with tab_2:
        st.line_chart(monthly_summary)

    

# Setting up Tabs on for Descriptive
tab1 = st.tabs(["Overview"])

with tab1:

    st.write("Dataset Description")
    st.write(df.describe())

    st.write("Dataset Null Count")
    st.write(df.isnull().sum())
