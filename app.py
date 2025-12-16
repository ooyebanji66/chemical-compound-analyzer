import streamlit as st
import requests
import base64
from PIL import Image

# --------------------------------
# Streamlit configuration
# --------------------------------
st.set_page_config(
    page_title="Chemical Compound Image Analyzer",
    layout="centered"
)

st.title("Chemical Compound Image Analyzer")
st.caption("Powered by Ollama (LLaVA + Gemma)")

OLLAMA_URL = "http://localhost:11434/api/chat"

# --------------------------------
# File uploader
# --------------------------------
uploaded_image = st.file_uploader(
    "Upload a chemical compound image",
    type=["jpg", "jpeg", "png"]
)

# --------------------------------
# Ollama API helper
# --------------------------------
def call_ollama(payload):
    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=600
        )
        response.raise_for_status()
        result = response.json()

        if "message" in result and "content" in result["message"]:
            return result["message"]["content"]

        return f"Unexpected response format:\n{result}"

    except requests.exceptions.RequestException as e:
        return f"Ollama request failed:\n{e}"

# --------------------------------
# Step 1: Image analysis (LLaVA)
# --------------------------------
def analyze_image_with_llava(image_bytes):
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "model": "llava:latest",   # use llava:7b if needed
        "messages": [
            {
                "role": "user",
                "content": (
                    "Analyze the given chemical compound image and describe:\n"
                    "1. Functional groups\n"
                    "2. Elements present\n"
                    "3. Bond types\n"
                    "4. Nature of the compound\n"
                    "5. Common or industrial uses\n\n"
                    "Provide a scientific but concise explanation."
                ),
                "images": [encoded_image]
            }
        ],
        "stream": False
    }

    return call_ollama(payload)

# --------------------------------
# Step 2: Academic refinement (Gemma)
# --------------------------------
def refine_with_gemma(text):
    payload = {
        "model": "gemma3:4b",   # safe for low-memory systems
        "messages": [
            {
                "role": "user",
                "content": (
                    "Rewrite the following into a clean, formal academic "
                    "chemical explanation suitable for a university report:\n\n"
                    f"{text}"
                )
            }
        ],
        "stream": False
    }

    return call_ollama(payload)

# --------------------------------
# Main application logic
# --------------------------------
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Chemical Compound", use_container_width=True)

    if st.button("Analyze Compound"):
        with st.spinner("Analyzing image using local AI models..."):
            llava_result = analyze_image_with_llava(uploaded_image.getvalue())
            final_result = refine_with_gemma(llava_result)

        st.subheader("Chemical Analysis Result")
        st.write(final_result)

# --------------------------------
# Footer
# --------------------------------
st.markdown(
    "---\n"
    "**Note:** This application runs fully locally using Ollama. "
    "No data is sent to external servers."
)