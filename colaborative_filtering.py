import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv("data/streams.csv")
df.user_id = df.user_id.apply(lambda x: "user_" + str(x))
df.song_id = df.song_id.apply(lambda x: "song_" + str(x))

df = df.groupby(["song_id", "user_id"]).agg(stream_count=("steam_id", "count"))
df = df[df.stream_count < 10]


df = (
    pd.pivot_table(data=df, values="stream_count", index="song_id", columns="user_id")
    .fillna(0)
    .astype(np.uint8)
)


df, df_test = train_test_split(df, random_state=7, test_size=0.2)
df1 = df.copy()


def recommend_songs(user, num_recommended_songs, df1):
    print("The list of the Songs {} Has Streamed \n".format(user))

    for song_id in df[df[user] > 0][user].index.tolist()[:10]:
        print(song_id)

    print("\n")

    recommended_songs = []

    for song_id in df[df[user] == 0].index.tolist():
        index_df = df.index.tolist().index(song_id)
        predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
        recommended_songs.append((song_id, predicted_rating))

    sorted_rm = sorted(recommended_songs, key=lambda x: x[1], reverse=True)

    rank = 1
    recommendations = []
    for recommended_songs in sorted_rm[:num_recommended_songs]:
        recommendations.append(
            {
                "song_id": recommended_songs[0],
                "streams_cnt_pred": recommended_songs[1],
            }
        )
        rank = rank + 1
    return pd.DataFrame(recommendations)


def song_recommender(user, num_neighbors, num_recommendation):
    number_neighbors = num_neighbors

    knn = NearestNeighbors(metric="cosine", algorithm="brute")
    knn.fit(df.values)
    distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)

    user_index = df.columns.tolist().index(user)

    for song_id, t in list(enumerate(df.index)):
        if df.iloc[song_id, user_index] == 0:
            sim_songs = indices[song_id].tolist()
            songs_distances = distances[song_id].tolist()

            if song_id in sim_songs:
                indices_song_id = sim_songs.index(song_id)
                sim_songs.remove(song_id)
                songs_distances.pop(indices_song_id)

            else:
                sim_songs = sim_songs[: num_neighbors - 1]
                songs_distances = songs_distances[: num_neighbors - 1]

            song_similarity = [1 - x for x in songs_distances]
            song_similarity_copy = song_similarity.copy()
            nominator = 0

            for s in range(0, len(song_similarity)):
                if df.iloc[sim_songs[s], user_index] == 0:
                    if len(song_similarity_copy) == (number_neighbors - 1):
                        song_similarity_copy.pop(s)

                    else:
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
                    predicted_r = nominator / sum(song_similarity_copy)

                else:
                    predicted_r = 0

            else:
                predicted_r = 0

            df1.iloc[song_id, user_index] = predicted_r
    recommendations_df = recommend_songs(user, num_recommendation, df1=df1)
    return recommendations_df


if __name__ == "__main__":
    recommendations_df = song_recommender(
        user="user_5", num_neighbors=3, num_recommendation=5
    )
    print(recommendations_df)
