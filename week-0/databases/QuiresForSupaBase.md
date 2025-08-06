# Supabase Queries: Exploring Music Data 🎵

## Basic Queries

### 1. Find Songs from Your Birth Year

```sql
-- Replace 1990 with your birth year
SELECT track_name, artist, decade
FROM "MostPlayedSogs"
WHERE decade = (1990 / 10) * 10
LIMIT 10;
```

### 2. Find the Happiest Songs

```sql
SELECT track_name, artist, valence as happiness_score
FROM "MostPlayedSogs"
ORDER BY valence DESC
LIMIT 10;
```

### 3. Find Party Songs

```sql
SELECT track_name, artist, danceability
FROM "MostPlayedSogs"
WHERE danceability > 0.8
ORDER BY danceability DESC
LIMIT 15;
```

## Bonus Queries

### 4. Find the LOUDEST Songs

```sql
SELECT track_name, artist, loudness
FROM "MostPlayedSogs"
ORDER BY loudness DESC
LIMIT 5;
```

### 5. Find the LONGEST Songs

```sql
SELECT track_name, artist, duration_ms/60000 as minutes
FROM "MostPlayedSogs"
ORDER BY duration_ms DESC
LIMIT 5;
```

### 6. Count Songs by Decade

```sql
SELECT decade, COUNT(*) as total_songs
FROM "MostPlayedSogs"
GROUP BY decade
ORDER BY decade;
```