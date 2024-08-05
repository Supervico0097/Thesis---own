from pathlib import Path

import pandas as pd
import pytest

# Directory where the data files are located
DATA_DIR = Path("../data")

# Expected checks for each file
check_dict = {
    "data/songs.csv": {"Shape": (320, 8), "Unique id": 320},
    "data/users_favorite_genre.csv": {"Shape": (1202, 2), "Unique id": 788},
    "data/users.csv": {"Shape": (959, 6), "Unique id": 959},
    "data/users_favorite_song.csv": {"Shape": (2290, 2), "Unique id": 841},
    "data/artists.csv": {"Shape": (96, 6), "Unique id": 96},
    "data/users_favorite_artist.csv": {"Shape": (1288, 2), "Unique id": 693},
    # "data/streams.csv": {"Shape": (115829, 4), "Unique id": 115829},
}


@pytest.mark.parametrize("data_file", DATA_DIR.glob("*.csv"))
def test_file_integrity(data_file):
    df = pd.read_csv(data_file)
    file_checks = check_dict.get(str(data_file))
    if file_checks is None:
        pytest.skip(f"No checks available for {data_file}")
    # Checking column count
    assert (
        df.shape[1] == file_checks["Shape"][1]
    ), f"Column count mismatch in {data_file}. Expected {file_checks['Shape'][1]}, found {df.shape[1]}"

    # Checking row count within ±10% of the original value
    min_rows, max_rows = int(file_checks["Shape"][0] * 0.8), int(
        file_checks["Shape"][0] * 1.2
    )
    assert (
        min_rows <= df.shape[0] <= max_rows
    ), f"Row count in {data_file} not within ±10% of the original value. Expected between {min_rows} and {max_rows}, found {df.shape[0]}"
