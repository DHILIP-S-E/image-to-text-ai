import streamlit as st
import requests

# API details
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

# Function to query the model
def query(image_data):
    response = requests.post(API_URL, headers=headers, data=image_data)
    return response.json()

# Streamlit interface
st.title("Image Caption Generator")
st.write("Upload an image and get its caption generated using the BLIP model.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    
    # Convert the file to bytes and send to the model
    image_data = uploaded_file.read()
    st.write("Generating caption...")
    
    # Call the query function and get the result
    result = query(image_data)
    
    # Display the caption
    st.write("**Caption:**", result[0]['generated_text'])

import base64
def get_base64_image(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Get base64 of the background image
img_base64 = get_base64_image("images/back.png")

# Adding custom CSS to set a background image with a black fade effect
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 1)),
                    url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-blend-mode: multiply;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
