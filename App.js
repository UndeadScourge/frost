import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('');
  const [input3, setInput3] = useState('');
  const [response1, setResponse1] = useState('');
  const [response2, setResponse2] = useState('');
  const [loading1, setLoading1] = useState(false);
  const [loading2, setLoading2] = useState(false);

  const API_BASE_URL = 'http://localhost:5000/api';

  // First button - GET request
  const handleButton1Click = async () => {
    if (!input1.trim()) {
      alert('Please enter first parameter');
      return;
    }

    setLoading1(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/get_message`, {
        params: {
          param: input1
        }
      });
      setResponse1(response.data.message);
    } catch (error) {
      console.error('GET request error:', error);
      setResponse1('Request failed, please check backend service');
    } finally {
      setLoading1(false);
    }
  };

  // Second button - POST request
  const handleButton2Click = async () => {
    if (!input2.trim() || !input3.trim()) {
      alert('Please fill both second and third inputs');
      return;
    }

    setLoading2(true);
    try {
      const response = await axios.post(
        `${API_BASE_URL}/post_message?param=${encodeURIComponent(input3)}`,
        {
          bodyParam: input2
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      setResponse2(response.data.message);
    } catch (error) {
      console.error('POST request error:', error);
      setResponse2('Request failed, please check backend service');
    } finally {
      setLoading2(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>React + Flask - Full Demo</h1>
      
      {/* GET Request Section */}
      <div style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '20px', 
        borderRadius: '8px',
        marginBottom: '20px',
        border: '1px solid #dee2e6'
      }}>
        <h2 style={{ color: '#007bff' }}>GET Request Test</h2>
        <p style={{ color: '#6c757d' }}>First input: URL parameter for GET request</p>
        
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
          <input
            type="text"
            placeholder="Enter GET request parameter"
            value={input1}
            onChange={(e) => setInput1(e.target.value)}
            style={{ 
              padding: '10px', 
              width: '300px', 
              fontSize: '16px',
              marginRight: '10px',
              border: '1px solid #ced4da',
              borderRadius: '4px'
            }}
          />
          <button 
            onClick={handleButton1Click} 
            disabled={loading1}
            style={{ 
              padding: '10px 20px', 
              fontSize: '16px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {loading1 ? 'Sending...' : 'Send GET Request'}
          </button>
        </div>

        {response1 && (
          <div style={{ 
            padding: '15px', 
            backgroundColor: '#d1ecf1', 
            borderRadius: '4px',
            border: '1px solid #bee5eb'
          }}>
            <strong>GET Response:</strong> {response1}
          </div>
        )}
      </div>

      {/* POST Request Section */}
      <div style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '20px', 
        borderRadius: '8px',
        border: '1px solid #dee2e6'
      }}>
        <h2 style={{ color: '#28a745' }}>POST Request Test</h2>
        <p style={{ color: '#6c757d' }}>Second input: Body parameter, Third input: URL parameter</p>
        
        <div style={{ marginBottom: '15px' }}>
          <input
            type="text"
            placeholder="Enter POST request body parameter"
            value={input2}
            onChange={(e) => setInput2(e.target.value)}
            style={{ 
              padding: '10px', 
              width: '300px', 
              fontSize: '16px',
              marginRight: '10px',
              border: '1px solid #ced4da',
              borderRadius: '4px',
              marginBottom: '10px',
              display: 'block'
            }}
          />
          <input
            type="text"
            placeholder="Enter POST request URL parameter"
            value={input3}
            onChange={(e) => setInput3(e.target.value)}
            style={{ 
              padding: '10px', 
              width: '300px', 
              fontSize: '16px',
              marginRight: '10px',
              border: '1px solid #ced4da',
              borderRadius: '4px',
              display: 'block'
            }}
          />
        </div>

        <button 
          onClick={handleButton2Click} 
          disabled={loading2}
          style={{ 
            padding: '10px 20px', 
            fontSize: '16px',
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          {loading2 ? 'Sending...' : 'Send POST Request'}
        </button>

        {response2 && (
          <div style={{ 
            padding: '15px', 
            backgroundColor: '#d4edda', 
            borderRadius: '4px',
            border: '1px solid #c3e6cb',
            marginTop: '15px'
          }}>
            <strong>POST Response:</strong> {response2}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;