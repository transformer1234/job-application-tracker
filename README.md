# 💼 Job Application Tracker (Full-Stack Python App)

A full-stack job application tracking system built with **FastAPI (backend)** and **Streamlit (frontend)**.  
The application allows users to manage job applications through a REST API while interacting via a clean web UI.

This project demonstrates **backend API design**, **frontend integration**, and **clean software architecture**.

---

## 🚀 Project Overview

Tracking job applications across multiple companies can become disorganized quickly.  
This project solves that problem by separating responsibilities:

- **FastAPI** handles data validation, business logic, and persistence
- **Streamlit** provides an interactive user interface
- **SQLite** stores application data persistently

This architecture mirrors real-world production systems.

---

## 🧱 Architecture

Streamlit (Frontend UI)
↓ HTTP Requests
FastAPI (REST API)
↓
CRUD Layer
↓
SQLite Database


### Why this design?
- Decoupled frontend and backend
- Backend can be reused by any client (web, mobile, CLI)
- Clear separation of concerns

---

## ✨ Features

### Frontend (Streamlit)
- Add new job applications
- View applications in a table
- Filter by status and search by company
- Update application status
- Delete applications
- Export applications as CSV
- View analytics (status distribution, total count)

### Backend (FastAPI)
- RESTful API with full CRUD operations
- Request & response validation using Pydantic
- SQLite persistence
- Auto-generated Swagger documentation

---

## 🛠 Tech Stack

- **Python**
- **FastAPI** – Backend API
- **Streamlit** – Frontend UI
- **SQLite** – Database
- **Pydantic** – Data validation
- **Pandas** – Data handling
- **Uvicorn** – ASGI server

---

## 🧠 API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/applications` | Add a new application |
| GET | `/applications` | Get all applications |
| GET | `/applications/{id}` | Get application by ID |
| PUT | `/applications/{id}` | Update application status |
| DELETE | `/applications/{id}` | Delete application |

Swagger UI available at:
http://localhost:8000/docs


---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
streamlit run frontend/app.py
```
## 📊 Analytics Included

Total applications count

Applications grouped by status (bar chart)