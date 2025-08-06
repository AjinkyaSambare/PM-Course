import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import re


class SpotifyDataProcessor:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.scaler = StandardScaler()
        self.audio_features = [
            'danceability', 'energy', 'speechiness', 'acousticness', 
            'instrumentalness', 'liveness', 'valence', 'tempo', 'loudness'
        ]
    
    def preprocess_data(self):
        """Preprocess Spotify data for vector embedding"""
        # Clean and prepare the data
        self.df = self.df.dropna()
        
        # Normalize tempo (convert to 0-1 range)
        tempo_scaler = MinMaxScaler()
        self.df['tempo_normalized'] = tempo_scaler.fit_transform(self.df[['tempo']])
        
        # Normalize loudness (convert to 0-1 range)
        loudness_scaler = MinMaxScaler()
        self.df['loudness_normalized'] = loudness_scaler.fit_transform(self.df[['loudness']])
        
        # Update audio features to use normalized values
        audio_features_normalized = [
            'danceability', 'energy', 'speechiness', 'acousticness', 
            'instrumentalness', 'liveness', 'valence', 'tempo_normalized', 'loudness_normalized'
        ]
        
        return audio_features_normalized
    
    def create_embeddings(self):
        """Create vector embeddings from audio features"""
        audio_features = self.preprocess_data()
        
        # Extract features for embedding
        feature_matrix = self.df[audio_features].values
        
        # Standardize the features
        feature_matrix_scaled = self.scaler.fit_transform(feature_matrix)
        
        # Create embeddings dictionary
        embeddings = []
        for idx, row in self.df.iterrows():
            embedding = {
                'id': f"spotify_{idx}",
                'title': f"{row['track_name']} - {row['artists']}",
                'genre': row['track_genre'],
                'vector': feature_matrix_scaled[idx].tolist(),
                'metadata': {
                    'track_name': row['track_name'],
                    'artists': row['artists'],
                    'album_name': row['album_name'],
                    'genre': row['track_genre'],
                    'popularity': row['popularity'],
                    'danceability': row['danceability'],
                    'energy': row['energy'],
                    'valence': row['valence'],
                    'tempo': row['tempo']
                }
            }
            embeddings.append(embedding)
        
        return embeddings
    
    def get_processed_dataframe(self):
        """Return the processed dataframe"""
        self.preprocess_data()
        return self.df


class NetflixDataProcessor:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=100, 
            stop_words='english',
            lowercase=True
        )
    
    def clean_text(self, text):
        """Clean text data for TF-IDF vectorization"""
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text
    
    def preprocess_data(self):
        """Preprocess Netflix data for vector embedding"""
        # Clean and prepare the data
        self.df = self.df.dropna(subset=['title', 'description'])
        
        # Clean text fields
        self.df['description_clean'] = self.df['description'].apply(self.clean_text)
        self.df['listed_in_clean'] = self.df['listed_in'].apply(self.clean_text)
        self.df['cast_clean'] = self.df['cast'].fillna('').apply(self.clean_text)
        self.df['director_clean'] = self.df['director'].fillna('').apply(self.clean_text)
        
        # Combine text features
        self.df['combined_features'] = (
            self.df['description_clean'] + ' ' + 
            self.df['listed_in_clean'] + ' ' + 
            self.df['cast_clean'] + ' ' + 
            self.df['director_clean']
        )
        
        return self.df
    
    def create_embeddings(self):
        """Create vector embeddings from text features using TF-IDF"""
        self.preprocess_data()
        
        # Create TF-IDF vectors
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['combined_features'])
        
        # Create embeddings dictionary
        embeddings = []
        for idx, row in self.df.iterrows():
            embedding = {
                'id': f"netflix_{idx}",
                'title': row['title'],
                'type': row['type'],
                'vector': tfidf_matrix[idx].toarray()[0].tolist(),
                'metadata': {
                    'title': row['title'],
                    'type': row['type'],
                    'director': row['director'] if not pd.isna(row['director']) else 'Unknown',
                    'cast': row['cast'] if not pd.isna(row['cast']) else 'Unknown',
                    'country': row['country'] if not pd.isna(row['country']) else 'Unknown',
                    'release_year': row['release_year'],
                    'rating': row['rating'],
                    'listed_in': row['listed_in'],
                    'description': row['description']
                }
            }
            embeddings.append(embedding)
        
        return embeddings
    
    def get_processed_dataframe(self):
        """Return the processed dataframe"""
        return self.preprocess_data()


def load_and_process_datasets(spotify_path, netflix_path):
    """Load and process both datasets"""
    # Process Spotify data
    spotify_processor = SpotifyDataProcessor(spotify_path)
    spotify_embeddings = spotify_processor.create_embeddings()
    spotify_df = spotify_processor.get_processed_dataframe()
    
    # Process Netflix data
    netflix_processor = NetflixDataProcessor(netflix_path)
    netflix_embeddings = netflix_processor.create_embeddings()
    netflix_df = netflix_processor.get_processed_dataframe()
    
    return {
        'spotify': {
            'embeddings': spotify_embeddings,
            'dataframe': spotify_df,
            'processor': spotify_processor
        },
        'netflix': {
            'embeddings': netflix_embeddings,
            'dataframe': netflix_df,
            'processor': netflix_processor
        }
    }