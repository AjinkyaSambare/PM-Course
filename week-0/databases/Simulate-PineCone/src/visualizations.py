import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import seaborn as sns


class VisualizationEngine:
    """Handle all visualizations for the vector database similarity demo"""
    
    def __init__(self):
        self.spotify_colors = [
            '#1DB954',  # Spotify Green
            '#FF6B6B',  # Red
            '#4ECDC4',  # Teal
            '#45B7D1',  # Blue
            '#FECA57',  # Yellow
            '#FF9FF3',  # Pink
        ]
        
        self.netflix_colors = [
            '#E50914',  # Netflix Red
            '#221F1F',  # Netflix Black
            '#FF6B6B',  # Red
            '#4ECDC4',  # Teal
            '#45B7D1',  # Blue
            '#FECA57',  # Yellow
        ]
    
    def create_spotify_cluster_plot(self, clustering_results: Dict[str, Any], use_tsne: bool = True) -> go.Figure:
        """Create simple, clean Spotify song visualization"""
        
        embeddings = clustering_results['embeddings']
        cluster_labels = clustering_results['cluster_labels']
        vectors_2d = clustering_results['vectors_2d_tsne'] if use_tsne else clustering_results['vectors_2d_pca']
        
        # Simple color palette
        colors = ['#1DB954', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FECA57', '#FF9FF3']
        
        # Prepare data for plotting
        plot_data = []
        for i, (emb, label) in enumerate(zip(embeddings, cluster_labels)):
            track_name = emb['metadata']['track_name']
            artist = emb['metadata']['artists']
            genre = emb['metadata']['genre']
            
            plot_data.append({
                'x': vectors_2d[i, 0],
                'y': vectors_2d[i, 1],
                'cluster': f'Group {label + 1}',  # Simple group names
                'track_name': track_name,
                'artists': artist,
                'genre': genre,
                'popularity': emb['metadata']['popularity'],
                'danceability': emb['metadata']['danceability'],
                'energy': emb['metadata']['energy'],
                'valence': emb['metadata']['valence']
            })
        
        df = pd.DataFrame(plot_data)
        
        # Create simple scatter plot - color by genre for clarity
        fig = px.scatter(
            df, 
            x='x', 
            y='y',
            color='genre',
            title='🎵 Spotify Songs - Similar Songs Cluster Together',
            color_discrete_sequence=colors,
            width=600,
            height=500
        )
        
        # Clean, simple styling with song names visible
        fig.update_traces(
            marker=dict(size=18, opacity=0.9, line=dict(width=2, color='white')),
            textposition="middle center",
            textfont=dict(size=9, color="black", family="Arial"),
            text=df['track_name'].str[:12] + df['track_name'].str.len().map(lambda x: '...' if x > 12 else ''),
            hovertemplate="<b>%{customdata[0]}</b><br>" +
                         "by %{customdata[1]}<br>" +
                         "Genre: %{customdata[2]}<br>" +
                         "Popularity: %{customdata[3]}<br>" +
                         "<extra></extra>",
            customdata=df[['track_name', 'artists', 'genre', 'popularity']]
        )
        
        # Clean layout
        fig.update_layout(
            xaxis_title="← Different Musical Styles →",
            yaxis_title="← Different Moods & Energy →",
            showlegend=True,
            legend=dict(
                title="Genre",
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            plot_bgcolor='white',
            font=dict(size=12),
            title_font_size=16
        )
        
        # Clean axes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', zeroline=False)
        
        return fig
    
    def create_netflix_cluster_plot(self, clustering_results: Dict[str, Any], use_tsne: bool = True) -> go.Figure:
        """Create simple, clean Netflix movies visualization - same style as Spotify"""
        
        embeddings = clustering_results['embeddings']
        cluster_labels = clustering_results['cluster_labels']
        vectors_2d = clustering_results['vectors_2d_tsne'] if use_tsne else clustering_results['vectors_2d_pca']
        
        # Simple color palette - same as Spotify
        colors = ['#E50914', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FECA57', '#FF9FF3']
        
        # First pass - collect genres for each cluster to determine dominant type
        cluster_genres = {}
        for i, (emb, label) in enumerate(zip(embeddings, cluster_labels)):
            if emb['metadata'].get('type', 'Movie') != 'Movie':
                continue
            if label not in cluster_genres:
                cluster_genres[label] = []
            genres = emb['metadata'].get('listed_in', '')
            if genres:
                cluster_genres[label].extend([g.strip() for g in genres.split(',')])
        
        # Determine dominant genre for each cluster
        cluster_names = {}
        for label, genres_list in cluster_genres.items():
            if genres_list:
                # Find most common genre
                from collections import Counter
                genre_counts = Counter(genres_list)
                most_common = genre_counts.most_common(1)[0][0]
                
                # Simplify genre names
                if 'Crime' in most_common or 'Thrillers' in most_common:
                    cluster_names[label] = 'Crime & Thrillers'
                elif 'Action' in most_common:
                    cluster_names[label] = 'Action Movies'
                elif 'Drama' in most_common:
                    cluster_names[label] = 'Drama Movies'
                elif 'Biographical' in most_common or 'Historical' in most_common:
                    cluster_names[label] = 'Biographical & Historical'
                elif 'Sci-Fi' in most_common:
                    cluster_names[label] = 'Sci-Fi Movies'
                elif 'Comedies' in most_common:
                    cluster_names[label] = 'Comedy Movies'
                else:
                    cluster_names[label] = most_common
            else:
                cluster_names[label] = f'Group {label + 1}'
        
        # Prepare data for plotting
        plot_data = []
        for i, (emb, label) in enumerate(zip(embeddings, cluster_labels)):
            # Only process movies
            if emb['metadata'].get('type', 'Movie') != 'Movie':
                continue
                
            title = emb['metadata']['title']
            director = emb['metadata']['director'] if emb['metadata']['director'] != 'Unknown' else 'N/A'
            year = emb['metadata']['release_year']
            rating = emb['metadata']['rating']
            genres = emb['metadata']['listed_in']
            
            plot_data.append({
                'x': vectors_2d[i, 0],
                'y': vectors_2d[i, 1],
                'cluster': cluster_names.get(label, f'Group {label + 1}'),  # Use meaningful names
                'title': title,
                'director': director,
                'year': year,
                'rating': rating,
                'genres': genres
            })
        
        df = pd.DataFrame(plot_data)
        
        # Create simple scatter plot - exactly like Spotify
        fig = px.scatter(
            df, 
            x='x', 
            y='y',
            color='cluster',
            title='🎬 Netflix Movies - Similar Movies Are Close Together',
            color_discrete_sequence=colors,
            width=600,
            height=500
        )
        
        # Clean, simple styling - exactly like Spotify
        fig.update_traces(
            marker=dict(size=18, opacity=0.9, line=dict(width=2, color='white')),
            textposition="middle center",
            textfont=dict(size=9, color="black", family="Arial"),
            text=df['title'].str[:12] + df['title'].str.len().map(lambda x: '...' if x > 12 else ''),
            hovertemplate="<b>%{customdata[0]}</b><br>" +
                         "Director: %{customdata[1]}<br>" +
                         "Year: %{customdata[2]}<br>" +
                         "Rating: %{customdata[3]}<br>" +
                         "Genres: %{customdata[4]}<br>" +
                         "<extra></extra>",
            customdata=df[['title', 'director', 'year', 'rating', 'genres']]
        )
        
        # Clean layout - exactly like Spotify
        fig.update_layout(
            xaxis_title="← Different Themes & Stories →",
            yaxis_title="← Different Styles & Ratings →",
            showlegend=True,
            legend=dict(
                title="Movie Groups",
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            plot_bgcolor='white',
            font=dict(size=12),
            title_font_size=16
        )
        
        # Clean axes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', zeroline=False)
        
        return fig
    
    def create_similarity_visualization(self, query_item: Dict[str, Any], similar_items: List[Dict[str, Any]], content_type: str) -> go.Figure:
        """Create visualization showing similar items"""
        
        if content_type == 'spotify':
            return self._create_spotify_similarity_plot(query_item, similar_items)
        else:
            return self._create_netflix_similarity_plot(query_item, similar_items)
    
    def _create_spotify_similarity_plot(self, query_item: Dict[str, Any], similar_items: List[Dict[str, Any]]) -> go.Figure:
        """Create Spotify similarity plot"""
        
        # Prepare data
        items = [query_item] + similar_items
        similarities = [1.0] + [item.get('similarity', 0.0) for item in similar_items]
        
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=[f"{item['metadata']['track_name'][:20]}..." if len(item['metadata']['track_name']) > 20 
               else item['metadata']['track_name'] for item in items],
            y=similarities,
            text=[f"{sim:.3f}" for sim in similarities],
            textposition='outside',
            marker_color=['#1DB954' if i == 0 else '#FF6B6B' for i in range(len(items))],
            hovertemplate="<b>%{x}</b><br>Similarity: %{y:.3f}<extra></extra>"
        ))
        
        fig.update_layout(
            title="Similar Spotify Tracks",
            xaxis_title="Tracks",
            yaxis_title="Similarity Score",
            yaxis=dict(range=[0, 1.1]),
            height=400
        )
        
        return fig
    
    def _create_netflix_similarity_plot(self, query_item: Dict[str, Any], similar_items: List[Dict[str, Any]]) -> go.Figure:
        """Create Netflix similarity plot"""
        
        # Prepare data
        items = [query_item] + similar_items
        similarities = [1.0] + [item.get('similarity', 0.0) for item in similar_items]
        
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=[f"{item['metadata']['title'][:20]}..." if len(item['metadata']['title']) > 20 
               else item['metadata']['title'] for item in items],
            y=similarities,
            text=[f"{sim:.3f}" for sim in similarities],
            textposition='outside',
            marker_color=['#E50914' if i == 0 else '#221F1F' for i in range(len(items))],
            hovertemplate="<b>%{x}</b><br>Similarity: %{y:.3f}<extra></extra>"
        ))
        
        fig.update_layout(
            title="Similar Netflix Content",
            xaxis_title="Content",
            yaxis_title="Similarity Score",
            yaxis=dict(range=[0, 1.1]),
            height=400
        )
        
        return fig
    
    def create_cluster_analysis_chart(self, cluster_analysis: Dict[str, Any], content_type: str) -> go.Figure:
        """Create cluster analysis visualization"""
        
        if content_type == 'spotify':
            return self._create_spotify_cluster_analysis(cluster_analysis)
        else:
            return self._create_netflix_cluster_analysis(cluster_analysis)
    
    def _create_spotify_cluster_analysis(self, cluster_analysis: Dict[str, Any]) -> go.Figure:
        """Create Spotify cluster analysis chart"""
        
        clusters = list(cluster_analysis.keys())
        sizes = [cluster_analysis[c]['size'] for c in clusters]
        avg_popularity = [cluster_analysis[c]['avg_popularity'] for c in clusters]
        avg_energy = [cluster_analysis[c]['avg_energy'] for c in clusters]
        avg_valence = [cluster_analysis[c]['avg_valence'] for c in clusters]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Cluster Sizes', 'Average Popularity', 'Average Energy', 'Average Valence'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Cluster sizes
        fig.add_trace(
            go.Bar(x=[f'Cluster {c}' for c in clusters], y=sizes, name='Size', marker_color=self.spotify_colors[0]),
            row=1, col=1
        )
        
        # Average popularity
        fig.add_trace(
            go.Bar(x=[f'Cluster {c}' for c in clusters], y=avg_popularity, name='Popularity', marker_color=self.spotify_colors[1]),
            row=1, col=2
        )
        
        # Average energy
        fig.add_trace(
            go.Bar(x=[f'Cluster {c}' for c in clusters], y=avg_energy, name='Energy', marker_color=self.spotify_colors[2]),
            row=2, col=1
        )
        
        # Average valence
        fig.add_trace(
            go.Bar(x=[f'Cluster {c}' for c in clusters], y=avg_valence, name='Valence', marker_color=self.spotify_colors[3]),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            title_text="Spotify Cluster Analysis",
            showlegend=False
        )
        
        return fig
    
    def _create_netflix_cluster_analysis(self, cluster_analysis: Dict[str, Any]) -> go.Figure:
        """Create Netflix cluster analysis chart"""
        
        clusters = list(cluster_analysis.keys())
        sizes = [cluster_analysis[c]['size'] for c in clusters]
        avg_years = [cluster_analysis[c]['avg_release_year'] for c in clusters]
        
        # Count types and genres
        type_counts = {}
        genre_counts = {}
        
        for c in clusters:
            cluster_info = cluster_analysis[c]
            type_counts[f'Cluster {c}'] = cluster_info['most_common_type']
            genre_counts[f'Cluster {c}'] = cluster_info['most_common_genre']
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Cluster Sizes', 'Average Release Year'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Cluster sizes
        fig.add_trace(
            go.Bar(x=[f'Cluster {c}' for c in clusters], y=sizes, name='Size', marker_color=self.netflix_colors[0]),
            row=1, col=1
        )
        
        # Average release year
        fig.add_trace(
            go.Bar(x=[f'Cluster {c}' for c in clusters], y=avg_years, name='Avg Year', marker_color=self.netflix_colors[1]),
            row=1, col=2
        )
        
        fig.update_layout(
            height=400,
            title_text="Netflix Cluster Analysis",
            showlegend=False
        )
        
        return fig
    
    def display_cluster_details(self, cluster_analysis: Dict[str, Any], content_type: str):
        """Display detailed cluster information in Streamlit"""
        
        st.subheader(f"{content_type.title()} Cluster Details")
        
        for cluster_id, details in cluster_analysis.items():
            with st.expander(f"Cluster {cluster_id} ({details['size']} items)"):
                if content_type == 'spotify':
                    st.write(f"**Most Common Genre:** {details['most_common_genre']}")
                    st.write(f"**Average Popularity:** {details['avg_popularity']:.2f}")
                    st.write(f"**Average Danceability:** {details['avg_danceability']:.2f}")
                    st.write(f"**Average Energy:** {details['avg_energy']:.2f}")
                    st.write(f"**Average Valence:** {details['avg_valence']:.2f}")
                    st.write(f"**Average Tempo:** {details['avg_tempo']:.1f} BPM")
                    st.write("**Sample Tracks:**")
                    for track in details['sample_tracks']:
                        st.write(f"• {track}")
                
                else:  # Netflix
                    st.write(f"**Most Common Type:** {details['most_common_type']}")
                    st.write(f"**Most Common Genre:** {details['most_common_genre']}")
                    st.write(f"**Most Common Country:** {details['most_common_country']}")
                    st.write(f"**Average Release Year:** {details['avg_release_year']:.0f}")
                    st.write("**Sample Titles:**")
                    for title in details['sample_titles']:
                        st.write(f"• {title}")


    def create_similarity_map(self, clustering_results: Dict[str, Any], selected_item: Dict[str, Any], 
                             similar_items: List[Dict[str, Any]], content_type: str, use_tsne: bool = True) -> go.Figure:
        """Create vector map showing selected item and similar items highlighted"""
        
        embeddings = clustering_results['embeddings']
        vectors_2d = clustering_results['vectors_2d_tsne'] if use_tsne else clustering_results['vectors_2d_pca']
        
        # Get IDs of similar items for highlighting
        selected_id = selected_item['id']
        similar_ids = [item['id'] for item in similar_items[1:5]]  # Top 4 similar items
        
        # Prepare data for plotting
        plot_data = []
        for i, emb in enumerate(embeddings):
            item_id = emb['id']
            
            # Determine item type for styling
            if item_id == selected_id:
                item_type = 'Selected'
                size = 25
                opacity = 1.0
            elif item_id in similar_ids:
                item_type = 'Similar'
                size = 20
                opacity = 0.9
            else:
                item_type = 'Other'
                size = 10
                opacity = 0.3
            
            if content_type == 'spotify':
                plot_data.append({
                    'x': vectors_2d[i, 0],
                    'y': vectors_2d[i, 1],
                    'type': item_type,
                    'name': emb['metadata']['track_name'],
                    'artist': emb['metadata']['artists'],
                    'genre': emb['metadata']['genre'],
                    'size': size,
                    'opacity': opacity
                })
            else:  # Netflix
                if emb['metadata'].get('type', 'Movie') == 'Movie':
                    plot_data.append({
                        'x': vectors_2d[i, 0],
                        'y': vectors_2d[i, 1],
                        'type': item_type,
                        'name': emb['metadata']['title'],
                        'director': emb['metadata']['director'],
                        'year': emb['metadata']['release_year'],
                        'size': size,
                        'opacity': opacity
                    })
        
        df = pd.DataFrame(plot_data)
        
        # Create scatter plot
        colors = {'Selected': '#FF0000', 'Similar': '#00FF00', 'Other': '#CCCCCC'}
        
        fig = px.scatter(
            df, 
            x='x', 
            y='y',
            color='type',
            size='size',
            color_discrete_map=colors,
            title=f'🎯 Vector Similarity Map - {content_type.title()}',
            width=600,
            height=500
        )
        
        # Update marker opacity manually for each trace based on their names
        for trace in fig.data:
            if trace.name == 'Selected':
                trace.marker.opacity = 1.0
            elif trace.name == 'Similar':
                trace.marker.opacity = 0.9
            elif trace.name == 'Other':
                trace.marker.opacity = 0.3
        
        # Update traces for better visualization
        if content_type == 'spotify':
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>" +
                             "by %{customdata[1]}<br>" +
                             "Genre: %{customdata[2]}<br>" +
                             "<extra></extra>",
                customdata=df[['name', 'artist', 'genre']]
            )
        else:
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>" +
                             "Director: %{customdata[1]}<br>" +
                             "Year: %{customdata[2]}<br>" +
                             "<extra></extra>",
                customdata=df[['name', 'director', 'year']]
            )
        
        # Update layout
        fig.update_layout(
            xaxis_title="← Vector Dimension 1 →",
            yaxis_title="← Vector Dimension 2 →",
            showlegend=True,
            legend=dict(
                title="Item Type",
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            plot_bgcolor='white',
            font=dict(size=12),
            title_font_size=16
        )
        
        # Clean axes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', zeroline=False)
        
        return fig


def create_visualization_engine() -> VisualizationEngine:
    """Factory function to create visualization engine"""
    return VisualizationEngine()