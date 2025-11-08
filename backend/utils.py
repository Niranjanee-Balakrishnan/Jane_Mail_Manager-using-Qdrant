from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class EmailProcessor:
    """
    Handles email processing: chunking and embedding
    """
    
    def __init__(self):
        print("🔄 Loading embedding model...")
        # Load embedding model (local, no API key needed)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded!")
    
    def chunk_email(self, email_content, chunk_size=200):
        """
        Split email into smaller chunks for better embedding
        chunk_size: number of characters per chunk
        """
        print(f"✂️ Chunking email (size: {chunk_size} chars)")
        
        # Simple chunking by fixed length
        chunks = []
        sentences = email_content.split('. ')
        
        current_chunk = ""
        for sentence in sentences:
            # If adding this sentence would exceed chunk size, save current chunk
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
            else:
                current_chunk += sentence + ". "
        
        # Add the last chunk if it's not empty
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # If no chunks were created (very short email), use the whole content
        if not chunks:
            chunks = [email_content]
            
        print(f"📄 Created {len(chunks)} chunks")
        return chunks
    
    def get_embedding(self, text):
        """
        Generate embedding vector for text
        """
        return self.embedding_model.encode(text).tolist()

class VectorDBManager:
    """
    Manages Qdrant vector database operations
    """
    
    def __init__(self):
        print("🔄 Initializing Qdrant database...")
        # Initialize Qdrant client (in-memory for simplicity)
        self.client = QdrantClient(":memory:")
        
        # Create collection if it doesn't exist
        try:
            self.client.create_collection(
                collection_name="emails",
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print("✅ Created new Qdrant collection 'emails'")
        except Exception as e:
            print("✅ Using existing Qdrant collection 'emails'")
        
        self.email_processor = EmailProcessor()
        self.point_id = 0
        print("✅ Vector database initialized!")
    
    def store_email_chunks(self, chunks, receiver_name):
        """
        Store email chunks in vector database with metadata
        """
        print(f"💾 Storing {len(chunks)} chunks for {receiver_name}")
        
        points = []
        
        for i, chunk in enumerate(chunks):
            # Generate embedding for chunk
            embedding = self.email_processor.get_embedding(chunk)
            
            # Create point with metadata
            point = PointStruct(
                id=self.point_id,
                vector=embedding,
                payload={
                    "chunk_text": chunk,
                    "receiver_name": receiver_name,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            )
            points.append(point)
            self.point_id += 1
        
        # Upload points to Qdrant
        self.client.upsert(
            collection_name="emails",
            points=points
        )
        
        print(f"✅ Successfully stored {len(points)} chunks in database")
    
def search_by_receiver(self, receiver_name, limit=10):
    """
    Search for emails by receiver name using vector similarity
    """
    print(f"🔎 Searching for emails to: {receiver_name}")
    
    # Create query vector from receiver name
    query_vector = self.email_processor.get_embedding(receiver_name)
    
    # Search in vector database
    search_result = self.client.search(
        collection_name="emails",
        query_vector=query_vector,
        limit=limit
    )
    
    print(f"📊 Found {len(search_result)} potential matches")
    
    # Reconstruct emails from chunks - FILTER BY RECEIVER NAME
    emails = {}
    for result in search_result:
        payload = result.payload
        stored_receiver = payload["receiver_name"]
        chunk_text = payload["chunk_text"]
        chunk_index = payload["chunk_index"]
        
        # ONLY include emails that match the searched receiver name
        if stored_receiver.lower() == receiver_name.lower():
            if stored_receiver not in emails:
                emails[stored_receiver] = []
            
            emails[stored_receiver].append({
                'text': chunk_text,
                'score': result.score,
                'chunk_index': chunk_index
            })
    
    # Sort chunks by their index to reconstruct original order
    for receiver in emails:
        emails[receiver].sort(key=lambda x: x['chunk_index'])
    
    print(f"✅ Filtered to {len(emails)} matching receivers")
    return emails

class LLMService:
    """
    Handles response formatting
    """
    
    def __init__(self):
        print("✅ LLM service initialized (simple formatter)")
    
    def format_email_response(self, emails, receiver_name):
        """
        Format email search results in a readable way
        """
        if not emails:
            return f"No emails found for '{receiver_name}'"
        
        formatted_response = f"📧 EMAILS FOR: {receiver_name}\n"
        formatted_response += "=" * 50 + "\n\n"
        
        for receiver, chunks in emails.items():
            formatted_response += f"👤 RECEIVER: {receiver}\n"
            formatted_response += f"📊 CONFIDENCE: {chunks[0]['score']:.2f}\n"
            formatted_response += "-" * 30 + "\n"
            
            # Reconstruct full email from chunks
            full_email = " ".join([chunk['text'] for chunk in chunks])
            formatted_response += f"📄 CONTENT:\n{full_email}\n\n"
            formatted_response += "=" * 50 + "\n\n"
        
        return formatted_response