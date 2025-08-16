import io
import threading
import time

import streamlit as st
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from src.api.router import router

# FastAPI setup - Do this once at the top
fastapi_app = FastAPI()
fastapi_app.include_router(router)

# Add CORS middleware to FastAPI app
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific Streamlit origin
    allow_methods=["*"],
    allow_headers=["*"],
)


# def run_api():
#     """Function to run FastAPI server"""
#     uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)


# ---------------- Streamlit code ----------------
# st.title("Brain Tumor Detection")
#
# # # Start FastAPI in background only once
# # if 'api_started' not in st.session_state:
# #     st.session_state.api_started = True
# #     threading.Thread(target=run_api, daemon=True).start()
# #     st.info("Starting API server... please wait")
# #     time.sleep(2)  # Give API time to start
#
# st.write("Upload an MRI image and the model will predict if a tumor is present.")
#
# # Upload image
# uploaded_file = st.file_uploader("Choose an MRI image", type=["png", "jpg", "jpeg"])
#
# if uploaded_file is not None:
#     # Show image
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded MRI", use_column_width=True)
#
#     # Button to predict
#     if st.button("Predict"):
#         # Convert PIL Image to bytes
#         buffered = io.BytesIO()
#         image.save(buffered, format="PNG")
#         buffered.seek(0)
#         files = {"file": ("image.png", buffered, "image/png")}
#
#         try:
#             # Send request to FastAPI with timeout
#             response = requests.post(
#                 "http://localhost:8000/predict/",
#                 files=files,
#                 timeout=10
#             )
#             response.raise_for_status()  # Raise exception for bad status
#
#             if response.status_code == 200:
#                 data = response.json()
#                 label = data.get("label", "N/A")
#                 confidence = data.get("confidence", 0.0)
#                 st.success(f"Prediction: {label} (Confidence: {confidence:.2f})")
#             else:
#                 st.error(f"API returned status: {response.status_code}")
#
#         except requests.exceptions.ConnectionError:
#             st.error("Could not connect to API server. Is it running?")
#         except requests.exceptions.Timeout:
#             st.error("API request timed out. Try again.")
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
