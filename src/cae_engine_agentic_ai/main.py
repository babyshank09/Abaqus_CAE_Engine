import os 
import streamlit as st
from src.cae_engine_agentic_ai.ui.streamlit.loadui import LoadStreamlitUI   
from src.cae_engine_agentic_ai.LLMs.openai_llm import OpenAILLM

def load_cae_engine(): 
    load_streamlit_ui = LoadStreamlitUI() 
    user_controls = load_streamlit_ui.load_ui()       
    
    user_message = st.chat_input("Enter your query here")   

    if user_message: 
        try: 
            openai_llm_obj = OpenAILLM(user_controls_input = user_controls)  
            llm = openai_llm_obj.get_llm_model()  
            



        except Exception as e: 
            raise ValueError(f"e")

            



