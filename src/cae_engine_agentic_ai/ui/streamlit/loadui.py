import streamlit as st 
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage 
from src.cae_engine_agentic_ai.ui.uiconfigfile import Config 


class LoadStreamlitUI: 
    def __init__(self): 
        self.config = Config() 
        self.user_controls = {}  


    def load_ui(self): 
        st.set_page_config(page_title = self.config.get_title(), page_icon = self.config.get_icon()) 
        st.header(self.config.get_title())   
        st.chat_message("assistant").write("Hi, How can I assist you today?") 

        with st.sidebar:    
            st.title("Settings") 

            usecase_options = self.config.get_usecase_options() 
            self.user_controls["selected_usecase"] = st.selectbox("Select Use Case", usecase_options)   

            self.user_controls["working_dir"] = st.text_input("Working Directory") 
            
            llm_options = self.config.get_llm_options()  
            self.user_controls["selected_llm"] = st.selectbox("Select LLM Service Provider", llm_options)  

            if self.user_controls["selected_llm"] == "OpenAI":  
                openai_model_options = self.config.get_openai_model_options() 
                self.user_controls["selected_openai_model"] = st.selectbox("Select OpenAI Model", openai_model_options)  

                self.user_controls["OPENAI_API_KEY"] = st.text_input("OpenAI API Key", type="password") 
                if not self.user_controls["OPENAI_API_KEY"]:
                    st.warning("⚠️ Please enter your Groq API key to proceed!")   

            if st.button("Clear Session"): 
                st.write("Session Cleared")

        return self.user_controls
                
            


            









            


