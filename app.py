import streamlit as st
import requests
import os
from PIL import Image
import io

# ============================================================
# Environment Detection
# ============================================================
# Streamlit Cloud sets this automatically
IS_STREAMLIT_CLOUD = os.getenv("STREAMLIT_SERVER_RUNNING") == "1"

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="Chemical Compound Image Analyzer",
    layout="centered"
)

st.title("Chemical Compound Image Analyzer")
st.caption("Powered by Ollama (LLaVA + Gemma)")

# ============================================================
# File Upload
# ============================================================
uploaded_image = st.file_uploader(
    "Upload a chemical compound image",
    type=["jpg", "jpeg", "png"]
)

# ============================================================
# Demo Analysis (Cloud-Safe)
# ============================================================
def demo_analysis():
    return """
### Chemical Characterization of Hexane (C₆H₁₄)

**1. Composition and Elements**  
The compound is composed exclusively of carbon (C) and hydrogen (H) atoms in a
stoichiometric ratio of 6:14.

**2. Bonding and Structure**  
All bonds present are single covalent bonds (C–C and C–H), indicating a saturated
hydrocarbon structure.

**3. Functional Groups**  
No functional groups are present. The absence of heteroatoms or multiple bonds
confirms its classification as an alkane.

**4. Chemical Nature**  
Hexane is nonpolar, chemically stable, and highly volatile.

**5. Industrial and Laboratory Uses**  
Hexane is widely used as an industrial solvent, in fuel formulations, oil extraction
processes, and as a reagent in organic synthesis.
"""

# ============================================================
# Ollama Request (LOCAL ONLY)
# ============================================================
def call_ollama(prompt, model):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )
    response.raise_for_status()
    return response.json()["response"]

# ============================================================
# Main Application Logic
# ============================================================
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Chemical Compound", width=350)

    st.subheader("Chemical Analysis Result")

    # --------------------------------------------------------
    # CLOUD MODE (NO OLLAMA)
    # --------------------------------------------------------
    if IS_STREAMLIT_CLOUD:
        st.warning("⚠️ Cloud Demo Mode Enabled (Ollama not available)")
        st.markdown(demo_analysis())

    # --------------------------------------------------------
    # LOCAL MODE (OLLAMA ENABLED)
    # --------------------------------------------------------
    else:
        try:
            prompt = (
                "Analyze the chemical compound shown in the image. "
                "Describe its elements, functional groups, bond types, "
                "chemical nature, and industrial or laboratory uses."
            )

            result = call_ollama(prompt, model="llava:latest")
            st.markdown(result)

        except Exception as e:
            st.error("❌ Failed to communicate with Ollama")
            st.info("Ensure that Ollama is running locally and the required models are installed.")
            st.code(str(e))

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.caption("© 2025 Chemical Compound Image Analyzer — Academic Demonstration Project")
