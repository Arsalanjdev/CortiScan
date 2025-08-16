from fastapi import APIRouter, File, UploadFile
from schemas import PredictionResponse

from src.model.inference import infer
from src.model.preprocess import normalize_single_file

router = APIRouter()


@router.get("/predict/", response_model=PredictionResponse, status_code=200)
async def upload_file(
    image: UploadFile = File(
        ..., description="Upload MRI brain picture.", max_length=1024 * 1024
    ),
):
    # preprocessing the image
    image = normalize_single_file(image)

    # inference
    label, confidence = infer(image)
    return {"label": label, "confidence": confidence}
