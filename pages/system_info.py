import streamlit as st

# This CSS creates the Gradient Background -- The Main Background
st.markdown("""
<style>
.stApp {
    /* Linear gradient example: top-left blue to bottom-right purple */
    background: linear-gradient(135deg, #2257d6 25%, #3b77bc 50%, #009cde 66%, #d0d0d0 100%);
}
</style>
""", unsafe_allow_html=True)

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


import pandas as pd

from helpers.data_funcs import *
from helpers.data_load import *

st.title("System Information")
st.divider()

df_visser, df_bissell, df_aeso = load_data()

# ------------------------------------ CSS & HTML GRAPHICAL SETUP AREA ---------------------------------------------------------------


# Loading in the Icons
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
        <img src="data:image/png;base64,{icon_home}">
        <div class="card-text">Home</div>
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



# ------------------------------------------------ CODE & DATA AREA -------------------------------------------------------------------


# Clickable-Icon Navigation Area -- Routing to Other Pages -- this is what allows interactivity 

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button(" ", key="home_btn"):
        st.switch_page("home.py")

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

st.divider()

# DataFrame Selection for Solar Site
df_select = st.radio("Select Solar Site:", ['Bissell Thrift Shop', 'New Jubilee Greenhouse', 'Idylwylde Community League', 'St. Augustine Anglican Church'])



# Hard-Coding Stuff for Bissell Thrift Shop
if df_select == 'Bissell Thrift Shop':

    df = df_bissell
    sys_size = 30.7
    total_gen = total_generated(df_bissell).round()
    total_load_hours = total_load_hours(df, sys_size)
    
    tab_1, tab_2, tab_3, tab_4 = st.tabs(["General Overview", "Technical Specs", "Financial Info", "Location & Contact Info"])

    # This is for the 'General Overview' Tab on the Home Page
    with tab_1:

        info_col_1, info_col_2, info_col_3 = st.columns(3)

        with info_col_1:
            st.metric("Status:", "Active")

        with info_col_2:
            st.metric("Total Load Hours:", total_load_hours)
            st.metric("Comp. Date:", "Oct-2023")
        
        with info_col_3:
            st.metric("Total Energy Made (kWh):", total_gen)
            st.metric("Cost/kW Installed ($)", 2079.29)

    
    # This is for the 'Technical Specs' Tab on the Home Page
    with tab_2:

        info_col_1, info_col_2, info_col_3, info_col_4 = st.columns(4)

        with info_col_1:
            st.metric("System Size (kW):", sys_size)
            st.metric("Total A/C Cap (kW):", 30)
            st.metric("Total D/C Cap (kW)", 30.7)
            st.metric("Perf. Warranty:", "30-Year")
    
        with info_col_2:

            st.metric("Modules: (Jinko - 66x)", "465W")
            st.metric("Type:", "MonoCryst")
            st.metric("Prod. Warranty:", "12-Year")
        
            
        with info_col_3:

            st.metric("Inverters (Fronius 3x)", '208-240')
            st.metric("Inv. Warranty:", "10-Year")
        

    # This is for the Financial Info Tab in the Home page
    with tab_3:

        info_col_1, info_col_2, info_col_3, info_col_4 = st.columns(4)

        with info_col_1:

            st.metric("Total Cost ($):", 63650)
            st.metric("Downpayment ($):", 31825)
            st.metric("Investment ($):", 33500)
        
        with info_col_2:

            st.metric("Model:", "Class-B")
            st.metric("Tax:", "GST-5%")
        
        with info_col_3:
            st.metric("Lease:", "11-Year")
            st.metric("Annual. Pay ($):", 4480)
            st.metric("Int. Rate:", "6.7%")
    
    with tab_4:

        info_col_1, info_col_2 = st.columns(2)

        with info_col_1:
            st.subheader("Address")
            st.write("8818 118 Ave NW, Edmonton")
        
        with info_col_2:
            st.subheader("Contact Info")
            st.write("PLEASE ENTER CONTACT INFO HERE")
    
# Coding the Home Page for New Jubilee (Visser)
elif df_select == 'New Jubilee Greenhouse':

    df = df_visser
    sys_size = 14.2
    total_gen = total_generated(df_visser).round()
    total_hours = total_load_hours(df, sys_size).round()
    

    tab_1, tab_2, tab_3, tab_4 = st.tabs(["General Overview", "Technical Specs", "Financial Info", "Location & Contact Info"])

    # This is for the 'General Overview' Tab on the Home Page
    with tab_1:

        info_col_1, info_col_2, info_col_3 = st.columns(3)

        with info_col_1:
            st.metric("System Size (kW):", sys_size)
            st.metric("Status:", "Active")
            
        with info_col_2:
            st.metric("Total Load Hours:", total_hours)
            st.metric("Comp. Date:", "Nov-2024")
        
        with info_col_3:
            st.metric("Total Energy Made (kWh):", total_gen)
            st.metric("Cost/kW Installed ($)", 3163.15)

    
    # This is for the 'Technical Specs' Tab on the Home Page
    with tab_2:

        info_col_1, info_col_2, info_col_3, info_col_4 = st.columns(4)

        with info_col_1:
            st.metric("System Size (kW):", sys_size)
            st.metric("Total A/C Cap (kW):", 10)
            st.metric("Total D/C Cap (kW)", 14.2)
            st.metric("Perf. Warranty:", "27-Year")
    
        with info_col_2:

            st.metric("Modules: (Saat - 32x)", "445W")
            st.metric("Type:", "N/A")
            st.metric("Prod. Warranty:", "12-Year")
        
            
        with info_col_3:

            st.metric("Inverters (Solis - 1x)", '10K-String')
            st.metric("Inv. Warranty:", "10-Year Limited")
        

    # This is for the Financial Info Tab in the Home page
    with tab_3:

        info_col_1, info_col_2, info_col_3, info_col_4 = st.columns(4)

        with info_col_1:

            st.metric("Total Cost ($):", 44916.67)
            st.metric("Downpayment ($):", 0.00)
            st.metric("Investment ($):", 0.00)
        
        with info_col_2:

            st.metric("Model:", "Direct")
            st.metric("Tax:", "GST-5%")
        
        with info_col_3:
            st.metric("Lease:", "None")
            st.metric("Annual. Pay ($):", 0)
            st.metric("Int. Rate:", "None")
    
    with tab_4:

        info_col_1, info_col_2 = st.columns(2)

        with info_col_1:
            st.subheader("Address")
            st.write("20303 33 St NE, Edmonton")
        
        with info_col_2:
            st.subheader("Contact Info")
            st.write("PLEASE ENTER CONTACT INFO HERE")





elif df_select == "Idylwylde Community League":
    
    sys_size = 12.43
      
    tab_1, tab_2, tab_3, tab_4 = st.tabs(["General Overview", "Technical Specs", "Financial Info", "Location & Contact Info"])

    # This is for the 'General Overview' Tab on the Home Page
    with tab_1:

        info_col_1, info_col_2, info_col_3 = st.columns(3)

        with info_col_1:
            st.metric("Status:", "Active")
            st.metric("System Size:", sys_size)
    


        with info_col_2:
            st.metric("Comp. Date:", "Nov-2025")
            
        with info_col_3:
            st.metric("Cost/kW Installed ($)", 1377.58)
    
        
        # This is for the 'Technical Specs' Tab on the Home Page
        with tab_2:
    
            info_col_1, info_col_2, info_col_3, info_col_4 = st.columns(4)
    
            with info_col_1:
                st.metric("System Size (kW):", sys_size)
                st.metric("Total A/C Cap (kW):", 12.43)
                st.metric("Total D/C Cap (kW)", 16.6)
                st.write("Perf. Warranty:", "27-Year")
        
            with info_col_2:
    
                st.metric("Modules: 27x Thornova", "615W")
                st.metric("Type:", "Bi-Facial")
                st.metric("Prod. Warranty:", "12 Years")
            
                
            with info_col_3:
                st.write("Inverters: 14x APSystems DS3 Micro")

            
    
        # This is for the Financial Info Tab in the Home page
        with tab_3:
    
            info_col_1, info_col_2, info_col_3, info_col_4 = st.columns(4)
    
            with info_col_1:
    
                st.metric("Total Cost ($):", 17123.33)
                st.metric("Downpayment ($):", 17000)
                st.metric("Investment ($):", 18000)
            
            with info_col_2:
    
                st.metric("Model:", "Class-B")
                st.metric("Tax:", "GST-5%")
            
            with info_col_3:
                st.metric("Lease:", "5 Years")
                st.metric("Annual. Pay ($):", 3924.96)
                st.metric("Monthly Pay ($):", 327.08)
                st.metric("Int. Rate (%):", 5.5)
        
        with tab_4:
    
            info_col_1, info_col_2 = st.columns(2)
    
            with info_col_1:
                st.subheader("Address")
                st.write("8631 81 St NW, Edmonton")
            
            with info_col_2:
                st.subheader("Contact Info")
                st.write("PLEASE ENTER CONTACT INFO HERE")


elif df_select == "St. Augustine Anglican Church":
    
    sys_size = 19
      
    tab_1, tab_2, tab_3, tab_4 = st.tabs(["General Overview", "Technical Specs", "Financial Info", "Location & Contact Info"])

    # This is for the 'General Overview' Tab on the Home Page
    with tab_1:

        info_col_1, info_col_2, info_col_3 = st.columns(3)

        with info_col_1:
            st.metric("System Size:", sys_size)
            st.metric("Status:", "Active")    


        with info_col_2:
            st.metric("Comp. Date:", "Jan-2026")
            
        with info_col_3:
            st.metric("Cost/kW Installed ($)", 3525.23)
    
        
        # This is for the 'Technical Specs' Tab on the Home Page
        with tab_2:
    
            info_col_1, info_col_2, info_col_3, info_col_4 = st.columns(4)
    
            with info_col_1:
                st.metric("System Size (kW):", sys_size)
                st.metric("Total A/C Cap (kW):", 19)
                st.metric("Total D/C Cap (kW)", 25.215)
                st.metric("Perf. Warranty:", "25-Year")
        
            with info_col_2:
    
                st.metric("Modules: 41x Longi", "615W")
                st.metric("Type:", "N/A")
                st.metric("Prod. Warranty:", "12 Years")
            
                
            with info_col_3:
                st.write("Inverters: SolarEdge 11.4kW + 7.6kW")
                

            
    
        # This is for the Financial Info Tab in the Home page
        with tab_3:
    
            info_col_1, info_col_2, info_col_3, info_col_4 = st.columns(4)
    
            with info_col_1:
    
                st.metric("Total Cost ($):", 66979.44)
                st.metric("Downpayment ($):", 0)
                st.metric("Investment ($):", 0)
            
            with info_col_2:
    
                st.metric("Model:", "Diocese (Internal Financing)")
                st.metric("Tax:", "GST-5%")
            
            with info_col_3:
                st.metric("Lease:", "N/A")
        
        with tab_4:
    
            info_col_1, info_col_2 = st.columns(2)
    
            with info_col_1:
                st.subheader("Address")
                st.write("6110 Fulton Rd NW, Edmonton")
            
            with info_col_2:
                st.subheader("Contact Info")
                st.write("PLEASE ENTER CONTACT INFO HERE")
