import React, { useState } from 'react';
import axios from 'axios';

function SearchMail() {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setError('Please enter a receiver name to search');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await axios.post('http://localhost:5000/api/search-email', {
        receiver_name: searchQuery
      });

      setResults(response.data);
    } catch (error) {
      setError('Search failed: ' + (error.response?.data?.error || error.message));
    }

    setLoading(false);
  };

  return React.createElement('div', { className: 'search-mail-container' },
    React.createElement('div', { className: 'search-header' },
      React.createElement('i', { className: 'fas fa-search' }),
      React.createElement('h2', null, 'Search Emails')
    ),

    React.createElement('form', { onSubmit: handleSearch, className: 'search-form' },
      React.createElement('div', { className: 'search-input-group' },
        React.createElement('input', {
          type: 'text',
          placeholder: 'Enter receiver name to search...',
          value: searchQuery,
          onChange: (e) => setSearchQuery(e.target.value),
          disabled: loading
        }),
        React.createElement('button', {
          type: 'submit',
          disabled: loading,
          className: `search-btn ${loading ? 'loading' : ''}`
        },
          loading 
            ? React.createElement('i', { className: 'fas fa-spinner fa-spin' })
            : React.createElement('i', { className: 'fas fa-search' })
        )
      )
    ),

    error && React.createElement('div', { className: 'error-message' },
      React.createElement('i', { className: 'fas fa-exclamation-circle' }),
      error
    ),

    loading && React.createElement('div', { className: 'loading-message' },
      React.createElement('i', { className: 'fas fa-spinner fa-spin' }),
      'Searching emails...'
    ),

    results && React.createElement('div', { className: 'search-results' },
      React.createElement('div', { className: 'results-header' },
        React.createElement('h3', null,
          React.createElement('i', { className: 'fas fa-envelope' }),
          ` Results for: ${results.receiver_name}`
        ),
        React.createElement('span', { className: 'results-count' },
          `${results.results_count || Object.keys(results.emails || {}).length} found`
        )
      ),

      React.createElement('div', { className: 'results-content' },
        React.createElement('div', { className: 'formatted-results' },
          React.createElement('h4', null,
            React.createElement('i', { className: 'fas fa-file-alt' }),
            ' Formatted Results'
          ),
          React.createElement('pre', null, results.formatted_response)
        ),

        React.createElement('details', { className: 'raw-data' },
          React.createElement('summary', null,
            React.createElement('i', { className: 'fas fa-code' }),
            ' Raw Data (Technical Details)'
          ),
          React.createElement('pre', null, 
            JSON.stringify({
              receiver_name: results.receiver_name,
              emails: results.emails,
              results_count: results.results_count
            }, null, 2)
          )
        )
      )
    ),

    !loading && !results && !error && React.createElement('div', { className: 'search-guide' },
      React.createElement('i', { className: 'fas fa-lightbulb' }),
      React.createElement('h3', null, 'Search Tips'),
      React.createElement('ul', null,
        React.createElement('li', null, 'Enter the exact receiver name used when sending the email'),
      )
    )
  );
}

export default SearchMail;