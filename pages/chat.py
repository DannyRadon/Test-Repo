
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from helpers.data_funcs import *
from helpers.data_load import *

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
icon_impacts_info = get_base64_image("static/icon_impacts.png")
icon_ml_info = get_base64_image("static/icon_ml.png")
icon_home = get_base64_image("static/icon_home.png")
icon_analytics = get_base64_image("static/icon_analytics.png")

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
st.markdown(
    """
    <style>
    div[data-testid="stChatInput"] {
        background-color: #009cde; /* Change background color */
        border-radius: 15px;               /* Adjust corner roundness */
        border: 1px solid #cccccc;         /* Add a custom border */
        padding: 5px;                      /* Adjust internal spacing */
    }
    
    /* Optional: Style the text area inside the bar */
    div[data-testid="stChatInput"] textarea {
        color: #ffffff;                    /* Change typing text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>
[data-testid="stBottomBlockContainer"],
[data-testid="stChatInputContainer"],
section[data-testid="stChatInput"] {
    background: rgba(0,0,0,0) !important;
    box-shadow: none !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Remove default spacing */
div[data-testid="stTextInput"] {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
}

/* Style the actual input */
input {
    background: rgba(49, 112, 222, 0.4) !important;
    backdrop-filter: blur(12px);
    color: white !important;
    border-radius: 25px !important;
    padding: 15px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* Placeholder */
input::placeholder {
    color: rgba(255,255,255,0.6);
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
        <img src="data:image/png;base64,{icon_analytics}>
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
    if st.button(" ", key="analytics_info_btn"):
        st.switch_page("pages/analytics.py")

# -----------------------------------------------------------------------------
# 1. Resource Loading (Cached for Speed)
# -----------------------------------------------------------------------------
@st.cache_resource
def load_models():
    # 1. Load Embedder
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Load LLM and Tokenizer directly (skipping the broken pipeline)
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    return embedder, tokenizer, model

# Unpack the three objects
embedder, tokenizer, model = load_models()

# -----------------------------------------------------------------------------
# 2. Data Preparation
# -----------------------------------------------------------------------------

# Load and clean data (Assumes your helper functions work as intended)
df_visser, df_bissell, df_aeso = load_data()
aeso_clean = clean_fe1(df_aeso)
monthly = fe(aeso_clean)

# Generating Narrative
bissell_env_narrative = (
    "Environmental Impact Summary (Bissell):\n"
    f"Total CO2 Avoided: {df_bissell['co2_avoided'].sum():.2f} tonnes.\n"
    f"Homes Powered: {df_bissell['homes_powered'].sum():.2f}\n"
    f"Trees Saved: {df_bissell['trees_saved'].sum()}\n"
    f"Cars off the road: {df_bissell['cars_offroad'].sum()}\n"
    f"Coal Emissions Avoided: {df_bissell['coal_emission_avoided'].sum()}\n"
    f"Coal Tonnage Avoided: {df_bissell['coal_tonnage_avoided'].sum()}\n"
)

bissell_eng_narrative = (
    "Solar Site Energy Summary (Bissell):\n"
    f"Total Energy: {df_bissell['Daily Value Imputed'].sum()}\n"
    f"Average Energy: {df_bissell['Daily Value Imputed'].mean()}\n"
    f"Max Energy: {df_bissell['Daily Value Imputed'].max()}\n"
    f"Lowest Energy: {df_bissell['Daily Value Imputed'].min()}\n"
    f"Average Performance Ratio: {df_bissell['PR_Daily'].mean()}\n"
    f"Max Performance Ratio: {df_bissell['PR_Daily'].max()}\n"
    f"Lowest Performance Ratio: {df_bissell['PR_Daily'].min()}\n" 
)

visser_env_narrative = (
    "Environmental Impact Summar (New Jubilee Greenhouse):\n"
    f"Total CO2 Avoided: {df_visser['co2_avoided'].sum():.2f} tonnes.\n"
    f"Homes Powered: {df_visser['homes_powered'].sum():.2f}\n"
    f"Trees Saved: {df_visser['trees_saved'].sum()}\n"
    f"Cars off the road: {df_visser['cars_offroad'].sum()}\n"
    f"Coal Emissions Avoided: {df_visser['coal_emission_avoided'].sum()}\n"
    f"Coal Tonnage Avoided: {df_visser['coal_tonnage_avoided'].sum()}\n"   
)


visser_eng_narrative = (
    "Solar Site Energy Summary (New Jubilee Greenhouse):\n"
    f"Total Energy: {df_visser['Daily Value Imputed'].sum()}\n"
    f"Average Energy: {df_visser['Daily Value Imputed'].mean()}\n"
    f"Max Energy: {df_visser['Daily Value Imputed'].max()}\n"
    f"Lowest Energy: {df_visser['Daily Value Imputed'].min()}\n"
    f"Average Performance Ratio: {df_visser['PR_Daily'].mean()}\n"
    f"Max Performance Ratio: {df_visser['PR_Daily'].max()}\n"
    f"Lowest Performance Ratio: {df_visser['PR_Daily'].min()}\n" 
)


# Generative Narratives for the AESO Dataset ---------------

aeso_market_narrative = (
    "AESO Market Summaries (Alberta Energy)"
    f"Average Pool Price: {monthly['pool_price'].mean()}\n"
    f"Highest Pool Price: {monthly['pool_price'].max()}\n"
    f"Lowest Pool Price {monthly['pool_price'].min()}\n"
    f"Max Market Share: {monthly['solar_market_share'].max()}\n"
    f"Average Market Share: {monthly['solar_market_share'].mean}\n"
    
)

aeso_energy_narrative = (
    "AESO Energy Summaries (Alberta Energy)"
    f"Max Generation per Capacity: {monthly['solar_generation_per_capacity'].max()}"
    f"Average Generation per Capacity: {monthly['solar_generation_per_capacity'].mean()}"
    
)


documents = {"bissell_env": bissell_env_narrative,
             "greenhouse_env": visser_env_narrative,
             "bissel_eng": bissell_eng_narrative,
             "greenhouse_eng": visser_eng_narrative,
             "aeso_market":aeso_market_narrative,
             "aeso_energy":aeso_energy_narrative}

@st.cache_data
def compute_embeddings(docs):
    return {k: embedder.encode(v, convert_to_tensor=True) for k, v in docs.items()}

doc_embeddings = compute_embeddings(documents)

# -----------------------------------------------------------------------------
# 3. RAG Logic
# -----------------------------------------------------------------------------

def retrieve_context(query, top_k=1):
    q_emb = embedder.encode(query, convert_to_tensor=True)
    scores = {doc_id: util.pytorch_cos_sim(q_emb, emb).item() for doc_id, emb in doc_embeddings.items()}
    top_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return "\n\n".join(documents[doc_id] for doc_id, _ in top_docs)

def query_llm(query, context):
    prompt = f"Context: {context}\n\nQuestion: {query}"
    
    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate the answer
    outputs = model.generate(
        **inputs, 
        max_new_tokens=150, 
        do_sample=False  # Keep it deterministic for data summaries
    )
    
    # Decode only the generated part
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
# -----------------------------------------------------------------------------
# 4. Streamlit Chat Interface
# -----------------------------------------------------------------------------

st.title("📊 Energy Dashboard RAG Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.text_input("", placeholder="Ask me about the data...", key="chat_input"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            context = retrieve_context(prompt)
            response = query_llm(prompt, context)
            st.markdown(response)
            
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# ------------------------ Dashboard Page Building Section ---------------------

