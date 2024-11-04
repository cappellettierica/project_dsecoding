import pandas as pd
import os

class DataHandler:
    def __init__(self):
        self.filepath = os.path.expanduser("~") + "/python/imdb_project/moviequiz/data/imdb_data.csv"
        self.data = None

    def load_data(self):
        """Load IMDb data from a CSV file and perform any necessary preprocessing."""
        try:
            self.data = pd.read_csv(self.filepath)
            self.data.dropna(subset=['Series_Title', 'Genre', 'Director', 'Released_Year'], inplace=True)
            return self.data
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return pd.DataFrame()

    def get_data(self):
        """Return the loaded data."""
        if self.data is None:
            self.load_data()
        return self.data
