import React, { useState } from 'react';
import Login from './components/login.js';
import Dashboard from './components/dashboard.js';
import './styles/App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLogin = (userData) => {
    setLoading(true);
    // Simulate login process
    setTimeout(() => {
      setUser(userData);
      setLoading(false);
    }, 1000);
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (loading) {
    return React.createElement('div', { className: 'loading-container' },
      React.createElement('div', { className: 'loading-spinner' },
        React.createElement('i', { className: 'fas fa-envelope fa-spin' }),
        React.createElement('p', null, 'Signing in...')
      )
    );
  }

  if (!user) {
    return React.createElement(Login, { onLogin: handleLogin });
  }

  return React.createElement(Dashboard, { user: user, onLogout: handleLogout });
}

export default App;