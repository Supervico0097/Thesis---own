import datetime
import random

import faker
import numpy as np
import yaml
import pandas as pd


class SyntheticStreamingDataGenerator:

    def __init__(self, config_file_path):
        super().__init__()
        self.fake = faker.Faker()
        self.user_list = []
        self.artist_list = []
        self.song_list = []
        self.stream_list = []

        with open(config_file_path) as fh:
            read_data = yaml.load(fh, Loader=yaml.FullLoader)

        # TODO: remove unused params
        self.users_number = read_data['music']['users_number']
        self.artists_number = read_data['music']['artists_number']
        self.weeks_num = read_data['music']['WEEKS_NUM']
        self.probabilities_genre_users = read_data['music']['probabilities_genre_users']
        self.probabilities_genre_artists = read_data['music']['probabilities_genre_artists']
        self.min_songs_per_week = read_data['music']['min_songs_per_week']
        self.max_songs_per_week = read_data['music']['max_songs_per_week']
        self.p_favorite = read_data['music']['p_favorite']
        self.p_favorite_playlist = read_data['music']['p_favorite_playlist']
        self.p_repeat_fav_sg = read_data['music']['repeat_fav_sg']

        # TODO: rename the probs and move them when needed out of config file


    def run(self):

        # self.continents = ['North America']  # we assume that at the intital release, only US users are available
        # self.geners = ['Pop', 'Rock', 'The 90\'s', 'The 80\'s', 'Soundtracks', 'Hip-hop', 'Electronic', 'Blues']

        for week_no in range(self.weeks_num):
            self.create_users(week_no)
            self.create_artists(week_no)
            self.generate_songs(week_no)
            self.generate_streams(week_no)


        # TODO: pandas df save to csv (use ./data path)
        users_df = pd.DataFrame(self.user_list)
        artist_df = pd.DataFrame(self.artist_list)
        song_df = pd.DataFrame(self.song_list)
        users_df.to_csv('users.csv')
        artist_df.to_csv('artists.csv')
        song_df.to_csv('songs.csv')

    def create_users(self, week_no):
        # https://mycurvefit.com/
        num_users_to_add = round(
            (11.17315 + 0.3660266 * week_no + 0.009279995 * week_no ** 2) * (self.users_number / 5976.23302825)
        )

        s = sum(self.probabilities_genre_users)
        prob_pop = self.probabilities_genre_users[0]/s
        prob_Rock = self.probabilities_genre_users[1]/s
        prob_HipHop = self.probabilities_genre_users[2]/s
        prob_Electronic = self.probabilities_genre_users[3]/s
        prob_Jazz = self.probabilities_genre_users[4]/s
        prob_Classical = self.probabilities_genre_users[5]/s
        prob_Blues = self.probabilities_genre_users[6]/s
        prob_Alternative = self.probabilities_genre_users[7]/s



        for _ in range(num_users_to_add):

            user = {
                'user_id': len(self.user_list),
                'user_name': self.fake.name(),
                'age': int(((np.random.lognormal(mean=1, sigma=0.1, size=1)) * 20 - 25)[0]),
                'music_fan': np.random.choice([True, False], p=[0.55, 0.45]),
                'favorite genre': np.random.choice(['Pop', 'Rock', 'Hip-hop', 'Electronic', 'Jazz', 'Classical', 'Blues', 'Alternative'], p=[prob_pop, prob_Rock,prob_HipHop, prob_Electronic, prob_Jazz, prob_Classical, prob_Blues, prob_Alternative]),
                'favorite artist': [],
                'favorite songs': [],
                'streams': {},
                'is_subscribed': np.random.choice([True, False], p=[0.1, 0.9]),
                'week': week_no
            }
            self.user_list.append(user)





    def create_artists(self, week_no):
        num_artists_to_add = round(
            (11.17315 + 0.3660266 * week_no + 0.009279995 * week_no ** 2) * (self.artists_number / 5976.23302825)
        )

        s = sum(self.probabilities_genre_artists)
        prob_pop = self.probabilities_genre_artists[0]/s
        prob_Rock = self.probabilities_genre_artists[1]/s
        prob_HipHop = self.probabilities_genre_artists[2]/s
        prob_Electronic = self.probabilities_genre_artists[3]/s
        prob_Jazz = self.probabilities_genre_artists[4]/s
        prob_Classical = self.probabilities_genre_artists[5]/s
        prob_Blues = self.probabilities_genre_artists[6]/s
        prob_Alternative = self.probabilities_genre_artists[7]/s

        for i in range(num_artists_to_add):
            artist = {
                'artist_id': len(self.artist_list),
                'genre': np.random.choice(['Pop', 'Rock', 'Hip-hop', 'Electronic', 'Jazz', 'Classical', 'Blues', 'Alternative'], p=[prob_pop, prob_Rock,prob_HipHop, prob_Electronic, prob_Jazz, prob_Classical, prob_Blues, prob_Alternative]),
                'famous': np.random.choice([True, False], p=[0.1, 0.9]),
                'week': week_no
            }
            self.artist_list.append(artist)






    def generate_songs(self, week_no):
        for artist in self.artist_list:
            is_generating_songs = np.random.choice([True, False], p=[0.25, 0.75])

            if is_generating_songs:
                song = {
                    'song_id': len(self.song_list),
                    'artist': artist['artist_id'],
                    'is_artist_famous': artist['famous'],
                    'Premium': np.random.choice([True, False], p=[0.1, 0.9]), #premium songs can be listened by both subscribed and unsubscribed users
                    'Famous': None,
                    'week': week_no,
                    'number of streams': 0,
                }

                if artist['famous']:
                    song['Famous'] = np.random.choice([True, False], p=[0.7, 0.3])
                else:
                    song['Famous'] = np.random.choice([True, False], p=[0.1, 0.9])


                self.song_list.append(song)





    def generate_streams(self, week_no):

        weekly_playlist = []
        number_of_listens = random.randrange(self.min_songs_per_week, self.max_songs_per_week)


        for user_i in range(self.user_list):

            #TODO: 1) going through favorite playlist
            if random.uniform(0,1) < self.p_favorite_playlist: #check if user will access favourites
                for i in user_list[user_i]['favorite songs']: #go through random songs

                    if random.uniform(0,1) < self.p_favorite: #check if user will listen to favorite
                        user = self.add_stream(user_list[user_i], i)
                        user_list[user_i] = user

                        while random.uniform(0,1) < self.p_repeat_fav_sg: #check if user will repeat favourite song
                            user = self.add_stream(user_list[user_i], i)
                            user_list[user_i] = user







            #TODO: 2) going through random songs for favorite genre



            #TODO: 3) goign through random songs




    def add_stream(self, user, i):

        stream = {
            'steam_id': len(self.stream_list),
            'user_id': user['user_id'],
            'song_id': i
        }

        #tracking how many times user listened to particular song
        if i in user['streams']:
            user['streams'][i] += 1
        else:
            user['streams'][i] = 1

        self.stream_list.append(stream)
        return user













