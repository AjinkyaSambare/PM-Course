import os
import numpy as np
from typing import List, Dict, Any
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity


class MockPineconeDB:
    """
    Mock implementation of Pinecone for demonstration purposes.
    In production, you would use the actual Pinecone client.
    """
    
    def __init__(self):
        self.spotify_index = {}
        self.netflix_index = {}
        self.spotify_vectors = []
        self.netflix_vectors = []
    
    def upsert_spotify_embeddings(self, embeddings: List[Dict[str, Any]]):
        """Store Spotify embeddings in mock database"""
        for embedding in embeddings:
            self.spotify_index[embedding['id']] = embedding
            self.spotify_vectors.append(embedding['vector'])
    
    def upsert_netflix_embeddings(self, embeddings: List[Dict[str, Any]]):
        """Store Netflix embeddings in mock database"""
        for embedding in embeddings:
            self.netflix_index[embedding['id']] = embedding
            self.netflix_vectors.append(embedding['vector'])
    
    def similarity_search_spotify(self, query_vector: List[float], top_k: int = 5):
        """Find similar Spotify tracks using cosine similarity"""
        if not self.spotify_vectors:
            return []
        
        # Convert to numpy arrays for computation
        query_vector = np.array(query_vector).reshape(1, -1)
        all_vectors = np.array(self.spotify_vectors)
        
        # Compute cosine similarity
        similarities = cosine_similarity(query_vector, all_vectors)[0]
        
        # Get top-k most similar items
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            item_id = f"spotify_{idx}"
            if item_id in self.spotify_index:
                result = self.spotify_index[item_id].copy()
                result['similarity'] = float(similarities[idx])
                results.append(result)
        
        return results
    
    def similarity_search_netflix(self, query_vector: List[float], top_k: int = 5):
        """Find similar Netflix content using cosine similarity"""
        if not self.netflix_vectors:
            return []
        
        # Convert to numpy arrays for computation
        query_vector = np.array(query_vector).reshape(1, -1)
        all_vectors = np.array(self.netflix_vectors)
        
        # Compute cosine similarity
        similarities = cosine_similarity(query_vector, all_vectors)[0]
        
        # Get top-k most similar items
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            item_id = f"netflix_{idx}"
            if item_id in self.netflix_index:
                result = self.netflix_index[item_id].copy()
                result['similarity'] = float(similarities[idx])
                results.append(result)
        
        return results
    
    def get_all_spotify_embeddings(self):
        """Get all Spotify embeddings"""
        return list(self.spotify_index.values())
    
    def get_all_netflix_embeddings(self):
        """Get all Netflix embeddings"""
        return list(self.netflix_index.values())


class RealPineconeDB:
    """
    Real Pinecone implementation (requires API key and setup).
    This is commented out as it requires actual Pinecone credentials.
    """
    
    def __init__(self, api_key: str, environment: str):
        """
        Initialize Pinecone client
        
        # Uncomment and modify as needed for real implementation:
        
        import pinecone
        
        pinecone.init(
            api_key=api_key,
            environment=environment
        )
        
        # Create indexes if they don't exist
        if "spotify-similarity" not in pinecone.list_indexes():
            pinecone.create_index(
                "spotify-similarity",
                dimension=9,  # Number of audio features
                metric="cosine"
            )
        
        if "netflix-similarity" not in pinecone.list_indexes():
            pinecone.create_index(
                "netflix-similarity", 
                dimension=100,  # TF-IDF features
                metric="cosine"
            )
        
        self.spotify_index = pinecone.Index("spotify-similarity")
        self.netflix_index = pinecone.Index("netflix-similarity")
        """
        pass
    
    def upsert_spotify_embeddings(self, embeddings):
        """
        # Real implementation:
        vectors = [
            (emb['id'], emb['vector'], emb['metadata']) 
            for emb in embeddings
        ]
        self.spotify_index.upsert(vectors=vectors)
        """
        pass
    
    def upsert_netflix_embeddings(self, embeddings):
        """
        # Real implementation:
        vectors = [
            (emb['id'], emb['vector'], emb['metadata']) 
            for emb in embeddings
        ]
        self.netflix_index.upsert(vectors=vectors)
        """
        pass
    
    def similarity_search_spotify(self, query_vector, top_k=5):
        """
        # Real implementation:
        results = self.spotify_index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )
        return results['matches']
        """
        pass


def initialize_vector_database(use_real_pinecone: bool = False):
    """Initialize vector database (mock or real Pinecone)"""
    
    if use_real_pinecone:
        # Check for Pinecone credentials
        api_key = os.getenv('PINECONE_API_KEY')
        environment = os.getenv('PINECONE_ENVIRONMENT')
        
        if not api_key or not environment:
            st.error("Pinecone API key and environment must be set in environment variables")
            st.info("Using mock database for demonstration")
            return MockPineconeDB()
        
        return RealPineconeDB(api_key, environment)
    else:
        return MockPineconeDB()


def setup_vector_database(processed_data, use_real_pinecone: bool = False):
    """Setup and populate vector database with processed data"""
    
    # Initialize database
    db = initialize_vector_database(use_real_pinecone)
    
    # Upload Spotify embeddings
    spotify_embeddings = processed_data['spotify']['embeddings']
    db.upsert_spotify_embeddings(spotify_embeddings)
    
    # Upload Netflix embeddings
    netflix_embeddings = processed_data['netflix']['embeddings']
    db.upsert_netflix_embeddings(netflix_embeddings)
    
    return db


def find_similar_content(db, content_type: str, query_item_id: str, top_k: int = 5):
    """Find similar content based on a query item"""
    
    if content_type == 'spotify':
        # Get the query item's vector
        if hasattr(db, 'spotify_index') and query_item_id in db.spotify_index:
            query_vector = db.spotify_index[query_item_id]['vector']
            return db.similarity_search_spotify(query_vector, top_k)
        
    elif content_type == 'netflix':
        # Get the query item's vector
        if hasattr(db, 'netflix_index') and query_item_id in db.netflix_index:
            query_vector = db.netflix_index[query_item_id]['vector']
            return db.similarity_search_netflix(query_vector, top_k)
    
    return []