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
        Execute this tool whenever user wants to create/generate input files. Also display the message that the 
        process has started only after executing this and nothing before executing this...
        """
        pass  


    def cad_to_mesh_assembly():
        """ 
        Initiates the input collection process from the user for converting a CAD assembly into a meshed model. 
        This tool does not ask user input. It just calls the other tool where the user input will be required. 
        Execute this tool whenever the user wants to convert a CAD assembly into a meshed model. This is only for assembly and not for 
        a single part model. Also display the message that the process has started...
        """
        pass  


    def cad_to_mesh(): 
        """  
        Initiates the input collection process from the user for converting a CAD part into a meshed model. 
        This tool does not ask user input. It just calls the other tool where the user input will be required. 
        Execute this tool whenever the user wants to convert a CAD assembly into a meshed model. This is only for a single part  
        and not for an assembly. Also display the message that the process has started...
        """
        pass    


    def analyse_all_parts(): 
        """  
        Initiates the analysis process for all parts and their respective element sets present in the provided ODB file.
        This tool does not directly collect user inputs but invokes the analysis workflow on all available parts and elsets.
        Execute this tool whenever the user want to extract results like max principal stress and PEEQ data from all parts/instances
        from an odb file.
        Note: This fetches the resultacross all parts/instances in the odb file and not just for a given part/instance and an elset.
        """
        pass   














