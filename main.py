from abc import ABC, abstractmethod
import SyntheticData
import Music


class vehicle(ABC):

    @abstractmethod
    def go(self):
        pass

    def drive(self):
        print('driving')


class car(vehicle):
    def go(self):
        print('going')


c = car()
c.go()
c.drive()





music = Music.Music()
music.create_users()
music.get_parameters_from_file()
music.create_songs()

