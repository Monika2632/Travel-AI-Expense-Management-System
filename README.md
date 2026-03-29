# 🚀 Travel AI Expense Management System

## 📌 Overview

The **Travel AI Expense Management System** is a full-stack application that automates expense tracking using AI.

It allows users to upload receipts, extract details using AI, validate expenses based on company policies, and visualize analytics through a frontend dashboard.

---

## 🎯 Features

* 🔐 User Authentication (Register & Login)
* 📤 Upload receipts (image/PDF)
* 🤖 AI-based receipt data extraction (Gemini API)
* ✅ Policy-based expense validation
* 💾 Store expenses with GST (tax)
* 📊 Analytics dashboard (category-wise + total + tax)
* 🌐 REST API using FastAPI
* ⚛️ Interactive frontend using React

---

## 🛠️ Tech Stack

### 🔹 Backend

* FastAPI (Python)
* SQLAlchemy (Database ORM)
* SQLite (Database)
* JWT Authentication (python-jose, passlib)

### 🔹 Frontend

* React.js
* Axios (API calls)


### 🔹 AI Integration

* Google Gemini API

---

## 📂 Project Structure

```id="r8fd0z"
project/
│── backend/
│   │── main.py
│   │── models.py
│   │── database.py
│   │── auth.py
│   │── services/
│
│── frontend/
│   │── src/
│   │── public/
│   │── package.json
│
│── screenshots/
│── README.md
│── requirements.txt
```

---

## ⚙️ Setup Instructions

### 🔹 Backend Setup

```bash id="9j3y7x"
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 🔹 Frontend Setup

```bash id="ymt1qv"
cd frontend
npm install
npm start
```

👉 Frontend runs on:

```id="k3k0g3"
http://localhost:3000
```

---

## 🔗 API Endpoints

### 🔐 Authentication

* `POST /register`
* `POST /login`

### 📤 Expense APIs

* `POST /upload`
* `POST /confirm`

### 📊 Analytics

* `GET /analytics`

---

## 📥 Example Request

```json id="x5q3g6"
{
  "user_id": 101,
  "role": "employee",
  "amount": 1500,
  "type": "travel",
  "gst": 100
}
```

---

## 📤 Example Response

```json id="l5ppl6"
{
  "total_expense": 1600,
  "total_tax": 100,
  "travel_expense": 1600,
  "taxi_expense": 0,
  "hotel_expense": 0
}
```



## 🧠 How It Works

1. User logs in via frontend
2. Uploads receipt
3. AI extracts details
4. User confirms expense
5. Backend validates policy
6. Data stored in database
7. Dashboard displays analytics

---

## 🚀 Future Enhancements

* 📅 Monthly & yearly reports
* 🤖 AI insights & fraud detection
* ☁️ Cloud deployment
* 📱 Mobile-friendly UI

---

## 👩‍💻 Author

**Monika Nagadevi**

---

## ⭐ Project Highlights

* Full-stack application (React + FastAPI)
* AI-powered automation
* Real-world expense management system
* Interactive analytics dashboard
