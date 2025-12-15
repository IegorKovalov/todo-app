from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Todo App API",
        "endpoints": {
            "get_todos": "GET /api/todos",
            "create_todo": "POST /api/todos",
            "update_todo": "PUT /api/todos/<id>",
            "delete_todo": "DELETE /api/todos/<id>"
        }
    })

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'Flask is working!'})

@app.route('/api/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, completed FROM todos ORDER BY id')
    todos = []
    for row in cur.fetchall():
        todos.append({
            'id': row[0],
            'title': row[1],
            'completed': row[2]
        })
    cur.close()
    conn.close()
    return jsonify({'todos': todos})

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO todos (title, completed) VALUES (%s, %s) RETURNING id, title, completed',
        (data['title'], False)
    )
    row = cur.fetchone()
    new_todo = {
        'id': row[0],
        'title': row[1],
        'completed': row[2]
    }
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE todos SET title = %s, completed = %s WHERE id = %s RETURNING id, title, completed',
        (data['title'], data['completed'], todo_id)
    )
    row = cur.fetchone()
    if row is None:
        return jsonify({'error': 'Todo not found'}), 404
    updated_todo = {
        'id': row[0],
        'title': row[1],
        'completed': row[2]
    }
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(updated_todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')