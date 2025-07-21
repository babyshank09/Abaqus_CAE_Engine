import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


class DonnaAssistant:
    def __init__(self, llm):
        self.llm = llm
        self.session_key = "1"
        self._initialize_prompt()
        self._initialize_chain()

        if "store" not in st.session_state:
            st.session_state.store = {}

        if "chat_history_2" not in st.session_state:
            st.session_state.chat_history_2 = []


    def _initialize_prompt(self):
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(
                content="You are Donna, an expert in writing scripts for Abaqus Software with 20 years of experience. You are a helpful assistant."
            ),
            MessagesPlaceholder(variable_name="messages"),
        ])


    def _initialize_chain(self):
        base_chain = self.prompt | self.llm
        self.chain_with_history = RunnableWithMessageHistory(
            base_chain,
            self.get_message_history
        )


    def get_message_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in st.session_state.store:
            st.session_state.store[session_id] = ChatMessageHistory()
        return st.session_state.store[session_id]


    def render_chat_history(self):
        st.chat_message("assistant").write(
            "Hi, I'm Donna, your Abaqus Script writing Assistant. How can I help you?"
        )

        for msg in st.session_state.chat_history_2:
            if isinstance(msg, HumanMessage):
                st.chat_message("user").write(msg.content)
            elif isinstance(msg, AIMessage):
                st.chat_message("assistant").write(msg.content)


    def run(self):
        self.render_chat_history()

        user_input = st.chat_input("Enter your query here")
        if user_input:
            st.session_state.chat_history_2.append(HumanMessage(content=user_input))
            with st.spinner("Processing your request..."):
                response = self.chain_with_history.invoke(
                    {"messages": [HumanMessage(content=user_input)]},
                    config={"configurable": {"session_id": self.session_key}},
                )
                st.session_state.chat_history_2.append(AIMessage(content=response.content))
                st.chat_message("user").write(user_input)
                st.chat_message("assistant").write(response.content)



