# Import Pool
import streamlit as st              # Importing StreamLit Dashboard Module as 'st'

from helpers.data_load import *     # Importing Data Loaders from Helpers File
from helpers.data_funcs import *    # Importing Helper Functions for Dashboard 


# Initializing the Data into Dashboard
df_visser, df_bissell = load_data()     # Loading the datasets


# ---------------------------------------------
st.title("SPICE Dashboard Home Page")
st.divider()

# // Insert Code here for putting in the company logo for side-bar



# Testing Input Columns -- Used for KPI Style Metric Outputs

col1, col2, col3, col4 = st.columns(4)
st.divider()

with col1:
    total_hours_visser = total_load_hours(df_visser, 14.2)
    total_hours_bissell = total_load_hours(df_bissell, 30.7)

    st.subheader("Total Load Hours")
    st.metric("New Jubilee", f"{total_hours_visser:,.0f}")
    st.metric("Bissell Thrift Shop", f"{total_hours_bissell:,.0f}")

with col2:

    total_yield = df_visser['Total Yield (kWh)'].mean()
    st.metric("Total Yield", f"{total_yield:,.0f}")


with col3:
    total_gen = df_visser['Daily Value Imputed'].sum()
    st.metric("Total Generation (kWh)", f"{total_gen:,.0f}")

with col4:
    co2_avoided = eco_impacts(df_visser, 'co2_avoided')
    st.metric("CO2 Emissions Avoided (Tonnes)", f"{co2_avoided:,.0f}")



# Building the Home Page ---------------------------------------------------------------------------------------------------


df_select = st.radio("Select Solar Site:", ['Bissell Thrift Shop', 'New Jubilee Greenhouse'])

st.header("System Information")

# Hard-Coding Stuff for Bissell Thrift Shop
if df_select == 'Bissell Thrift Shop':
    sys_size = 30.7
    total_gen = total_generated(df_bissell).round()
    total_hours = total_hours_bissell.round()
    df = df_bissell

    tab_1, tab_2, tab_3, tab_4 = st.tabs(["General Overview", "Technical Specs", "Financial Info", "Location & Contact Info"])

    # This is for the 'General Overview' Tab on the Home Page
    with tab_1:

        info_col_1, info_col_2, info_col_3 = st.columns(3)

        with info_col_1:
            st.metric("System Size (kW):", sys_size)
            st.metric("Status:", "Active")
            
        with info_col_2:
            st.metric("Total Load Hours:", total_hours)
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
    sys_size = 14.2
    total_gen = total_generated(df_visser).round()
    total_hours = total_hours_visser.round()
    df = df_visser

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




# NEXT SECTION OF HOME PAGE AFTER SYS-INFO  ------------------------------------------------------------
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
tab_1, tab_2 = st.tabs(['Sheet Data', 'Graph Data'])

if range_select == 'Daily':
    with tab_1:
        if year_select:
            
            st.dataframe(df_filtered[['time', 'Daily Value Imputed']])

        else:    
            st.dataframe(df[['time', 'Daily Value Imputed']])
    
    with tab_2:
        if year_select:
            st.bar_chart(df_filtered['Daily Value Imputed'])

        else:
            df['time'] = pd.to_datetime(df['time'])
            df = df.set_index('time')

            st.bar_chart(df['Daily Value Imputed'])
    

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
