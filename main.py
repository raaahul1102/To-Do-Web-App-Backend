from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database connection details
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to establish a database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Function to create the schema
def create_schema():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS task (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                is_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()

# Call the schema creation function on app startup
create_schema()

# Routes

# Get all todos
@app.route('/api/todos', methods=['GET'])
def get_all_todos():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM task;")
            task = cur.fetchall()
            result = [
                {
                    "id": task[0],
                    "title": task[1],
                    "is_completed": task[2],
                    "created_at": str(task[3]),
                    "updated_at": str(task[4])
                }
                for task in task
            ]
            return jsonify(result), 200

# Create a new todo
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    title = data.get('title')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO task (title) 
            VALUES (%s) 
            RETURNING id, title, is_completed, created_at, updated_at;
            """, (title,))
            task = cur.fetchone()
            conn.commit()
            return jsonify({
                "id": task[0],
                "title": task[1],
                "is_completed": task[2],
                "created_at": str(task[3]),
                "updated_at": str(task[4])
            }), 201

# Update a todo
@app.route('/api/todos/<int:task_id>', methods=['PUT'])
def update_todo(task_id):
    data = request.get_json()
    title = data.get('title')
    is_completed = data.get('is_completed')

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE task
            SET title = COALESCE(%s, title),
                is_completed = COALESCE(%s, is_completed),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, title, is_completed, created_at, updated_at;
            """, (title, is_completed, task_id))
            task = cur.fetchone()
            if not task:
                return jsonify({"error": "Task not found"}), 404
            conn.commit()
            return jsonify({
                "id": task[0],
                "title": task[1],
                "is_completed": task[2],
                "created_at": str(task[3]),
                "updated_at": str(task[4])
            }), 200

# Delete a single todo
@app.route('/api/todos/<int:task_id>', methods=['DELETE'])
def delete_todo(task_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM task WHERE id = %s RETURNING id;", (task_id,))
            task = cur.fetchone()
            if not task:
                return jsonify({"error": "Task not found"}), 404
            conn.commit()
            return jsonify({"message": "Task deleted"}), 200

# Delete all todos
@app.route('/api/todos', methods=['DELETE'])
def delete_all_todos():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM task;")
            conn.commit()
            return jsonify({"message": "All task deleted"}), 200

@app.route('/')
def index():
    return {"message": "Welcome to the Todo App API"}

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
