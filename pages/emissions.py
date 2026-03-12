# TESTING FILE FOR STREAMLIT NAVIGATION SIDE-PANEL

import streamlit as st
import matplotlib.pyplot as plt

from helpers.data_load import *

# Initializing the Data into Dashboard
df_visser, df_bissell = load_data()     # Loading the datasets

st.write("TESTING FROM THE EMISSIONS PAGE")

impact_columns = ['coal_emission_avoided', 'homes_powered', 'cars_offroad']

# Sum up each impact over the dataset to get total contribution
impact_totals = df_visser[impact_columns].sum()

# Pie chart
plt.figure(figsize=(4,4))
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']  # you can pick more colors if needed
plt.pie(impact_totals, labels=impact_totals.index, autopct='%1.1f%%', startangle=140, colors=colors, shadow=True)
plt.title("Environmental Impact Contribution")
# Display in Streamlit
st.pyplot(plt)