# MongoDB Queries: Exploring Movies Like a Data Detective 🎬

## Basic Queries

### 1. Find the Best Movie from Your Birth Year

```javascript
// Replace 1995 with your birth year
db.movies.find(
  { year: 1995 },
  { title: 1, "imdb.rating": 1, genres: 1, year: 1 }
).sort({ "imdb.rating": -1 }).limit(1)
```

### 2. Discover Movies Longer Than a Typical Workday

```javascript
db.movies.find(
  { runtime: { $gte: 480 } },
  { title: 1, runtime: 1, year: 1, genres: 1 }
).sort({ runtime: -1 })
```

### 3. Find Highly Rated Movies in Your Favorite Genre

```javascript
// Replace "Comedy" with your favorite genre
db.movies.find(
  { 
    genres: "Comedy",
    "imdb.rating": { $gte: 8.0 }
  },
  { title: 1, "imdb.rating": 1, year: 1 }
).sort({ "imdb.rating": -1 }).limit(5)
```

### 4. Hunt for the Oldest Movie in the Database

```javascript
db.movies.find(
  {},
  { title: 1, year: 1, directors: 1, plot: 1 }
).sort({ year: 1 }).limit(1)
```

### 5. Find Movies from a Specific Country

```javascript
// Replace "India" with any country
db.movies.find(
  { countries: "India" },
  { title: 1, year: 1, "imdb.rating": 1, languages: 1 }
).sort({ "imdb.rating": -1 }).limit(5)
```

## Advanced Queries

### 6. Discover the Most Controversial Movies

```javascript
db.movies.aggregate([
  { $match: { 
    "tomatoes.critic.rating": { $exists: true },
    "tomatoes.viewer.rating": { $exists: true }
  }},
  { $addFields: { 
    ratingDiff: { $abs: { $subtract: ["$tomatoes.critic.rating", "$tomatoes.viewer.rating"] } }
  }},
  { $sort: { ratingDiff: -1 } },
  { $project: { 
    title: 1, 
    year: 1,
    criticRating: "$tomatoes.critic.rating",
    viewerRating: "$tomatoes.viewer.rating",
    difference: "$ratingDiff"
  }},
  { $limit: 5 }
])
```

## Text Search

### 7. Find Movies Mentioning Your Name

```javascript
// Replace "John" with your first name
db.movies.find(
  { 
    $or: [
      { cast: { $regex: "John", $options: "i" } },
      { directors: { $regex: "John", $options: "i" } }
    ]
  },
  { title: 1, year: 1, cast: 1, directors: 1 }
).limit(3)
```
