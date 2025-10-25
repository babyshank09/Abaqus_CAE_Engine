import os 
from typing import Optional
import streamlit as st
import pandas as pd
import openpyxl
import json  


class Tasks: 
    def __init__(self, working_dir): 
        self.working_dir = working_dir 


    def display_input_model(self, input_file_address: str):
        """ 
        displays the picture of the model in the input file (.inp) in Abaqus CAE GUI and saves it as a PNG file.
        """
        import textwrap  
        import os
        import subprocess  

        base_dir = os.path.abspath(self.working_dir) 
        #print(base_dir)
        executions_dir = os.path.join(base_dir, "Executions") 
        #print(executions_dir)
        results_dir = os.path.join(base_dir, "Results") 
        #print(results_dir)

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_path = os.path.join(executions_dir, "display_input_model.py")

        code = textwrap.dedent(f"""
        # -*- coding: mbcs -*-
        from abaqus import *
        from abaqusConstants import *
        import visualization
        import os

        def display_inp_model(inp_file_path):
            
            if not os.path.isfile(inp_file_path):
                raise ValueError(f"The specified .inp file does not exist: {{inp_file_path}}")

        
            model_name = os.path.splitext(os.path.basename(inp_file_path))[0]

        
            try:
                mdb.ModelFromInputFile(name=model_name, inputFileName=inp_file_path)
            except Exception as e:
                raise RuntimeError(f"Failed to import .inp file: {{str(e)}}")

            
            session.Viewport(name='Model Viewport', origin=(0, 0), width=300, height=200)
            vp = session.viewports['Model Viewport']
            vp.setValues(displayedObject=mdb.models[model_name].rootAssembly)
            #vp.view.setValues(cameraPosition=(200, 200, 200), cameraUpVector=(0, 1, 0))
            
            vp.view.fitView()
            
            
            output_file = os.path.splitext(inp_file_path)[0] + '_display' 
            output_file_path = os.path.join(r"{results_dir}", "output_image.png") 
            session.printOptions.setValues(rendition=COLOR)
            session.printToFile(fileName= output_file_path, format=PNG, canvasObjects=(vp,))
            print(f"Model displayed and saved as {{output_file_path}}")


        try:
            display_inp_model(r"{input_file_address}")
        except Exception as e:
            print(f"Error: {{str(e)}}") 
        """)
        
        with open(script_path, "w") as file: 
            file.write(code)    
        #print(f"\nPython script successfully created at: {script_path}\n") 
        

        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", "noGUI=display_input_model.py"]
        subprocess.run(abaqus_command, cwd=current_working_dir, check=True, capture_output=True, text=True, shell=True)   

        image_path = os.path.join(results_dir, "output_image.png") 
        return os.path.normpath(image_path)








    def ask_inp_file_inputs(self)-> dict: 
        try:
            if "inp_file_path" not in st.session_state: 
                st.session_state.inp_file_path = ""
            if "start_angle" not in st.session_state:
                st.session_state.start_angle = 0
            if "final_angle" not in st.session_state:
                st.session_state.final_angle = 0
            if "step_size" not in st.session_state:
                st.session_state.step_size = 1
            if "model_name" not in st.session_state:
                st.session_state.model_name = ""
            if "instance_list" not in st.session_state:
                st.session_state.instance_list = ()
            if "axis_point" not in st.session_state:
                st.session_state.axis_point = (0.0, 0.0, 0.0)
            if "axis_direction" not in st.session_state:
                st.session_state.axis_direction = (0.0, 0.0, 0.0)
            if "drop_axis" not in st.session_state:
                st.session_state.drop_axis = "y"
            if "floor_instance_name" not in st.session_state:
                st.session_state.floor_instance_name = "" 
            if "output_image" not in st.session_state: 
                st.session_state.output_image = ""

            inp_file_path= st.text_input(
                "Input File Location (e.g., path/to/file.inp)",
                value=st.session_state.inp_file_path,
                key="inp_file_path_input"
                )  
            if st.button("Display Model", key="display_model_button"): 
                if not inp_file_path: 
                    st.error("Error: Please provide a valid input file path.")
                else:
                    image_path_abs = self.display_input_model(input_file_address=inp_file_path) 
                    st.image(image_path_abs, 
                            caption="Current Model", 
                            use_column_width=True,
                            ) 
                    st.success("Model displayed successfully!")
                
            start_angle = st.number_input(
                "Start Angle (degrees)",
                step=1,
                format="%d",
                value=st.session_state.start_angle,
                key="start_angle_input"
            )
            final_angle = st.number_input(
                "Final Angle (degrees)",
                step=1, 
                format="%d",
                value=st.session_state.final_angle,
                key="final_angle_input"
            )
            step_size = st.number_input(
                "Step Size (degrees)",
                step=1,
                format="%d",
                value=st.session_state.step_size,
                key="step_size_input"
            )
            model_name = st.text_input(
                "Model Name",
                value=st.session_state.model_name,
                key="model_name_input"
            )

            st.markdown("Enter the names of the instances to rotate in the given format:")
            instance_list_input = st.text_input(
                "Instances (comma-separated)",
                placeholder="e.g., PART1, PART2, PART3",
                value=", ".join(st.session_state.instance_list),
                key="instance_list_input"
            )
            instance_list = tuple(i.strip() for i in instance_list_input.split(",") if i.strip())
            if instance_list and st.button("check instance_list", key="check_instance_list_button"):
                st.write(instance_list)

            st.markdown("Enter the Axis Points (points on the axis of rotation):")
            axis_point_x = st.number_input(
                "Axis Point X",
                format="%.6f",
                value=st.session_state.axis_point[0],
                key="axis_point_x_input"
            )
            axis_point_y = st.number_input(
                "Axis Point Y",
                format="%.6f",
                value=st.session_state.axis_point[1],
                key="axis_point_y_input"
            )
            axis_point_z = st.number_input(
                "Axis Point Z",
                format="%.6f",
                value=st.session_state.axis_point[2],
                key="axis_point_z_input"
            )
            axis_point = (axis_point_x, axis_point_y, axis_point_z)
            if st.button("check axis_point", key="check_axis_point_button"):
                st.write(axis_point)

            st.markdown("Enter the Axis Direction (direction vector of the rotation axis):")
            axis_dir_x = st.number_input(
                "Axis Direction X",
                format="%.6f",
                value=st.session_state.axis_direction[0],
                key="axis_dir_x_input"
            )
            axis_dir_y = st.number_input(
                "Axis Direction Y",
                format="%.6f",
                value=st.session_state.axis_direction[1],
                key="axis_dir_y_input"
            )
            axis_dir_z = st.number_input(
                "Axis Direction Z",
                format="%.6f",
                value=st.session_state.axis_direction[2],
                key="axis_dir_z_input"
            )
            axis_direction = (axis_dir_x, axis_dir_y, axis_dir_z)
            if st.button("check axis_direction", key="check_axis_direction_button"):
                st.write(axis_direction)

            drop_axis = st.selectbox(
                "Drop Axis (for clearance)",
                options=["x", "y", "z"],
                index=["x", "y", "z"].index(st.session_state.drop_axis),
                key="drop_axis_input"
            )
            floor_instance_name = st.text_input(
                "Floor Instance Name",
                value=st.session_state.floor_instance_name,
                key="floor_instance_name_input"
            )
            
            st.session_state.inp_file_path = inp_file_path
            st.session_state.start_angle = start_angle
            st.session_state.final_angle = final_angle
            st.session_state.step_size = step_size
            st.session_state.model_name = model_name
            st.session_state.instance_list = instance_list
            st.session_state.axis_point = axis_point
            st.session_state.axis_direction = axis_direction
            st.session_state.drop_axis = drop_axis
            st.session_state.floor_instance_name = floor_instance_name   
           

            return { 
                "inp_file_path": inp_file_path,
                "start_angle": start_angle,
                "final_angle": final_angle,
                "step_size": step_size,
                "model_name": model_name,
                "instance_list": instance_list,
                "axis_point": axis_point,
                "axis_direction": axis_direction,
                "drop_axis": drop_axis,
                "floor_instance_name": floor_instance_name
            } 
        
        except Exception as e: 
            raise e





    

    def generate_inp_scripts_task(self, start_angle: int, final_angle: int, step_size: int, inp_file_location: str, model_name: str, instance_list: tuple[str, ...], axis_point: tuple[float, ...], axis_direction: tuple[float, ...], drop_axis: str, floor_instance_name: str):
        """
        Automates the generation of Abaqus input files (.inp) by dynamically creating and executing a Python script 
        that performs rotational transformations and clearance validation on specified model instances.

        This function enables parametric simulation setups by rotating model instances from a given start angle 
        to a final angle in specified step increments, generating a unique input file for each configuration. 
        For each angle, it ensures a minimum clearance (0.01 units) from a designated floor instance along a specified axis 
        by calculating and applying corrective translations. Once the desired configuration is achieved, an Abaqus input file 
        is generated and the model is reset to its original state, allowing for batch simulation and design space exploration.

        Designed as a tool for Agentic AI workflows, this function supports intelligent automation in simulation pipelines, 
        making it ideal for iterative optimization, clearance analysis, and virtual prototyping tasks.

        Args:
            start_angle (int): Starting angle (in degrees) for rotation about the specified axis.
            final_angle (int): Final angle (in degrees) for the rotation loop (exclusive).
            step (int): Step size (in degrees) for each rotation increment.
            inp_file_location (str): Path to the original Abaqus .inp file used to load the model.
            model_name (str): Name to assign to the Abaqus model created from the .inp file.
            instance_list (tuple[str, ...]): Tuple of instance names (e.g., parts or assemblies) to rotate and analyze.
            axis_point (tuple[float, float, float]): A point on the axis of rotation.
            axis_direction (tuple[float, float, float]): Direction vector of the axis of rotation.
            drop_axis (str): Axis ("x", "y", or "z") along which to compute and adjust vertical clearance from the floor.
            floor_instance_name (str): Name of the floor instance used as a reference for clearance calculations.

        Behavior:
            - Rotates the given instances incrementally within the specified angle range.
            - Checks clearance between each rotated instance and the floor instance.
            - Translates the rotated assembly to maintain a minimum clearance of 0.01 units.
            - Generates an input file (.inp) for each configuration using Abaqus.
            - Restores the original orientation and position after each input file is created.

        Example:
            generate_inp_scripts(
                start_angle=0,
                final_angle=90,
                step=15,
                inp_file_location="C:/models/car_assembly.inp",
                model_name="CarAssemblyModel",
                instance_list=("Wheel1", "Wheel2", "Chassis"),
                axis_point=(0.0, 0.0, 0.0),
                axis_direction=(0.0, 1.0, 0.0),
                drop_axis="z",
                floor_instance_name="GroundPlane"
            )
        """

        import textwrap  
        import os
        import subprocess  

        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_path = os.path.join(executions_dir, "input_file_generation.py")
        
        code = textwrap.dedent(f"""
        # -*- coding: mbcs -*-
        from abaqus import *
        from abaqusConstants import *
        import __main__
        import section
        import regionToolset
        import displayGroupMdbToolset as dgm
        import part
        import material
        import assembly
        import step
        import interaction
        import load
        import mesh
        import optimization
        import job
        import sketch
        import visualization
        import xyPlot
        import displayGroupOdbToolset as dgo
        import connectorBehavior
        
        os.chdir(r"{results_dir}")

        inp_file = r"{inp_file_location}" 

        model_name = "{model_name}"  
        mdb.ModelFromInputFile(name=model_name, inputFileName=inp_file)

        instance_list = {instance_list}
        floor_instance = "{floor_instance_name}"

        axis_point = {axis_point}
        axis_dir = {axis_direction}  

        start_angle = {start_angle}
        final_angle = {final_angle}
        step = {step_size}

        clearance_info_partwise={{}} 
        clearance_info_total={{}}



        def get_bounds(inst_name, assembly):
            a = assembly
            instance = a.instances[inst_name]
            if not instance.nodes:
                raise ValueError(f"Instance '{{inst_name}}' has no nodes. Ensure the instance is meshed.")

            z_coords = [node.coordinates[2] for node in instance.nodes]  
            y_coords = [node.coordinates[1] for node in instance.nodes] 
            x_coords = [node.coordinates[0] for node in instance.nodes]


            if not z_coords:
                raise ValueError(f"Instance '{{inst_name}}' has no valid z node coordinates.") 

            if not y_coords:
                raise ValueError(f"Instance '{{inst_name}}' has no valid y node coordinates.") 

            if not x_coords:
                raise ValueError(f"Instance '{{inst_name}}' has no valid x node coordinates.")

            z_min = min(z_coords)
            z_max = max(z_coords) 
            y_min = min(y_coords)
            y_max = max(y_coords) 
            x_min = min(x_coords)
            x_max = max(x_coords)
            return z_min, z_max, y_min, y_max, x_min, x_max




        if __name__ =="__main__": 

            drop_axis = "{drop_axis}"
            for angle in range(start_angle, final_angle, step): 
                job_name = f"{{model_name}}_{{angle}}"
                a = mdb.models[model_name].rootAssembly
            
                a.rotate(instanceList=instance_list, axisPoint=axis_point, axisDirection=axis_dir, angle=float(angle))


                try: 
                    
                    floor_low_z, floor_high_z, floor_low_y, floor_high_y, floor_low_x, floor_high_x = get_bounds(floor_instance, assembly= a )
                    print(f"FLOOR bounds: low(z)={{floor_low_z:.3f}}, high(z)={{floor_high_z:.3f}},    low(y)={{floor_low_y:.3f}}, high(y)={{floor_high_y:.3f}},    low(x)={{floor_low_x:.3f}}, high(x)={{floor_high_x:.3f}}")

                    
                    for inst in instance_list:
                        part_low_z, part_high_z, part_low_y, part_high_y, part_low_x, part_high_x = get_bounds(inst, assembly=a)
                        distance_above_z = part_low_z - floor_high_z
                        distance_below_z = floor_low_z - part_high_z
                        distance_above_y = part_low_y - floor_high_y
                        distance_below_y = floor_low_y - part_high_y
                        distance_above_x = part_low_x - floor_high_x
                        distance_below_x = floor_low_x - part_high_x
                        
                        if drop_axis == "z":
                            clearance = min(abs(distance_above_z), abs(distance_below_z)) 
                            if abs(distance_above_z) < abs(distance_below_z):  
                                clearance_info_partwise[inst]= {{"clearance": clearance, "clearance_type": "above"}}

                            else:
                                clearance_info_partwise[inst]= {{"clearance": clearance, "clearance_type": "below"}}

                        
                        elif drop_axis == "y":
                            clearance = min(abs(distance_above_y), abs(distance_below_y)) 
                            if abs(distance_above_y) < abs(distance_below_y):  
                                clearance_info_partwise[inst]= {{"clearance": clearance, "clearance_type": "above"}}

                            else:
                                clearance_info_partwise[inst]= {{"clearance": clearance, "clearance_type": "below"}} 

                        
                        if drop_axis == "x":
                            clearance = min(abs(distance_above_x), abs(distance_below_x)) 
                            if abs(distance_above_x) < abs(distance_below_x):  
                                clearance_info_partwise[inst]= {{"clearance": clearance, "clearance_type": "above"}}

                            else:
                                clearance_info_partwise[inst]= {{"clearance": clearance, "clearance_type": "below"}}

                            
                    
                    
                    min_clearance = 1000
                    for part, clearance_properties in clearance_info_partwise.items(): 
                        if clearance_properties["clearance"] < min_clearance: 
                            min_clearance = clearance_properties["clearance"] 
                            min_clearance_part = part  
                            min_clearance_type = clearance_properties["clearance_type"] 

                    
                    clearance_info_total["Part"] = min_clearance_part 
                    clearance_info_total["Clearance"] = min_clearance 
                    clearance_info_total["Clearance Type"] = min_clearance_type
                    
                    
                            
                
                    if clearance_info_total["Clearance"] > 0.01: 
                        if clearance_info_total["Clearance Type"] == "above":   
                            if drop_axis == "y": 
                                y_translation = clearance_info_total["Clearance"] - 0.01 
                                print(-y_translation)
                                translation_vector = (0.0, -y_translation, 0.0)
                                a.translate(instanceList=instance_list, vector=translation_vector)
                    
                            
                            if drop_axis == "z": 
                                z_translation = clearance_info_total["Clearance"] - 0.01
                                translation_vector = (0.0, 0.0, -z_translation)
                                a.translate(instanceList=instance_list, vector=translation_vector)

                            if drop_axis == "x": 
                                x_translation = clearance_info_total["Clearance"] - 0.01
                                translation_vector = (-x_translation, 0.0, 0.0)
                                a.translate(instanceList=instance_list, vector=translation_vector)

                        if clearance_info_total["Clearance Type"] == "below": 
                            if drop_axis == "y": 
                                y_translation = clearance_info_total["Clearance"] - 0.01
                                translation_vector = (0.0, y_translation, 0.0)
                                a.translate(instanceList=instance_list, vector=translation_vector)
                            
                            if drop_axis == "z": 
                                z_translation = clearance_info_total["Clearance"] - 0.01
                                translation_vector = (0.0, 0.0, z_translation)
                                a.translate(instanceList=instance_list, vector=translation_vector)

                            if drop_axis == "x": 
                                x_translation = clearance_info_total["Clearance"] - 0.01
                                translation_vector = (x_translation, 0.0, 0.0)
                                a.translate(instanceList=instance_list, vector=translation_vector)
                
                        print("Corrected the clearance... Current clearance = 0.01")

                
                    mdb.Job(
                        name=job_name, model=model_name, description='', type=ANALYSIS,
                        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
                        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE,
                        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
                        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='',
                        resultsFormat=ODB, numDomains=1, activateLoadBalancing=False,
                        numThreadsPerMpiProcess=1, multiprocessingMode=DEFAULT, numCpus=1
                    )


                    mdb.jobs[job_name].writeInput(consistencyChecking=OFF)
                    
                    print(translation_vector)
                    neg_translation_vector = tuple(-x for x in translation_vector) 
                    print(neg_translation_vector) 

                    a.translate(instanceList=instance_list, vector=neg_translation_vector)
                    a.rotate(instanceList=instance_list, axisPoint=axis_point, axisDirection=axis_dir, angle=float(-angle))
                

                except Exception as e:
                    a.rotate(instanceList=instance_list, axisPoint=axis_point, axisDirection=axis_dir, angle=float(-angle))
                    a.regenerate()
                    raise e
                    continue
        """) 

        with open(script_path, "w") as file: 
            file.write(code)    
        print(f"\nPython script successfully created at: {script_path}\n") 

        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", "noGUI=input_file_generation.py"]
        subprocess.run(abaqus_command, cwd=current_working_dir, check=True, capture_output=True, text=True, shell=True) 









    def ask_cad2mesh_assembly_inputs(self)-> dict: 
        if "stp_file_path" not in st.session_state: 
            st.session_state.stp_file_path = ""
        if "model_name" not in st.session_state:
            st.session_state.model_name = ""


        st.info("This is for an assembly file with multiple parts. If you have a single part file, please use the Single Part option instead.")

        stp_file_path= st.text_input(
            "Step File Location (e.g., path/to/file.stp or .step)",
            value=st.session_state.stp_file_path
        ) 
  
        model_name = st.text_input(
            "Model Name",
            value=st.session_state.model_name,
            key="model_name_input"
        )

        st.session_state.stp_file_path = stp_file_path
        st.session_state.model_name = model_name

        return {
            "stp_file_path": stp_file_path,
            "model_name": model_name,
        }



    def ask_partwise_mesh_inputs(self, part_names, part_images):  
        import os 
        import json 

        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True) 


        mesh_info = {}
        for i, part_name in enumerate(part_names, start=1):
            st.subheader(part_name)  
            renamed_part_name = st.text_input(f"Rename {part_name} (Optional)", value=part_name, key= f"{part_name}_rename")

            image_path = os.path.normpath(part_images.get(part_name, ""))

            if image_path:
                st.image(image_path, caption=f"{part_name}", use_column_width=True)
                

            mesh_size = st.number_input(
                "Mesh Size",
                step=0.1,
                format="%.1f",
                key=f"{part_name}_mesh_size"
            )

            element_types = ["C3D10", "C3D4", "C3D8R", "C3D8I", "C3D10M", "C3D10HS"]
            element_type = st.selectbox(
                "Element Type",
                element_types,
                key=f"{part_name}_element_type"
            )    


            mesh_info[part_name] = { 
                "renamed_part_name": renamed_part_name,
                "mesh_size": mesh_size,
                "element_type": element_type
            } 
        
        mesh_info_path = os.path.join(results_dir, "mesh_info.json")
        with open(mesh_info_path, "w") as f:
            json.dump(mesh_info, f, indent=4) 

        return mesh_info_path



    def cad_to_mesh_assembly_task(self, step_file_path: str, model_name: str, mesh_info_path: str):
        import os
        import subprocess
        import textwrap

        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_dir = executions_dir
        script_path = os.path.join(script_dir, "CAD2Mesh_Assembly.py") 


        code=textwrap.dedent(f"""
        # -*- coding: mbcs -*-
        from abaqus import *
        from abaqusConstants import *
        import part, material, assembly, step, mesh
        import section, regionToolset
        import os 
        import json


        def mesh_assembly(step_file_path, model_name, results_dir, mesh_info):
            print("AUTOMATIC STEP FILE IMPORT")


            step_geometry = mdb.openStep(fileName=step_file_path)
            num_parts_in_file = step_geometry.numberOfParts
            print("STEP file contains: %d parts" % num_parts_in_file)


            if model_name in mdb.models:
                del mdb.models[model_name]
            mdb.Model(name=model_name)
            model = mdb.models[model_name]
            print("Created model: %s" % model_name)


            print("Importing parts...")
            imported_parts = []
            failed_imports = []

            for i in range(1, num_parts_in_file + 1):
                try:
                    part_name = "Part_%d" % i
                    model.PartFromGeometryFile(
                        name=part_name,
                        geometryFile=step_geometry,
                        bodyNum=i,
                        combine=False,
                        dimensionality=THREE_D,
                        type=DEFORMABLE_BODY,
                        scale=1.0
                    )
                    imported_parts.append(part_name)
                    print("Imported: %s" % part_name) 

                except Exception as e:
                    failed_imports.append(i)
                    print("Failed Part %d: %s" % (i, str(e)))

            print("Successfully imported: %d parts" % len(imported_parts))


            valid_parts = []
            for part_name in imported_parts:
                part_obj = model.parts[part_name]
                num_cells = len(part_obj.cells)
                num_faces = len(part_obj.faces)

                if num_cells > 0 or num_faces > 0:
                    valid_parts.append(part_name)

            print("Valid parts for meshing: %d" % len(valid_parts))


            print("Creating assembly...")
            assembly = model.rootAssembly

            created_instances = []
            for part_name in valid_parts:
                try:
                    instance_name = "%s" % part_name
                    assembly.Instance(
                        name=instance_name,
                        part=model.parts[part_name],
                        dependent=OFF 
                    )
                    created_instances.append(instance_name)
                    print("Created instance: %s" % instance_name)
                except Exception as e:
                    print("Failed instance %s: %s" % (part_name, str(e)))


            print("Meshing at assembly level...")
            meshed_instances = []
            total_elements = 0
            total_nodes = 0
            elem = False 
            
            for instance_name, instance_info in mesh_info.items():
            #for instance_name in created_instances:
                element_type = instance_info["element_type"]
                mesh_size = instance_info["mesh_size"]

                try:
                    instance = assembly.instances[instance_name]


                    assembly.seedPartInstance(
                        regions=(instance,),
                        size= mesh_size,
                        deviationFactor=0.1,
                        minSizeFactor=0.1
                    )

                
                    cells = instance.cells
                    if len(cells) > 0:
                        try:
                            if element_type in ["C3D8R", "C3D8I"]:
                                assembly.setMeshControls(
                                    regions=cells,
                                    technique=SWEEP,
                                    elemShape=HEX 
                                )
                                elem =True
                            else:
                                assembly.setMeshControls(
                                    regions=cells,
                                    technique=FREE,
                                    elemShape=TET
                                )   
                                elem =False

                        except:  
                            assembly.setMeshControls(
                                    regions=cells,
                                    technique=FREE,
                                    elemShape=TET
                                )  
                            elem =False

                        
                        if element_type == "C3D10":
                            elem_type = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
                        elif element_type == "C3D4":
                            elem_type = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD) 
                        elif element_type == "C3D8R" and not elem:
                            elem_type = mesh.ElemType(elemCode=C3D10M, elemLibrary=STANDARD)  
                        elif element_type == "C3D8I"and not elem:
                            elem_type = mesh.ElemType(elemCode=C3D10M, elemLibrary=STANDARD) 
                        elif element_type == "C3D8R" and elem:
                            elem_type = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)  
                        elif element_type == "C3D8I"and elem:
                            elem_type = mesh.ElemType(elemCode=C3D8I, elemLibrary=STANDARD) 
                        elif element_type == "C3D10M":
                            elem_type = mesh.ElemType(elemCode=C3D10M, elemLibrary=STANDARD)
                        elif element_type == "C3D10HS":
                            elem_type = mesh.ElemType(elemCode=C3D10HS, elemLibrary=STANDARD) 
                        else:
                            elem_type = mesh.ElemType(elemCode=C3D10M, elemLibrary=STANDARD)


                        region = regionToolset.Region(cells=cells)
                        assembly.setElementType(regions=region, elemTypes=(elem_type,))

                    
                    assembly.generateMesh(regions=(instance,)) 


                    elements = len(instance.elements)
                    nodes = len(instance.nodes)

                    print("Meshed %s: %d elements, %d nodes" % (instance_name, elements, nodes))

                    meshed_instances.append(instance_name)
                    total_elements += elements
                    total_nodes += nodes

                except Exception as e:
                    print("Meshing error on instance %s: %s" % (instance_name, str(e)))


            print("SUMMARY")
            print("Parts detected: %d" % num_parts_in_file)
            print("Parts imported: %d" % len(imported_parts))
            print("Instances meshed: %d" % len(meshed_instances))
            print("Total elements: %d" % total_elements)
            print("Total nodes: %d" % total_nodes)

            if len(meshed_instances) == len(valid_parts):
                print("SUCCESS: All %d instances meshed at assembly level" % len(valid_parts))
            else:
                print("Partial success: %d/%d instances meshed" % (len(meshed_instances), len(valid_parts)))   


            for instance_name, instance_info in mesh_info.items():
                renamed_part_name = instance_info["renamed_part_name"]
                rename_part(model, instance_name, renamed_part_name)


            job_name = f"temp_inp"
            os.chdir(results_dir)
            mdb.Job(name=job_name, model=model_name)
            mdb.jobs[job_name].writeInput(consistencyChecking=OFF)
            
            inp_file = os.path.join(results_dir, "temp_inp.inp")
            print(f"Saved the model to {{inp_file}}")     
            mdb.close()

            return inp_file




        def rename_part(model, part_name, renamed_part_name):  
                model.parts.changeKey(fromName=part_name, toName= renamed_part_name)

                assembly = model.rootAssembly
                assembly.features.changeKey(fromName=part_name, toName=renamed_part_name)
                assembly.regenerate()




        def create_elset(temp_inp_file, model_name):
            file_path = temp_inp_file 

            if not os.path.exists(file_path):
                raise ValueError("File not found: " + file_path)

            print("Opening file:", file_path)
            mdb.ModelFromInputFile(name=model_name, inputFileName=file_path)

            model = mdb.models[model_name]
            print("Working on model:", model_name)

            print("Creating ALL_ELEMENTS sets at PART level...")
            for part_name, part in model.parts.items(): 
                if len(part.elements) > 0:   # only if the part has elements
                    elems = part.elements[:]
                    if 'ALL_ELEMENTS' in part.sets.keys():
                        del part.sets['ALL_ELEMENTS']
                    part.Set(name='ALL_ELEMENTS', elements=elems) 
                    print("  -> Part:", part_name, "set created.")
            



        def save_cae_file(cae_file_path): 
            print("Saving model...")
            try:
                mdb.saveAs(pathName=cae_file_path)
                print("Saved: %s" % cae_file_path)
            except Exception as e:
                print("Save error: %s" % str(e))




        def save_inp_file(job_name, results_dir, model_name, temp_inp_file):

            job = mdb.Job(name=job_name, model=model_name) 
            os.chdir(results_dir)
            job.writeInput(consistencyChecking=OFF)
            print(f".inp file written in current directory: {{job_name}}.inp")

            if os.path.exists(temp_inp_file):
                os.remove(temp_inp_file) 
                print(f"Removed temporary file: {{temp_inp_file}}")

            return os.path.join(results_dir, job_name + '.inp') 




        def print_step_attributes(step_file_path):
            step_geometry = mdb.openStep(fileName=step_file_path)
            print("Attributes and methods of step_geometry:")
            for attr in dir(step_geometry):
                print(attr) 


            


        if __name__ == "__main__":   
            step_file_path = r"{step_file_path}"
            model_name = "{model_name}"
            job_name = f"{{model_name}}_Mesh" 
            results_dir = r"{results_dir}"
            cae_file_path = os.path.join(results_dir, f"{{job_name}}.cae")
            cae_file_path = os.path.normpath(cae_file_path)



            json_file_path = r"{mesh_info_path}"
            with open(json_file_path, "r") as f:
                mesh_info = json.load(f)

            temp_inp_file = mesh_assembly(
                step_file_path = step_file_path,
                model_name = model_name,
                results_dir = results_dir,
                mesh_info = mesh_info
            )
            create_elset(temp_inp_file = temp_inp_file, model_name = model_name)
            meshed_inp_file = save_inp_file(job_name= job_name, results_dir= results_dir, model_name= model_name, temp_inp_file= temp_inp_file)
            save_cae_file(cae_file_path= cae_file_path)
        """) 

        with open(script_path, "w") as file: 
            file.write(code) 

        #print(f"\nPython script successfully created at: {script_path}\n")
        
        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", f"noGUI=CAD2Mesh_Assembly.py"]
        subprocess.run(abaqus_command, cwd=current_working_dir, check=True, capture_output=True, text=True, shell=True)
        









    def ask_cad2mesh_inputs(self)-> dict: 
        if "stp_file_path" not in st.session_state: 
            st.session_state.stp_file_path = ""
        if "mesh_size" not in st.session_state:
            st.session_state.mesh_size = 1.0
        if "model_name" not in st.session_state:
            st.session_state.model_name = ""
        if "part_name" not in st.session_state:
            st.session_state.part_name = ""
        if "element_type" not in st.session_state:
            st.session_state.element_type = "" 

        st.info("This is for a single part file. If you have an assembly, please use the Assembly option instead.")

        stp_file_path= st.text_input(
            "Step File Location (e.g., path/to/file.stp or .step)",
            value=st.session_state.stp_file_path
        ) 
        mesh_size = st.number_input(
            "Mesh Size",
            step=0.1,
            format="%.1f",
            value=st.session_state.mesh_size,
            key="mesh_size_input"
        )
        model_name = st.text_input(
            "Model Name",
            value=st.session_state.model_name,
            key="model_name_input"
        )
        part_name = st.text_input(
            "Part Name",
            value=st.session_state.part_name,
            key="part_name_input"
        )
        element_type = st.text_input(
            "Element Type",
            value=st.session_state.element_type,
            key="element_type_input"
        )   

        st.session_state.stp_file_path = stp_file_path
        st.session_state.mesh_size = mesh_size
        st.session_state.model_name = model_name
        st.session_state.part_name = part_name
        st.session_state.element_type = element_type

        return {
            "stp_file_path": stp_file_path,
            "mesh_size": mesh_size,
            "model_name": model_name,
            "part_name": part_name,
            "element_type": element_type
        }




    def cad_to_mesh_task(self, step_file_path: str, model_name: str, part_name: str, mesh_size: float, element_type: str): 
        """
        Automates the CAD-to-mesh conversion process using Abaqus CAE in noGUI mode. This is only for a single part file 

        This function dynamically generates and executes an Abaqus Python script that:
        1. Imports a 3D STEP file into a new Abaqus model.
        2. Creates a part from the geometry and assigns mesh controls.
        3. Applies meshing using either C3D10 (quadratic tetrahedron) or C3D4 (linear tetrahedron) elements.
        4. Saves the generated mesh and model to a .cae file for further simulation.

        Additionally, the function manages the execution environment by organizing scripts and results into structured directories.

        Parameters:
            step_file_path (str): Absolute path to the STEP (.step/.stp) file to be imported.
            model_name (str): Name to assign to the Abaqus model.
            part_name (str): Name to assign to the part created from the STEP geometry.
            mesh_size (float): Approximate global size of mesh elements.
            element_type (str): Element type for meshing, either 'C3D10' or 'C3D4'.

        Example:
            cad_to_mesh(
                step_file_path="C:/path/to/file.step",
                model_name="TestModel",
                part_name="Bracket",
                mesh_size=10.0,
                element_type="C3D10"
            )
        """
        
        import os
        import subprocess
        import textwrap 

        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_dir = executions_dir
        script_path = os.path.join(script_dir, "CAD2Mesh.py") 


        
        code =textwrap.dedent(f"""
        # -*- coding: mbcs -*-
        from abaqus import *
        from abaqusConstants import *
        import part, material, assembly, step, mesh
        import section, regionToolset
        import os


        step_file_path = r"{step_file_path}"
        model_name = "{model_name}"
        part_name = "{part_name}"
        mesh_size = {mesh_size}
        element_type = "{element_type}"


        step_file_path = os.path.normpath(step_file_path)  


        if model_name not in mdb.models:  
            mdb.Model(name=model_name)


        try:
            step_geometry = mdb.openStep(fileName=step_file_path)
            mdb.models[model_name].PartFromGeometryFile(
                name=part_name,
                geometryFile=step_geometry,
                combine=False,
                dimensionality=THREE_D,
                type=DEFORMABLE_BODY,
                scale=1.0
            )
            print("STEP file imported successfully.")

        except Exception as e:
            print(f"Error importing STEP file: {{e}}")



        try:
            part_obj = mdb.models[model_name].parts[part_name]

            
            if not part_obj.cells:
                raise ValueError("No valid cells found in the imported geometry.")

            
            part_obj.seedPart(size=mesh_size, deviationFactor=0.1, minSizeFactor=0.1)

            
            part_obj.setMeshControls(regions=part_obj.cells, technique=FREE, elemShape=TET)

            
            if element_type == 'C3D10':
                elem_type = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
            elif element_type == 'C3D4':
                elem_type = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
            else:
                raise ValueError(f"Unsupported element type: {{element_type}}")

            all_cells = part_obj.cells
            region = (all_cells,)
            part_obj.setElementType(regions=region, elemTypes=(elem_type,))

            
            part_obj.generateMesh()
            print("Mesh generated successfully.")


        except Exception as e:
            print(f" Error during meshing: {{e}}")
            raise




        try: 
            cae_file_path = os.path.join(r"{results_dir}", f"{{part_name}}.cae")
            #cae_file_path = f'C:/Users/v-sisubraman/Documents/Perfect_Environment/Agentic_AI/Abaqus_CAE_Cockpit/Abaqus Scripts/{{part_name}}.cae'
            cae_file_path = os.path.normpath(cae_file_path)
            mdb.saveAs(pathName=cae_file_path)
            print(f"CAE file created and saved successfully to {{cae_file_path}}.")

        except Exception as e: 
            print(f"Error saving .cae file: {{e}}")
        """) 
        

        with open(script_path, "w") as file: 
            file.write(code) 

        print(f"\nPython script successfully created at: {script_path}\n")
        
        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", f"noGUI=CAD2Mesh.py"]
        subprocess.run(abaqus_command, cwd= current_working_dir, check=True, capture_output=True, text=True, shell=True) 








    


    def ask_analyse_all_parts_inputs(self)-> dict: 
        if "odb_file_path" not in st.session_state: 
            st.session_state.odb_file_path = "" 


        st.info("This is for analysing all instances and its elsets in the odb file. If you want to analyse a specific part and elset, please use the Single Part option instead.")

        odb_file_path= st.text_input(
            "ODB File Location (e.g., path/to/file.odb)",
            value=st.session_state.odb_file_path, 
            key = "odb_path"
        )  
  
        max_stress_limit = st.text_input(
            "Max Stress Limit",
        ) 

        if not max_stress_limit:
            max_stress_limit = None
        

        min_stress_limit = st.text_input(
            "Min Stress Limit",
        )

        if not min_stress_limit:
            min_stress_limit = None


        st.session_state.odb_file_path = odb_file_path  
    

        return {
            "odb_file_path": odb_file_path, 
            "max_stress_limit": float(max_stress_limit) if max_stress_limit else None, 
            "min_stress_limit": float(min_stress_limit) if min_stress_limit else None
        }




    def analyse_all_parts_task(self, odb_path, max_stress_limit=None, min_stress_limit=None):
        import os
        import subprocess
        import textwrap 

        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_dir = executions_dir
        script_path = os.path.join(script_dir, "analyse_all_parts.py") 


        
        code =textwrap.dedent(f"""
        # -*- coding: mbcs -*-
        from abaqus import *
        from odbAccess import *
        import pandas as pd
        from abaqusConstants import *
        import odbAccess  
        from odbAccess import openOdb 
        import math 
        from collections import defaultdict 
        import visualization 
        from displayGroupOdbToolset import LeafFromElementSets 
        import openpyxl 
        import os

        class AnalyseAllParts: 
            def __init__(self, odb_path, max_stress_limit=None, min_stress_limit=None, results_dir=None):
                self.odb_path = odb_path
                self.max_stress_limit = max_stress_limit
                self.min_stress_limit = min_stress_limit
                self.results_dir = results_dir 


            def print_elements(self):

                from odbAccess import openOdb

                odb = openOdb(path= self.odb_path) 
                parts_and_elsets = {{}}

                instances = odb.rootAssembly.instances.keys()

                print("Available Element Sets in ODB:")

                for instance in instances: 
                    elsets = odb.rootAssembly.instances[instance].elementSets.keys()
                    parts_and_elsets[instance] = elsets 

                print(parts_and_elsets) 

                odb.close() 
                return parts_and_elsets



            def extract_results(self, instance_name, elset_name):
                try:

                    odb = openOdb(path=self.odb_path)
                    print(f"Opened ODB File: {{self.odb_path}}")


                    try:
                        instance = odb.rootAssembly.instances[instance_name]
                        if elset_name not in instance.elementSets:
                            raise ValueError(f"Elset '{{elset_name}}' not found in instance '{{instance_name}}'.")
                        elset = instance.elementSets[elset_name]
                        print(f"Element set '{{elset_name}}' found in instance '{{instance_name}}'")
                    except KeyError:
                        raise ValueError(f"Instance '{{instance_name}}' not found in ODB")


                    last_step_name = list(odb.steps.keys())[-1]
                    step = odb.steps[last_step_name]
                    print(f"Accessing step: {{last_step_name}}")


                    max_stress = float('-inf')
                    max_stress_elem = None
                    max_stress_node = None
                    framewise_data = [] 

                    max_stress_all_frames = 0
                    max_stress_node_all_frames = 0
                    current_frame_no = 0
                    self.max_frame_no = 0

                    for frame in step.frames:
                        if 'S' in frame.fieldOutputs:
                            stress_field = frame.fieldOutputs['S'].getSubset(
                                region=elset,
                                position=ELEMENT_NODAL
                            )


                            node_map = defaultdict(list)
                            max_principal_stress= 0 
                            avg =0 
                            for v in stress_field.values:
                                if hasattr(v, 'maxPrincipal') and hasattr(v, 'nodeLabel'):
                                    node_map[v.nodeLabel].append(v.maxPrincipal) 


                            for node_label, stress_list in node_map.items(): 
                                top_n = int(len(stress_list) * 1)
                                top_values = sorted(stress_list, reverse=True)[:top_n]  
                                if len(top_values) !=0:
                                    avg = sum(top_values) / len(top_values)

                                if avg > max_principal_stress:
                                    max_principal_stress = avg
                                    max_stress_node = node_label 

                                    if avg > max_stress_all_frames: 
                                        max_stress_all_frames = avg 
                                        max_stress_node_all_frames = node_label 
                                        self.max_frame_no = current_frame_no
                                        self.max_timestamp = frame.frameValue


                            timestamp = frame.frameValue
                            print(f"Frame {{timestamp}}: Max principal stress: {{max_principal_stress:.6f}}, Node: {{max_stress_node}}")
                            current_frame_no += 1
                    print(f"max stress all frames: {{max_stress_all_frames}}")

                              

                    max_peeq = 0
                    max_peeq_node = None

                    last_frame = step.frames[-1]
                    if 'PEEQ' in last_frame.fieldOutputs:
                        peeq_field = last_frame.fieldOutputs['PEEQ'].getSubset(
                            region=elset,
                            position=ELEMENT_NODAL
                        )
                        for value in peeq_field.values:
                            if value.data > max_peeq:
                                max_peeq = value.data
                                max_peeq_elem = value.elementLabel
                                try:
                                    max_peeq_node = value.nodeLabel
                                except AttributeError:
                                    max_peeq_node = None

                
                    if max_stress_node_all_frames:
                        print(f"Results for ODB:")
                        print(f"Max Principal Stress: {{max_stress_all_frames:.6f}} at Node {{max_stress_node_all_frames}}")
                        print(f"Max PEEQ: {{max_peeq:.6f}} at Node {{max_peeq_node}}")

                        # Save to master CSV 
                        image_path = self.visualize_result( 
                                                            instance_name= instance_name,
                                                            elset_name= elset_name,
                                                            frame_no= self.max_frame_no,
                                                            max_stress_limit=self.max_stress_limit, 
                                                            min_stress_limit=self.min_stress_limit
                                                        )

                        odb.close() 
                        return [instance_name, elset_name, max_stress_all_frames, max_stress_node_all_frames, self.max_timestamp, image_path, max_peeq, max_peeq_node]


                    else:
                        odb.close()
                        print("No stress or PEEQ data found in ODB") 
                        return None


                except Exception as e:
                    print(f"Error processing ODB {{self.odb_path}}: {{str(e)}}")
                    if 'odb' in locals():
                        odb.close()  




            def visualize_result(self, instance_name, elset_name, frame_no, max_stress_limit=None, min_stress_limit=None):  
                odb = visualization.openOdb(path=self.odb_path)

                session.Viewport(name='Stress Viewport', origin=(0, 0), width=250, height=150) 
                session.viewports['Stress Viewport'].odbDisplay.basicOptions.setValues(
                averagingThreshold=100)
                vp = session.viewports['Stress Viewport']
                vp.setValues(displayedObject=odb)


                last_step = odb.steps[list(odb.steps.keys())[-1]]
                last_frame = last_step.frames[self.max_frame_no]

                vp.odbDisplay.setFrame(step= last_step.name, frame= frame_no)


                vp.odbDisplay.setPrimaryVariable( 
                    variableLabel='S',
                    outputPosition=INTEGRATION_POINT,
                    refinement=(INVARIANT, 'Max. Principal')
                )


                leaf = LeafFromElementSets((f"{{instance_name}}.{{elset_name}}",))  
                vp.odbDisplay.displayGroup.replace(leaf=leaf) 


                if max_stress_limit and not min_stress_limit:
                    session.viewports['Stress Viewport'].odbDisplay.contourOptions.setValues(
                    maxAutoCompute=OFF, maxValue=max_stress_limit, minAutoCompute=ON)  

                elif min_stress_limit and not max_stress_limit:
                    session.viewports['Stress Viewport'].odbDisplay.contourOptions.setValues(
                    minAutoCompute=OFF, minValue=min_stress_limit, maxAutoCompute=ON) 

                elif max_stress_limit and min_stress_limit:
                    session.viewports['Stress Viewport'].odbDisplay.contourOptions.setValues(
                    maxAutoCompute=OFF, maxValue=max_stress_limit, minAutoCompute=OFF, minValue=min_stress_limit)

                elif not max_stress_limit and not min_stress_limit:
                    session.viewports['Stress Viewport'].odbDisplay.contourOptions.setValues(
                    maxAutoCompute=ON, minAutoCompute=ON)


                vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF,))
                vp.view.setValues(cameraPosition=(200, 200, 200), cameraUpVector=(0, 1, 0))

                output_image_name = os.path.join(self.results_dir, f"{{instance_name}}_{{elset_name}}_sigma_max_plot_frame_{{frame_no}}")
                session.printOptions.setValues(rendition=COLOR)
                session.printToFile(fileName= output_image_name, format=PNG, canvasObjects=(vp,))

                output_image_path = os.path.join(self.results_dir, f"{{instance_name}}_{{elset_name}}_sigma_max_plot_frame_{{frame_no}}.png")

                return  output_image_path




            def create_table_with_image_link(self, dataframe, table_name):            

                df = dataframe 
                df["Image Link"] = df["Image Path"].apply(lambda x: f'=HYPERLINK("{{x}}", "View Image")') 

                styled_df = df.style.applymap(
                    lambda val: 'color: blue; text-decoration: underline', 
                    subset=['Image Link']
                )

                table_path = os.path.join(self.results_dir, table_name) 
                with pd.ExcelWriter(table_path, engine="openpyxl") as writer:
                    styled_df.to_excel(writer, index=False)





        if __name__ == "__main__":  
            analyse_all_parts = AnalyseAllParts(odb_path = r"{odb_path}",
                                                results_dir = r"{results_dir}", 
                                                max_stress_limit= {max_stress_limit},
                                                min_stress_limit= {min_stress_limit}
                                            )
            
            parts_and_elsets = analyse_all_parts.print_elements()  
            
            master_dataset = []
            for instance, elsets in parts_and_elsets.items(): 
                for elset in elsets: 
                    master_dataset_row = analyse_all_parts.extract_results(instance_name = instance , elset_name = elset) 
                    if master_dataset_row is not None:
                        master_dataset.append(master_dataset_row)
                        

            master_df = pd.DataFrame(
                master_dataset,
                columns=["Instance", "Element Set", "Max Principal Stress", "Max Stress Node", "Max Stress Timestamp", "Image Path", "Max PEEQ", "Max PEEQ Node"]
            )
            analyse_all_parts.create_table_with_image_link(dataframe= master_df, table_name= "Master_Dataset_All_Parts_and_Elsets.xlsx")
            
            print("Results saved to Master_Dataset_All_Parts_and_Elsets.xlsx")
        """) 

        with open(script_path, "w") as file: 
                file.write(code) 

        print(f"\nPython script successfully created at: {script_path}\n")
        
        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", f"noGUI=analyse_all_parts.py"]
        subprocess.run(abaqus_command, cwd= current_working_dir, check=True, capture_output=True, text=True, shell=True) 



        def make_clickable(path):
                path = str(path).replace("\\", "/")
                return f'<a href="file:///{path}" target="_blank">View Image</a>'

        master_filename = f"Master_Dataset_All_Parts_and_Elsets.xlsx"
        master_path = os.path.join(results_dir, master_filename)

        try:
            df_master = pd.read_excel(master_path, engine="openpyxl")
            df_master['Image Link'] = df_master['Image Path'].apply(make_clickable) 
            image_paths = df_master["Image Path"]
            df_master.drop(columns=['Image Path'], inplace=True) 

            return df_master, image_paths.tolist()  

        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")







    def ask_analyse_single_part_inputs(self)-> dict: 
        if "odb_file_path" not in st.session_state: 
            st.session_state.odb_file_path = "" 
        if "instance_name" not in st.session_state: 
            st.session_state.instance_name = "" 
        if "elset_name" not in st.session_state: 
            st.session_state.elset_name = ""  


        st.info("This is for analysing a single instance and its elset in the odb file. If you want to analyse all the instances and elsets, please switch to the analyse all parts option instead.")

        odb_file_path= st.text_input(
            "ODB File Location (e.g., path/to/file.odb)",
            value=st.session_state.odb_file_path, 
            key = "odb_path"
        )  
        instance_name = st.text_input(
            "Part Name",
            value=st.session_state.instance_name,
            key="instance_name_input"
        )
        elset_name = st.text_input(
            "Elset Name",
            value=st.session_state.elset_name,
            key="elset_name_input"
        )  
        
        max_stress_limit = st.text_input(
            "Max Stress Limit",
        ) 

        if not max_stress_limit:
            max_stress_limit = None
        
    
        min_stress_limit = st.text_input(
            "Min Stress Limit",
        )

        if not min_stress_limit:
            min_stress_limit = None


        st.session_state.odb_file_path = odb_file_path  
        st.session_state.instance_name = instance_name  
        st.session_state.elset_name = elset_name


        return {
            "odb_file_path": odb_file_path, 
            "instance_name": instance_name, 
            "elset_name": elset_name, 
            "max_stress_limit": float(max_stress_limit) if max_stress_limit else None, 
            "min_stress_limit": float(min_stress_limit) if min_stress_limit else None
        }

    

    def analyse_single_part_task(self, odb_path, instance_name, elset_name, max_stress_limit=None, min_stress_limit=None):
        import os
        import subprocess
        import textwrap 

        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_dir = executions_dir
        script_path = os.path.join(script_dir, "analyse_single_part.py") 
        
        code = textwrap.dedent(f"""
        # -*- coding: mbcs -*-
        from abaqus import *
        from odbAccess import *
        import pandas as pd
        from abaqusConstants import *
        import odbAccess  
        from odbAccess import openOdb 
        import math 
        from collections import defaultdict 
        import visualization 
        from displayGroupOdbToolset import LeafFromElementSets 
        import openpyxl 
        import os


        class AnalyseSinglePart(): 
            def __init__(self, odb_path, instance_name, elset_name, results_dir, max_stress_limit= None, min_stress_limit=None):
                self.odb_path = odb_path
                self.instance_name = instance_name
                self.elset_name = elset_name 
                self.max_frame_no = 0
                self.results_dir = results_dir 
                self.max_stress_limit= max_stress_limit 
                self.min_stress_limit = min_stress_limit

            def extract_results(self):
                try:
                    
                    odb = openOdb(path=self.odb_path)
                    print(f"Opened ODB File: {{self.odb_path}}")

                
                    try:
                        instance = odb.rootAssembly.instances[self.instance_name]
                        if self.elset_name not in instance.elementSets:
                            raise ValueError(f"Elset '{{self.elset_name}}' not found in instance '{{self.instance_name}}'.")
                        elset = instance.elementSets[self.elset_name]
                        print(f"Element set '{{self.elset_name}}' found in instance '{{self.instance_name}}'")
                    except KeyError:
                        raise ValueError(f"Instance '{{self.instance_name}}' not found in ODB")

                
                    last_step_name = list(odb.steps.keys())[-1]
                    step = odb.steps[last_step_name]
                    print(f"Accessing step: {{last_step_name}}")

                
                    max_stress = float('-inf')
                    max_stress_elem = None
                    max_stress_node = None
                    framewise_data = [] 
        
                    max_stress_all_frames = 0
                    max_stress_node_all_frames = 0
                    current_frame_no = 0

                    for frame in step.frames:
                        if 'S' in frame.fieldOutputs:
                            stress_field = frame.fieldOutputs['S'].getSubset(
                                region=elset,
                                position=ELEMENT_NODAL
                            )
                            
                            
                            node_map = defaultdict(list)
                            max_principal_stress= 0 
                            avg =0 
                            for v in stress_field.values:
                                if hasattr(v, 'maxPrincipal') and hasattr(v, 'nodeLabel'):
                                    node_map[v.nodeLabel].append(v.maxPrincipal) 


                            for node_label, stress_list in node_map.items(): 
                                top_n = int(len(stress_list) * 1)
                                top_values = sorted(stress_list, reverse=True)[:top_n]  
                                if len(top_values) !=0:
                                    avg = sum(top_values) / len(top_values)
                            
                                if avg > max_principal_stress:
                                    #print(stress_list)
                                    max_principal_stress = avg
                                    max_stress_node = node_label 

                                    if avg > max_stress_all_frames: 
                                        max_stress_all_frames = avg 
                                        max_stress_node_all_frames = node_label 
                                        self.max_frame_no = current_frame_no
                                        self.max_timestamp = frame.frameValue
                            

                            timestamp = frame.frameValue
                        
                            print(f"Frame {{timestamp}}: Max principal stress: {{max_principal_stress:.6f}}, Node: {{max_stress_node}}")   
                            current_frame_no += 1
                    print(f"max stress all frames: {{max_stress_all_frames}}")



                    max_peeq = 0
                    max_peeq_node = None
                    
                    last_frame = step.frames[-1]
                    if 'PEEQ' in last_frame.fieldOutputs:
                        peeq_field = last_frame.fieldOutputs['PEEQ'].getSubset(
                            region=elset,
                            position=ELEMENT_NODAL
                        )
                        for value in peeq_field.values:
                            if value.data > max_peeq:
                                max_peeq = value.data
                                max_peeq_elem = value.elementLabel
                                try:
                                    max_peeq_node = value.nodeLabel
                                except AttributeError:
                                    max_peeq_node = None

                    
                    if max_stress_node:
                        print(f"Results for ODB:")
                        print(f"Max Principal Stress: {{max_stress_all_frames:.6f}} at Node {{max_stress_node_all_frames}}")
                        print(f"Max PEEQ: {{max_peeq:.6f}} at Node {{max_peeq_node}}")

                        image_path = self.visualize_result(
                                                            frame_no= self.max_frame_no,
                                                            max_stress_limit=self.max_stress_limit, 
                                                            min_stress_limit=self.min_stress_limit
                                                        )

                        master_df = pd.DataFrame(
                            [[max_stress_all_frames, max_stress_node_all_frames, self.max_timestamp, image_path, max_peeq, max_peeq_node]],
                            columns=["Max Principal Stress", "Max Stress Node","Max Stress Timestamp", "Image Path", "Max PEEQ", "Max PEEQ Node"]
                        )
                        self.create_table_with_image_link(dataframe= master_df, table_name= f"Master_Dataset_{{self.instance_name}}_{{self.elset_name}}.xlsx")
                        print(f"Results saved to Master_Dataset_{{self.instance_name}}_{{self.elset_name}}.xlsx")
        

                    else:
                        print("No stress or PEEQ data found in ODB")

                    odb.close()

                except Exception as e:
                    print(f"Error processing ODB {{self.odb_path}}: {{str(e)}}")
                    if 'odb' in locals():
                        odb.close()  




            def visualize_result(self, frame_no, max_stress_limit=None, min_stress_limit=None):  
                odb = visualization.openOdb(path=self.odb_path)

                session.Viewport(name='Stress Viewport', origin=(0, 0), width=250, height=150) 
                session.viewports['Stress Viewport'].odbDisplay.basicOptions.setValues(
                averagingThreshold=100)
                vp = session.viewports['Stress Viewport']
                vp.setValues(displayedObject=odb)

            
                last_step = odb.steps[list(odb.steps.keys())[-1]]
                last_frame = last_step.frames[self.max_frame_no]

                vp.odbDisplay.setFrame(step= last_step.name, frame= frame_no)


                vp.odbDisplay.setPrimaryVariable( 
                    variableLabel='S',
                    outputPosition=INTEGRATION_POINT,
                    refinement=(INVARIANT, 'Max. Principal')
                )


                leaf = LeafFromElementSets((f"{{self.instance_name}}.{{self.elset_name}}",))  # format: 'instanceName.setName'
                vp.odbDisplay.displayGroup.replace(leaf=leaf) 
                

                if max_stress_limit and not min_stress_limit:
                    session.viewports['Stress Viewport'].odbDisplay.contourOptions.setValues(
                    maxAutoCompute=OFF, maxValue=max_stress_limit, minAutoCompute=ON)  

                elif min_stress_limit and not max_stress_limit:
                    session.viewports['Stress Viewport'].odbDisplay.contourOptions.setValues(
                    minAutoCompute=OFF, minValue=min_stress_limit, maxAutoCompute=ON) 
                
                elif max_stress_limit and min_stress_limit:
                    session.viewports['Stress Viewport'].odbDisplay.contourOptions.setValues(
                    maxAutoCompute=OFF, maxValue=max_stress_limit, minAutoCompute=OFF, minValue=min_stress_limit)

                elif not max_stress_limit and not min_stress_limit:
                    session.viewports['Stress Viewport'].odbDisplay.contourOptions.setValues(
                    maxAutoCompute=ON, minAutoCompute=ON)

        
                vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF,))
                vp.view.setValues(cameraPosition=(200, 200, 200), cameraUpVector=(0, 1, 0))

                output_image_name = os.path.join(self.results_dir, f"{{self.instance_name}}_{{self.elset_name}}_sigma_max_plot_frame_{{frame_no}}")
                session.printOptions.setValues(rendition=COLOR)
                session.printToFile(fileName= output_image_name, format=PNG, canvasObjects=(vp,))

                output_image_path = os.path.join(self.results_dir, f"{{self.instance_name}}_{{self.elset_name}}_sigma_max_plot_frame_{{frame_no}}.png")

                return  output_image_path


            

            def create_table_with_image_link(self, dataframe, table_name):            

                df = dataframe 
                df["Image Link"] = df["Image Path"].apply(lambda x: f'=HYPERLINK("{{x}}", "View Image")')

                # Optionally drop the 'File Path' column if you only want name + hyperlink
                # df.drop(columns="Image Path", inplace=True) 
                
                styled_df = df.style.applymap(
                    lambda val: 'color: blue; text-decoration: underline', 
                    subset=['Image Link']
                )
 
                # Export to Excel
                table_path = os.path.join(self.results_dir, table_name) 
                with pd.ExcelWriter(table_path, engine="openpyxl") as writer:
                    styled_df.to_excel(writer, index=False)

            
                    

        if __name__ == "__main__": 
            analyse_single_part = AnalyseSinglePart(odb_path= r"{odb_path}",
                                                    instance_name = "{instance_name}", 
                                                    elset_name= "{elset_name}", 
                                                    results_dir = r"{results_dir}", 
                                                    max_stress_limit= {max_stress_limit},
                                                    min_stress_limit= {min_stress_limit}
                                                ) 

            analyse_single_part.extract_results()  
        """)  

        with open(script_path, "w") as file: 
                file.write(code) 

        print(f"\nPython script successfully created at: {script_path}\n")
        
        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", f"noGUI=analyse_single_part.py"]
        subprocess.run(abaqus_command, cwd= current_working_dir, check=True, capture_output=True, text=True, shell=True)  


        def make_clickable(path):
            path = str(path).replace("\\", "/")
            return f'<a href="file:///{path}" target="_blank">View Image</a>'


        master_filename = f"Master_Dataset_{instance_name}_{elset_name}.xlsx"
        master_path = os.path.join(results_dir, master_filename)


        try:
            df_master = pd.read_excel(master_path, engine="openpyxl")
            df_master['Image Link'] = df_master['Image Path'].apply(make_clickable)
           
            image_path = df_master["Image Path"]
            df_master.drop(columns=['Image Path'], inplace=True)
            
            return df_master, image_path.tolist()     

        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")









    def extract_existing_materials(self, model_name, input_inp_path):
        import textwrap  
        import os
        import subprocess  
        
        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")
        
        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)
        
        script_dir = executions_dir
        script_path = os.path.join(script_dir, "extract_existing_materials.py") 

        code =textwrap.dedent(f"""
        from abaqus import *
        from abaqusConstants import *
        import os 
        import json 

        def check_existing_material(model_name, input_inp_path):
            mdb.ModelFromInputFile(name=model_name, inputFileName=input_inp_path)
            model = mdb.models[model_name]

            material_list = list(model.materials.keys())
            print(material_list)  
            
            data ={{"Existing_Materials": material_list}}
            
            material_list_path = os.path.join(r"{results_dir}", "existing_materials.json")
            with open(material_list_path, "w") as f:
                json.dump(data, f, indent=4) 

            print(f"The existing Materials are: {{material_list}}") 
        
        if __name__ == "__main__":
            inp_path = r"{input_inp_path}"
            model_name = "{model_name}"

            check_existing_material(model_name, inp_path)
        """) 

        with open(script_path, "w") as file: 
                file.write(code) 

        print(f"\nPython script successfully created at: {script_path}\n")
        
        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", f"noGUI=extract_existing_materials.py"]
        subprocess.run(abaqus_command, cwd= current_working_dir, check=True, capture_output=True, text=True, shell=True)
        
        material_list_path = os.path.join(results_dir, "existing_materials.json")

        if os.path.exists(material_list_path):
            with open(material_list_path, "r") as f:
                data = json.load(f)   

            return data["Existing_Materials"] 
        else:
            print(f"{material_list_path} does not exist.")


    
    def extract_part_names_and_images(self, model_name, model_file_path):
        import textwrap  
        import os
        import subprocess   
        import json 
        
        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_dir = executions_dir
        script_path = os.path.join(script_dir, "extract_part_names_and_images.py") 

        code =textwrap.dedent(f"""
        # -*- coding: mbcs -*- 
        from abaqus import *
        from abaqusConstants import *
        import part, material, assembly, step, mesh
        import section, regionToolset
        import os 
        import json
                                

        def create_model(model_name, model_file_path):
            file_ext = os.path.splitext(model_file_path)[1].lower()

            if file_ext == ".inp":
                if model_name in mdb.models:
                    del mdb.models[model_name]
                    
                mdb.ModelFromInputFile(name=model_name, inputFileName=model_file_path) 
                model = mdb.models[model_name]
                print("INP file loaded:", model_name)
                return model

            elif file_ext in [".stp", ".step"]:
                if model_name in mdb.models:
                    del mdb.models[model_name]

                step_geometry = mdb.openStep(fileName = model_file_path) 
                num_parts_in_file = step_geometry.numberOfParts
                print("STEP file contains: %d parts" % num_parts_in_file)

                model = mdb.Model(name=model_name)
                print("Importing parts...")
                imported_parts = []
                failed_imports = []

                for i in range(1, num_parts_in_file + 1):
                    try:
                        part_name = "Part_%d" % i
                        model.PartFromGeometryFile(
                            name=part_name,
                            geometryFile=step_geometry,
                            bodyNum=i,
                            combine=False,
                            dimensionality=THREE_D,
                            type=DEFORMABLE_BODY,
                            scale=1.0
                        )
                        imported_parts.append(part_name)
                        print("Imported: %s" % part_name)

                    except Exception as e:
                        failed_imports.append(i)
                        print("Failed Part %d: %s" % (i, str(e)))

                print("Successfully imported: %d parts" % len(imported_parts))
                print("STEP file loaded:", model_name)
                return model

            else:
                raise ValueError("Unsupported file type: {{}}. Use .inp, .stp, or .step".format(file_ext))


        def print_part_names(model, results_dir):

            part_list = model.parts.keys()
            print(part_list) 
                                
            data ={{"Part_Names": part_list}}

            part_list_path = os.path.join(results_dir, "parts.json")
            with open(part_list_path, "w") as f:
                json.dump(data, f, indent=4)

            print(f"The existing Parts are: {{part_list}}")      

            
        def capture_part_images(model, results_dir):
            vp_name = 'TempViewport'
            session.Viewport(name=vp_name)
            vp = session.viewports[vp_name]

            images_dir = os.path.join(results_dir, "Part_Images")
            if not os.path.exists(images_dir):
                os.makedirs(images_dir, exist_ok=True)

            part_images = {{}}

            for part_name, part in model.parts.items():
                print(f"Capturing image for part: {{part_name}}")

                vp.setValues(displayedObject=part)
                vp.view.fitView()

                image_file = os.path.join(images_dir, f"{{part_name}}.png")
                session.printToFile(fileName=image_file, format=PNG, canvasObjects=(vp,))
                print(f"  -> Saved image as {{image_file}}")

                part_images[part_name] = image_file 

            part_images_path = os.path.join(results_dir, "parts_images.json")
            with open(part_images_path, "w") as f:    
                json.dump(part_images, f, indent=4)  


        if __name__ == "__main__":
            model_file_path = r"{model_file_path}"
            model_name = "{model_name}" 
            results_dir = r"{results_dir}"

            model = create_model(model_name, model_file_path)
            print_part_names(model, results_dir)
            capture_part_images(model, results_dir) 
        """)

        with open(script_path, "w") as file: 
                    file.write(code) 

        print(f"\nPython script successfully created at: {script_path}\n")
        
        current_working_dir = executions_dir 
        abaqus_command = ["abaqus", "cae", f"noGUI=extract_part_names_and_images.py"]
        subprocess.run(abaqus_command, cwd= current_working_dir, check=True, capture_output=True, text=True, shell=True)
        
        part_list_path = os.path.join(results_dir, "parts.json") 
        part_images_path = os.path.join(results_dir, "parts_images.json")

        exist= False
        if os.path.exists(part_list_path):
            with open(part_list_path, "r") as f:
                part_data = json.load(f)    
            exist= True 

        if os.path.exists(part_images_path) and exist:
            with open(part_images_path, "r") as f:
                images_data = json.load(f)

            return part_data["Part_Names"], images_data
        
        else:
            print(f"{part_list_path} or {part_images_path} does not exist.")
    


    def ask_inp_model_name_inputs(self):  

        if "inp_file_path" not in st.session_state: 
            st.session_state.inp_file_path = ""
        if "model_name" not in st.session_state:
            st.session_state.model_name = ""

        inp_file_path= st.text_input(
            "Input File Location (e.g., path/to/file.inp)",
            value=st.session_state.inp_file_path,
            key="inp_file_path_input"
        )  
        model_name = st.text_input(
            "Model Name",
            value=st.session_state.model_name,
            key="model_name_input"
        ) 

        return inp_file_path, model_name 
        

   
    def extract_materials_and_parts_info(self, model_name, inp_file_path):
        existing_materials_list = self.extract_existing_materials(model_name, input_inp_path= inp_file_path) 
        part_names, part_images = self.extract_part_names_and_images(model_name, model_file_path= inp_file_path)  

        return existing_materials_list, part_names, part_images



    def ask_material_assignment_inputs(self, existing_materials_list, part_names, part_images): 
        import os 

        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        material_database = pd.read_excel("src/cae_engine_agentic_ai/knowledge/Material_Properties_Database.xlsx") 
        material_list = sorted(material_database['Name'].dropna().unique())
        material_list.insert(0, "CUSTOM MATERIAL")

        properties ={}

        for i, part_name in enumerate(part_names, start=1):
            st.subheader(part_name) 
            image_path = os.path.normpath(part_images.get(part_name, ""))

            if image_path:
                st.image(image_path, caption=f"{part_name}", use_column_width=True)
                
            selected_material = st.selectbox(f"{part_name} Material", material_list)
            renamed_part_name = st.text_input(f"Rename {part_name} (Optional)", value=part_name, key= f"{part_name}_rename")

            if selected_material == "CUSTOM MATERIAL": 
                col1, col2, col3, col4 = st.columns(4)
                col1.markdown("**Elastic Properties:**")
                col1.write(" ")
                col1.write(" ")
                col1.write(" ")
                e = col2.text_input("Young's Modulus", key = f"{part_name}_e")
                p = col3.text_input("Poisson's Ratio", key = f"{part_name}_p")
                d = col4.text_input("Density",key = f"{part_name}_d")
    
                col1.markdown("**Plastic Properties:**")
                y1 = col2.text_input("Yield1", key = f"{part_name}_y1")
                ps1 = col3.text_input("Plastic Strain1", key = f"{part_name}_ps1")
                t1 = col4.text_input("Temp1",key = f"{part_name}_t1")

                y2 = col2.text_input("Yield2", key = f"{part_name}_y2")
                ps2 = col3.text_input("Plastic Strain2", key = f"{part_name}_ps2")
                t2 = col4.text_input("Temp2",key = f"{part_name}t2")

            else:
                if selected_material in existing_materials_list:
                    st.info("This material already defined in the model. Modifying the properties will change the defined material")
                
                Density	= material_database.loc[material_database['Name'] == selected_material, 'Density'].iloc[0]
                Y_mod = material_database.loc[material_database['Name'] == selected_material, 'E'].iloc[0]
                Nu = material_database.loc[material_database['Name'] == selected_material, 'Nu'].iloc[0]	
                YieldStress1 = material_database.loc[material_database['Name'] == selected_material, 'YieldStress1'].iloc[0]		
                PlasticStrain1 = material_database.loc[material_database['Name'] == selected_material, 'PlasticStrain1'].iloc[0]
                Temp1 = material_database.loc[material_database['Name'] == selected_material, 'Temp1'].iloc[0]
                YieldStress2 = material_database.loc[material_database['Name'] == selected_material, 'YieldStress2'].iloc[0]
                PlasticStrain2 = material_database.loc[material_database['Name'] == selected_material, 'PlasticStrain2'].iloc[0]
                Temp2 = material_database.loc[material_database['Name'] == selected_material, 'Temp2'].iloc[0]

                col1, col2, col3, col4 = st.columns(4)
                col1.markdown("**Elastic Properties:**")
                col1.write(" ")
                col1.write(" ")
                col1.write(" ")
                e = col2.text_input("Young's Modulus", value = Y_mod, key = f"{part_name}_e")
                p = col3.text_input("Poisson's Ratio", value = Nu, key = f"{part_name}_p")
                d = col4.text_input("Density", value = Density, key = f"{part_name}_d")
    
                col1.markdown("**Plastic Properties:**")
                y1 = col2.text_input("Yield1", value = "" if YieldStress1 is None else str(YieldStress1), key = f"{part_name}_y1")
                ps1 = col3.text_input("Plastic Strain1", value = "" if PlasticStrain1 is None else str(PlasticStrain1), key = f"{part_name}_ps1")
                t1 = col4.text_input("Temp1", value = "" if Temp1 is None else str(Temp1), key = f"{part_name}_t1")

                y2 = col2.text_input("Yield2", value = "" if YieldStress2 is None else str(YieldStress2), key = f"{part_name}_y2")
                ps2 = col3.text_input("Plastic Strain2", value = "" if PlasticStrain2 is None else str(PlasticStrain2), key = f"{part_name}_ps2")
                t2 = col4.text_input("Temp2", value = "" if Temp2 is None else str(Temp2), key = f"{part_name}t2")

            section_type = st.radio(
                f"{part_name} Section Type",
                ["Solid", "Shell"]
            )
            
            properties[part_name] = {
                "Material": selected_material, 
                "Section Type": section_type, 
                "Young's Modulus": None if (e == "" or str(e).lower() == "nan") else float(e),
                "Poisson's Ratio": None if (p == "" or str(p).lower() == "nan") else float(p),
                "Density": None if (d == "" or str(d).lower() == "nan") else float(d),
                "Yield1": None if (y1 == "" or str(y1).lower() == "nan") else float(y1),
                "Plastic Strain1": None if (ps1 == "" or str(ps1).lower() == "nan") else float(ps1),
                "Temp1": None if (t1 == "" or str(t1).lower() == "nan") else float(t1),
                "Yield2": None if (y2 == "" or str(y2).lower() == "nan") else float(y2),
                "Plastic Strain2": None if (ps2 == "" or str(ps2).lower() == "nan") else float(ps2),
                "Temp2": None if (t2 == "" or str(t2).lower() == "nan") else float(t2), 
                "Renamed Part Name": renamed_part_name
            }

        part_material_properties_path = os.path.join(results_dir, "part_material_properties.json")
        with open(part_material_properties_path, "w") as f:    
            json.dump(properties, f, indent=4)  
    


    def assign_material_properties_tasks(self, inp_file_path, model_name): 
        import textwrap  
        import os
        import subprocess  
        
        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_dir = executions_dir
        script_path = os.path.join(script_dir, "material_assignment.py")  

        code =textwrap.dedent(f"""
        from abaqus import *
        from abaqusConstants import *
        import os 
        import json 


        def create_model(model_name, input_inp_path):

            mdb.ModelFromInputFile(name=model_name, inputFileName=input_inp_path)
            model = mdb.models[model_name]
        
            print(model.materials)
            return model 
                              


        def rename_part(model, part_name, renamed_part_name):  
            model.parts.changeKey(fromName=part_name, toName= renamed_part_name)

            assembly = model.rootAssembly
            assembly.features.changeKey(fromName=part_name, toName=renamed_part_name)
            assembly.regenerate()



        def modify_or_create_material(model, part_name, material_name, section_type, density, y_mod, u, y1, ps1, t1, y2, ps2, t2):

            if material_name in model.materials.keys():
                material = model.materials[material_name]
                print(f"Modified existing material '{{material_name}}'")
            else:
                material = model.Material(name=material_name)
                print(f"Created new material '{{material_name}}'")

            new_elastic = (y_mod, u) 

            material.Elastic(table=(new_elastic,))
            material.Density(table=((density,),)) 

            
            # ---- Plastic Behavior ----
            if y1 is None or ps1 is None:
                print("in condition 1 (no plasticity defined)")

            elif (y1 is not None and ps1 is not None and t1 is None 
                and (y2 is None or ps2 is None)):
                print("in condition 2 (1 yield, no temp, no 2nd yield)")
                new_plastic1 = (y1, ps1)
                material.Plastic(temperatureDependency=OFF, scaleStress=None, table=(new_plastic1,))

            elif (y1 is not None and ps1 is not None and t1 is not None 
                and (y2 is None or ps2 is None)):
                print("in condition 3 (1 yield with temp)")
                new_plastic1 = (y1, ps1, t1)
                material.Plastic(temperatureDependency=ON, scaleStress=None, table=(new_plastic1,))

            elif (y1 is not None and ps1 is not None and y2 is not None and ps2 is not None 
                and (t1 is None or t2 is None)):
                print("in condition 4 (2 yields, no temp)")
                new_plastic1 = (y1, ps1)
                new_plastic2 = (y2, ps2)
                material.Plastic(temperatureDependency=OFF, scaleStress=None, table=(new_plastic1, new_plastic2))

            elif (y1 is not None and ps1 is not None and t1 is not None 
                and y2 is not None and ps2 is not None and t2 is not None):
                print("in condition 5 (2 yields with both temps)")
                new_plastic1 = (y1, ps1, t1)
                new_plastic2 = (y2, ps2, t2)
                material.Plastic(temperatureDependency=ON, scaleStress=None, table=(new_plastic1, new_plastic2))

            
            
            section_name = material_name + "_Section" 
            if section_name in model.sections.keys():
                print(f"Section '{{section_name}}' already exists. Modifying...")
                del model.sections[section_name] 
                              
            if section_type == "Solid":
                model.HomogeneousSolidSection(name=section_name, material=material_name)
                print(f"Solid Homogenous Section '{{section_name}}' created.")  
            elif section_type == "Shell": 
                model.HomogeneousShellSection(name=section_name, 
                preIntegrate=OFF, material=material_name, thicknessType=UNIFORM, 
                thickness=5.0, thicknessField='', nodalThicknessField='', 
                idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
                thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
                    integrationRule=SIMPSON, numIntPts=5)
                


            part = model.parts[part_name]
            print(f"Now in {{part_name}}")

            for elset_name, elset_obj in part.sets.items():

                part.SectionAssignment(
                    region=elset_obj,
                    sectionName=section_name
                )

                print(f"Section '{{section_name}}' assigned to set '{{elset_name}}' in part '{{part_name}}'.")
            

            model.sections[section_name].setValues(
                    material=material_name, thickness=1.0)
        

        def save_cae_file(job_name, results_dir): 
            cae_file = os.path.join(results_dir, f"{{job_name}}.cae")
            mdb.saveAs(pathName=cae_file)
            print(f"Saved modified model to {{cae_file}}")   
            mdb.close() 

 
        def save_inp_file(model_name, results_dir): 
            job_name = f"{{model_name}}_Material_Assigned"
            os.chdir(results_dir)
            mdb.Job(name=job_name, model=model_name)
            mdb.jobs[job_name].writeInput(consistencyChecking=OFF)
            
            inp_file = os.path.join(results_dir, f"{{model_name}}_Material_Assigned.inp")
            print(f"Saved the model to {{inp_file}}")   

            temp_mesh_file = os.path.join(results_dir, "temp_mesh.inp")
            if os.path.exists(temp_mesh_file):
                os.remove(temp_mesh_file) 
                print(f"Removed temporary file: {{temp_mesh_file}}") 
            
            return job_name




        if __name__ == "__main__":
            inp_path = os.path.normpath(r"{inp_file_path}")
            model_name = "{model_name}" 
            results_dir = r"{results_dir}" 
            materials_property_path = os.path.join(results_dir, "part_material_properties.json")

            
            with open(materials_property_path, "r") as f:
                properties = json.load(f) 

            model = create_model(model_name, inp_path)  

            for part_name, material_properties in properties.items():  
                modify_or_create_material(model= model, 
                                        part_name = part_name, 
                                        material_name = material_properties["Material"], 
                                        section_type = material_properties["Section Type"], 
                                        density = material_properties["Density"],
                                        y_mod = material_properties["Young's Modulus"],
                                        u = material_properties["Poisson's Ratio"], 
                                        y1 = material_properties["Yield1"],
                                        ps1 = material_properties["Plastic Strain1"],
                                        t1 = material_properties["Temp1"],
                                        y2 = material_properties["Yield2"],
                                        ps2 = material_properties["Plastic Strain2"],
                                        t2 = material_properties["Temp2"]
                                        )  
                rename_part(model = model, part_name= part_name, renamed_part_name= material_properties["Renamed Part Name"])

            job_name = save_inp_file(model_name= model_name, results_dir = results_dir) 
            save_cae_file(job_name = job_name, results_dir = results_dir)  

        """) 

        with open(script_path, "w") as file: 
            file.write(code) 

        print(f"\nPython script successfully created at: {script_path}\n")
        
        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", f"noGUI=material_assignment.py"]
        subprocess.run(abaqus_command, cwd= current_working_dir, check=True, capture_output=True, text=True, shell=True)


    




    def cad_to_inp_task(self, step_file_path, model_name, mesh_info_path):
        import os
        import subprocess
        import textwrap

        base_dir = os.path.abspath(self.working_dir)
        executions_dir = os.path.join(base_dir, "Executions")
        results_dir = os.path.join(base_dir, "Results")

        os.makedirs(executions_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)

        script_dir = executions_dir
        script_path = os.path.join(script_dir, "CAD_Mesh_Material.py") 


        code= textwrap.dedent(f""" 
        # -*- coding: mbcs -*-
        from abaqus import *
        from abaqusConstants import *
        import part, material, assembly, step, mesh
        import section, regionToolset
        import os 
        import json 

                                  
        def mesh_assembly(step_file_path, model_name, results_dir, mesh_info):
            print("AUTOMATIC STEP FILE IMPORT")


            step_geometry = mdb.openStep(fileName=step_file_path)
            num_parts_in_file = step_geometry.numberOfParts
            print("STEP file contains: %d parts" % num_parts_in_file)


            if model_name in mdb.models:
                del mdb.models[model_name]
            mdb.Model(name=model_name)
            model = mdb.models[model_name]
            print("Created model: %s" % model_name)


            print("Importing parts...")
            imported_parts = []
            failed_imports = []

            for i in range(1, num_parts_in_file + 1):
                try:
                    part_name = "Part_%d" % i
                    model.PartFromGeometryFile(
                        name=part_name,
                        geometryFile=step_geometry,
                        bodyNum=i,
                        combine=False,
                        dimensionality=THREE_D,
                        type=DEFORMABLE_BODY,
                        scale=1.0
                    )
                    imported_parts.append(part_name)
                    print("Imported: %s" % part_name)

                except Exception as e:
                    failed_imports.append(i)
                    print("Failed Part %d: %s" % (i, str(e)))

            print("Successfully imported: %d parts" % len(imported_parts))


            valid_parts = []
            for part_name in imported_parts:
                part_obj = model.parts[part_name]
                num_cells = len(part_obj.cells)
                num_faces = len(part_obj.faces)

                if num_cells > 0 or num_faces > 0:
                    valid_parts.append(part_name)

            print("Valid parts for meshing: %d" % len(valid_parts))


            print("Creating assembly...")
            assembly = model.rootAssembly

            created_instances = []
            for part_name in valid_parts:
                try:
                    instance_name = "%s" % part_name
                    assembly.Instance(
                        name=instance_name,
                        part=model.parts[part_name],
                        dependent=OFF 
                    )
                    created_instances.append(instance_name)
                    print("Created instance: %s" % instance_name)
                except Exception as e:
                    print("Failed instance %s: %s" % (part_name, str(e)))


            print("Meshing at assembly level...")
            meshed_instances = []
            total_elements = 0
            total_nodes = 0
            elem = False 
            
            for instance_name, instance_info in mesh_info.items():
            #for instance_name in created_instances:
                element_type = instance_info["element_type"]
                mesh_size = instance_info["mesh_size"]

                try:
                    instance = assembly.instances[instance_name]


                    assembly.seedPartInstance(
                        regions=(instance,),
                        size= mesh_size,
                        deviationFactor=0.1,
                        minSizeFactor=0.1
                    )

                
                    cells = instance.cells
                    if len(cells) > 0:
                        try:
                            if element_type in ["C3D8R", "C3D8I"]:
                                assembly.setMeshControls(
                                    regions=cells,
                                    technique=SWEEP,
                                    elemShape=HEX 
                                )
                                elem =True
                            else:
                                assembly.setMeshControls(
                                    regions=cells,
                                    technique=FREE,
                                    elemShape=TET
                                )   
                                elem =False

                        except:  
                            assembly.setMeshControls(
                                    regions=cells,
                                    technique=FREE,
                                    elemShape=TET
                                )  
                            elem =False

                        
                        if element_type == "C3D10":
                            elem_type = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD)
                        elif element_type == "C3D4":
                            elem_type = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD) 
                        elif element_type == "C3D8R" and not elem:
                            elem_type = mesh.ElemType(elemCode=C3D10M, elemLibrary=STANDARD)  
                        elif element_type == "C3D8I"and not elem:
                            elem_type = mesh.ElemType(elemCode=C3D10M, elemLibrary=STANDARD) 
                        elif element_type == "C3D8R" and elem:
                            elem_type = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD)  
                        elif element_type == "C3D8I"and elem:
                            elem_type = mesh.ElemType(elemCode=C3D8I, elemLibrary=STANDARD) 
                        elif element_type == "C3D10M":
                            elem_type = mesh.ElemType(elemCode=C3D10M, elemLibrary=STANDARD)
                        elif element_type == "C3D10HS":
                            elem_type = mesh.ElemType(elemCode=C3D10HS, elemLibrary=STANDARD) 
                        else:
                            elem_type = mesh.ElemType(elemCode=C3D10M, elemLibrary=STANDARD)


                        region = regionToolset.Region(cells=cells)
                        assembly.setElementType(regions=region, elemTypes=(elem_type,))

                    
                    assembly.generateMesh(regions=(instance,)) 


                    elements = len(instance.elements)
                    nodes = len(instance.nodes)

                    print("Meshed %s: %d elements, %d nodes" % (instance_name, elements, nodes))

                    meshed_instances.append(instance_name)
                    total_elements += elements
                    total_nodes += nodes

                except Exception as e:
                    print("Meshing error on instance %s: %s" % (instance_name, str(e)))


            print("SUMMARY")
            print("Parts detected: %d" % num_parts_in_file)
            print("Parts imported: %d" % len(imported_parts))
            print("Instances meshed: %d" % len(meshed_instances))
            print("Total elements: %d" % total_elements)
            print("Total nodes: %d" % total_nodes)

            if len(meshed_instances) == len(valid_parts):
                print("SUCCESS: All %d instances meshed at assembly level" % len(valid_parts))
            else:
                print("Partial success: %d/%d instances meshed" % (len(meshed_instances), len(valid_parts)))   


            for instance_name, instance_info in mesh_info.items():
                renamed_part_name = instance_info["renamed_part_name"]
                rename_part(model, instance_name, renamed_part_name)


            job_name = f"temp_inp"
            os.chdir(results_dir)
            mdb.Job(name=job_name, model=model_name)
            mdb.jobs[job_name].writeInput(consistencyChecking=OFF)
            
            inp_file = os.path.join(results_dir, "temp_inp.inp")
            print(f"Saved the model to {{inp_file}}")
            mdb.close()

            return inp_file



        def rename_part(model, part_name, renamed_part_name):  
            model.parts.changeKey(fromName=part_name, toName= renamed_part_name)

            assembly = model.rootAssembly
            assembly.features.changeKey(fromName=part_name, toName=renamed_part_name)
            assembly.regenerate()
                              


        def create_elset(temp_inp_file, model_name):
            file_path = temp_inp_file 

            if not os.path.exists(file_path):
                raise ValueError("File not found: " + file_path)

            print("Opening file:", file_path)
            mdb.ModelFromInputFile(name=model_name, inputFileName=file_path)

            model = mdb.models[model_name]
            print("Working on model:", model_name)

            print("Creating ALL_ELEMENTS sets at PART level...")
            for part_name, part in model.parts.items(): 
                if len(part.elements) > 0:   # only if the part has elements
                    elems = part.elements[:]
                    if 'ALL_ELEMENTS' in part.sets.keys():
                        del part.sets['ALL_ELEMENTS']
                    part.Set(name='ALL_ELEMENTS', elements=elems) 
                    print("  -> Part:", part_name, "set created.")
            



        def save_cae_file(cae_file_path): 
            print("Saving model...")
            try:
                mdb.saveAs(pathName=cae_file_path)
                print("Saved: %s" % cae_file_path)
            except Exception as e:
                print("Save error: %s" % str(e))




        def save_inp_file(job_name, results_dir, model_name, temp_inp_file):

            job = mdb.Job(name=job_name, model=model_name) 
            os.chdir(results_dir)
            job.writeInput(consistencyChecking=OFF)
            print(f".inp file written in current directory: {{job_name}}.inp")

            if os.path.exists(temp_inp_file):
                os.remove(temp_inp_file) 
                print(f"Removed temporary file: {{temp_inp_file}}") 

            mdb.close()

            return os.path.join(results_dir, job_name + '.inp') 




        def print_step_attributes(step_file_path):
            step_geometry = mdb.openStep(fileName=step_file_path)
            print("Attributes and methods of step_geometry:")
            for attr in dir(step_geometry):
                print(attr) 


            


        if __name__ == "__main__":   
            step_file_path = r"{step_file_path}"
            model_name = "{model_name}"
            results_dir = r"{results_dir}"
            
            json_file_path = r"{mesh_info_path}"
            with open(json_file_path, "r") as f: 
                mesh_info = json.load(f) 

            temp_inp_file = mesh_assembly(
                step_file_path = step_file_path,
                model_name = model_name,
                results_dir = results_dir,
                mesh_info = mesh_info
            )

            create_elset(temp_inp_file = temp_inp_file, model_name = model_name)
            temp_mesh_file = save_inp_file(job_name= "temp_mesh", results_dir= results_dir, model_name= model_name, temp_inp_file= temp_inp_file)
        """)  

        with open(script_path, "w") as file: 
                file.write(code) 

        print(f"\nPython script successfully created at: {script_path}\n")
        
        current_working_dir = executions_dir
        abaqus_command = ["abaqus", "cae", f"noGUI=CAD_Mesh_Material.py"]
        subprocess.run(abaqus_command, cwd=current_working_dir, check=True, capture_output=True, text=True, shell=True) 

        temp_mesh_file = os.path.join(results_dir, "temp_mesh.inp") 
        return temp_mesh_file
