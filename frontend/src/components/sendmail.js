import axios from 'axios';
import React, { useState } from 'react';

function SendMail() {
  const [formData, setFormData] = useState({
    to: '',
    subject: '',
    content: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post('http://localhost:5000/api/process-email', {
        email_content: `Subject: ${formData.subject}\n\nTo: ${formData.to}\n\n${formData.content}`,
        receiver_name: formData.to
      });

      setMessage({
        type: 'success',
        text: `Email processed successfully! Created ${response.data.chunks_count} chunks.`
      });

      // Reset form
      setFormData({
        to: '',
        subject: '',
        content: ''
      });

    } catch (error) {
      setMessage({
        type: 'error',
        text: 'Failed to process email: ' + (error.response?.data?.error || error.message)
      });
    }

    setLoading(false);
  };

  return React.createElement('div', { className: 'send-mail-container' },
    React.createElement('div', { className: 'send-mail-header' },
      React.createElement('i', { className: 'fas fa-paper-plane' }),
      React.createElement('h2', null, 'Send & Process Email')
    ),

    React.createElement('form', { onSubmit: handleSubmit, className: 'send-mail-form' },
      React.createElement('div', { className: 'form-group' },
        React.createElement('label', null, 
          React.createElement('i', { className: 'fas fa-user' }),
          'To (Receiver Name)'
        ),
        React.createElement('input', {
          type: 'text',
          placeholder: 'Enter receiver name',
          value: formData.to,
          onChange: (e) => handleChange('to', e.target.value),
          required: true
        })
      ),

      React.createElement('div', { className: 'form-group' },
        React.createElement('label', null,
          React.createElement('i', { className: 'fas fa-tag' }),
          'Subject'
        ),
        React.createElement('input', {
          type: 'text',
          placeholder: 'Enter email subject',
          value: formData.subject,
          onChange: (e) => handleChange('subject', e.target.value),
          required: true
        })
      ),

      React.createElement('div', { className: 'form-group' },
        React.createElement('label', null,
          React.createElement('i', { className: 'fas fa-envelope' }),
          'Email Content'
        ),
        React.createElement('textarea', {
          placeholder: 'Write your email content here...',
          rows: '8',
          value: formData.content,
          onChange: (e) => handleChange('content', e.target.value),
          required: true
        })
      ),

      message && React.createElement('div', { 
        className: `message ${message.type}` 
      },
        React.createElement('i', { 
          className: `fas ${message.type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}` 
        }),
        message.text
      ),

      React.createElement('button', {
        type: 'submit',
        disabled: loading,
        className: `submit-btn ${loading ? 'loading' : ''}`
      },
        loading 
          ? [React.createElement('i', { key: 'loading', className: 'fas fa-spinner fa-spin' }), ' Processing...']
          : [React.createElement('i', { key: 'send', className: 'fas fa-paper-plane' }), ' Process Email']
      )
    ),

    
  );
}

export default SendMail;