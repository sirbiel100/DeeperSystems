
# User Management App

This is a full-stack user management application built with **Vue 3 + Vite** (frontend) and **Flask + MongoDB** (backend). It supports creating, editing, viewing, and deleting user data.

---

## 🌐 Features

- RESTful API using Flask
- MongoDB for data storage
- JSON parsing and seeding via `parser.py`
- Vue 3 frontend with PrimeVue components
- Cross-Origin Resource Sharing enabled
- Role management and user status control

---

## 📁 Project Structure

```
.
├── backend/
│   ├── app.py               # Flask API
│   ├── parser.py            # JSON parser and MongoDB seeder
│   ├── udata.json           # Provided JSON data
│   ├── .env                 # Environment variables (MongoDB URI)
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── UserFormModal.vue
│   │   ├── views/
│   │   │   ├── UsersView.vue
│   │   │   └── UserView.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── services/
│   │   │   └── apiService.js
│   │   └── App.vue, main.js, etc.
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sirbiel100/DeeperSystems.git
cd DeeperSystems
```

### 2. Setup Backend

#### Create `.env` file:

```bash
cd backend
cp .env.example .env
```

Edit `.env` and provide your MongoDB URI:

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/user_db?retryWrites=true&w=majority&appName=<appname>
```

#### Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Seed MongoDB with initial data:

```bash
python parser.py
```

#### Run the Flask server:

```bash
python app.py
```

Server will be available at `http://localhost:5000`.

---

### 3. Setup Frontend

```bash
cd ../frontend
npm install
npm run dev
```

Frontend will run on `http://localhost:5173`.

---

## 📡 API Endpoints

- `GET /api/users` - List users
- `GET /api/users/<id>` - Get user
- `PATCH /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

---

## 🧪 Notes

- Ensure MongoDB is running and accessible.
- Frontend is configured to access backend at `localhost:5000`.
- Do not forget to replace `<password>` in `.env`.

---