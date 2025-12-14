import { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/test')
        .then(response => response.json())
        .then(data => setMessage(data.message))
        .catch(error => console.error('Error:', error));
    }, []);

    return (
      <div className="App">
        <h1>Todo App</h1>
        <p>Message from Flask: {message}</p>
      </div>
    );
}

export default App;