from flask import Flask, request, jsonify
from flask_cors import CORS

todos = []
todo_id_counter = 1

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
    return jsonify({'todos': todos})

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    global todo_id_counter
    new_todo = {
        'id': todo_id_counter,
        'title': data['title'],
        'completed': False
    }
    todos.append(new_todo)
    todo_id_counter += 1
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    global todos
    for todo in todos:
        if todo['id'] == todo_id:
            todo['title'] = data['title']
            todo['completed'] = data['completed']
            return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404
    

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'message': 'Todo deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')