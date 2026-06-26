# 🖼️ Pixel Truth – AI Generated Image Detection System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep_Learning-red?style=for-the-badge&logo=pytorch)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?style=for-the-badge&logo=mysql)
![HTML](https://img.shields.io/badge/HTML5-Frontend-orange?style=for-the-badge&logo=html5)
![CSS](https://img.shields.io/badge/CSS3-Design-blue?style=for-the-badge&logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-Interactive-yellow?style=for-the-badge&logo=javascript)

</p>

---

# 📖 Overview

Pixel Truth is an AI-powered web application designed to distinguish between **Real Images** and **AI Generated Images** using Deep Learning and Computer Vision.

The system enables users to upload an image and instantly receive a prediction along with a confidence score indicating whether the image is authentic or AI-generated.

The project combines modern web development with machine learning to address one of today's growing challenges—the detection of synthetic media.

---

# 🎯 Objectives

- Detect AI-generated images accurately.
- Help users identify manipulated or synthetic images.
- Provide a simple web interface for image prediction.
- Display prediction confidence.
- Manage users through an admin dashboard.
- Demonstrate practical application of Deep Learning.

---

# ✨ Key Features

- 🔍 AI vs Real Image Detection
- 🤖 Deep Learning Model
- 📤 Image Upload
- 📊 Confidence Score
- 👤 User Login & Registration
- 🔐 Authentication System
- 🛡️ Admin Dashboard
- ⚡ Fast Predictions
- 💻 Responsive Interface
- 🎨 Modern UI Design

---
# 🛠️ Technologies Used

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Flask |
| Deep Learning | PyTorch |
| Database | MySQL |
| IDE | Visual Studio Code |
| Version Control | Git & GitHub |

---

# 🧠 AI Model

Pixel Truth uses a Deep Learning model trained to classify images into two categories:

- ✅ Real Images
- 🤖 AI Generated Images

The model analyzes image patterns, textures, and visual artifacts to determine authenticity.

Output includes:

- Prediction Label
- Confidence Score

---

# 🏗️ System Architecture

```
                User
                  │
                  ▼
        Upload Image (Frontend)
                  │
                  ▼
          Flask Backend Server
                  │
                  ▼
        Deep Learning AI Model
                  │
                  ▼
      Prediction + Confidence Score
                  │
                  ▼
         Display Result to User
```

---

# 📂 Project Structure

```
Pixel-Truth/
│
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── admin.html
│   └── result.html
│
├── models/
│   ├── model.pth
│   └── predictor.py
│
├── database/
│   └── schema.sql
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Workflow

1. User opens Pixel Truth.
2. User logs into the application.
3. User uploads an image.
4. Flask backend receives the image.
5. AI model processes the uploaded image.
6. Prediction is generated.
7. Confidence score is calculated.
8. Result is displayed instantly.
9. Admin can manage registered users.

---

# 💻 Installation

Clone the repository

```bash
git clone https://github.com/praveenjoe115/pixel-truth.git
```

Move into the project folder

```bash
cd pixel-truth
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---
# 📸 Project Screenshots

## 🏠 Home Page

<img src="screenshots/home.png" width="900">

---

## 🔐 Login Page

<img src="screenshots/login.png" width="900">

---

## 📝 Registration Page

<img src="screenshots/signup.png" width="900">

---

## 📤 Image Upload

<img src="screenshots/upload.png" width="900">

---

## 📊 Prediction Result

<img src="screenshots/result.png" width="900">

---

## 🛡️ Admin Dashboard

<img src="screenshots/admin.png" width="900">

---

# 📊 Sample Output

```
Prediction : AI Generated Image

Confidence Score : 98.47%

Status : Prediction Successful
```

---

# 🚀 Future Enhancements

- 🔥 Grad-CAM Heatmap Visualization
- 📷 Live Camera Detection
- ☁ Cloud Deployment
- 📱 Mobile Responsive Version
- 🤖 Support Multiple AI Models
- ⚡ Faster Prediction Pipeline
- 🧠 Explainable AI (XAI)
- 📈 Prediction History Dashboard
- 🔔 Email Notifications
- 🌍 Multi-language Support

---

# 🎯 Learning Outcomes

Through this project I gained practical experience in:

- Artificial Intelligence
- Deep Learning
- Computer Vision
- Flask Development
- MySQL Database
- Authentication Systems
- Git & GitHub
- Python Programming
- Responsive Web Design

---

# 📈 Project Highlights

✔ AI-powered Image Detection

✔ Flask Full Stack Application

✔ User Authentication

✔ Admin Dashboard

✔ Confidence Score Prediction

✔ Modern Responsive UI

✔ MySQL Integration

✔ Deep Learning Model

---

# 👨‍💻 Author

## Praveen Kumar U

BCA Graduate

AI & Software Developer

GitHub

https://github.com/praveenjoe115

LinkedIn

https://linkedin.com/in/praveen-kumar-0a731a417

---

# 🤝 Contributing

Contributions, ideas and suggestions are always welcome.

If you'd like to improve Pixel Truth:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

# ⭐ Support

If you found this project useful,

⭐ Star this repository.

It helps others discover the project.

---

# 📜 License

This project is created for educational and learning purposes.

© 2026 Praveen Kumar U

---

<p align="center">

Made with ❤️ using Python • Flask • PyTorch • MySQL

</p>