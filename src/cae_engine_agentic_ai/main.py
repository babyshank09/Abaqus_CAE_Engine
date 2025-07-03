import os 
from src.cae_engine_agentic_ai.ui.streamlit.loadui import LoadStreamlitUI   
import streamlit as st

def load_cae_engine(): 
    load_streamlit_ui = LoadStreamlitUI() 
    user_controls = load_streamlit_ui.load_ui()       

    user_message = st.chat_input("Enter your query here")  


