from fastapi import APIRouter, File, UploadFile

from src.api.schemas import PredictionResponse
from src.model.inference import infer
from src.model.preprocess import normalize_single_file

router = APIRouter()


@router.post("/predict/", response_model=PredictionResponse, status_code=200)
async def upload_file(
    image: UploadFile = File(
        ...,
        description="Upload MRI brain picture.",
    ),
):
    # preprocessing the image
    image = await normalize_single_file(image)

    # inference
    label, confidence = infer(image)
    return {"label": label, "confidence": confidence}
