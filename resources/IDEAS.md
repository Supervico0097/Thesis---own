Business Problem
- MUSIC - song popularity
- MUSIC - song/artist recommendation
- MUSIC - subscription discount classification
- CAR SELLING - HOW Much Cars to produce
  ML Problem
- SELECT - MUSIC - song popularity - number of streams in next week or month - regression problem (ML)  <--- CHOOSEN
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

IDEA:

- car selling
- pokemon
- make_classification sklearn (pure synthetic no real world interpretation)

TO TALK:

- 2 scenarios
- use more ML?

# TODO 2023_06_30

- [ ] Separate table for users, favourite genres to be saved in a different CSV file and remove it from users file
- [ ] Remove streams data from users, CSV file
- [ ] line 195 ```list_songs = self.song_list``` don't do that.
- [ ] Tried to use the less nested, if

- [ ] ML resources: https://www.kaggle.com/code/yasserh/song-popularity-prediction-best-ml-models