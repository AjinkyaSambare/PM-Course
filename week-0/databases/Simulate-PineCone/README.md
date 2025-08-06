# 🎵🎬 Vector Database Similarity Demo

A comprehensive demonstration of how Spotify and Netflix use vector databases for content recommendations, featuring interactive clustering visualizations and similarity search.

## 🚀 Features

- **Dual Platform Visualization**: Side-by-side clustering of Spotify music and Netflix content
- **Interactive Scatter Plots**: Explore clusters with hover details and clickable points
- **Similarity Search**: Find similar songs and movies using vector similarity
- **Cluster Analysis**: Understand what makes each cluster unique
- **Educational Content**: Learn how vector databases work in practice
- **Mock Vector Database**: Simulates Pinecone functionality without requiring API keys

## 📁 Project Structure

```
Simulate-PineCone/
├── app.py                 # Main Streamlit application
├── data/
│   ├── spotify_sample.csv # Sample Spotify tracks with audio features
│   └── netflix_sample.csv # Sample Netflix content with metadata
├── src/
│   ├── data_processor.py  # Data preprocessing and embedding creation
│   ├── vector_db.py       # Vector database operations (mock + real)
│   ├── clustering.py      # K-means clustering and analysis
│   └── visualizations.py  # Plotly visualizations and charts
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### 1. Clone or Navigate to Directory

```bash
cd /path/to/Simulate-PineCone
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📊 How It Works

### Spotify Similarity

The app analyzes Spotify tracks using audio features:
- **Danceability**: How suitable for dancing (0.0 to 1.0)
- **Energy**: Perceptual measure of intensity (0.0 to 1.0)
- **Valence**: Musical positivity (0.0 to 1.0)
- **Acousticness**: Whether the track is acoustic (0.0 to 1.0)
- **Instrumentalness**: Predicts vocal content (0.0 to 1.0)
- **Speechiness**: Presence of spoken words (0.0 to 1.0)
- **Tempo**: Beats per minute (BPM)
- **Loudness**: Overall loudness in decibels

These features are normalized and used to create vector embeddings that represent each song in high-dimensional space.

### Netflix Similarity

The app analyzes Netflix content using metadata:
- **Description**: Plot summary and content description
- **Genres**: Listed categories (Drama, Comedy, etc.)
- **Cast & Director**: People involved in production
- **Country**: Production country
- **Type**: Movie vs TV Show

Text features are processed using TF-IDF (Term Frequency-Inverse Document Frequency) to create vector embeddings.

### Clustering Algorithm

1. **K-means Clustering**: Groups similar content into 6 clusters
2. **Dimensionality Reduction**: Uses PCA or t-SNE to visualize high-dimensional data in 2D
3. **Similarity Search**: Finds similar items using cosine similarity between vectors

## 🎯 Using the App

### Main Interface

1. **Cluster Visualizations**: Two side-by-side scatter plots showing Spotify and Netflix clusters
2. **Controls Sidebar**: 
   - Switch between t-SNE and PCA visualization
   - Toggle cluster analysis and similarity search sections
3. **Metrics**: Silhouette scores showing cluster quality

### Similarity Search

1. Select a song or movie from the dropdown menus
2. View similar recommendations with similarity scores
3. Explore the bar charts showing similarity rankings

### Cluster Analysis

- View cluster characteristics and statistics
- Expand cluster details to see sample content
- Understand what makes each cluster unique

## 🔧 Configuration

### Using Real Pinecone (Optional)

To use a real Pinecone vector database instead of the mock implementation:

1. Sign up for Pinecone at [pinecone.io](https://pinecone.io)
2. Get your API key and environment
3. Set environment variables:
   ```bash
   export PINECONE_API_KEY="your-api-key"
   export PINECONE_ENVIRONMENT="your-environment"
   ```
4. Modify `app.py` to set `use_real_pinecone=True` in the `setup_database()` call

### Adding More Data

Replace the sample CSV files in the `data/` directory with larger datasets:

- **Spotify**: Should include columns for audio features (danceability, energy, etc.)
- **Netflix**: Should include title, description, genre, cast, director, etc.

## 📚 Educational Value

This demo teaches:

- **Vector Embeddings**: How to represent content as numerical vectors
- **Similarity Search**: Finding similar items using cosine similarity
- **Clustering**: Grouping similar items using machine learning
- **Dimensionality Reduction**: Visualizing high-dimensional data
- **Real-world Applications**: How major platforms implement recommendations

## 🛠 Technical Details

### Dependencies

- **streamlit**: Web application framework
- **plotly**: Interactive visualizations
- **scikit-learn**: Machine learning algorithms
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **pinecone-client**: Vector database client (optional)

### Performance

- **Caching**: Uses Streamlit's caching for data loading and processing
- **Mock Database**: Simulates vector database operations for demonstration
- **Efficient Clustering**: Optimized K-means implementation
- **Interactive Plots**: Real-time hover and selection

## 🚦 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Memory Issues**: Reduce dataset size if running on limited memory
3. **Port Conflicts**: Use `streamlit run app.py --server.port 8502` for different port
4. **Font Cache**: First run may be slow due to matplotlib font cache building

### Support

For issues with the demo application, check:
- Python version compatibility (3.8+)
- All required packages installed
- CSV files in correct format in `data/` directory

## 📄 License

This is an educational demonstration project. The code is provided for learning purposes about vector databases and similarity search.

## 🎓 Learning Resources

- [Pinecone Documentation](https://docs.pinecone.io/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Built with ❤️ for educational purposes**