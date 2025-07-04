import os 
import streamlit as st  
from langchain_openai import ChatOpenAI

class OpenAILLM():     
    def __init__(self, user_controls_input): 
        self.user_controls_input = user_controls_input   

    def get_llm_model(self):  
        try:
            openai_api_key = self.user_controls_input["OPENAI_API_KEY"]   
            selected_openai_model = self.user_controls_input["selected_openai_model"] 

            if openai_api_key == "": 
                st.error("⚠️ Please Enter your OpenAI API KEY to proceed!")
            
            llm = ChatOpenAI(model = selected_openai_model, api_key = openai_api_key)   
            
        except Exception as e: 
            raise ValueError(f"{e}") 
        
        return llm 

            
        
         




