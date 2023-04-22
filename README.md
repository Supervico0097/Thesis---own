Business Problem
- MUSIC - song popularity
- MUSIC - song/artist recommendation
- MUSIC - subscription discount classification
- CAR SELLING - HOW Much Cars to produce
ML Problem
- SELECT - MUSIC - song popularity - number of streams in next week or month - regression problem (ML)
- MUSIC - song/artist recommendation - COMPLEX
- MUSIC - subscription discount - ML classification
- CAR SELLING - HOW Much Cars to produce - Time Series Analysis - Regression Problem
ML Architecture
- Logistic Regression/Decision Tree/Random Forest
Design the train data
- Y - "Number of streams of a song 2 Months after the given date" and date have to be at least 2 months after release.
- X (Song Data):
  - Date
  - Streams# n-weeks BeforeDate, where n from 0 to 8
  - Country
  - Genre
  - Song Length
  - Language (isEnglish)
  - ArtisSongs#
  - ArtistStreams#
  - MostPopularSongStreams# "Take the song with most streams for the artist of a given song and get number of streams from a given date"
  - MostCommonGenreStreams#
  - ... (add like max 10 more)
Design the Raw Data
  - Users
  - Artists
  - Songs
    - It takes time to release a song
    - first songs may not be as popular
    - every artist has its most popular song, some of them will have more than one
    - 
