from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from ultralytics import YOLO
from PIL import Image
import io
import json
from model import load_efficientnet, load_prices, classify_crop

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

print("Model was uploading...")
efficientnet = load_efficientnet()
prices = load_prices()
yolo = YOLO('yolov8n.pt')
print("Models loaded!")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')

    results = yolo(image, conf=0.3)
    boxes = results[0].boxes

    detected_products = []
    total_price = 0.0

    if len(boxes) == 0:
        product_name, confidence = classify_crop(efficientnet, image)
        price = prices.get(product_name, 0.0)
        detected_products.append({
            'name': product_name,
            'confidence': confidence,
            'price': price
        })
        total_price = price
    else:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = image.crop((x1, y1, x2, y2))
            product_name, confidence = classify_crop(efficientnet, crop)
            price = prices.get(product_name, 0.0)
            detected_products.append({
                'name': product_name,
                'confidence': confidence,
                'price': price
            })
            total_price += price

    return {
        'products': detected_products,
        'total_price': round(total_price, 2),
        'count': len(detected_products)
    }