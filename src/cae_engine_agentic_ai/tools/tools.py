from typing import Optional
import os  
import streamlit as st

class Tools:
    def __init__(self): 
        pass 


    def generate_inp_scripts():
        """
        Collects user input and initiates the generation of Abaqus input files for 
        parametric simulations involving rotational transformations and clearance validation. 
        This tool does not ask user input. It just calls the other tool where the user input will be required. 
        Execute this tool whenever user wants to create/generate input files or asks whether this task can be accomplished.
        Also, display the message that the process has started only after executing this and nothing before executing this...
        """
        pass  


    def cad_to_mesh_assembly():
        """ 
        Initiates the input collection process from the user for converting a CAD assembly into a meshed model. 
        This tool does not ask user input. It just calls the other tool where the user input will be required. 
        Execute this tool whenever the user wants to convert a CAD assembly into a meshed model. This is only for assembly and not for 
        a single part model.  Also, display the message that the process has started only
        after executing this and nothing before executing this...
        """
        pass  


    def cad_to_mesh(): 
        """  
        Initiates the input collection process from the user for converting a CAD part into a meshed model. 
        This tool does not ask user input. It just calls the other tool where the user input will be required. 
        Execute this tool whenever the user wants to convert a CAD assembly into a meshed model. This is only for a single part  
        and not for an assembly.  Also, display the message that the process has started only 
        after executing this and nothing before executing this...
        """
        pass    


    def analyse_all_parts(): 
        """  
        Initiates the analysis process for all parts and their respective element sets present in the provided ODB file.
        This tool also displays the image of the contour plot of the results of max principal stress for all the 
        instances/parts and its elsets in the form of a link in a table that will be generated. 
        This tool does not directly collect user inputs but invokes the analysis workflow on all available parts and elsets.
        Execute this tool whenever the user wants to extract results like max principal stress and PEEQ data from all parts/instances
        from an odb file or asks whether this task can be accomplished. Display the message that the process has 
        started only after this function is executed,and not before. Also display the message that the process has started only
        after executing this and nothing before executing this...
        Note: This fetches the result across all parts/instances in the odb file and not just for a given part/instance and an elset.
        """
        pass    


    def analyse_single_part():
        """
        Initiates the analysis process for a specific part/instance and its associated element set from the provided ODB file.
        This tool also displays the image of the contour plot of the results of max principal stress for a particular 
        instance/part and its elset in the form of a link in a table that will be generated. 
        This tool does not directly collect user inputs but invokes the analysis workflow for the selected instance and elset.
        Execute this tool whenever the user wants to extract results like max principal stress and PEEQ data from a single part/instance
        and a specified elset within an ODB file or asks whether this task can be accomplished. Display the message that the process has 
        started only after this function is executed,and not before. Also display the message that the process has started only
        after executing this and nothing before executing this...
        Note: This fetches results only for the given part/instance and elset, not across all parts.
        """
        pass 
    

    def assign_material_properties():
        """
        Initiates the workflow for assigning material properties to a specified part or set of parts within the current model.
        This tool does not directly assign the properties but triggers the setup process where the user will define material
        parameters such as elastic modulus, Poisson's ratio, density, or any other relevant attributes. The actual assignment
        will occur in the subsequent steps of the workflow.
        Execute this tool whenever the user wants to assign or modify material properties for a specific part,
        multiple parts, or a material definition within the model, or inquires whether this task can be performed.
        Display the message that the process has started only after this function is executed, and not before.
        Note: This tool initiates the process for assigning material properties but does not perform the assignment itself.
        """
        pass  


    def cad_to_inp():
        """
        Initiates the end-to-end workflow for converting a CAD model into a simulation-ready input file (.inp).
        This tool automates the intermediate stages including geometry import, meshing, material assignment,
        and preparation of the analysis setup. The final output of this process is a fully generated Abaqus
        input file that can be directly used for simulation runs.
        Execute this tool whenever the user wants to seamlessly transform a CAD model into a structured
        simulation file without manually performing each step. It is particularly useful for streamlining
        repetitive preprocessing tasks, ensuring consistency, and reducing setup time.
        Display the message that the process has started only after this function is executed, and not before.
        Note: This tool orchestrates the CAD-to-INP pipeline but does not individually expose the intermediate
        meshing or material assignment operations outside of its workflow.
        """
        pass


TOOLS = [
    Tools.cad_to_inp, 
    Tools.assign_material_properties, 
    Tools.analyse_single_part, 
    Tools.analyse_all_parts, 
    Tools.cad_to_mesh,
    Tools.cad_to_mesh_assembly, 
    Tools.generate_inp_scripts
]











