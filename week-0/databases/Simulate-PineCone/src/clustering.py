import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Any


class ContentClusterer:
    """Clustering algorithms for content similarity analysis"""
    
    def __init__(self, n_clusters: int = 6, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.spotify_kmeans = None
        self.netflix_kmeans = None
        self.spotify_pca = None
        self.netflix_pca = None
        self.spotify_tsne = None
        self.netflix_tsne = None
    
    def cluster_spotify_data(self, embeddings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform clustering on Spotify data"""
        # Extract vectors
        vectors = np.array([emb['vector'] for emb in embeddings])
        
        # Perform K-means clustering
        self.spotify_kmeans = KMeans(
            n_clusters=self.n_clusters, 
            random_state=self.random_state,
            n_init=10
        )
        cluster_labels = self.spotify_kmeans.fit_predict(vectors)
        
        # Calculate silhouette score
        silhouette_avg = silhouette_score(vectors, cluster_labels)
        
        # Reduce dimensionality for visualization (PCA)
        self.spotify_pca = PCA(n_components=2, random_state=self.random_state)
        vectors_2d_pca = self.spotify_pca.fit_transform(vectors)
        
        # Reduce dimensionality for visualization (t-SNE) - better clustering
        self.spotify_tsne = TSNE(
            n_components=2, 
            random_state=self.random_state,
            perplexity=min(5, len(embeddings) - 1),  # Lower perplexity for tighter clusters
            learning_rate=200,
            max_iter=1000
        )
        vectors_2d_tsne = self.spotify_tsne.fit_transform(vectors)
        
        # Create results
        results = {
            'embeddings': embeddings,
            'vectors': vectors,
            'cluster_labels': cluster_labels,
            'vectors_2d_pca': vectors_2d_pca,
            'vectors_2d_tsne': vectors_2d_tsne,
            'silhouette_score': silhouette_avg,
            'cluster_centers': self.spotify_kmeans.cluster_centers_
        }
        
        return results
    
    def cluster_netflix_data(self, embeddings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform clustering on Netflix data"""
        # Extract vectors
        vectors = np.array([emb['vector'] for emb in embeddings])
        
        # Perform K-means clustering
        self.netflix_kmeans = KMeans(
            n_clusters=self.n_clusters, 
            random_state=self.random_state,
            n_init=10
        )
        cluster_labels = self.netflix_kmeans.fit_predict(vectors)
        
        # Calculate silhouette score
        silhouette_avg = silhouette_score(vectors, cluster_labels)
        
        # Reduce dimensionality for visualization (PCA)
        self.netflix_pca = PCA(n_components=2, random_state=self.random_state)
        vectors_2d_pca = self.netflix_pca.fit_transform(vectors)
        
        # Reduce dimensionality for visualization (t-SNE) - better clustering
        self.netflix_tsne = TSNE(
            n_components=2, 
            random_state=self.random_state,
            perplexity=min(5, len(embeddings) - 1),  # Lower perplexity for tighter clusters
            learning_rate=200,
            max_iter=1000
        )
        vectors_2d_tsne = self.netflix_tsne.fit_transform(vectors)
        
        # Create results
        results = {
            'embeddings': embeddings,
            'vectors': vectors,
            'cluster_labels': cluster_labels,
            'vectors_2d_pca': vectors_2d_pca,
            'vectors_2d_tsne': vectors_2d_tsne,
            'silhouette_score': silhouette_avg,
            'cluster_centers': self.netflix_kmeans.cluster_centers_
        }
        
        return results
    
    def analyze_spotify_clusters(self, clustering_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze characteristics of Spotify clusters"""
        embeddings = clustering_results['embeddings']
        cluster_labels = clustering_results['cluster_labels']
        
        cluster_analysis = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_items = [
                emb for i, emb in enumerate(embeddings) 
                if cluster_labels[i] == cluster_id
            ]
            
            if cluster_items:
                # Extract metadata for analysis
                genres = [item['metadata']['genre'] for item in cluster_items]
                popularities = [item['metadata']['popularity'] for item in cluster_items]
                danceabilities = [item['metadata']['danceability'] for item in cluster_items]
                energies = [item['metadata']['energy'] for item in cluster_items]
                valences = [item['metadata']['valence'] for item in cluster_items]
                tempos = [item['metadata']['tempo'] for item in cluster_items]
                
                # Most common genre
                most_common_genre = max(set(genres), key=genres.count)
                
                cluster_analysis[cluster_id] = {
                    'size': len(cluster_items),
                    'most_common_genre': most_common_genre,
                    'avg_popularity': np.mean(popularities),
                    'avg_danceability': np.mean(danceabilities),
                    'avg_energy': np.mean(energies),
                    'avg_valence': np.mean(valences),
                    'avg_tempo': np.mean(tempos),
                    'sample_tracks': [
                        f"{item['metadata']['track_name']} - {item['metadata']['artists']}"
                        for item in cluster_items[:3]  # Show first 3 tracks
                    ]
                }
        
        return cluster_analysis
    
    def analyze_netflix_clusters(self, clustering_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze characteristics of Netflix clusters"""
        embeddings = clustering_results['embeddings']
        cluster_labels = clustering_results['cluster_labels']
        
        cluster_analysis = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_items = [
                emb for i, emb in enumerate(embeddings) 
                if cluster_labels[i] == cluster_id
            ]
            
            if cluster_items:
                # Extract metadata for analysis
                types = [item['metadata']['type'] for item in cluster_items]
                genres = []
                for item in cluster_items:
                    if item['metadata']['listed_in']:
                        genres.extend([g.strip() for g in item['metadata']['listed_in'].split(',')])
                
                countries = [item['metadata']['country'] for item in cluster_items if item['metadata']['country'] != 'Unknown']
                years = [item['metadata']['release_year'] for item in cluster_items]
                
                # Most common type (Movie or TV Show)
                most_common_type = max(set(types), key=types.count) if types else 'Unknown'
                
                # Most common genre
                most_common_genre = max(set(genres), key=genres.count) if genres else 'Unknown'
                
                # Most common country
                most_common_country = max(set(countries), key=countries.count) if countries else 'Unknown'
                
                cluster_analysis[cluster_id] = {
                    'size': len(cluster_items),
                    'most_common_type': most_common_type,
                    'most_common_genre': most_common_genre,
                    'most_common_country': most_common_country,
                    'avg_release_year': np.mean(years) if years else 0,
                    'sample_titles': [
                        item['metadata']['title']
                        for item in cluster_items[:3]  # Show first 3 titles
                    ]
                }
        
        return cluster_analysis
    
    def get_cluster_colors(self) -> List[str]:
        """Get colors for cluster visualization"""
        return [
            '#FF6B6B',  # Red
            '#4ECDC4',  # Teal
            '#45B7D1',  # Blue
            '#96CEB4',  # Green
            '#FECA57',  # Yellow
            '#FF9FF3',  # Pink
            '#54A0FF',  # Light Blue
            '#5F27CD'   # Purple
        ][:self.n_clusters]
    
    def predict_cluster_for_item(self, content_type: str, item_vector: np.ndarray) -> int:
        """Predict cluster for a new item"""
        if content_type == 'spotify' and self.spotify_kmeans is not None:
            return self.spotify_kmeans.predict(item_vector.reshape(1, -1))[0]
        elif content_type == 'netflix' and self.netflix_kmeans is not None:
            return self.netflix_kmeans.predict(item_vector.reshape(1, -1))[0]
        else:
            return 0


def perform_clustering_analysis(processed_data: Dict[str, Any], n_clusters: int = 6) -> Dict[str, Any]:
    """Perform complete clustering analysis on both datasets"""
    
    clusterer = ContentClusterer(n_clusters=n_clusters)
    
    # Cluster Spotify data
    spotify_clustering = clusterer.cluster_spotify_data(processed_data['spotify']['embeddings'])
    spotify_analysis = clusterer.analyze_spotify_clusters(spotify_clustering)
    
    # Cluster Netflix data  
    netflix_clustering = clusterer.cluster_netflix_data(processed_data['netflix']['embeddings'])
    netflix_analysis = clusterer.analyze_netflix_clusters(netflix_clustering)
    
    results = {
        'clusterer': clusterer,
        'spotify': {
            'clustering': spotify_clustering,
            'analysis': spotify_analysis
        },
        'netflix': {
            'clustering': netflix_clustering,
            'analysis': netflix_analysis
        }
    }
    
    return results


def find_optimal_clusters(vectors: np.ndarray, max_k: int = 10) -> int:
    """Find optimal number of clusters using elbow method"""
    inertias = []
    silhouette_scores = []
    
    k_range = range(2, min(max_k + 1, len(vectors)))
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(vectors)
        
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(vectors, cluster_labels))
    
    # Find elbow point (simplified approach)
    # Choose k where silhouette score is maximized
    optimal_k = k_range[np.argmax(silhouette_scores)]
    
    return optimal_k