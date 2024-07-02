import streamlit as st
from openai import OpenAI
import base64
import os

# Initialize OpenAI client with your API key
client = OpenAI(api_key= "Enter api Key Here")
MODEL = "gpt-4o"

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #2e2e2e;
            color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
        }
        .stButton button {
            background-color: #ff6f61;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            margin: 10px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: white;
            color: black;
            border: 2px solid #ff6f61;
        }
        .title {
            color: #96C9F4;
            text-align: center;
            font-family: 'Helvetica', sans-serif;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-family: 'Helvetica', sans-serif;
        }
        .footer {
            text-align: center;
            font-family: 'Helvetica', sans-serif;
            margin-top: 2rem;
            font-size: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit app layout
st.markdown("<h1 class='title'>Invoice Image Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>Upload an invoice image to analyze its content</h3>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an invoice image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    temp_file_path = os.path.join("temp_image", uploaded_file.name)
    os.makedirs("temp_image", exist_ok=True)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())

    # Encode the image to base64
    base64_image = encode_image(temp_file_path)

    with st.spinner("Analyzing the image..."):
        # Send the image to OpenAI API
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in Markdown. Help me with my math homework!"},
                {"role": "user", "content": [
                    {"type": "text", "text": "Map the field with values in this image?"},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"}
                    }
                ]}
            ],
            temperature=0.0,
        )

    # Display the response
    st.markdown("### Analysis Results")
    st.markdown(response.choices[0].message.content, unsafe_allow_html=True)

    # Cleanup temporary files
    os.remove(temp_file_path)

st.markdown("<div class='footer'>Developed by Aqib Rehman PirZada</div>", unsafe_allow_html=True)
