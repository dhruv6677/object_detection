import os
import sys
import subprocess
import yaml
from pathlib import Path
from signLanguage.utils.main_utils import read_yaml_file
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifacts_entity import DataValidationArtifact, ModelTrainerArtifact


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_validation_artifact: DataValidationArtifact,
    ):
        self.model_trainer_config = model_trainer_config
        self.data_validation_artifact = data_validation_artifact

    def _prepare_data_yaml(self, feature_store: Path) -> Path:
        data_yaml = feature_store / "data.yaml"
        dataset_cfg = yaml.safe_load(data_yaml.read_text())
        # dataset_cfg.update({
        #     "path": str(feature_store.resolve()),
        #     "train": "train/images",
        #     "val": "test/images",
        # })
        dataset_cfg.update({
            "path": str(feature_store.resolve()),           # absolute path
            # absolute
            "train": str((feature_store / "train" / "images").resolve()),
            # absolute
            "val": str((feature_store / "test" / "images").resolve()),
        })
        train_data_yaml = feature_store / "data_train.yaml"
        train_data_yaml.write_text(yaml.dump(dataset_cfg, sort_keys=False))
        return train_data_yaml

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info(
                "Entered initiate_model_trainer method of ModelTrainer class")
            os.makedirs(
                self.model_trainer_config.model_trainer_dir, exist_ok=True)

            feature_store = Path(
                self.data_validation_artifact.validated_data_dir)
            train_data_yaml = self._prepare_data_yaml(feature_store)

            project_root = Path(__file__).resolve().parents[2]
            yolov5_dir = project_root / "yolov5"
            runs_dir = os.path.join(
                self.model_trainer_config.model_trainer_dir, "runs")

            cmd = [
                sys.executable,
                "train.py",
                "--img", "640",
                "--batch", str(self.model_trainer_config.batch_size),
                "--epochs", str(self.model_trainer_config.no_epochs),
                "--data", str(train_data_yaml.resolve()),
                "--cfg", "models/customyolov5s.yaml",
                "--weights", "yolov5s.pt",
                "--name", "sign_language",
                "--project",  str(Path(runs_dir).resolve()),
            ]
            logging.info(f"Starting YOLOv5 training: {' '.join(cmd)}")
            subprocess.run(cmd, cwd=yolov5_dir, check=True)

            weights_dir = Path(runs_dir) / "sign_language" / "weights"
            trained_model = weights_dir / "best.pt"
            if not trained_model.exists():
                trained_model = weights_dir / "last.pt"

            artifact = ModelTrainerArtifact(
                trained_model_file_path=str(trained_model))
            logging.info(
                "Exited initiate_model_trainer method of ModelTrainer class")
            return artifact
        except Exception as e:
            raise SignException(e, sys) from e
