import io

import numpy as np
from fastapi import UploadFile
from PIL import Image

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224


async def normalize_single_file(file: UploadFile) -> np.ndarray:
    """
    Reads an uploaded image file, resizes it to (IMAGE_WIDTH, IMAGE_HEIGHT),
    normalizes pixel values to [0,1], converts it to RGB if needed,
    and returns a batch with a single image ready for model input.

    The output shape is (1, IMAGE_HEIGHT, IMAGE_WIDTH, 3), suitable for
    feeding directly into Keras or ONNX models.

    Preprocessing steps:
    1. Read image bytes from UploadFile.
    2. Open the image using PIL and convert to RGB.
    3. Resize the image to (IMAGE_WIDTH, IMAGE_HEIGHT).
    4. Convert to NumPy array and normalize to [0,1].
    5. Handle grayscale fallback by repeating channels.
    6. Add batch dimension.

    :param file: UploadFile object representing the uploaded image.
                 Must be a valid image file (e.g., PNG, JPEG).
    :type file: fastapi.UploadFile

    :return: NumPy array of shape (1, IMAGE_HEIGHT, IMAGE_WIDTH, 3) with dtype float32,
             normalized to [0,1], ready for model inference.
    :rtype: np.ndarray
    """

    # Read file contents
    contents = await file.read()

    # Open image with PIL and ensure RGB
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    # Resize
    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))

    # Convert to NumPy array
    img_array = np.array(img, dtype=np.float32)

    # Normalize to [0,1]
    img_array /= 255.0

    # Ensure shape is (H, W, 3) in case of grayscale
    if img_array.ndim == 2:
        img_array = np.repeat(img_array[..., np.newaxis], 3, axis=-1)

    # Add batch dimension: (1, H, W, 3)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array.astype("float32")
