import json 
import streamlit as st  
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage  
from src.cae_engine_agentic_ai.state.state import State 
from src.cae_engine_agentic_ai.tasks.tasks import Tasks 
import os 
import pandas as pd 

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
            if type(msg)==b and msg.content != '':  
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
            if st.session_state.get("current_tool") != "cad_to_mesh_assembly":
                st.session_state.current_tool = "cad_to_mesh_assembly"
                st.session_state.part_names = [] 
                st.session_state.part_images = {} 
                st.session_state.step_file_path = "" 
                st.session_state.model_name = ""

            st.header("Assembly Mesh Builder 🛠️")
            results = self.tasks.ask_cad2mesh_assembly_inputs()  

            if st.button("Open Mesh Builder"):
                part_names, part_images = self.tasks.extract_part_names_and_images(
                    model_file_path= results["stp_file_path"],
                    model_name = results["model_name"]
                )  
                st.session_state.part_names = part_names
                st.session_state.part_images = part_images
            
            mesh_info = self.tasks.ask_partwise_mesh_inputs(
                part_names = st.session_state.part_names,
                part_images = st.session_state.part_images
            )

            if st.button("Mesh Parts"):
                with st.spinner("Processing your request..."): 
                    self.tasks.cad_to_mesh_assembly_task( 
                        step_file_path = results["stp_file_path"],
                        model_name = results["model_name"],
                        mesh_info_path= mesh_info
                    )  
                st.session_state.part_names = [] 
                st.session_state.part_images = {} 
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

            if st.session_state.get("current_tool") != "analyse_all_parts":
                st.session_state.df_master = pd.DataFrame()
                st.session_state.image_path_list = []
                st.session_state.current_tool = "analyse_all_parts"

            results = self.tasks.ask_analyse_all_parts_inputs()

            if st.button("Submit Values"):
                with st.spinner("Processing your request..."): 
                    df_master, image_path_list = self.tasks.analyse_all_parts_task( 
                        odb_path = results["odb_file_path"],
                        max_stress_limit = results["max_stress_limit"],
                        min_stress_limit = results["min_stress_limit"]
                    )
                    st.session_state.df_master = df_master
                    st.session_state.image_path_list = image_path_list

                    if not df_master.empty and image_path_list:
                        st.success("Successfully executed")

            if not st.session_state.df_master.empty and st.session_state.image_path_list:
                st.subheader("📊 Master Dataset")
                st.markdown(st.session_state.df_master.to_html(escape=False, index=False), unsafe_allow_html=True)

                st.subheader("📈 Contour Plots") 
                selected_image_path = st.selectbox("Select the Contour Plot you want to view:", st.session_state.image_path_list)

                if selected_image_path:
                    st.image(os.path.normpath(selected_image_path), caption="Contour Plot", use_column_width=True)

                     
        elif "analyse_single_part" in st.session_state.response["tool_called"]:

            st.header("Single Part and Elset Analyser 🔍")  
            results = self.tasks.ask_analyse_single_part_inputs()  

            if st.session_state.get("current_tool") != "analyse_single_part":
                st.session_state.df_master_single_part = pd.DataFrame()
                st.session_state.image_path_list_single_part = []
                st.session_state.current_tool = "analyse_single_part"

                results = self.tasks.ask_analyse_all_parts_inputs()

            if st.button("Submit Values"):
                with st.spinner("Processing your request..."): 
                    df_master_single_part, image_path_list_single_part = self.tasks.analyse_single_part_task( 
                        odb_path = results["odb_file_path"], 
                        instance_name = results["instance_name"],
                        elset_name = results["elset_name"],
                        max_stress_limit = results["max_stress_limit"],
                        min_stress_limit = results["min_stress_limit"]
                    ) 
                    st.session_state.df_master_single_part = df_master_single_part
                    st.session_state.image_path_list_single_part = image_path_list_single_part

                    if not df_master_single_part.empty and image_path_list_single_part:
                        st.success("Successfully executed")

            if not st.session_state.df_master_single_part.empty and st.session_state.image_path_list_single_part:
                st.subheader("📊 Master Dataset")
                st.markdown(st.session_state.df_master_single_part.to_html(escape=False, index=False), unsafe_allow_html=True)

                st.subheader("📈 Contour Plots") 
                selected_image_path = st.selectbox("Select the Contour Plot you want to view:", st.session_state.image_path_list_single_part)

                if selected_image_path:
                    st.image(os.path.normpath(selected_image_path), caption="Contour Plot", use_column_width=True)

        
        elif "assign_material_properties" in st.session_state.response["tool_called"]: 
            st.header("Assign Material Properties🪨")

            if st.session_state.get("current_tool") != "assign_material_properties":
                st.session_state.current_tool = "assign_material_properties"
                st.session_state.existing_materials_list = [] 
                st.session_state.part_names = [] 
                st.session_state.part_images = {}

            inp_file_path, model_name = self.tasks.ask_inp_model_name_inputs()  
            
            if st.button("Open Material Assigner"):
                with st.spinner("Processing your request..."): 
                    existing_materials_list, part_names, part_images = self.tasks.extract_materials_and_parts_info(model_name= model_name, inp_file_path=inp_file_path)
                    st.session_state.existing_materials_list = existing_materials_list 
                    st.session_state.part_names = part_names 
                    st.session_state.part_images = part_images

            self.tasks.ask_material_assignment_inputs(
                existing_materials_list= st.session_state.existing_materials_list, 
                part_names = st.session_state.part_names,
                part_images = st.session_state.part_images
            ) 
            
            if st.button("Submit Values"): 
                self.tasks.assign_material_properties_tasks(inp_file_path = inp_file_path, model_name= model_name) 
                st.success("Successfully assigned material properties") 
                st.session_state.existing_materials_list = [] 
                st.session_state.part_names = [] 
                st.session_state.part_images = {} 



        elif "cad_to_inp" in st.session_state.response["tool_called"]:  

            if st.session_state.get("current_tool") != "cad_to_inp":
                st.session_state.current_tool = "cad_to_inp"
                st.session_state.existing_materials_list = [] 
                st.session_state.part_names = [] 
                st.session_state.part_images = {} 
                st.session_state.inp_file_path = "" 
                st.session_state.model_name = ""
    
            st.header("CAD to INP Generator⚡")
            results = self.tasks.ask_cad2mesh_assembly_inputs()  


            if st.button("Open Material Assigner"):
                with st.spinner("Processing your request..."): 
                    temp_mesh_file = self.tasks.cad_to_inp_task( 
                        step_file_path = results["stp_file_path"],
                        model_name = results["model_name"],
                        mesh_size = results["mesh_size"],
                        element_type = results["element_type"]
                    )  
                    
                    model_name = results["model_name"]
                    inp_file_path = temp_mesh_file

                    existing_materials_list, part_names, part_images = self.tasks.extract_materials_and_parts_info(model_name= model_name, inp_file_path=inp_file_path)
                    st.session_state.existing_materials_list = existing_materials_list 
                    st.session_state.part_names = part_names 
                    st.session_state.part_images = part_images
                    st.session_state.inp_file_path = inp_file_path

            self.tasks.ask_material_assignment_inputs(
                existing_materials_list= st.session_state.existing_materials_list, 
                part_names = st.session_state.part_names,
                part_images = st.session_state.part_images
            ) 
            
            if st.button("Submit Values"): 
                self.tasks.assign_material_properties_tasks(inp_file_path = st.session_state.inp_file_path, model_name= st.session_state.model_name) 
                st.success("Successfully assigned material properties") 
                st.session_state.existing_materials_list = [] 
                st.session_state.part_names = [] 
                st.session_state.part_images = {} 
                st.session_state.inp_file_path = "" 
                st.session_state.model_name = ""

        else: 
            return 

    