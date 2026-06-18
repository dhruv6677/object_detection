import os
ARTIFACT_DIR: str = "artifacts"

DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_DOWNLOAD_URL: str = "https://github.com/entbappy/Branching-tutorial/raw/master/Sign_language_data.zip"

'''
Data Validation related constants starts with DATA_VALIDATION VAR NAME
'''
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_STATUS_FILE: str = "status.txt"
DATA_VALIDATION_ALL_REQUIRED_FILES = [ "train", "test","data.yaml"]

'''
Model Trainer related constants starts with MODEL_TRAINER VAR NAME
'''
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_PRETRAINED_MODEL_NAME: str = "yolov5s.pt"
MODEL_TRAINER_NO_EPOCHS: int = 1
MODEL_TRAINER_BATCH_SIZE: int = 16