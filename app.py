from flask import Flask, render_template, request, redirect, url_for, session
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os
import mysql.connector
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "pixeltruth_secret_key"


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pixeltruth_db"
    )


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint = torch.load("checkpoints/best_model.pth", map_location=device)
class_names = checkpoint["class_names"]

model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, len(class_names))
model.load_state_dict(checkpoint["model_state_dict"])
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

UPLOAD_FOLDER = "static/uploads"
HEATMAP_FOLDER = "static/heatmaps"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HEATMAP_FOLDER, exist_ok=True)


def generate_gradcam(image_path, output_path):
    gradients = []
    activations = []

    target_layer = model.layer4[-1]

    def forward_hook(module, input, output):
        activations.append(output)

    def backward_hook(module, grad_input, grad_output):
        gradients.append(grad_output[0])

    fh = target_layer.register_forward_hook(forward_hook)
    bh = target_layer.register_full_backward_hook(backward_hook)

    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    output = model(input_tensor)
    class_idx = output.argmax(dim=1).item()

    model.zero_grad()
    output[0, class_idx].backward()

    grads = gradients[0].detach().cpu().numpy()[0]
    acts = activations[0].detach().cpu().numpy()[0]

    weights = np.mean(grads, axis=(1, 2))
    cam = np.zeros(acts.shape[1:], dtype=np.float32)

    for i, w in enumerate(weights):
        cam += w * acts[i]

    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (224, 224))

    if cam.max() != 0:
        cam = cam / cam.max()

    heatmap = np.uint8(255 * cam)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    original = cv2.imread(image_path)
    original = cv2.resize(original, (224, 224))

    result = cv2.addWeighted(original, 0.6, heatmap, 0.4, 0)
    cv2.imwrite(output_path, result)

    fh.remove()
    bh.remove()


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        fullname = request.form.get("fullname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            error = "Passwords do not match"
            return render_template("signup.html", error=error)

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (fullname, username, email, password) VALUES (%s, %s, %s, %s)",
                (fullname, username, email, password)
            )
            db.commit()
            cursor.close()
            db.close()
            return redirect(url_for("login"))

        except mysql.connector.IntegrityError:
            error = "Username already exists"
        except Exception as e:
            error = str(e)

    return render_template("signup.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    prediction = None
    confidence = None
    image_path = None
    heatmap_path = None

    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename:
            filename = secure_filename(file.filename)

            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)

            image = Image.open(image_path).convert("RGB")
            input_tensor = transform(image).unsqueeze(0).to(device)

            with torch.no_grad():
                outputs = model(input_tensor)
                probs = torch.softmax(outputs, dim=1)
                conf, pred = torch.max(probs, 1)

            prediction = class_names[pred.item()]
            confidence = round(conf.item() * 100, 2)

            if prediction.lower() == "fake":
                heatmap_filename = "heatmap_" + filename
                heatmap_path = os.path.join(HEATMAP_FOLDER, heatmap_filename)
                generate_gradcam(image_path, heatmap_path)
            else:
                heatmap_path = None

            try:
                print("Saving detection...")
                print("Username:", session.get("username"))
                print("Image:", filename)
                print("Prediction:", prediction)
                print("Confidence:", confidence)
                print("Image Path:", image_path)
                print("Heatmap Path:", heatmap_path)

                db = get_db_connection()
                cursor = db.cursor()

                cursor.execute(
                    """
                    INSERT INTO detections 
                    (username, image_name, prediction, confidence, image_path, heatmap_path)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        session.get("username"),
                        filename,
                        prediction,
                        confidence,
                        image_path,
                        heatmap_path
                    )
                )

                db.commit()
                cursor.close()
                db.close()

                print("Detection saved successfully")

            except Exception as e:
                print("Database insert error:", e)

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        image_path=image_path,
        heatmap_path=heatmap_path
    )


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid admin username or password"

    return render_template("admin_login.html", error=error)


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM detections ORDER BY id DESC")
    detections = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "admin_dashboard.html",
        users=users,
        detections=detections
    )


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    app.run(debug=True)