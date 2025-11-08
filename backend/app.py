from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re

app = Flask(__name__)
CORS(app)

print("✅ Starting Email Processing Server...")

# Simple in-memory storage
email_database = []

class EmailProcessor:
    def chunk_email(self, email_content, chunk_size=200):
        """Split email into smaller chunks"""
        print(f"✂️ Chunking email content...")
        
        # Simple sentence-based chunking
        sentences = re.split(r'[.!?]+', email_content)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        print(f"📄 Created {len(chunks)} chunks")
        return chunks

email_processor = EmailProcessor()

@app.route('/api/process-email', methods=['POST'])
def process_email():
    """Process incoming email and store"""
    try:
        data = request.json
        email_content = data.get('email_content')
        receiver_name = data.get('receiver_name')
        
        print(f"📧 Processing email for: {receiver_name}")
        
        if not email_content or not receiver_name:
            return jsonify({'error': 'Email content and receiver name are required'}), 400
        
        # Process email: chunk and store
        chunks = email_processor.chunk_email(email_content)
        
        # Create email record
        email_id = len(email_database) + 1
        email_record = {
            'id': email_id,
            'receiver_name': receiver_name,
            'email_content': email_content,
            'chunks': chunks,
            'full_content': email_content,
            'timestamp': '2025-11-08 12:00:00'  # Simple timestamp
        }
        
        email_database.append(email_record)
        
        print(f"✅ Email stored successfully! Total emails: {len(email_database)}")
        
        return jsonify({
            'message': 'Email processed successfully',
            'chunks_count': len(chunks),
            'receiver_name': receiver_name,
            'email_id': email_id,
            'total_emails': len(email_database)
        }), 200
        
    except Exception as e:
        print(f"❌ Error processing email: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-email', methods=['POST'])
def search_email():
    """Search for emails by receiver name - EXACT MATCHING"""
    try:
        data = request.json
        receiver_name = data.get('receiver_name')
        
        print(f"🔍 Searching emails for: {receiver_name}")
        print(f"📊 Total emails in database: {len(email_database)}")
        
        if not receiver_name:
            return jsonify({'error': 'Receiver name is required'}), 400
        
        # EXACT MATCH search by receiver name (case-insensitive)
        matching_emails = []
        for email in email_database:
            if email['receiver_name'].lower() == receiver_name.lower():
                matching_emails.append(email)
        
        print(f"✅ Found {len(matching_emails)} emails for {receiver_name}")
        
        # Format results
        formatted_response = format_email_response(matching_emails, receiver_name)
        
        return jsonify({
            'receiver_name': receiver_name,
            'emails': matching_emails,
            'formatted_response': formatted_response,
            'results_count': len(matching_emails),
            'total_in_database': len(email_database)
        }), 200
        
    except Exception as e:
        print(f"❌ Error searching emails: {str(e)}")
        return jsonify({'error': str(e)}), 500

def format_email_response(emails, receiver_name):
    """Format email search results in a readable way"""
    if not emails:
        return f"No emails found for '{receiver_name}'"
    
    formatted_response = f"📧 EMAILS FOR: {receiver_name}\n"
    formatted_response += "=" * 50 + "\n\n"
    
    for i, email in enumerate(emails, 1):
        formatted_response += f"📄 EMAIL {i}:\n"
        formatted_response += f"👤 Receiver: {email['receiver_name']}\n"
        formatted_response += f"🆔 ID: {email['id']}\n"
        formatted_response += f"📅 Date: {email.get('timestamp', 'N/A')}\n"
        formatted_response += "-" * 40 + "\n"
        formatted_response += f"{email['full_content']}\n\n"
        formatted_response += "=" * 50 + "\n\n"
    
    return formatted_response

@app.route('/api/all-emails', methods=['GET'])
def get_all_emails():
    """Get all stored emails (for debugging)"""
    return jsonify({
        'total_emails': len(email_database),
        'emails': email_database
    })

@app.route('/api/clear-emails', methods=['POST'])
def clear_emails():
    """Clear all emails"""
    email_database.clear()
    return jsonify({
        'message': 'All emails cleared!', 
        'total_emails': 0
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'Backend is running!', 
        'total_emails_stored': len(email_database),
        'endpoints': {
            'process_email': 'POST /api/process-email',
            'search_email': 'POST /api/search-email',
            'all_emails': 'GET /api/all-emails',
            'clear_emails': 'POST /api/clear-emails',
            'health': 'GET /api/health'
        }
    })

@app.route('/api/test-data', methods=['POST'])
def add_test_data():
    """Add some test emails for demo"""
    test_emails = [
        {
            'receiver_name': 'Yaalini',
            'content': '''Hi Yaalini,

I hope this email finds you well. I wanted to follow up on our conversation about the upcoming project deadline.

We need to finalize the design specifications by next Friday. Please let me know if you need any additional resources.

Best regards,
John'''
        },
        {
            'receiver_name': 'Yaalini',
            'content': '''Hello Yaalini,

Quick reminder about the team meeting tomorrow at 10 AM in Conference Room B.

Please bring your project updates and any blockers you're facing.

Thanks,
Sarah'''
        },
        {
            'receiver_name': 'Rajesh',
            'content': '''Dear Rajesh,

Thank you for submitting your report. I've reviewed it and have some feedback.

Could we schedule a quick call to discuss the changes?

Regards,
Manager'''
        }
    ]
    
    for test_email in test_emails:
        chunks = email_processor.chunk_email(test_email['content'])
        email_id = len(email_database) + 1
        email_record = {
            'id': email_id,
            'receiver_name': test_email['receiver_name'],
            'email_content': test_email['content'],
            'chunks': chunks,
            'full_content': test_email['content'],
            'timestamp': '2025-11-08 12:00:00'
        }
        email_database.append(email_record)
    
    return jsonify({
        'message': f'Added {len(test_emails)} test emails',
        'total_emails': len(email_database)
    })

if __name__ == '__main__':
    print("🚀 Email Processing Server Started!")
    print("📍 http://localhost:5000")
    print("📚 Available Endpoints:")
    print("   GET  /api/health - Health check")
    print("   POST /api/process-email - Process email")
    print("   POST /api/search-email - Search emails")
    print("   GET  /api/all-emails - List all emails")
    print("   POST /api/clear-emails - Clear all emails")
    print("   POST /api/test-data - Add test data")
    print("\n💡 Use POST /api/test-data to add sample emails for testing")
    app.run(debug=True, port=5000, host='0.0.0.0')