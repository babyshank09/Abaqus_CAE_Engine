import os 
import streamlit as st  
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from src.cae_engine_agentic_ai.tools.tools import Tools 
from azure.identity import DefaultAzureCredential  
from langchain_ollama import ChatOllama

class OpenAILLM():     
    def __init__(self, user_controls_input): 
        self.user_controls_input = user_controls_input     
        self.tools = [
            Tools.cad_to_inp, 
            Tools.assign_material_properties, 
            Tools.analyse_single_part, 
            Tools.analyse_all_parts, 
            Tools.cad_to_mesh,
            Tools.cad_to_mesh_assembly, 
            Tools.generate_inp_scripts
        ]


    def get_llm_model(self):  
        try:
            openai_api_key = self.user_controls_input["OPENAI_API_KEY"]   
            selected_openai_model = self.user_controls_input["selected_openai_model"] 

            if openai_api_key == "": 
                st.error("⚠️ Please Enter your OpenAI API KEY to proceed!") 
                return 
            
            llm = ChatOpenAI(model = selected_openai_model, api_key = openai_api_key)    

            # Initialize the local model
            # llm = ChatOllama(model="phi4-mini:3.8b")  
            
        except Exception as e: 
            raise ValueError(f"{e}") 
        
        return llm 


    def get_llm_with_tools(self): 
        try:   
            llm = self.get_llm_model()  
            llm_with_tools = llm.bind_tools(self.tools) # parallel_tool_calls=False

            return llm_with_tools

        except Exception as e: 
            raise ValueError(f"{e}") 




            
        
         




