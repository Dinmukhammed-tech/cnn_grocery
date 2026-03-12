# 🛒 Grocery Price Estimator

CNN-based product recognition and price estimation system.

## Overview
This project uses deep learning to identify grocery products 
from images and estimate their total cost using YOLOv8 for 
object detection and EfficientNet-B0 for classification.

## Models Trained
| Model | Top-1 Accuracy | Top-5 Accuracy | F1-Score | Size |
|-------|---------------|---------------|----------|------|
| AlexNet | 75.5% | 94.6% | 0.757 | 217.8 MB |
| VGG16 | 83.9% | 96.6% | 0.836 | 512.6 MB |
| GoogLeNet | 80.9% | 96.7% | 0.808 | 21.6 MB |
| ResNet50 | 86.0% | 96.7% | 0.858 | 90.2 MB |
| **EfficientNet** | **90.6%** | **97.8%** | **0.906** | **15.7 MB** |

## Dataset
- **Source:** Freiburg Groceries Dataset
- **Categories:** 25 product classes
- **Total images:** 4,947
- **Split:** 70% train / 15% val / 15% test

## Project Structure
```
grocery_app/
├── main.py                 # FastAPI backend
├── model.py                # EfficientNet model loader
├── prices.json             # Product price database
├── static/
│   ├── style.css           # Styles
│   └── script.js           # Frontend logic
├── templates/
│   └── index.html          # Main page
└── README.md
```

## Installation
```bash
pip install fastapi uvicorn pillow torch torchvision ultralytics python-multipart jinja2
```

## Usage
1. Download `efficientnet_best.pth` from Google Drive
2. Place it in the project root folder
3. Run the app:
```bash
uvicorn main:app --reload
```
4. Open `http://localhost:8000`

## How It Works
1. User uploads an image
2. **YOLOv8** detects individual products in the image
3. **EfficientNet-B0** classifies each detected product
4. Prices are looked up from `prices.json`
5. Total cost is calculated and displayed

## Results
- Best model: **EfficientNet-B0**
- Top-1 Accuracy: **90.6%**
- Top-5 Accuracy: **97.8%**
- F1-Score: **0.906**
- MAE: **$0.185**
- RMSE: **$0.765**

## Technologies
- **Deep Learning:** PyTorch
- **Object Detection:** YOLOv8 (Ultralytics)
- **Backend:** FastAPI
- **Frontend:** HTML / CSS / JavaScript
- **Dataset:** Freiburg Groceries Dataset