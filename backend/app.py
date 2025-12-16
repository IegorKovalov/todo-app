from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_session, Todo
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
    session = get_db_session()
    try:
        todos = session.query(Todo).order_by(Todo.id).all()
        return jsonify({'todos': [todo.to_dict() for todo in todos]})
    finally:
        session.close()

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.json
    session = get_db_session()
    try:
        new_todo = Todo(title=data['title'], completed=False)
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)
        return jsonify(new_todo.to_dict()), 201
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    session = get_db_session()
    try:
        todo = session.query(Todo).filter(Todo.id == todo_id).first()
        if todo is None:
            return jsonify({'error': 'Todo not found'}), 404
        
        todo.title = data['title']
        todo.completed = data['completed']
        session.commit()
        session.refresh(todo)
        return jsonify(todo.to_dict())
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    session = get_db_session()
    try:
        todo = session.query(Todo).filter(Todo.id == todo_id).first()
        if todo is None:
            return jsonify({'error': 'Todo not found'}), 404
        
        session.delete(todo)
        session.commit()
        return jsonify({'message': 'Todo deleted successfully'})
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
