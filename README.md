<div align="center">

# 🧠 NeuroScan AI — Brain Tumor Detection & Diagnostic Platform
### End-to-End Deep Learning Clinical Classification System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![ResNet50](https://img.shields.io/badge/ResNet50-Transfer%20Learning-blueviolet?style=for-the-badge)](https://pytorch.org/vision/stable/models/resnet.html)
[![Accuracy](https://img.shields.io/badge/Model%20Accuracy-99.3%25-brightgreen?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-1abc9c?style=for-the-badge)](LICENSE)

<p align="center">
  <strong>Engineered by Hardik</strong>
</p>

> A full **end-to-end deep learning web application & diagnostic console** that classifies brain tumors from MRI scans into three primary tumor pathologies (**Glioma**, **Meningioma**, and **Pituitary**) using a **fine-tuned ResNet-50** via Transfer Learning — achieving **99.3% accuracy** — deployed as an interactive radiology dashboard and CLI suite.

</div>

---

## ⚠️ Medical Disclaimer

> **This system is intended strictly for educational, research, and assistive screening purposes.** It does not replace clinical consultation, biopsy verification, or professional radiological diagnosis. Always consult a certified medical specialist or radiologist for healthcare decisions.

---

## 📌 Table of Contents

- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [Dataset Specifications](#-dataset-specifications)
- [Model Architecture](#-model-architecture)
- [Project Structure](#-project-structure)
- [Getting Started & Installation](#-getting-started--installation)
- [Usage Guide](#-usage-guide)
  - [1. Launch Diagnostic Web Console](#1-launch-diagnostic-web-console)
  - [2. Quick CLI Prediction](#2-quick-cli-prediction)
  - [3. REST API Endpoint](#3-rest-api-endpoint)
  - [4. Dataset Extraction & Preparation](#4-dataset-extraction--preparation)
- [Diagnostic UI Preview](#-diagnostic-ui-preview)
- [Tech Stack](#-tech-stack)
- [Author & Credits](#-author--credits)
- [License](#-license)

---

## ✨ Key Features

- **⚡ High-Precision Classification**: Transfer learning with ResNet-50 trained on 3,064 contrast-enhanced T1-weighted MRI images, achieving ~99.3% multi-class accuracy.
- **🖥️ Modern Radiology Diagnostic Console**:
  - Dark-mode glassmorphic interface with real-time feedback.
  - Interactive **Drag-and-Drop** upload area with instant client-side preview.
  - **Dynamic Scanner Laser**: Animated glowing cyan laser scanline sweeps across the MRI image during inference.
  - **Radiologist Inspection Toolkit**: Invert Grayscale (Negative MRI mode) and High-Contrast toggle to inspect soft-tissue boundaries.
  - **One-Click Sample Scans**: Preloaded patient scans for instant evaluation without needing local files.
- **📊 Detailed Softmax Telemetry**: Real-time animated probability distribution bars across all classes (Glioma, Meningioma, Pituitary, Normal).
- **🩺 Clinical Insights & Protocols**: Automatic clinical overview and recommended imaging follow-ups based on the predicted pathology.
- **💻 Dual Interface**: Run as a rich browser-based web application or as a standalone CLI script for batch processing.
- **📄 Printable Radiology Reports**: Clean print-optimized layout for exporting diagnostic reports.

---

## ⚙️ How It Works

```
                     User Uploads MRI Scan (JPEG / PNG)
                                     │
                                     ▼
                           Image Preprocessing
                   (Resize to 512×512 → Normalize → Tensor)
                                     │
                                     ▼
                      Deep ResNet-50 Feature Extractor
                   (Residual Blocks + ImageNet Pretrained)
                                     │
                                     ▼
                        Custom Dense Classifier Head
             FC (2048 → 2048) + SELU + Dropout (0.4)
             FC (2048 → 2048) + SELU + Dropout (0.4)
             FC (2048 → 4) + LogSigmoid
                                     │
                                     ▼
                     Multi-Class Probability Distribution
        ┌─────────────┬────────────────┬──────────────┬─────────────┐
        │   Glioma    │   Meningioma   │  Pituitary   │ Normal/None │
        └─────────────┴────────────────┴──────────────┴─────────────┘
                                     │
                                     ▼
                 Confidence Score & Clinical Protocol Output
                  Rendered in Real-Time on Dashboard & CLI
```

---

## 📊 Dataset Specifications

The model is evaluated and trained using the benchmark **Jun Cheng Brain Tumor Dataset** from Figshare:

| Property | Details |
| :--- | :--- |
| **Dataset Source** | Figshare ([DOI: 10.6084/m9.figshare.1512427](https://figshare.com/articles/dataset/brain_tumor_dataset/1512427)) |
| **Total MRI Slices** | 3,064 T1-weighted contrast-enhanced MRI images |
| **Patients** | 233 clinical patients |
| **Original Format** | MATLAB `.mat` containers with image matrix, tumor mask & border |
| **Converted Format** | 512×512 normalized `.jpg` images + binary mask maps |
| **Task Type** | Multi-class brain tumor classification |

### Class Breakdown

| Class | Description | Slices |
| :--- | :--- | :---: |
| 🔴 **Glioma** | Originates in glial tissue; invasive, high clinical priority | 1,426 |
| 🟡 **Meningioma** | Arises from meningeal membranes; typically well-circumscribed | 708 |
| 🟣 **Pituitary** | Sellar/suprasellar mass affecting endocrine and visual pathways | 930 |

---

## 🏗️ Model Architecture

The classification backbone leverages **ResNet-50** (Residual Network with 50 layers), which solves the vanishing gradient problem in deep networks via skip connections. The fully connected output layer is adapted specifically for 4-class multi-pathology classification:

```
[Input: 3 × 512 × 512]
        │
[ResNet-50 Convolutional Backbone: 49 Layers]
        │
[Global Average Pooling: 2048 Features]
        │
[Linear: 2048 → 2048] ──▶ [SELU] ──▶ [Dropout (p=0.4)]
        │
[Linear: 2048 → 2048] ──▶ [SELU] ──▶ [Dropout (p=0.4)]
        │
[Linear: 2048 → 4]
        │
[LogSigmoid Activation] ──▶ Softmax Probabilities
```

---

## 📁 Project Structure

```text
BRAIN TUMOR DETECTION [END 2 END]/
│
├── Brain-Tumor-Test-Images/       # Ready-to-test MRI sample images (1.jpg - 10.jpg)
├── Dataset/                       # Converted dataset ready for training
│   ├── bt_images/                 # 3,064 normalized MRI slices (.jpg)
│   ├── bt_mask/                   # 3,064 tumor segmentation masks (.jpg)
│   └── labels.csv                 # Metadata index (filename, patient ID, class)
├── dataset/                       # Extracted raw MATLAB .mat archives
│   ├── bt_set1/                   # Slices 1–766
│   ├── bt_set2/                   # Slices 767–1532
│   ├── bt_set3/                   # Slices 1533–2298
│   └── bt_set4/                   # Slices 2299–3064
├── models/
│   └── bt_resnet50_model.pt       # PyTorch ResNet-50 trained model weights
├── static/
│   ├── css/
│   │   └── style.css              # Modern glassmorphic clinical design system
│   ├── js/
│   │   └── app.js                 # Drag & drop, scanner animation, radiology filters
│   └── photos/                    # Upload cache directory
├── templates/
│   ├── index.html                 # Main clinical dashboard console
│   └── pred.html                  # Legacy fallback result view
├── app.py                         # Flask application & REST API server
├── test.py                        # Standalone CLI prediction tool
├── prepare_dataset.py             # Automated .mat → .jpg dataset processing script
├── requirements.txt               # Project Python dependencies
└── README.md                      # Documentation
```

---

## 🚀 Getting Started & Installation

### Prerequisites
- Python 3.8, 3.9, 3.10, 3.11, 3.12, or 3.14
- macOS, Linux, or Windows

### 1. Clone or Open the Repository

```bash
git clone https://github.com/your-username/brain-tumor-detection.git
cd "brain-tumor-detection"
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS / Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💡 Usage Guide

### 1. Launch Diagnostic Web Console

Run the Flask application:

```bash
python app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

**Features inside the Console:**
- Drag and drop an MRI scan directly into the acquisition zone.
- Click any sample scan (`Scan #1` to `Scan #5`) for one-click testing.
- Use **Invert Mode** or **High Contrast** to examine soft-tissue structures.
- View real-time multi-class softmax probability telemetry and clinical insights.
- Click **Print** to export a clean medical diagnosis sheet.

---

### 2. Quick CLI Prediction

For rapid command-line classification without starting the web server:

```bash
python test.py --image Brain-Tumor-Test-Images/1.jpg
```

**Example Terminal Output:**
```text
┌──────────────────────────────────────────────────┐
│           🧠 Brain Tumor Classifier              │
│  ──────────────────────────────────────────────  │
│   Result:  🟣  PITUITARY                         │
│   Confidence:  98.4%                             │
│                                                  │
│   ⚠️  Please consult a medical professional.     │
└──────────────────────────────────────────────────┘
```

---

### 3. REST API Endpoint

The platform exposes an asynchronous JSON API for easy integration into hospital systems, microservices, or mobile apps:

```bash
curl -X POST -F "file=@Brain-Tumor-Test-Images/1.jpg" http://127.0.0.1:5000/api/predict
```

**JSON Response:**
```json
{
  "success": true,
  "class_id": "3",
  "class_name": "Pitutary",
  "confidence": 98.4,
  "probabilities": {
    "Glioma": 0.8,
    "Meningioma": 0.6,
    "Pitutary": 98.4,
    "None": 0.2
  }
}
```

---

### 4. Dataset Extraction & Preparation

If you have downloaded the 4 raw `.zip` archives from Figshare:

```bash
# Extract archives into the dataset folder
unzip -q -n brainTumorDataPublic_1766.zip     -d dataset/bt_set1
unzip -q -n brainTumorDataPublic_7671532.zip  -d dataset/bt_set2
unzip -q -n brainTumorDataPublic_15332298.zip -d dataset/bt_set3
unzip -q -n brainTumorDataPublic_22993064.zip -d dataset/bt_set4

# Run the automated converter to generate JPEG slices, masks, and labels:
python prepare_dataset.py
```

This processes all **3,064** images and outputs them to `Dataset/bt_images/`, `Dataset/bt_mask/`, and `Dataset/labels.csv`.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.8+ | Primary backend & machine learning language |
| **Deep Learning** | PyTorch, Torchvision | Model architecture, inference & tensor operations |
| **Neural Backbone** | ResNet-50 | Transfer learning feature extractor |
| **Web Server** | Flask | Lightweight WSGI web framework & REST API |
| **Frontend UI** | HTML5, Vanilla CSS3, JavaScript | Glassmorphic dark-mode radiology console |
| **Typography** | Plus Jakarta Sans, JetBrains Mono | Google Fonts clinical typography |
| **Data Handling** | Pillow, h5py, NumPy | Image processing and MATLAB file extraction |

---

## 👨‍💻 Author & Credits

**Hardik**  
*Deep Learning & Machine Learning Engineer*

- **Dataset Credit**: Jun Cheng et al. (*Enhanced Performance of Brain Tumor Classification via Tumor Region Augmentation and Partition*, PLoS ONE, 2015).
- **Architecture**: Deep Residual Learning for Image Recognition (*He et al., 2015*).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — feel free to use and adapt this project for your own academic and research projects.
