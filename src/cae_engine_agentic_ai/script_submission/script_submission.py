import streamlit as st
import subprocess
import os

class AbaqusScriptExecutor:
    def __init__(self, working_directory: str): 
        self.working_directory = os.path.abspath(working_directory)
        self.script_path = os.path.join(self.working_directory, "submitted_script.py")

    def write_script(self, code: str):
        with open(self.script_path, "w") as file:
            file.write(code)

    def run_script(self):
        abaqus_command = ["abaqus", "cae", "noGUI=submitted_script.py"]
        subprocess.run(
            abaqus_command,
            cwd=self.working_directory,
            check=True,
            capture_output=True,
            text=True,
            shell=True
        )
    

    def run(self):

        code_input = st.text_area("Enter your code here", height=900)

        if code_input and st.button("Submit"):
            with st.spinner("Execution in progress..."):
                try:
                    self.write_script(code_input)
                    self.run_script()
                    st.success("Script executed successfully!")
                except subprocess.CalledProcessError as e:
                    st.error("Execution failed.")
                    st.text_area("Error Output", value=e.stderr, height=300)





    
