# Product CRUD App

This is a simple CRUD application for managing products using Python (FastAPI), MongoDB, and Vue.js.

## Prerequisites

- Python 3.8+
- Node.js & npm
- MongoDB (running locally on port 27017)

## Setup

### Backend

1.  Navigate to `backend` folder.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
    Server runs at http://localhost:8000

### Frontend

1.  Navigate to `frontend` folder.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
    App runs at http://localhost:5173 (or check terminal output)

## Features

- Create, Read, Update, Delete products.
- Uses FastAPI for backend API.
- Uses MongoDB (via Motor) for database.
- Uses Vue 3 + Vite for frontend.
