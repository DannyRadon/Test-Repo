import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from helpers.data_funcs import *
from helpers.data_load import *

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
# Generating Narrative
bissell_env_narrative = (
    "Environmental Impact Summary (Bissell):\n"
    f"Total CO2 Avoided: {df_bissell['co2_avoided'].sum():.2f} tonnes.\n"
    f"Homes Powered: {df_bissell['homes_powered'].sum():.2f}\n"
    f"Trees Saved: {df_bissell['trees_saved'].sum()}\n"
    f"Cars off the road: {df_bissell['cars_offroad'].sum()}"
    f"Coal Emissions Avoided: {df_bissell['coal_emission_avoided'].sum()}"
    f"Coal Tonnage Avoided: {df_bissell['coal_tonnage_avoided'].sum()}"
)


visser_env_narrative = (
    "Environmental Impact Summar (New Jubilee Greenhouse):\n"
    f"Total CO2 Avoided: {df_visser['co2_avoided'].sum():.2f} tonnes.\n"
    f"Homes Powered: {df_visser['homes_powered'].sum():.2f}\n"
    f"Trees Saved: {df_visser['trees_saved'].sum()}\n"
    f"Cars off the road: {df_visser['cars_offroad'].sum()}"
    f"Coal Emissions Avoided: {df_visser['coal_emission_avoided'].sum()}"
    f"Coal Tonnage Avoided: {df_visser['coal_tonnage_avoided'].sum()}"   
)

documents = {"bissell_env": bissell_env_narrative,
             "greenhouse_env": visser_env_narrative
}

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
if prompt := st.chat_input("Ask me about the environmental data..."):
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

