import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from text_summarizer.logging import logger
from text_summarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from text_summarizer.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from text_summarizer.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline

stages = [
    ("Data Ingestion Stage", DataIngestionTrainingPipeline),
    ("Data Validation Stage", DataValidationTrainingPipeline),
    ("Data Transformation Stage", DataTransformationTrainingPipeline),
]

for name, pipeline_cls in stages:
    try:
        logger.info(f">>>>>> {name} started <<<<<<")
        pipeline_cls().main()
        logger.info(f">>>>>> {name} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
