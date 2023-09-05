import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';


const App = () => {
  const [fields, setFields] = useState([]);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({});

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const fetchFieldsData = (page) => {
    axios.get(`http://localhost:8000/loan/proposal-fields/`)
      .then((response) => {
        setFields(response.data.results);
      })
      .catch((error) => {
        setError('Erro ao buscar os campos de criação da proposta.');
      });
  };

  useEffect(() => {
    fetchFieldsData();
    setFormData({

    })
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault();

    setError(null);
    axios.post('http://localhost:8000/loan/proposals/', {"custom_data": formData})
      .then((response) => {
        setFormData({})
      })
      .catch((error) => {
        let errorMessage = 'Erro ao criar a proposta: ';

        for (let key in error.response.data) {
          if (error.response.data.hasOwnProperty(key)) {
            errorMessage += `${key}: ${error.response.data[key].join(', ')} `;
          }
        }
        setError(errorMessage);
      });
  };

  return (
      <div className="App">
        <hr />
        <h1 className="app-title">Loans for Good</h1>
        <div className="container">
          <div>
            {error && (
              <div className="error-message">{error}</div>
            )}
            <h2>Criar Nova Proposta</h2>
              <form onSubmit={handleSubmit}>
              {fields.map((field) => (
                <div key={field.name}>
                  <label>{field.name}: </label>
                  <input
                    type={field.type === 'STR' ? 'text' : field.type === 'INT' ? 'number' : field.type === 'DATE' ? 'date' : field.type === 'DATETIME' ? 'datetime-local' : field.type === 'DECIMAL'? 'number' : 'text'}
                    step={field.type === 'DECIMAL' ? '0.01' : undefined}
                    name={field.name}
                    value={formData[field.name] || ''}
                    onChange={handleInputChange}
                    required={field.required}
                  />
                </div>
              ))}
              <div>
                <button type="submit">Salvar</button>
              </div>
            </form>
          </div>
        </div>
        <hr />
      </div>
  );
};

export default App;