# 🧪 Chemical Compound Image Analyzer

A web-based application for analyzing chemical compound images using vision–language models. The system extracts chemical information such as elements, bonding types, functional groups, molecular nature, and common applications from uploaded compound images.

---

## 📌 Project Overview

This project demonstrates the integration of computer vision and large language models for educational chemical analysis. Users upload an image of a chemical compound (e.g., molecular structure diagrams), and the system generates a structured, academic-style explanation of the compound.

The application is implemented using **Streamlit** for the frontend and **Ollama (LLaVA + Gemma)** for local multimodal inference. A cloud-deployed demo is provided with graceful fallback behavior due to platform limitations.

---

## 🌐 Live Demo & Repository

* **Streamlit Demo:** [https://chemical-compound-analyzer.streamlit.app](https://chemical-compound-analyzer.streamlit.app)
* **GitHub Repository:** [https://github.com/ooyebanji66/chemical-compound-analyzer](https://github.com/ooyebanji66/chemical-compound-analyzer)

---

## 🖼️ Application Demo Screenshot

![Streamlit Demo](assets/demo.png)

---

## 🎯 Objectives

* Upload and visualize chemical compound images
* Identify elemental composition and bonding patterns
* Classify compounds based on functional groups
* Describe chemical nature and common industrial uses
* Present results in a clear academic format

---

## 🏆 Key Results

* Successful image-based chemical interpretation using LLaVA
* Academically structured output refined using Gemma
* Clean and interactive Streamlit user interface
* Local execution with Ollama for full functionality
* Cloud deployment with informative fallback messaging

---

## 🚀 Quick Start

### Prerequisites

* Python 3.9+
* Ollama installed and running locally
* Required models:

  ```bash
  ollama pull llava
  ollama pull gemma3
  ```

Verify Ollama is running:

```bash
ollama serve
```

---

### Installation

```bash
git clone git@github.com:ooyebanji66/chemical-compound-analyzer.git
cd chemical-compound-analyzer
pip install -r requirements.txt
```

---

### Run the Application (Local)

```bash
python -m streamlit run app.py
```

---

## 🛠️ Project Structure

```
chemical-compound-analyzer/
│
├── app.py               # Main Streamlit application
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
├── .gitignore           # Git ignore rules
├── assets/
│   └── demo.png         # Application screenshot
```

---

## ☁️ Streamlit Cloud Deployment Note

> ⚠️ Streamlit Cloud does **not** support local background services such as Ollama.
>
> * Full image analysis (LLaVA + Gemma) works when running locally
> * Cloud demo operates in fallback mode with explanatory output

This design choice ensures the demo remains accessible while clearly documenting platform constraints.

---

## ⚠️ Problems Encountered and Solutions

### 1. Ollama Connection Error on Streamlit Cloud

**Problem:** Streamlit Cloud cannot access `localhost:11434`.

**Solution:** Implemented error handling and fallback messaging. Full inference is supported locally.

---

### 2. Model Memory Constraints

**Problem:** Large models failed to load due to limited GPU/VRAM.

**Solution:** Used smaller model variants and CPU execution.

---

### 3. GitHub Push Failures (HTTPS)

**Problem:** Repeated connection reset and TLS errors.

**Solution:** Switched Git authentication from HTTPS to SSH.

---

### 4. Streamlit Command Not Recognized

**Problem:** `streamlit` command unavailable in PowerShell.

**Solution:** Used `python -m streamlit run app.py`.

---

## 💡 Helpful Hints for Others

* Test Ollama models independently before app integration
* Avoid localhost dependencies for cloud demos
* Use SSH for GitHub authentication on restricted networks
* Keep models lightweight for educational environments
* Document limitations clearly for evaluators

---

## 👤 Author

**Opeyemi Oyebanji**


---

## 📄 License

MIT License — see the `LICENSE` file for details.
