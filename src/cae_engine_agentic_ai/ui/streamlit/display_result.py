import json 
import streamlit as st  
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage  
from src.langgraphagenticai.state.state import State


class DisplayResultStreamlit:
    def __init__(self, graph, user_message, usecase): 
        self.graph = graph 
        self.user_message = user_message 
        self.usecase = usecase    