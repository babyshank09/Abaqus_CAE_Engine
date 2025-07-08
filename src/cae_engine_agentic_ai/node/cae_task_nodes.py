from src.cae_engine_agentic_ai.state.state import State
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage         


class CAETaskNode: 
    def __init__(self, model_with_tools): 
        self.llm_with_tools = model_with_tools  

    def assistant_node(self, state:State)-> dict: 
        content = """ 
        Your name is Jarvis. You are a helpful assistant tasked with performing Abaqus Software related tasks. 
        The user will give you the input from their side.Check if the user input is enough to execute the tasks. 
        If their input is not sufficient, ask for the missing inputs that are required and then execute the task.
        """   
        
        sys_msg = SystemMessage(content = content)  
        msg = self.llm_with_tools.invoke([sys_msg] + state["messages"]) 

        tool_flag =False
        if "tool_calls" in msg.additional_kwargs: 
            tool_flag=True
            tool_calls = msg.additional_kwargs["tool_calls"]
            for call in tool_calls:
                function_name = call["function"]["name"]
                print("Tool function name:", function_name)
        
        updated_tool_called = state.get("tool_called", []).copy()
        if tool_flag:
            updated_tool_called.append(function_name)
            return {"messages": [msg], "tool_called": updated_tool_called}   

        else:  
            print(updated_tool_called)
            return {"messages": [msg], "tool_called": updated_tool_called}   











