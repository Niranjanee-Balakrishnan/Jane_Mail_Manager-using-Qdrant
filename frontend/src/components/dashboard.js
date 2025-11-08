import React, { useState } from 'react';
import SearchMail from './searchmail.js';
import SendMail from './sendmail.js';

function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('send');

  const handleLogout = () => {
    onLogout();
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'send':
        return React.createElement(SendMail);
      case 'search':
        return React.createElement(SearchMail);
      default:
        return React.createElement(SendMail);
    }
  };

  return React.createElement('div', { className: 'dashboard-container' },
    React.createElement('header', { className: 'dashboard-header' },
      React.createElement('div', { className: 'header-left' },
        React.createElement('i', { className: 'fas fa-envelope-open-text logo' }),
        React.createElement('h1', null, 'Jane Mail Manager')
      ),
      React.createElement('div', { className: 'header-right' },
        React.createElement('div', { className: 'user-info' },
          React.createElement('img', { 
            src: user.avatar, 
            alt: user.name, 
            className: 'user-avatar' 
          }),
          React.createElement('span', { className: 'user-name' }, user.name)
        ),
        React.createElement('button', { 
          onClick: handleLogout, 
          className: 'logout-btn' 
        },
          React.createElement('i', { className: 'fas fa-sign-out-alt' }),
          'Logout'
        )
      )
    ),

    React.createElement('nav', { className: 'dashboard-nav' },
      React.createElement('button', {
        className: `nav-btn ${activeTab === 'send' ? 'active' : ''}`,
        onClick: () => setActiveTab('send')
      },
        React.createElement('i', { className: 'fas fa-paper-plane' }),
        'Send Mail'
      ),
      React.createElement('button', {
        className: `nav-btn ${activeTab === 'search' ? 'active' : ''}`,
        onClick: () => setActiveTab('search')
      },
        React.createElement('i', { className: 'fas fa-search' }),
        'Search Mail'
      )
    ),

    React.createElement('main', { className: 'dashboard-main' },
      renderContent()
    ),

    React.createElement('footer', { className: 'dashboard-footer' },
      React.createElement('p', null, 
        '© 2025 jane Mail Manager - Smart Email Processing System'
      )
    )
  );
}

export default Dashboard;