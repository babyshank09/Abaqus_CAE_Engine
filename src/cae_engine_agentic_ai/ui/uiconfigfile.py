import os 
from configparser import ConfigParser 


class Config: 
    def __init__(self, config_file ="./src/cae_engine_agentic_ai/ui/uiconfigfile.ini"): 
        self.config = ConfigParser()  
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config.read_file(f) 

    def get_llm_options(self): 
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ") 
    
    def get_usecase_options(self): 
        return self.config["DEFAULT"].get("USECASE_OPTIONS").split(", ") 
    
    def get_title(self): 
        return self.config["DEFAULT"].get("PAGE_TITLE") 
    
    def get_icon(self): 
        return self.config["DEFAULT"].get("PAGE_ICON") 
    
    def get_openai_model_options(self): 
        return self.config["DEFAULT"].get("OPENAI_MODEL_OPTIONS").split(", ") 
    



