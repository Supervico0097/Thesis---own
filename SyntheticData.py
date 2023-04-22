from abc import ABC, abstractmethod
import faker
from faker_music import MusicProvider



class SyntheticData(ABC):

    def __init__(self):
        self.fake = faker.Faker()
        self.fake.add_provider(MusicProvider)


    @abstractmethod
    def create_users(self):
        pass

