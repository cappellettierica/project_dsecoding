import pandas as pd
import os

class DataHandler:
    def __init__(self):
        self.filepath = os.path.expanduser("~") + "/python/imdb_project/data/imdb_data.csv"
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_csv(self.filepath)
            self.data.drop(columns=['Poster_Link', 'Meta_score', 'IMDB_Rating', 'Certificate', 'Runtime', 'Gross', 'Overview'], inplace=True)
            self.data.dropna(subset=['Series_Title', 'Genre', 'Director', 'Released_Year', 'Star1', 'Star2', 'Star3', 'Star4'], inplace=True)
            return self.data
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return pd.DataFrame()

    def get_data(self):
        if self.data is None:
            self.load_data()
        return self.data