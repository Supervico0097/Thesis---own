import random
from pathlib import Path

import faker
import numpy as np
import pandas as pd
import yaml

DATA_PATH = Path('data')
DATA_PATH.mkdir(exist_ok=True)


def _rand_bool(true_prob):
    return np.random.choice([True, False], p=[true_prob, 1 - true_prob])


class SyntheticStreamingDataGenerator:

    def __init__(self, config_file_path):
        super().__init__()
        self.fake = faker.Faker()
        self.user_list = []
        self.artist_list = []
        self.song_list = []
        self.stream_list = []
        self.user_fav_genre = []
        self.user_fav_artist = []
        self.user_fav_song = []

        with open(config_file_path) as fh:
            data = yaml.load(fh, Loader=yaml.FullLoader)

        self.users_number = data['users_number']
        self.artists_number = data['artists_number']
        self.weeks_num = data['WEEKS_NUM']

        frequencies_genre_df = pd.DataFrame(data['frequencies_genre']).T
        self.probabilities_genre_df = frequencies_genre_df / frequencies_genre_df.sum()
        frequencies_continent_df = pd.DataFrame(data['frequencies_continent']).T
        self.probabilities_continent_df = frequencies_continent_df / frequencies_continent_df.sum()

        self.p_favorite = data['p_favorite']
        self.p_favorite_playlist = data['p_favorite_playlist']
        self.p_random_songs_stream = data['p_random_songs_stream']
        self.avg_songs_unsub = data['avg_songs_unsub']
        self.avg_songs_sub = data['avg_songs_sub']
        self.p_fav_art_sng_gnr_cnt = data['p_fav_art_sng_gnr_cnt']
        self.p_fav_art_sng_gnr = data['p_fav_art_sng_gnr']
        self.p_fav_gnr = data['p_fav_gnr']
        self.p_other = data['p_other']
        self.min_streams_to_favorites = data['min_streams_to_favorites']
        self.min_streams_to_famous_song = data['min_streams_to_famous_song']
        self.min_streams_to_famous_artist = data['min_streams_to_famous_artist']

    def run(self):
        for week_no in range(self.weeks_num):
            self.create_artists(week_no)
            self.generate_songs(week_no)
            self.create_users(week_no)
            self.generate_streams(week_no)


        self.generate_additional_tables()
        users_df = pd.DataFrame(self.user_list)
        users_df.drop(columns=["favorite genres", "favorite artists", "favorite songs", "streams"], inplace=True)
        artist_df = pd.DataFrame(self.artist_list)
        song_df = pd.DataFrame(self.song_list)
        stream_df = pd.DataFrame(self.stream_list)
        users_df.to_csv(DATA_PATH / 'users.csv', index=False)
        artist_df.to_csv(DATA_PATH / 'artists.csv', index=False)
        song_df.to_csv(DATA_PATH / 'songs.csv', index=False)
        stream_df.to_csv(DATA_PATH / 'streams.csv', index=False)



    def create_users(self, week_no):
        # https://mycurvefit.com/
        num_users_to_add = round(
            (11.17315 + 0.3660266 * week_no + 0.009279995 * week_no ** 2) * (self.users_number / 5976.23302825)
        )

        for _ in range(num_users_to_add):

            user = {
                'user_id': len(self.user_list),
                'user_name': self.fake.name(),
                'age': int(((np.random.lognormal(mean=1, sigma=0.1, size=1)) * 20 - 25)[0]),
                'continent': np.random.choice(
                    a=self.probabilities_continent_df.index.to_list(),
                    p=self.probabilities_continent_df.user.to_list()),
                'favorite genres': [],
                'favorite artists': [],
                'favorite songs': [],
                'streams': {},
                'is_subscribed': _rand_bool(0.1),
                'week': week_no
            }

            # adding favorite genres
            for _ in range(int(np.random.choice([0, 1, 2, 3], p=[0.2, 0.4, 0.3, 0.1]))):
                user['favorite genres'].append(np.random.choice(
                    a=self.probabilities_genre_df.index.to_list(),
                    p=self.probabilities_genre_df.user.to_list())
                )
            user['favorite genres'] = list(dict.fromkeys(user['favorite genres']))  # remove duplicates

            # adding favorite artists
            to_add = False
            #  for singer in self.artist_list:
            for _ in range(random.randrange(5)):
                for _ in range(20):
                    choice = random.choice(self.artist_list)
                    if choice['continent'] == user['continent'] and choice['genre'] in user['favorite genres'] and \
                            choice['is_famous'] and random.uniform(0, 1) < 0.7:
                        to_add = True
                        break
                    elif choice['continent'] == user['continent'] and choice['genre'] in user['favorite genres'] and \
                            random.uniform(0, 1) < 0.4:
                        to_add = True
                        break
                    elif choice['genre'] in user['favorite genres'] and choice['is_famous'] and random.uniform(0,
                                                                                                               1) < 0.4:
                        to_add = True
                        break
                    elif random.uniform(0, 1) < 0.05:
                        to_add = True
                        break

                if to_add:
                    user['favorite artists'].append(choice['artist_id'])
                to_add = False

            user['favorite artists'] = list(dict.fromkeys(user['favorite artists']))  # remove duplicates

            # add favorite songs - first go through favorite artists
            for i in user['favorite artists']:
                favorite_artist_list = [song for song in self.song_list if song['artist_id'] == i]

                for song in favorite_artist_list:
                    # to check if to add to favorites song of favorite artist
                    if random.uniform(0, 1) < 0.7 and user['is_subscribed']:
                        user['favorite songs'].append(song['song_id'])

                    if random.uniform(0, 1) < 0.7 and not user['is_subscribed'] and song['is_premium']:
                        user['favorite songs'].append(song['song_id'])

            # then go randomly through songs
            for _ in range(15):
                if self.song_list:
                    random_song = random.choice(self.song_list)

                    if random.uniform(0, 1) < 0.1:
                        user['favorite songs'].append(random_song['song_id'])

            user['favorite songs'] = list(dict.fromkeys(user['favorite songs']))  # remove duplicates

            self.user_list.append(user)

    def create_artists(self, week_no):
        num_artists_to_add = round(
            (11.17315 + 0.3660266 * week_no + 0.009279995 * week_no ** 2) * (self.artists_number / 5976.23302825)
        )

        for i in range(num_artists_to_add):
            artist = {
                'artist_id': len(self.artist_list),
                'continent': np.random.choice(
                    a=self.probabilities_continent_df.index.to_list(),
                    p=self.probabilities_continent_df.artist.to_list()),
                'genre': np.random.choice(
                    a=self.probabilities_genre_df.index.to_list(),
                    p=self.probabilities_genre_df.artist.to_list()),
                'is_famous': _rand_bool(0.1),
                'number_of_streams': 0,
                'week_no_created': week_no
            }
            self.artist_list.append(artist)

    def generate_songs(self, week_no):
        assert self.artist_list, "artist_list is empty"  # It checks whether the list is empty
        for artist in self.artist_list:
            # Artist of generating songs every time few weeks,
            # so we are randomly something if this week he will produce a song
            if _rand_bool(.25):
                self.song_list.append(
                    {
                        'song_id': len(self.song_list),
                        'artist_id': artist['artist_id'],
                        'genre': artist['genre'],
                        'is_artist_famous': artist['is_famous'],
                        'is_premium': _rand_bool(.1),
                        # premium songs can be listened by both subscribed and unsubscribed users
                        'is_famous': _rand_bool(.7) if artist['is_famous'] else _rand_bool(.1),
                        'week_released': week_no,
                        'number_of_streams': 0,
                    })

    def generate_streams(self, week_no):
        # There will be a Spotify playlist that will consist songs that will appear
        # randomly on users streams regardless of their preferences.
        # weekly_playlist = []
        assert self.user_list, "user_list is empty"  # It checks whether the list is empty
        premium_songs = [song for song in self.song_list if song['is_premium']]  # create a list of premium songs

        for user_i in range(len(self.user_list)):
            # count number of songs users goes through
            list_songs = self.song_list
            n_songs = len(self.song_list)

            if self.user_list[user_i]['is_subscribed'] and len(self.song_list) > self.avg_songs_sub:
                n_songs = random.randrange(self.avg_songs_sub - int(0.5 * self.avg_songs_sub),
                                           self.avg_songs_sub + int(0.5 * self.avg_songs_sub))

            elif not self.user_list[user_i]['is_subscribed'] and len(premium_songs) < self.avg_songs_unsub:
                list_songs = premium_songs
                n_songs = len(premium_songs)

            elif not self.user_list[user_i]['is_subscribed'] and len(premium_songs) > self.avg_songs_unsub:
                list_songs = premium_songs
                n_songs = random.randrange(self.avg_songs_unsub - int(0.5 * self.avg_songs_unsub),
                                           self.avg_songs_unsub + int(0.5 * self.avg_songs_unsub))

            # Random songs outside user's favorites
            if random.uniform(0,1) < self.p_random_songs_stream and list_songs:  # check if user will access the random songs

                for _ in range(int(n_songs)):  # go through songs
                    random_song = random.choice(list_songs)  # choose random song

                    # if singer is famous, song is famous, same genre, same continent
                    if (
                            self.artist_list[random_song['artist_id']]['is_famous']) \
                            and (random_song['is_famous']) \
                            and (
                            random_song['genre'] in self.user_list[user_i]['favorite genres']) \
                            and (
                            self.artist_list[random_song['artist_id']]['continent'] == self.user_list[user_i][
                        'continent']) \
                            and random.uniform(0, 1) < self.p_fav_art_sng_gnr_cnt:
                        user = self.add_stream(self.user_list[user_i], random_song['song_id'], week_no)
                        self.user_list[user_i] = user


                    # if singer is famous, song is famous, same genre
                    elif self.artist_list[random_song['artist_id']]['is_famous'] and random_song['is_famous'] and (
                            random_song['genre'] in self.user_list[user_i]['favorite genres']) and random.uniform(0,
                                                                                                                  1) < self.p_fav_art_sng_gnr:
                        user = self.add_stream(self.user_list[user_i], random_song['song_id'], week_no)
                        self.user_list[user_i] = user

                    # if singer is famous, song is famous, same genre
                    elif (random_song['genre'] in self.user_list[user_i]['favorite genres']) and random.uniform(0,
                                                                                                                1) < self.p_fav_gnr:
                        user = self.add_stream(self.user_list[user_i], random_song['song_id'], week_no)
                        self.user_list[user_i] = user

                    elif random.uniform(0, 1) < self.p_other:
                        user = self.add_stream(self.user_list[user_i], random_song['song_id'], week_no)
                        self.user_list[user_i] = user

            if random.uniform(0,1) < self.p_favorite_playlist and self.user_list[user_i]['favorite songs']: #check if user will access favorite songs
                list_songs = self.user_list[user_i]['favorite songs']
                if len(list_songs) > 1:
                    n_songs = random.randrange(len(list_songs) - int(0.5 * len(list_songs)),
                                                len(list_songs) + int(0.5 * len(list_songs)))
                else:
                    n_songs = len(list_songs)


                for _ in range(int(n_songs)):
                    if random.uniform(0,1) < self.p_favorite:
                        user = self.add_stream(self.user_list[user_i], random.choice(list_songs), week_no)
                        self.user_list[user_i] = user


    def add_stream(self, user, i, week_no):
        stream = {
            'steam_id': len(self.stream_list),
            'user_id': user['user_id'],
            'song_id': i,
            'week_no': week_no
        }
        # tracking how many times user listened to particular song and checking if users should add song to favorites
        if i in user['streams']:
            user['streams'][i] += 1
        else:
            user['streams'][i] = 1

        if user['streams'][i] > self.min_streams_to_favorites:
            user['favorite songs'].append(i)
            user['favorite songs'] = list(dict.fromkeys(user['favorite songs']))  # remove duplicates



        #tracking number of streams for each song and checking if to add to favorites
        self.song_list[i]['number_of_streams'] += 1

        if self.song_list[i]['number_of_streams'] > self.min_streams_to_famous_song:
            self.song_list[i]['is_famous'] = True


        #tracking number of streams for each artist and checking if to make famous
        self.artist_list[self.song_list[i]['artist_id']]['number_of_streams'] += 1

        if self.artist_list[self.song_list[i]['artist_id']]['number_of_streams'] > self.min_streams_to_famous_artist:
            self.artist_list[self.song_list[i]['artist_id']]['is_famous'] = True



        self.stream_list.append(stream)
        return user










    def generate_additional_tables(self):

        #generate users_favorite_gnres table
        for user in self.user_list:
            for genre in user['favorite genres']:
                row = {'user_id': user['user_id'], 'genre_id': genre}
                self.user_fav_genre.append(row)

        users_fav_genre_df = pd.DataFrame(self.user_fav_genre)
        users_fav_genre_df.to_csv(DATA_PATH / 'users_favorite_genre.csv', index=False)


        #generate users_favorite_artist table
        for user in self.user_list:
            for artist in user['favorite artists']:
                row = {'user_id': user['user_id'], 'artist_id': artist}
                self.user_fav_artist.append(row)

        users_fav_artist_df = pd.DataFrame(self.user_fav_artist)
        users_fav_artist_df.to_csv(DATA_PATH / 'users_favorite_artist.csv', index=False)


        #generate users_favorite_song table
        for user in self.user_list:
            for song in user['favorite songs']:
                row = {'user_id': user['user_id'], 'song_id': song}
                self.user_fav_song.append(row)

        users_fav_song_df = pd.DataFrame(self.user_fav_song)
        users_fav_song_df.to_csv(DATA_PATH / 'users_favorite_song.csv', index=False)





if __name__ == "__main__":
    generator = SyntheticStreamingDataGenerator(config_file_path='config_music.yaml')
    generator.run()
