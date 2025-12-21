import { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [todos, setTodos] = useState([]);
    const [newTodo, setNewTodo] = useState('');
    
    // Use environment variable for API URL - no fallback
    const API_URL = process.env.REACT_APP_API_URL;

    useEffect(() => {
      fetchTodos();
    }, []);

    const fetchTodos = async () => {
      try {
        const response = await fetch(`${API_URL}/api/todos`);
        if (!response.ok) {
          throw new Error('Failed to fetch todos');
        }
        const data = await response.json();
        setTodos(data.todos);
      } catch (error) {
        console.error('Error fetching todos:', error);
      }
    };

    const addTodo = async () => {
      if (!newTodo.trim()) return;
      try {
        const response = await fetch(`${API_URL}/api/todos`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ title: newTodo }),
        });
        if (!response.ok) throw new Error('Failed to add todo');
        fetchTodos();
        setNewTodo('');
      } catch (error) {
        console.error('Error adding todo:', error);
      }
    };
    
    const toggleTodo = async (id) => {
      const todo = todos.find(t => t.id === id);
      try {
        const response = await fetch(`${API_URL}/api/todos/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            title: todo.title,           
            completed: !todo.completed 
          })
        });
        if (!response.ok) throw new Error('Failed to toggle todo');
        fetchTodos();  
      } catch (error) {
        console.error('Error toggling todo:', error);
      }
    };

    const deleteTodo = async (id) => {
      try {
        const response = await fetch(`${API_URL}/api/todos/${id}`, {
          method: 'DELETE',
        });
        if (!response.ok) throw new Error('Failed to delete todo');
        await fetchTodos();
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    };

    return (
      <div className="App">
        <h1>Todo App</h1>
        
        {/* Input section */}
        <div className="todo-input">
          <input
            type="text"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addTodo()}
            placeholder="What needs to be done?"
          />
          <button onClick={addTodo}>Add Todo</button>
        </div>
    
        {/* Todo list */}
        <div className="todo-list">
          {todos.length === 0 ? (
            <p>No todos yet. Add one above!</p>
          ) : (
            todos.map(todo => (
              <div key={todo.id} className="todo-item">
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => toggleTodo(todo.id)}
                />
                <span className={todo.completed ? 'completed' : ''}>
                  {todo.title}
                </span>
                <button onClick={() => deleteTodo(todo.id)}>Delete</button>
              </div>
            ))
          )}
        </div>
      </div>
    );
}

export default App;