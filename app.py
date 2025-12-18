import streamlit as st
import requests
from PIL import Image

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
# Demo Analysis (Always Safe)
# ============================================================
def demo_analysis():
    return """
### Chemical Characterization of Hexane (C₆H₁₄)

**Composition:**  
Hexane consists exclusively of carbon and hydrogen atoms in a 6:14 ratio.

**Bonding and Structure:**  
All bonds are single covalent bonds. The molecule is a straight-chain alkane.

**Functional Groups:**  
No functional groups are present, confirming a saturated hydrocarbon.

**Chemical Nature:**  
Non-polar, chemically stable, and highly volatile.

**Applications:**  
Used as an industrial solvent, fuel component, and in organic synthesis.
"""

# ============================================================
# Ollama Call (Attempted, Not Assumed)
# ============================================================
def call_ollama(prompt, model="llava:latest"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["response"]

# ============================================================
# Main Logic
# ============================================================
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Chemical Compound", width=350)

    st.subheader("Chemical Analysis Result")

    try:
        prompt = (
            "Analyze the chemical compound shown in the image. "
            "Describe elements, functional groups, bonds, nature, and uses."
        )

        result = call_ollama(prompt)
        st.markdown(result)

    except Exception:
        # 🔒 AUTOMATIC DEMO FALLBACK
        st.warning("⚠️ Demo Mode Enabled (Ollama unavailable)")
        st.markdown(demo_analysis())

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.caption("© 2025 Chemical Compound Image Analyzer — Academic Demonstration Project")
