import pandas as pd
import numpy as np
from fetch_games import ChessAPI

class ChessDataCleaner:
    """
    A class for cleaning and processing chess game data.
    """

    COLUMNS_TO_DROP = [
        'url', 'pgn', 'tcn', 'uuid', 'initial_setup', 'fen',
        'white.@id', 'white.uuid', 'black.@id', 'black.uuid'
    ]

    def __init__(self, dataframe: pd.DataFrame, player_name: str):
        """
        Initialize the ChessDataCleaner.

        :param dataframe: The input DataFrame containing chess game data.
        :param player_name: The player's username for whom the data is being processed.
        """
        self.dataframe = dataframe.copy()
        self.player_name = player_name
        self.has_accuracy = 'accuracies.white' in self.dataframe.columns

    def drop_columns(self):
        """
        Drop unnecessary columns from the DataFrame.
        """
        self.dataframe.drop(columns=self.COLUMNS_TO_DROP, axis=1, inplace=True)
        
        if 'tournament' in self.dataframe.columns:
            self.dataframe.drop(columns=['tournament'], axis=1, inplace=True)

    def calculate_ratings(self):
        """
        Calculate player and opponent ratings based on the game's data.
        """
        self.dataframe[self.player_name + "'s rating"] = np.where(
            self.dataframe['white.username'] == self.player_name,
            self.dataframe['white.rating'],
            self.dataframe['black.rating']
        )
        self.dataframe["opponent's rating"] = np.where(
            self.dataframe['white.username'] != self.player_name,
            self.dataframe['white.rating'],
            self.dataframe['black.rating']
        )

    def calculate_accuracies(self):
        """
        Calculate player and opponent accuracies if available.
        """
        if self.has_accuracy:
            self.dataframe[self.player_name + " accuracy"] = np.where(
                self.dataframe['white.username'] == self.player_name,
                self.dataframe['accuracies.white'],
                self.dataframe['accuracies.black']
            )
            self.dataframe["Opponent accuracy"] = np.where(
                self.dataframe['white.username'] != self.player_name,
                self.dataframe['accuracies.white'],
                self.dataframe['accuracies.black']
            )

    def clean_data(self) -> pd.DataFrame:
        """
        Clean and process the data.

        :return: The cleaned DataFrame.
        """
        self.drop_columns()
        self.calculate_ratings()
        self.calculate_accuracies()

        # Convert the 'end_time' column to datetime format
        self.dataframe['end_time'] = pd.to_datetime(self.dataframe['end_time'], unit='s')

        return self.dataframe


