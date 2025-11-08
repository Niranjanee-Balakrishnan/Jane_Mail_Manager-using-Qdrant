import React, { useState } from 'react';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    // Simple validation - in real app, this would call an API
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    const userData = {
      email: email,
      name: email.split('@')[0],
      avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(email.split('@')[0])}&background=667eea&color=fff`
    };

    onLogin(userData);
  };

  return React.createElement('div', { className: 'login-container' },
    React.createElement('div', { className: 'login-card' },
      React.createElement('div', { className: 'login-header' },
        React.createElement('i', { className: 'fas fa-envelope-open-text login-icon' }),
        React.createElement('h1', null, 'Jane Mail Manager'),
        React.createElement('p', null, 'Smart Email Processing System')
      ),
      
      React.createElement('form', { onSubmit: handleSubmit, className: 'login-form' },
        React.createElement('div', { className: 'input-group' },
          React.createElement('i', { className: 'fas fa-envelope' }),
          React.createElement('input', {
            type: 'email',
            placeholder: 'Enter your email',
            value: email,
            onChange: (e) => setEmail(e.target.value),
            required: true
          })
        ),
        
        React.createElement('div', { className: 'input-group' },
          React.createElement('i', { className: 'fas fa-lock' }),
          React.createElement('input', {
            type: 'password',
            placeholder: 'Enter your password',
            value: password,
            onChange: (e) => setPassword(e.target.value),
            required: true
          })
        ),

        error && React.createElement('div', { className: 'error-message' },
          React.createElement('i', { className: 'fas fa-exclamation-circle' }),
          error
        ),
        
        React.createElement('button', { type: 'submit', className: 'login-btn' },
          React.createElement('i', { className: 'fas fa-sign-in-alt' }),
          'Sign In'
        )
      ),
      
      React.createElement('div', { className: 'demo-notes' },
        React.createElement('p', null, 
          React.createElement('i', { className: 'fas fa-info-circle' }),
          'Demo: Use any email and password (min 6 characters)'
        )
      )
    )
  );
}

export default Login;