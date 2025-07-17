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
        This tool does not directly collect user inputs but invokes the analysis workflow for the selected instance and elset.
        Execute this tool whenever the user wants to extract results like max principal stress and PEEQ data from a single part/instance
        and a specified elset within an ODB file or asks whether this task can be accomplished. Display the message that the process has 
        started only after this function is executed,and not before.
        Note: This fetches results only for the given part/instance and elset, not across all parts.
        """
        pass














