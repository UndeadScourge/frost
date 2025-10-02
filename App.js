import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const testConnection = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:5000/api/test');
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Connection failed! Check backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '50px' }}>
      <h1>React + Flask Demo</h1>
      <button 
        onClick={testConnection} 
        disabled={loading}
        style={{ 
          padding: '15px 30px', 
          fontSize: '18px', 
          backgroundColor: '#61dafb',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          margin: '20px'
        }}
      >
        {loading ? 'Testing...' : 'Test Connection'}
      </button>
      {message && (
        <div style={{ 
          marginTop: '20px', 
          padding: '20px', 
          backgroundColor: '#f0f0f0',
          borderRadius: '5px'
        }}>
          <h3>Backend Response:</h3>
          <p>{message}</p>
        </div>
      )}
    </div>
  );
}

export default App;