# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def load_data():
    # Read data from a CSV file into a Pandas DataFrame
    df = pd.read_csv("data/streams.csv")

    # Preprocess user and song IDs by adding prefixes to ensure consistent formatting
    df.user_id = df.user_id.apply(lambda x: "user_" + str(x))
    df.song_id = df.song_id.apply(lambda x: "song_" + str(x))

    # Group data by song and user IDs and calculate the count of streams
    df = df.groupby(["song_id", "user_id"]).agg(stream_count=("steam_id", "count"))

    # Filter out rows with stream counts less than 10
    df = df[df.stream_count < 10]

    # Create a pivot table to reshape the data for collaborative filtering and convert to unsigned integers
    df = (
        pd.pivot_table(
            data=df, values="stream_count", index="song_id", columns="user_id"
        )
        .fillna(0)
        .astype(np.uint8)
    )
    return df


# Define a function to recommend songs for a given user
def recommend_songs(user, num_recommended_songs, df_copy):
    # Print the list of songs the user has streamed
    print("The list of the Songs {} Has Streamed \n".format(user))
    for song_id in df[df[user] > 0][user].index.tolist()[:10]:
        print(song_id)
    print("\n")

    recommended_songs = []
    # Find songs the user has not streamed and calculate predicted ratings
    for song_id in df[df[user] == 0].index.tolist():
        index_df = df.index.tolist().index(song_id)
        predicted_rating = df_copy.iloc[index_df, df_copy.columns.tolist().index(user)]
        recommended_songs.append((song_id, predicted_rating))

    # Sort recommended songs by predicted rating in descending order
    sorted_rm = sorted(recommended_songs, key=lambda x: x[1], reverse=True)

    rank = 1
    recommendations = []
    for recommended_songs in sorted_rm[:num_recommended_songs]:
        # Create a list of recommended songs with their predicted ratings
        recommendations.append(
            {
                "rank": rank,
                "song_id": recommended_songs[0],
                "streams_cnt_pred": recommended_songs[1],
            }
        )
        rank = rank + 1
    return pd.DataFrame(recommendations)


# Define a song recommender function that uses collaborative filtering
def song_recommender(user, num_neighbors, num_recommendation, df):
    # Create a copy of the original DataFrame
    df1 = df.copy()

    # Number of neighbors for the Nearest Neighbors model
    number_neighbors = num_neighbors

    # Create a Nearest Neighbors model with cosine similarity
    knn = NearestNeighbors(metric="cosine", algorithm="brute")
    knn.fit(df.values)
    distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)

    # Find the index of the user in the DataFrame
    user_index = df.columns.tolist().index(user)

    # Loop through each song in the DataFrame
    for song_id, t in list(enumerate(df.index)):
        # Check if the user has not streamed the song (rating is 0)
        if df.iloc[song_id, user_index] == 0:
            # Get similar songs and their distances
            sim_songs = indices[song_id].tolist()
            songs_distances = distances[song_id].tolist()

            # Remove the current song from the list if it's present
            if song_id in sim_songs:
                indices_song_id = sim_songs.index(song_id)
                sim_songs.remove(song_id)
                songs_distances.pop(indices_song_id)
            else:
                # Limit the number of similar songs to the desired number of neighbors
                sim_songs = sim_songs[: num_neighbors - 1]
                songs_distances = songs_distances[: num_neighbors - 1]

            # Calculate song similarities based on distances
            song_similarity = [1 - x for x in songs_distances]
            song_similarity_copy = song_similarity.copy()
            nominator = 0

            # Calculate the predicted rating for the song
            for s in range(0, len(song_similarity)):
                if df.iloc[sim_songs[s], user_index] == 0:
                    if len(song_similarity_copy) == (number_neighbors - 1):
                        # Remove the first element when reaching the limit
                        song_similarity_copy.pop(s)
                    else:
                        # Remove the first element when the list isn't at its limit
                        song_similarity_copy.pop(
                            s - (len(song_similarity) - len(song_similarity_copy))
                        )
                else:
                    nominator = (
                        nominator
                        + song_similarity[s] * df.iloc[sim_songs[s], user_index]
                    )

            if len(song_similarity_copy) > 0:
                if sum(song_similarity_copy) > 0:
                    # Calculate the predicted rating for the song
                    predicted_r = nominator / sum(song_similarity_copy)
                else:
                    # Set predicted rating to 0 if no valid similarities
                    predicted_r = 0
            else:
                # Set predicted rating to 0 if no valid similarities
                predicted_r = 0

            # Update the predicted rating for the song in the copy of the DataFrame
            df1.iloc[song_id, user_index] = predicted_r

    # Generate song recommendations for the user using the updated DataFrame
    recommendations_df = recommend_songs(user, num_recommendation, df_copy=df1)
    return recommendations_df


# Entry point of the program
if __name__ == "__main__":
    # Call the song_recommender function with specific user, neighbor count, and recommendation count
    df = load_data()
    recommendations_df = song_recommender(
        user="user_5", num_neighbors=3, num_recommendation=5, df=df
    )
    # Print the recommendations
    print(recommendations_df)
