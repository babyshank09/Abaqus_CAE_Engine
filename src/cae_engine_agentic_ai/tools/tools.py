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
        process has started...
        """
        pass  


    def cad_to_mesh_assembly():
        """ 
        Initiates the input collection process from the user for converting a CAD assembly into a meshed model. 
        This tool does not ask user input. It just calls the other tool where the user input will be required. 
        Execute this tool whenever user wants to convert a CAD assembly into a meshed model. This is only for assembly and not for 
        a single part model. Also display the message that the process has started...
        """
        pass  


    def cad_to_mesh(): 
        """  
        Initiates the input collection process from the user for converting a CAD part into a meshed model. 
        This tool does not ask user input. It just calls the other tool where the user input will be required. 
        Execute this tool whenever user wants to convert a CAD assembly into a meshed model. This is only for a single part  
        and not for an assembly. Also display the message that the process has started...
        """
        pass  











