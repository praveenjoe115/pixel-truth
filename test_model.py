import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load checkpoint
checkpoint = torch.load(
    "checkpoints/best_model.pth",
    map_location=device
)

class_names = checkpoint["class_names"]

# Model
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(checkpoint["model_state_dict"])
model.to(device)
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# Get image path
image_path = input("Enter image path: ").strip().strip('"')

# Check file exists
if not os.path.exists(image_path):
    print("Image not found!")
    exit()

# Load image
image = Image.open(image_path).convert("RGB")
image = transform(image).unsqueeze(0).to(device)

# Predict
with torch.no_grad():
    outputs = model(image)
    probs = torch.softmax(outputs, dim=1)
    confidence, predicted = torch.max(probs, 1)

prediction = class_names[predicted.item()]
confidence = confidence.item() * 100

print("\n======================")
print("Prediction :", prediction)
print(f"Confidence : {confidence:.2f}%")
print("======================")