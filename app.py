import streamlit as st
import requests
import base64
import os

# ==================================================
# Automatic Streamlit Cloud Detection
# ==================================================
IS_CLOUD = os.getenv("STREAMLIT_SERVER_RUNNING") == "1"

OLLAMA_URL = "http://localhost:11434/api/generate"

# ==================================================
# Ollama Helper (LOCAL ONLY)
# ==================================================
def call_ollama(model: str, prompt: str, image_bytes: bytes = None):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    if image_bytes:
        payload["images"] = [base64.b64encode(image_bytes).decode("utf-8")]

    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    response.raise_for_status()
    return response.json().get("response", "")


# ==================================================
# LLaVA Image Analysis (LOCAL ONLY)
# ==================================================
def analyze_image_with_llava(image_bytes: bytes):
    prompt = (
        "Analyze the uploaded chemical compound image and identify the "
        "elements present, functional groups, bond types, molecular nature, "
        "and possible industrial or laboratory uses."
    )

    return call_ollama(
        model="llava:latest",
        prompt=prompt,
        image_bytes=image_bytes,
    )


# ==================================================
# Gemma Refinement (LOCAL ONLY)
# ==================================================
def refine_with_gemma(text: str):
    prompt = (
        "Rewrite the following chemical analysis in a formal academic tone, "
        "suitable for a university-level chemistry report:\n\n"
        f"{text}"
    )

    return call_ollama(
        model="gemma3:latest",
        prompt=prompt,
    )


# ==================================================
# Unified Analysis Function (CLOUD SAFE)
# ==================================================
def analyze_image(image_bytes: bytes):
    # -------- STREAMLIT CLOUD MODE --------
    if IS_CLOUD:
        return (
            "⚠️ **Cloud Demo Mode Enabled**\n\n"
            "This application relies on locally hosted Ollama models "
            "(LLaVA + Gemma), which cannot be executed within Streamlit Cloud.\n\n"
            "The output below demonstrates the expected academic format.\n\n"
            "---\n\n"
            "### Chemical Characterization of Hexane (C₆H₁₄)\n\n"
            "Hexane is a saturated hydrocarbon composed exclusively of carbon "
            "and hydrogen atoms arranged in a straight-chain alkane structure. "
            "All interatomic bonds are single covalent σ-bonds, confirming full "
            "saturation and the absence of functional groups. Due to its "
            "non-polar nature, low reactivity, and high volatility, hexane is "
            "widely employed as an industrial solvent in extraction, cleaning, "
            "and fuel blending processes."
        )

    # -------- LOCAL MODE --------
    try:
        llava_result = analyze_image_with_llava(image_bytes)
        final_result = refine_with_gemma(llava_result)
        return final_result
    except Exception as e:
        return (
            "❌ **Failed to communicate with Ollama**\n\n"
            "Ensure that Ollama is running locally and the required models "
            "are installed.\n\n"
            f"**Error details:** {e}"
        )


# ==================================================
# Streamlit UI
# ==================================================
st.set_page_config(
    page_title="Chemical Compound Image Analyzer",
    layout="centered"
)

st.title("🧪 Chemical Compound Image Analyzer")
st.caption("Powered by Ollama (LLaVA + Gemma)")

uploaded_file = st.file_uploader(
    "Upload a chemical compound image",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file:
    st.image(
        uploaded_file,
        caption="Uploaded Chemical Compound",
        width=700
    )

    with st.spinner("Analyzing compound..."):
        result = analyze_image(uploaded_file.getvalue())

    st.markdown("---")
    st.subheader("Chemical Analysis Result")
    st.markdown(result)
