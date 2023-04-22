import SyntheticData
import pandas as pd
import numpy as np
import faker
from faker_music import MusicProvider
from configparser import ConfigParser
from random import randint
import yaml

class Music(SyntheticData.SyntheticData):
    def __init__(self):
        super().__init__()
        with open('config.yaml') as fh:
            read_data = yaml.load(fh, Loader=yaml.FullLoader)['music']


        self.dataset_size = read_data['dataset_size']
        self.users_number = read_data['users_number']
        self.songs_number = read_data['songs_number']
        self.error_probability = read_data['error_probability']
        self.p1 = read_data['p1']
        self.p2 = read_data['p2']
        self.p3 = read_data['p3']
        self.p4 = read_data['p4']
        self.p5 = read_data['p5']
        self.p6 = read_data['p6']
        self.p7 = read_data['p7']
        self.p8 = read_data['p8']

    def create_users(self):
        # TODO if number of users <100k continents = ['North America'] etc
        continents = ['Asia', 'Africa', 'North America', 'South America', 'Europe', 'Australia']

        self.fake_users = [{'User ID': x + 1000,
                            'User Name': self.fake.name(),
                            'Age': np.random.choice([randint(15,39), randint(50,60),randint(60,85)], p=[0.60, 0.30, 0.10]),
                            'Continent': np.random.choice(continents),
                            'Favorite genre': self.fake.music_genre(),
                            'Favorite songs': [],
                            'is_Subscribed':np.random.choice(['True', 'False'], p=[0.5, 0.5])
                            } for x in range(1000)]

        users_df = pd.DataFrame(self.fake_users)
        users_df.to_csv('users.csv')








    def create_songs(self):

        self.fake_songs = [{'Song ID': x + 1000,
                            'genre': np.random.choice(['Pop', 'Rock', 'The 90\'s', 'The 80\'s', 'Soundtracks', 'Hip-hop'
                                                          , 'Electronic', 'Blues']),
                            'region': np.random.choice(['Latin', 'Asian', 'American', 'European'], p=[self.p1[0], self.p1[1], self.p1[2], self.p1[3]]),
                            'legnth': randint(80,190),
                            'in_Subscribtion': np.random.choice(['True', 'False'], p=[0.70, 0.30])} for x in range(self.songs_number)]

        songs_df = pd.DataFrame(self.fake_songs)
        songs_df.to_csv('songs.csv')


    def generate(self):
        self.create_songs()
        self.create_users()
        self.get_parameters_from_file()



