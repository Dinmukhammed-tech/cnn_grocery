import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json


CLASS_NAMES = [
    'BEANS', 'CAKE', 'CANDY', 'CEREAL', 'CHIPS',
    'CHOCOLATE', 'COFFEE', 'CORN', 'FISH', 'FLOUR',
    'HONEY', 'JAM', 'JUICE', 'MILK', 'NUTS',
    'OIL', 'PASTA', 'RICE', 'SODA', 'SPICES',
    'SUGAR', 'TEA', 'TOMATO_SAUCE', 'VINEGAR', 'WATER'
]

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def load_efficientnet():
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(1280, len(CLASS_NAMES))
    model.load_state_dict(torch.load(
        'efficientnet_best.pth', map_location=device))
    model.eval()
    return model.to(device)


def load_prices():
    with open('prices.json', 'r') as f:
        return json.load(f)


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def classify_crop(model, crop_img):
    img_tensor = transform(crop_img).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.softmax(outputs, dim=1)
        conf, pred = probs.max(1)
    return CLASS_NAMES[pred.item()], round(conf.item() * 100, 1)