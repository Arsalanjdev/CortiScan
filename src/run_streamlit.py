import io

import requests
import streamlit as st
from PIL import Image

st.title("Brain Tumor Detection")
st.markdown(
    "Upload an MRI image and the model will predict whether a tumor is present."
)

# Center uploader
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader("Choose an MRI image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # Create two columns: image on the left, prediction on the right
    img_col, result_col = st.columns([1, 1])

    # Show image
    with img_col:
        st.image(image, caption="Uploaded MRI", use_container_width=True)

    # Button and prediction in the right column
    with result_col:
        if st.button("Predict"):
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            buffered.seek(0)
            files = {"image": ("image.png", buffered, "image/png")}

            with st.spinner("Predicting..."):
                try:
                    response = requests.post(
                        "http://fastapi:8000/predict/", files=files, timeout=10
                    )
                    response.raise_for_status()

                    if response.status_code == 200:
                        data = response.json()
                        label = data.get("label", "N/A")
                        confidence = data.get("confidence", 0.0)
                        st.success(
                            f"Prediction:\n**{label}**\nConfidence: {confidence:.2f}%"
                        )
                    else:
                        st.error(f"API returned status: {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to API server. Is it running?")
                except requests.exceptions.Timeout:
                    st.error("API request timed out. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
