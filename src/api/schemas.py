from enum import Enum

from pydantic import BaseModel


class TumorType(str, Enum):
    no_tumor = "No Tumor"
    tumor = "Tumor"


class PredictionResponse(BaseModel):
    """
    Schema for prediction response of the brain tumor classification.
    """

    label: TumorType
    confidence: float
