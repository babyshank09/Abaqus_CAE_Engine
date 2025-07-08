import json 
import streamlit as st  
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage  
from src.cae_engine_agentic_ai.state.state import State


class DisplayResultStreamlit:
    def __init__(self, usecase):
        self.usecase = usecase     


    def display_intro_message(self, llm_with_tools):  
        self.llm_with_tools = llm_with_tools
        intro = self.llm_with_tools.invoke([HumanMessage(content="Who are you and what all can you do to help me?")])  
        st.session_state["chat_history"].append(AIMessage(content= intro.content)) 
        st.chat_message("assistant").write(st.session_state["chat_history"][0].content)  


    def display_result(self, graph, user_message):  
        self.graph = graph 
        self.user_message = user_message 

        a= type(HumanMessage(content="hi")) 
        b= type(AIMessage(content="hi there"))
        for msg in st.session_state["chat_history"]: 
            if type(msg)==a:  
                st.chat_message("user").write(msg.content) 
            if type(msg)==b and msg.content is not '':  
                st.chat_message("assistant").write(msg.content)  

        if self.usecase == "Execute Abaqus CAE Tasks": 
            st.chat_message("user").write(self.user_message) 
            st.session_state["chat_history"].append(HumanMessage(content= self.user_message)) 
            #st.write(st.session_state.chat_history)
            answer = self.graph.invoke({"messages": st.session_state.chat_history})
            st.chat_message("assistant").write(answer["messages"][-1].content)
            st.session_state["chat_history"].append(AIMessage(content=answer["messages"][-1].content)) 

    