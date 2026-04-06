# Loading Streamlit Engine
import streamlit as st              # Importing StreamLit Dashboard Module as 'st'

# This CSS creates the Gradient Background -- The Main Background of the PAge
st.markdown("""
<style>
.stApp {
    /* Linear gradient example: top-left blue to bottom-right purple */
    background: linear-gradient(135deg, #2257d6 25%, #3b77bc 50%, #009cde 66%, #d0d0d0 100%);
}
</style>
""", unsafe_allow_html=True)


# This Handles the "Card" Background for the Icons along with Icon Image Size (Default Card Color - Orange)
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

# Importing Base64 Encode/Decode
import base64

# Importing Helper & Data Functions
from helpers.data_load import *     # Importing Data Loaders from Helpers File
from helpers.data_funcs import *    # Importing Helper Functions for Dashboard 


# Initializing the Data into Dashboard
df_visser, df_bissell, df_aeso = load_data()     # Loading the datasets

# Open logo file
with open("static/logo.png", "rb") as l:
    logo_bytes = l.read()

# Encode to base64
b64_logo = base64.b64encode(logo_bytes).decode()


# Creating a Session-State for User
if "page" not in st.session_state:
    st.session_state.page = "home"


# This CSS Section Handles the Display of the Icons and the Clickable Regions for them 



st.markdown(f"""
<div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
    <img src="data:image/png;base64,{b64_logo}" style="height: 75px;">
    <h1 style="margin: 0; padding: 0;">SPICE Dashboard - Home Page</h1>
</div>
""", unsafe_allow_html=True)

# Pre-load icons
icon_sys_info = get_base64_image("static/icon_sysinfo.png")
icon_eda_info = get_base64_image("static/icon_analytics.png")
icon_impacts_info = get_base64_image("static/icon_impacts.png")
icon_ml_info = get_base64_image("static/icon_ml.png")
icon_home = get_base64_image("static/icon_home.png")
icon_chat = get_base64_image("static/icon_chat.png")




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
        <img src="data:image/png;base64,{icon_sys_info}">
        <div class="card-text">System Info</div>
    </div>
    <div class="icon-card">
        <img src="data:image/png;base64,{icon_eda_info}">
        <div class="card-text">Analytics</div>
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


# Overlay invisible buttons -- this is what allows interactivity -- they are like masks...
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button(" ", key="sys_info_btn"):
        st.switch_page("pages/system_info.py")

with col2:
    if st.button(" ", key="eda_info_btn"):
        st.switch_page("pages/analytics.py")

with col3:
    if st.button(" ", key="imp_info_btn"):
        st.switch_page("pages/impacts.py")

with col4:
    if st.button(" ", key="ml_info_btn"):
        st.switch_page("pages/ml.py")

with col5:
    if st.button(" ", key="chat_btn"):
        st.switch_page("pages/chat.py")


tab1, tab2, tab3, tab4 = st.tabs(['Welcome!', 'About SPICE', 'About the Dashboard', 'Developer Updates'])

with tab1:
    st.header("Welcome to the SPICE Dashboard!")
    st.write("To begin, click on one of the 'Page Navigation Icons' with the pictures.")
    st.write("For more Information about this dashboard, SPICE, or recent development updates please select a tab.")

with tab2:
    st.header("About the SPICE Organization")
    st.write("SPICE (Solar Powered Investment Cooperative of Edmonton) is a community-driven organization that enables individuals to invest in and also benefit from local solar energy projects.")
    st.write("Their objective is to make renewable energy more accessible by allowing members to collectively fund solar installations on community and commercial buildings, generating both environmental and financial returns.")
    st.write("By lowering the barrier to entry for solar investment, SPICE empowers everyday citizens, not just large corporations, to participate in the transition to clean energy.")
    st.write("The cooperative model also fosters community engagement, local economic development, and increased awareness of sustainable energy solutions.")
    st.write("Through its projects, SPICE contributes to reducing greenhouse gas emissions while providing members with transparent insights into energy generation and impact.")
    
with tab3:
    st.header("About the SPICE Dashboard")
    st.write("This dashboard was developed with a particular problem statement given to the project team.")
    st.write("The given problem statement to the team is determining how solar generation is evolving within Alberta's electricity market, and how can community solar projects like SPICE leverage this shift to demonstrate measurable environmental benefits and long-term viability?")
    st.write("As a result, this dashboard was developed with the intention to fully feature the user with the tools necessary for gaining useful insights from data analytics as well as observing detailed telemetry from Machine Learning Model output and performance.")
    st.write("The design philosphy of this application is to transform the end-to-end nature of a dashboard into a fully customizable and dynamic system capable of meeting the user's demand or desire at any time.")
    st.write("As time changes, so does data. We believe that a capable dashboard should not be locked into the perspective given to the user by the developer but instead the user should be free to update and change the way they are exploring the data as the information evolves over time.")

with tab4: 
    st.header("Recent Dev Updates:")
    st.write("3/29/26 - Restructured M-Learning Page -- XAI Section Completed")
    st.write("3/30/26 - Fixed - M-Learning Model Compatibility - Reduced Load to Cache Time")
    st.write("3/31/26 - Fixed - Interactivity Selecting Different Output Types for M-Learning Page.")
    st.write("3/31/26 - Added - Information to Model's Perf. Metrics, Feature importance & Residual Analysis")
    st.write("3/31/26 - Fixed - Metrics Value 'Blow Up'")
    st.write("4/1/26 - Added - RAG Chatbot (Course Instruction)")
    st.write("4/2/26 - Fixed - Selecting Time-Series Variable in Analytics Page")
    st.write("4/3/26 - Added - Data Overview & Methodology Page-Tabs to all Pages (not Sys Info)")
    st.write("4/3/26 - Added - View Modes to Impacts Page (Descriptive & Graphical)")
    st.write("4/3/26 - Added - Custom HTML KPI Metric Cards for Impacts Page (Descriptive View)")
    st.write("4/3/26 - Added - PVLib Simulation Framework (Implementation Coming Soon)")
    st.write("4/4/26 - Added - Tab Pages to Home Page adding SPICE Info, Dash Info, others.")
    st.write("4/5/26 - Added - Calculator & Write Pad")
    st.write("4/5/26 - Added - HTML-Rendered Descriptive Tables [Descriptive View]")
    st.write("4/5/26 - Added - HTML-Based KPI Cards")
    st.write("4/5/26 - Added - SPICE Logo to Home Page (PNG)")
    st.write("4/5/26 - Added - Import/Export Data Features to Impacts & Analytics")
    st.write("4/5/26 - Added - Comparison Format Seeing Two Datasets (Cannot Disable - Known Bug)")
    st.write("4/6/26 - Fixed - Updated Pages' Load Orders to Minimize Flickering (Engine > Graphics > Data)")
