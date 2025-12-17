import streamlit as st
import requests
import base64
import os
from PIL import Image
from io import BytesIO

# -------------------------------
# Configuration
# -------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
DEPLOY_MODE = os.getenv("STREAMLIT_CLOUD", "false").lower() == "true"

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(
    page_title="Chemical Compound Image Analyzer",
    layout="centered"
)

st.title("🧪 Chemical Compound Image Analyzer")
st.caption("Powered by Ollama (LLaVA + Gemma)")

# -------------------------------
# Helper Functions
# -------------------------------

def call_ollama(model, prompt, image_b64=None, timeout=300):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    if image_b64:
        payload["images"] = [image_b64]

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=timeout
    )
    response.raise_for_status()
    return response.json().get("response", "")


def analyze_image_with_llava(image_bytes):
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
You are a chemical analysis expert.
Analyze the uploaded chemical structure image and describe:
- Identifiable functional groups
- Elements present
- Bond types
- Molecular nature (saturated/unsaturated, organic/inorganic)
- Likely applications or uses

Respond in clear academic language.
"""

    return call_ollama(
        model="llava",
        prompt=prompt,
        image_b64=image_b64
    )


def refine_with_gemma(text):
    prompt = f"""
Rewrite the following chemical description into a clean,
formal, academic explanation suitable for a university report.

Text:
{text}
"""

    return call_ollama(
        model="gemma3",
        prompt=prompt
    )

# -------------------------------
# UI Logic
# -------------------------------

uploaded_image = st.file_uploader(
    "Upload a chemical compound image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Chemical Compound", use_container_width=True)

    st.divider()

    # -------------------------------
    # DEMO MODE (Streamlit Cloud)
    # -------------------------------
    if DEPLOY_MODE:
        st.warning("🚧 Demo Mode Enabled")

        st.markdown("""
**Important Notice**

This cloud-hosted version runs in **demonstration mode only**.

Due to hardware and security constraints, Streamlit Cloud does not
support local multimodal inference engines such as **Ollama**, nor
models like **LLaVA** and **Gemma**.

The full AI-powered analysis is available in the **local deployment**.
""")

        st.success("Chemical Analysis Result")

        st.write("""
This application is designed to analyze chemical compound images by:

- Identifying elemental composition (e.g., C, H, O, N)
- Detecting functional groups
- Classifying bond types (single, double, aromatic)
- Determining molecular nature (alkane, alkene, aromatic, etc.)
- Providing academic descriptions and real-world applications

In the local version, this analysis is performed using:
- **LLaVA** for visual interpretation
- **Gemma** for academic refinement
""")

    # -------------------------------
    # LOCAL MODE (Ollama Enabled)
    # -------------------------------
    else:
        try:
            with st.spinner("Analyzing image with LLaVA..."):
                llava_result = analyze_image_with_llava(uploaded_image.getvalue())

            with st.spinner("Refining analysis with Gemma..."):
                final_result = refine_with_gemma(llava_result)

            st.success("Chemical Analysis Result")
            st.write(final_result)

        except requests.exceptions.RequestException as e:
            st.error("❌ Failed to communicate with Ollama.")
            st.code(str(e))

        except Exception as e:
            st.error("❌ An unexpected error occurred.")
            st.code(str(e))