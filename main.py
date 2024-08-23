import streamlit as st
import requests
import base64

# API details
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": "Bearer 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"}

# Function to query the model
def query(image_data):
    try:
        response = requests.post(API_URL, headers=headers, data=image_data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the caption: {e}")
        return []

# Function to encode image to base64
def get_base64_image(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

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
    
    if result:
        # Display the caption
        st.write("**Caption:**", result[0]['generated_text'])
    else:
        st.write("No caption generated.")

# Get base64 of the background image
img_base64 = get_base64_image("images/back.png")

# Adding custom CSS with black fade effect and white text
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 1)),
                    url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
    }}
    /* General Text Color */
    .stApp, .stMarkdown, .stText, .stHeader, .stSidebar {{
        color: #ffffff; /* White text color for general content */
    }}
    /* Title Styling */
    h1 {{
        color: #ffffff !important; /* White text color for the title */
    }}
    .stButton {{
        background-color: rgba(255, 255, 255, 0.1); /* Transparent background */
        color: #ffffff; /* White text color */
        border: 1px solid rgba(255, 255, 255, 0.5); /* Transparent border */
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.3s ease, transform 0.3s ease;
        box-shadow: none;
    }}
    .stButton:hover {{
        background-color: rgba(255, 255, 255, 0.2); /* Slightly opaque on hover */
    }}
    .stButton:active {{
        background-color: rgba(255, 255, 255, 0.3); /* Slightly opaque when clicked */
        transform: translateY(1px);
    }}
    .stButton:disabled {{
        background-color: rgba(255, 255, 255, 0.05); /* Very transparent when disabled */
        color: rgba(255, 255, 255, 0.3); /* Light text color when disabled */
        border: 1px solid rgba(255, 255, 255, 0.2); /* Transparent border when disabled */
        cursor: not-allowed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
