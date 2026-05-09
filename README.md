# Vibe Checker: Emotion Analyzer Dashboard

[![Live Demo](https://img.shields.io/badge/Live_Demo-Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=000)](https://huggingface.co/spaces/mohamednagy11/vibe-checker)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

**Vibe Checker** is a fully containerized, interactive web application that leverages Natural Language Processing (NLP) to detect and analyze the emotional undertones of text input. Built with a minimalist, modern interface, it dynamically tracks the emotional composition of conversations over time.

---

## Live Demonstration
Experience the application live on Hugging Face Spaces:  
**🔗 [Launch Vibe Checker](https://huggingface.co/spaces/mohamednagy11/vibe-checker)**

---

## Key Features

* **Advanced Emotion Classification:** Utilizes the `distilroberta-base` model to classify text into 7 emotional categories (Joy, Anger, Sadness, Surprise, Fear, Disgust, Neutral) with an accuracy of 66%.
* **Interactive Timeline Analysis:** Features a dynamic line chart that visualizes the relative percentage of emotional composition across multiple inputs.
* **Dynamic Filtering:** Users can isolate the history of specific emotions using a live dropdown menu.
* **Highly Optimized Inference:** Engineered for extreme efficiency using a CPU-only PyTorch distribution and `safetensors`, drastically reducing the container size by bypassing massive GPU dependencies.
* **Cloud-Ready Infrastructure:** Fully containerized using Docker, ensuring perfectly deterministic builds and seamless deployment to cloud providers.

---

## Technology Stack

| Core Technology | Usage |
| :--- | :--- |
| ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) | Core backend logic |
| ![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white) ![Dash](https://img.shields.io/badge/Dash-008DE4?style=for-the-badge&logo=plotly&logoColor=white) | Frontend interactive dashboard and UI rendering |
| ![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-FFD21E?style=for-the-badge&logoColor=black) | NLP Model pipeline (`j-hartmann/emotion-english-distilroberta-base`) |
| ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white) | Machine Learning mathematical engine (CPU Optimized) |
| ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) | Containerization and environment isolation |

---

## Local Development Guide

To run this application locally on your machine, ensure you have [Docker](https://www.docker.com/products/docker-desktop/) installed and running.

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/vibe-checker.git](https://github.com/YourUsername/vibe-checker.git)
cd vibe-checker
```
### 2. Build the Docker Image
The Dockerfile is optimized with layer caching. The initial build will download the Hugging Face model and PyTorch libraries.

```bash
docker build -t vibe-checker .
```
### 3. Run the Container
Start the application and map it to your local port `7860` (the exact port required by Hugging Face Spaces).

```bash
docker run -p 7860:7860 vibe-checker
```

### 4. Access the Application
Open your preferred web browser and navigate to:

```bash
http://localhost:7860
```

(Note: If you wish to enable hot-reloading for local development, open app.py and temporarily change debug=False to debug=True inside the app.run_server command before building).

---

### Project Structure
```
vibe-checker/
│
├── app.py                 # Main Dash application logic, layout, and callbacks
├── Dockerfile             # Multi-layer Docker configuration for deployment
├── requirements.txt       # Version-locked dependencies with CPU-index URLs
├── .dockerignore          # Excludes local environments from the build context
├── .gitignore             # Excludes sensitive/local files from version control
└── README.md              # Project documentation
```

---

### Security & Optimization Notes
* **Safetensors Implementation:** This application explicitly utilizes the `safetensors` library to mitigate the CVE-2025-32434 vulnerability associated with legacy `.bin` model files.

* **Deterministic Builds:** All dependencies in `requirements.txt` are strictly version-pinned to ensure long-term stability and reproducibility.

---