from data_generator import SyntheticStreamingDataGenerator

if __name__ == "__main__":
    music = SyntheticStreamingDataGenerator(config_file_path='config.yaml')
    music.run()
