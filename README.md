# Jane_Mail_Manager-using-Qdrant
A full-stack web application that processes emails by chunking them, converting to embeddings, and storing in a vector database for intelligent searching. Built with React frontend and Flask backend.

🚀 Features

🔐 User Authentication - Modern login interface

📤 Send & Process Emails - Automatic chunking and embedding

🔍 Smart Search - Find emails by receiver name using vector similarity

🎨 Beautiful UI - Responsive design with modern styling

💾 Vector Storage - Qdrant vector database for efficient searching

Email-LLM/

├── backend/

│   ├── app.py                 # Flask server & API routes

│   ├── utils.py               # Email processing & vector DB logic

│   └── requirements.txt       # Python dependencies

├── frontend/

│   ├── index.html            # Main HTML file

│   ├── src/

│   │   ├── main.js           # React entry point

│   │   ├── App.js            # Main App component

│   │   ├── components/

│   │   │   ├── Login.js      # Login page component

│   │   │   ├── Dashboard.js  # Main dashboard

│   │   │   ├── SendMail.js   # Email processing interface

│   │   │   └── SearchMail.js # Email search interface

│   │   └── styles/

│   │       └── App.css       # All styling

│   └── package.json          # Node.js dependencies

└── README.md
