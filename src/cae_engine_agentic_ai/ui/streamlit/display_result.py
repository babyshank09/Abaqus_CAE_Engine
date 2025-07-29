import json 
import streamlit as st  
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage  
from src.cae_engine_agentic_ai.state.state import State 
from src.cae_engine_agentic_ai.tasks.tasks import Tasks


class DisplayResultStreamlit:
    def __init__(self, usecase, working_dir):
        self.usecase = usecase   
        self.working_dir = working_dir
        self.tasks = Tasks(working_dir = self.working_dir)    



    def display_intro_message(self, llm_with_tools):  
        self.llm_with_tools = llm_with_tools 
        content = """ 
        Your name is Jarvis. You are a helpful assistant tasked with performing Abaqus Software related tasks. 
        The user will give you the input from their side. Check if the user input is enough to execute the tasks.
        If their input is not sufficient, ask for the missing inputs that are required and then execute the task.
        """
        sys_msg = SystemMessage(content= content)
        intro = self.llm_with_tools.invoke([sys_msg] + [HumanMessage(content="Who are you and what all can you do to help me? List what all you can do individually")])  
        st.session_state["chat_history"].append(AIMessage(content= intro.content)) 
        st.chat_message("assistant").write(st.session_state["chat_history"][0].content)   


    
    def display_chat_history(self):  
        a= type(HumanMessage(content="hi")) 
        b= type(AIMessage(content="hi there"))
        for msg in st.session_state["chat_history"]: 
            if type(msg)==a:  
                st.chat_message("user").write(msg.content) 
            if type(msg)==b and msg.content is not '':  
                st.chat_message("assistant").write(msg.content)  



    def display_result(self, graph, user_message):  
        self.graph = graph 
        self.user_message = user_message 
        
        if self.usecase == "Execute Abaqus CAE Tasks": 
            st.chat_message("user").write(self.user_message) 
            st.session_state["chat_history"].append(HumanMessage(content= self.user_message)) 

            response = self.graph.invoke({"messages": st.session_state.chat_history})  
            st.session_state.response = response
    
            parsed_response = response["messages"][-1].content 
            st.session_state.chat_history.append(AIMessage(parsed_response))
            st.chat_message("assistant").write(st.session_state.chat_history[-1].content)  
        

    

    def execute_tasks(self):
        if "generate_inp_scripts" in st.session_state.response["tool_called"]:    

            st.header("Input File Generator 📄⚙️")
            results = self.tasks.ask_inp_file_inputs()   

            if st.button("Submit Values"): 
                with st.spinner("Processing your request..."): 
                    self.tasks.generate_inp_scripts_task( 
                        inp_file_location = results["inp_file_path"],
                        start_angle = results["start_angle"],
                        final_angle = results["final_angle"],
                        step_size = results["step_size"],
                        model_name = results["model_name"],
                        instance_list = results["instance_list"],
                        axis_point = results["axis_point"],
                        axis_direction = results["axis_direction"],
                        drop_axis = results["drop_axis"],
                        floor_instance_name = results["floor_instance_name"]  
                    ) 
                    
                    st.success("successfully executed")


        elif "cad_to_mesh_assembly" in st.session_state.response["tool_called"]:  

            st.header("Assembly Mesh Builder 🛠️")
            results = self.tasks.ask_cad2mesh_assembly_inputs() 

            if st.button("Submit Values"):
                with st.spinner("Processing your request..."): 
                    self.tasks.cad_to_mesh_assembly_task( 
                        step_file_path = results["stp_file_path"],
                        model_name = results["model_name"],
                        mesh_size = results["mesh_size"],
                        element_type = results["element_type"]
                    ) 
                    
                    st.success("successfully executed")

                
        elif "cad_to_mesh" in st.session_state.response["tool_called"]: 

            st.header("Part Mesh Builder 🛠️")
            results = self.tasks.ask_cad2mesh_inputs() 

            if st.button("Submit Values"):
                with st.spinner("Processing your request..."): 
                    self.tasks.cad_to_mesh_task( 
                        step_file_path = results["stp_file_path"],
                        model_name = results["model_name"],
                        part_name = results["part_name"],
                        mesh_size = results["mesh_size"],
                        element_type = results["element_type"]
                    ) 
                    
                    st.success("successfully executed")  


        elif "analyse_all_parts" in st.session_state.response["tool_called"]: 

            st.header("All Parts and Elsets Analyser 🔍")
            results = self.tasks.ask_analyse_all_parts_inputs()  

            if st.button("Submit Values"):
                with st.spinner("Processing your request..."): 
                    self.tasks.analyse_all_parts_task( 
                        odb_path = results["odb_file_path"],
                        max_stress_limit = results["max_stress_limit"],
                        min_stress_limit = results["min_stress_limit"]
                        ) 
                    
                    st.success("successfully executed")   


        elif "analyse_single_part" in st.session_state.response["tool_called"]: 

            header = st.header("Single Part and Elset Analyser 🔍")  
            results = self.tasks.ask_analyse_single_part_inputs()  

            if st.button("Submit Values"):
                with st.spinner("Processing your request..."): 
                    self.tasks.analyse_single_part_task( 
                        odb_path = results["odb_file_path"], 
                        instance_name = results["instance_name"],
                        elset_name = results["elset_name"],
                        max_stress_limit = results["max_stress_limit"],
                        min_stress_limit = results["min_stress_limit"]
                        ) 
                    
                    st.success("successfully executed")   
                    
        
        else: 
            return 

    