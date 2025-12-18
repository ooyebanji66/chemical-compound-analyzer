# Chemical Compound Image Analyzer

A web-based application for analyzing chemical compound images using multimodal
large language models. The system identifies elemental composition, bonding,
functional groups, chemical nature, and common applications of compounds.

The project supports **local AI inference using Ollama (LLaVA + Gemma)** and a
**cloud-safe demo mode** for Streamlit deployment.

---

## 📌 Project Overview

This project demonstrates how modern multimodal AI models can assist in chemical
structure interpretation by analyzing images of molecular diagrams.

Due to cloud infrastructure limitations, full AI inference is performed locally
using Ollama, while a robust demo mode is deployed on Streamlit Cloud to illustrate
the analytical workflow.

---

## 🎯 Features

- Upload chemical compound images (JPG, PNG, JPEG)
- Automatic chemical characterization:
  - Elements and composition
  - Bond types and structure
  - Functional groups
  - Chemical nature
  - Industrial and laboratory uses
- Fault-tolerant design:
  - Local AI inference when Ollama is available
  - Automatic demo fallback when Ollama is unavailable
- Streamlit-based interactive UI
- Cloud-safe deployment

---

## 🛠️ Technologies Used

- **Python 3**
- **Streamlit**
- **Ollama** (local inference)
- **LLaVA** (vision–language model)
- **Gemma 3** (text reasoning)
- **Pillow**
- **Requests**

---

## 🗂️ Project Structure

```text
chemical-compound-analyzer/
│
├── app.py                 # Main Streamlit application
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
└── .gitignore             # Git ignore rules
Prerequisites

Python 3.9+

Ollama installed
steps
ollama serve
ollama pull llava:latest
ollama pull gemma3:latest
streamlit run app.py
