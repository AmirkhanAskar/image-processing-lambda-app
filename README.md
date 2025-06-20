# 🖼️ Serverless Image Processing with AWS Lambda

This project demonstrates an end-to-end **serverless application** using **AWS Lambda**, **S3**, **API Gateway**, and **CloudFront**. It allows users to upload images through a web interface, apply image filters (grayscale, resize, rotate, crop, etc.), and perform **object detection** using **OpenCV + YOLO** — all without managing servers.

🌐 **Live demo**:  
👉 [Click here to try it](https://askarccproject2025.pythonanywhere.com/)

---

## 🚀 Features

✅ Upload images via presigned URL  
✅ Choose from 8 filters (Pillow & OpenCV-based)  
✅ Object detection (YOLO) with result preview  
✅ Result image + detected labels shown on page  
✅ Load testing using **k6**  
✅ Scalability charts created with **Python**

---

## ⚙️ Tech Stack

- **AWS Lambda (Python 3.9)**
- **Amazon S3 (input/output buckets)**
- **API Gateway** (REST + CORS setup)
- **HTML + JS frontend**
- **OpenCV** 
- **Pillow for filters (grayscale, rotate, etc.)**
- **k6** for load testing
- **Matplotlib** for visualizing performance


---

## 🎯 Filters Supported

- 🎨 Grayscale  
- 🔄 Rotate  
- ✂️ Crop  
- ↔️ Flip  
- 📏 Resize  
- 📂 Format Convert  
- 🗜️ Compress  
- 🧠 Object Detection (YOLO)

---

## 📊 Load Testing Example

Tests were run using **k6** with 15, 30, and 50 virtual users. The results confirmed AWS Lambda's automatic scaling under higher loads, with plots generated using Python.

---

## 📸 Demo Previews

| Upload & Filter Selection | Object Detection |
|---------------------------|------------------|
| ![](screenshots/demo1.png) | ![](screenshots/yolo_output.png) |

---

## 👤 Author

**Askar Amirkhan**  
📍 Master's in Data Science — Sapienza University of Rome  
📫 Feel free to reach out for collaboration or freelance work!


