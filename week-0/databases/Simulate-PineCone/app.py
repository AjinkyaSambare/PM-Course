import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_processor import load_and_process_datasets
from vector_db import setup_vector_database, find_similar_content
from clustering import perform_clustering_analysis
from visualizations import create_visualization_engine


# Page configuration
st.set_page_config(
    page_title="Vector Database Similarity Demo",
    page_icon="🎵🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Load and process datasets (cached for performance)"""
    try:
        spotify_path = "data/spotify_sample.csv"
        netflix_path = "data/netflix_movies.csv"
        
        processed_data = load_and_process_datasets(spotify_path, netflix_path)
        return processed_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

@st.cache_data
def perform_clustering(_processed_data):
    """Perform clustering analysis (cached for performance)"""
    try:
        clustering_results = perform_clustering_analysis(_processed_data, n_clusters=4)
        return clustering_results
    except Exception as e:
        st.error(f"Error in clustering: {str(e)}")
        return None

@st.cache_resource
def setup_database(_processed_data):
    """Setup vector database (cached for performance)"""
    try:
        db = setup_vector_database(_processed_data, use_real_pinecone=False)
        return db
    except Exception as e:
        st.error(f"Error setting up database: {str(e)}")
        return None

def main():
    """Main application function"""
    
    # Title
    st.title("Vector Database Similarity Demo")
    
    # Load data
    with st.spinner("Loading and processing datasets..."):
        processed_data = load_data()
    
    if processed_data is None:
        st.error("Failed to load data. Please check if the data files exist in the 'data' directory.")
        return
    
    # Perform clustering
    with st.spinner("Performing clustering analysis..."):
        clustering_results = perform_clustering(processed_data)
    
    if clustering_results is None:
        st.error("Failed to perform clustering analysis.")
        return
    
    # Setup vector database
    with st.spinner("Setting up vector database..."):
        db = setup_database(processed_data)
    
    if db is None:
        st.error("Failed to setup vector database.")
        return
    
    # Create visualization engine
    viz_engine = create_visualization_engine()
    
    # Sidebar controls
    st.sidebar.title("🎛️ Controls")
    
    # Dimensionality reduction method
    use_tsne = st.sidebar.selectbox(
        "Visualization Method",
        ["PCA (Faster)", "t-SNE (Better Clustering)"],
        index=0
    ) == "t-SNE (Better Clustering)"
    
    # Method explanation
    st.sidebar.markdown("### 🔬 Method Differences")
    if use_tsne:
        st.sidebar.info("""
        **t-SNE (Recommended)**
        - Groups similar items tighter
        - Better for finding clusters
        - Shows clear patterns
        - Slower processing
        """)
    else:
        st.sidebar.info("""
        **PCA (Linear)**
        - Preserves global structure
        - Faster processing
        - May spread clusters apart
        - Good for overview
        """)
    
    # Variables for disabled features
    show_analysis = False
    show_similarity = True  # Enable similarity search
    
    # Main content area
    col1, col2 = st.columns(2)
    
    # Spotify visualization
    with col1:
        try:
            spotify_fig = viz_engine.create_spotify_cluster_plot(
                clustering_results['spotify']['clustering'], 
                use_tsne=use_tsne
            )
            st.plotly_chart(spotify_fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating Spotify visualization: {str(e)}")
    
    # Netflix visualization
    with col2:
        try:
            netflix_fig = viz_engine.create_netflix_cluster_plot(
                clustering_results['netflix']['clustering'], 
                use_tsne=use_tsne
            )
            st.plotly_chart(netflix_fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error creating Netflix visualization: {str(e)}")
    
    # Remove Cluster Analysis Section
    if False:  # Disabled
        st.markdown("---")
        st.header("📊 Cluster Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                spotify_analysis_fig = viz_engine.create_cluster_analysis_chart(
                    clustering_results['spotify']['analysis'], 
                    'spotify'
                )
                st.plotly_chart(spotify_analysis_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating Spotify analysis: {str(e)}")
        
        with col2:
            try:
                netflix_analysis_fig = viz_engine.create_cluster_analysis_chart(
                    clustering_results['netflix']['analysis'], 
                    'netflix'
                )
                st.plotly_chart(netflix_analysis_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating Netflix analysis: {str(e)}")
        
        # Detailed cluster information
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                viz_engine.display_cluster_details(
                    clustering_results['spotify']['analysis'], 
                    'spotify'
                )
            except Exception as e:
                st.error(f"Error displaying Spotify cluster details: {str(e)}")
        
        with col2:
            try:
                viz_engine.display_cluster_details(
                    clustering_results['netflix']['analysis'], 
                    'netflix'
                )
            except Exception as e:
                st.error(f"Error displaying Netflix cluster details: {str(e)}")
    
    # Similarity Search Section
    if show_similarity:
        st.markdown("---")
        st.header(" Find Similar Content")
        st.markdown("**Select a song or movie to discover similar recommendations!**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Find Similar Songs")
            
            # Text search box for songs
            search_query = st.text_input(
                "Search for a song:",
                placeholder="Type song name or artist...",
                key="spotify_search"
            )
            
            if search_query:
                # Search through available tracks
                matching_tracks = []
                for emb in clustering_results['spotify']['clustering']['embeddings']:
                    track_name = emb['metadata']['track_name'].lower()
                    artist = emb['metadata']['artists'].lower()
                    query_lower = search_query.lower()
                    
                    # Match by song name or artist
                    if query_lower in track_name or query_lower in artist:
                        matching_tracks.append({
                            'display': f"{emb['metadata']['track_name']} - {emb['metadata']['artists']}",
                            'embedding': emb
                        })
                
                if matching_tracks:
                    # Show matching results
                    selected_track = st.selectbox(
                        "Select from matches:",
                        options=[track['display'] for track in matching_tracks],
                        key="spotify_match_select"
                    )
                    
                    if selected_track:
                        # Find the selected embedding
                        selected_item = next(
                            track['embedding'] for track in matching_tracks 
                            if track['display'] == selected_track
                        )
                        
                        # Find similar items
                        try:
                            similar_items = find_similar_content(db, 'spotify', selected_item['id'], top_k=6)
                            
                            if similar_items and len(similar_items) > 1:
                                # Show vector similarity map first
                                st.markdown("")
                                similarity_map = viz_engine.create_similarity_map(
                                    clustering_results['spotify']['clustering'],
                                    selected_item,
                                    similar_items,
                                    'spotify',
                                    use_tsne=use_tsne
                                )
                                st.plotly_chart(similarity_map, use_container_width=True)
                                
                                # Then display similar tracks list
                                st.markdown("### 🎶 **Songs Like This:**")
                                for i, item in enumerate(similar_items[1:], 1):  # Skip the first item (query itself)
                                    if i > 4:  # Show only top 4 similar songs
                                        break
                                    similarity = item.get('similarity', 0)
                                    track_name = item['metadata']['track_name']
                                    artist = item['metadata']['artists']
                                    genre = item['metadata']['genre']
                                    
                                    # Create a nice card-like display
                                    st.markdown(f"""
                                    **{i}. {track_name}**  
                                    *by {artist}* • {genre}  
                                    Similarity: {similarity:.1%}
                                    """)
                                    st.markdown("---")
                                
                            else:
                                st.info("No similar tracks found.")
                                
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning(f"No songs found matching '{search_query}'. Try searching for artist or song name.")
        
        with col2:
            st.subheader("🎬 Find Similar Movies")
            
            # Text search box for movies
            movie_search_query = st.text_input(
                "Search for a movie:",
                placeholder="Type movie title or director...",
                key="netflix_search"
            )
            
            if movie_search_query:
                # Search through available movies
                matching_movies = []
                for emb in clustering_results['netflix']['clustering']['embeddings']:
                    if emb['metadata'].get('type', 'Movie') == 'Movie':
                        title = emb['metadata']['title'].lower()
                        director = emb['metadata']['director'].lower()
                        query_lower = movie_search_query.lower()
                        
                        # Match by title or director
                        if query_lower in title or query_lower in director:
                            matching_movies.append({
                                'display': f"{emb['metadata']['title']} ({emb['metadata']['release_year']})",
                                'embedding': emb
                            })
                
                if matching_movies:
                    # Show matching results
                    selected_movie = st.selectbox(
                        "Select from matches:",
                        options=[movie['display'] for movie in matching_movies],
                        key="netflix_match_select"
                    )
                    
                    if selected_movie:
                        # Find the selected embedding
                        selected_item = next(
                            movie['embedding'] for movie in matching_movies 
                            if movie['display'] == selected_movie
                        )
                        
                        # Find similar items
                        try:
                            similar_items = find_similar_content(db, 'netflix', selected_item['id'], top_k=6)
                            
                            if similar_items and len(similar_items) > 1:
                                # Show vector similarity map first
                                st.markdown("")
                                similarity_map = viz_engine.create_similarity_map(
                                    clustering_results['netflix']['clustering'],
                                    selected_item,
                                    similar_items,
                                    'netflix',
                                    use_tsne=use_tsne
                                )
                                st.plotly_chart(similarity_map, use_container_width=True)
                                
                                # Then display similar movies list
                                st.markdown("### 🎬 **Movies Like This:**")
                                for i, item in enumerate(similar_items[1:], 1):  # Skip the first item (query itself)
                                    if i > 4:  # Show only top 4 similar movies
                                        break
                                    similarity = item.get('similarity', 0)
                                    title = item['metadata']['title']
                                    director = item['metadata']['director']
                                    genres = item['metadata']['listed_in'].split(',')[0].strip() if item['metadata']['listed_in'] else 'N/A'
                                    year = item['metadata']['release_year']
                                    
                                    # Create a nice card-like display
                                    st.markdown(f"""
                                    **{i}. {title}** ({year})  
                                    *Directed by {director}* • {genres}  
                                    Similarity: {similarity:.1%}
                                    """)
                                    st.markdown("---")
                                
                            else:
                                st.info("No similar movies found.")
                                
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning(f"No movies found matching '{movie_search_query}'. Try searching for movie title or director name.")
    
    # How Clustering Works Section - Dropdown
    st.markdown("---")
    with st.expander("🔬 How This Clustering Works"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎵 Spotify Songs")
            st.markdown("""
            **Uses audio features:**
            - Energy, Danceability, Mood
            - Acousticness, Tempo, Loudness
            
            **Result:** Similar-sounding songs appear close together. Pop songs cluster near other pop songs, acoustic songs group separately.
            """)
        
        with col2:
            st.markdown("###  Netflix Movies")
            st.markdown("""
            **Uses movie features:**
            - Genre, Director, Description
            - Rating, Year, Country
            
            **Result:** Movies with similar themes cluster together. Crime thrillers group near each other, dramas form their own clusters.
            """)
        
        st.info("💡 **Key Point**: Closer points = more similar content. This is how Netflix and Spotify recommend what you'll like!")

if __name__ == "__main__":
    main()