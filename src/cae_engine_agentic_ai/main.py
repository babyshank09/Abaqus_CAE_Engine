import os 
import streamlit as st 
from src.cae_engine_agentic_ai.ui.streamlit.loadui import LoadStreamlitUI   
from src.cae_engine_agentic_ai.LLMs.openai_llm import OpenAILLM 
from src.cae_engine_agentic_ai.graph.graph_builder import GraphBuilder 
from src.cae_engine_agentic_ai.ui.streamlit.display_result import DisplayResultStreamlit

def load_cae_engine():  
    load_streamlit_ui = LoadStreamlitUI()   
    user_controls = load_streamlit_ui.load_ui()  
      
    if user_controls["OPENAI_API_KEY"] and user_controls["working_dir"] :
        try:
            openai_llm_obj = OpenAILLM(user_controls_input = user_controls)  
            model = openai_llm_obj.get_llm_model()   
            if not model:  
                st.error("LLM could not be initialized")   
                return    
            
            model_with_tools = openai_llm_obj.get_llm_with_tools() 
            if not model_with_tools: 
                st.error("Tools could not be binded to the LLM")

            usecase = user_controls["selected_usecase"] 
            if not usecase: 
                st.error("Usecase is not selected")
                return 

            display_obj = DisplayResultStreamlit(usecase) 
            if st.session_state["intro_message_count"] == 0:
                display_obj.display_intro_message(llm_with_tools = model_with_tools) 
                st.session_state["intro_message_count"] = 1



            user_message = st.chat_input("Enter your query here")   
            if user_message:       
                try: 
                    graph_builder = GraphBuilder(model_with_tools = model_with_tools)  
                    graph = graph_builder.setup_graph(usecase = usecase)   
                except Exception as e: 
                    raise e 
                    return   
                
                display_obj.display_result(graph = graph, user_message = user_message) 
                

                

        except Exception as e:  
            raise e



    

            
            


                

        except Exception as e: 
            raise ValueError(f"{e}")

            



