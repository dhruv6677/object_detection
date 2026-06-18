import os.path
import sys
import yaml
import base64
from signLanguage.exception import SignException
from signLanguage.logger import logging

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            logging.info(f"Reading yaml file: {file_path}")
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SignException(e,sys) 

def write_yaml_file(file_path:str,content:object):
    try:
        with open(file_path,'w') as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise SignException(e,sys)
    
def decodeImage(b64_image_string:str,image_path:str):
    try:
        with open(image_path,'wb') as image_file:
            image_file.write(base64.b64decode(b64_image_string))
    except Exception as e:
        raise SignException(e,sys)
def encodeImageIntoBase64(image_path:str) -> str:
    try:
        with open(image_path,'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        raise SignException(e,sys)
