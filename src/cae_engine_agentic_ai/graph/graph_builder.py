from langgraph.graph import StateGraph, START, END  
from langgraph.prebuilt import tools_condition, ToolNode
from src.cae_engine_agentic_ai.state.state import State 
from src.cae_engine_agentic_ai.node.cae_task_nodes import CAETaskNode  
from src.cae_engine_agentic_ai.tools.tools import Tools


class GraphBuilder: 

    def __init__(self, model_with_tools): 
        self.llm_with_tools =  model_with_tools 
        self.graph_builder= StateGraph(State)   
        self.tools = [Tools.generate_inp_scripts, Tools.cad_to_mesh_assembly, Tools.cad_to_mesh, Tools.analyse_all_parts]


    def build_cae_engine_graph(self): 
        node_obj = CAETaskNode(model_with_tools = self.llm_with_tools)  
        self.graph_builder.add_node("assistant", node_obj.assistant_node)  
        self.graph_builder.add_node("tools", ToolNode(self.tools)) 
        
        self.graph_builder.add_edge(START, "assistant") 
        self.graph_builder.add_conditional_edges("assistant", tools_condition) 
        self.graph_builder.add_edge("tools", "assistant")   
    

    def setup_graph(self, usecase):  
        if usecase == "Execute Abaqus CAE Tasks":  
            self.build_cae_engine_graph()  
        
        return self.graph_builder.compile() 
    









