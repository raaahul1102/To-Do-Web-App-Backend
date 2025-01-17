
# To-Do-Web-App-Backend

This is the backend for a Todo App, built with Flask and PostgreSQL. It provides RESTful API endpoints to manage tasks, including creating, retrieving, updating, and deleting them.

---

## Features
- Create a new task.
- Retrieve all tasks.
- Delete a specific task.
- Delete all tasks.
- Automatic schema creation on startup.
- JSON-based API responses.

---

## Prerequisites
Ensure the following are installed on your system:

- **Python 3.8+**
- **PostgreSQL**
- **Pip** (Python package manager)

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install flask flask-cors psycopg2
   ```

4. **Set Up the Database:**
   - Ensure PostgreSQL is running.
   - Create a new database for the app.
   - Set the `DATABASE_URL` environment variable:
     ```bash
     export DATABASE_URL="postgresql://<username>:<password>@<host>:<port>/<database_name>"
     ```

5. **Run the Application:**
   ```bash
   python main.py
   ```

6. The backend server will run on `http://localhost:5000` by default.

---

## API Endpoints

### Base URL
`http://localhost:5000`

### Endpoints

#### 1. Get All Todos
**`GET /api/todos`**
- **Response:**
  ```json
  [
    {
      "id": 1,
      "title": "Buy a new gaming laptop",
      "is_completed": false,
      "created_at": "2025-01-18T10:00:00",
      "updated_at": "2025-01-18T10:00:00"
    }
  ]
  ```

#### 2. Create a New Todo
**`POST /api/todos`**
- **Request Body:**
  ```json
  {
    "title": "New Task"
  }
  ```
- **Response:**
  ```json
  {
    "id": 2,
    "title": "New Task",
    "is_completed": false,
    "created_at": "2025-01-18T10:05:00",
    "updated_at": "2025-01-18T10:05:00"
  }
  ```


#### 3. Delete a Specific Todo
**`DELETE /api/todos/<id>`**
- **Response:**
  ```json
  {
    "message": "Task deleted"
  }
  ```

#### 4. Delete All Todos
**`DELETE /api/todos`**
- **Response:**
  ```json
  {
    "message": "All tasks deleted"
  }
  ```

---

## Database Schema
The database includes the following table:

**Table: `task`**
| Column        | Type          | Description                     |
|---------------|---------------|---------------------------------|
| `id`          | SERIAL        | Primary key                    |
| `title`       | VARCHAR(255)  | Title of the task              |
| `is_completed`| BOOLEAN       | Completion status of the task  |
| `created_at`  | TIMESTAMP     | Timestamp when created         |
| `updated_at`  | TIMESTAMP     | Timestamp when last updated    |

---

## Project Structure
```
backend/
├── main.py             # Entry point of the application
├── requirements.txt    # Python dependencies
└── README.md           # Documentation (this file)
```

---

## Testing the API
You can test the API using tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/).

### Example with `cURL`

#### Get All Todos
```bash
curl -X GET http://localhost:5000/api/todos
```

#### Create a New Todo
```bash
curl -X POST http://localhost:5000/api/todos -H "Content-Type: application/json" -d '{"title": "New Task"}'
```

---

## Frontend 


