import streamlit as st 
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage 
from src.cae_engine_agentic_ai.ui.uiconfigfile import Config  
import os  
import dotenv 
from dotenv import load_dotenv 


class LoadStreamlitUI: 
    def __init__(self): 
        self.config = Config() 
        self.user_controls = {}    



    def load_ui(self): 
        st.set_page_config(page_title = self.config.get_title(), page_icon = self.config.get_icon()) 
        st.title(self.config.get_icon() + " " + self.config.get_title())   

        with st.sidebar:    
            st.title("Settings") 

            usecase_options = self.config.get_usecase_options() 
            self.user_controls["selected_usecase"] = st.selectbox("Select Use Case", usecase_options)   

            self.user_controls["working_dir"] = st.text_input("Working Directory", value = r"") 
            
            llm_options = self.config.get_llm_options()  
            #self.user_controls["selected_llm"] = st.selectbox("Select LLM Service Provider", llm_options)
            self.user_controls["selected_llm"] = "OpenAI"  
            

            if self.user_controls["selected_llm"] == "OpenAI":  
                openai_model_options = self.config.get_openai_model_options() 
                self.user_controls["selected_openai_model"] = st.selectbox("Select OpenAI Model", openai_model_options) 
                self.user_controls["OPENAI_API_KEY"] = st.text_input("OpenAI API Key",value ="", type="password") 
             

                if not self.user_controls["OPENAI_API_KEY"]:
                     st.warning("⚠️ Please enter your OpenAI API key to proceed!")  

            clear_session = st.button("Clear Session") 

            if "chat_history" not in st.session_state or clear_session: 
                st.session_state["chat_history"] = [] 
                st.session_state["chat_ui_history"] = [] 
                st.session_state["tools_called"] = []   
                st.session_state.current_tool = "" 
                st.session_state.chat_history_2 = []
                st.session_state["intro_message_count"] = 0
                st.session_state["response"] = {"messages": [], "tool_called": []}  
       
        return self.user_controls
                
            


            









            




