import requests
import pandas as pd

class ChessAPI:
    """
    A class to interact with the Chess.com API.
    """

    BASE_URL = "https://api.chess.com/pub"

    @classmethod
    def fetch_games(cls, player_name, year, month):
        """
        Fetches and returns a DataFrame containing all games for a given year and month from a player's Chess.com game archive.
        
        :param player_name: The player's username on Chess.com.
        :param year: The year for which to filter the games.
        :param month: The month for which to filter the games.
        :return: A pandas DataFrame containing the games for the specified year and month.
        """
        url = f"{cls.BASE_URL}/player/{player_name}/games/{year}/{month}"
        all_games = pd.DataFrame()

        try:
            response = requests.get(url)
            response.raise_for_status()
            games_data = response.json().get('games', [])

            if games_data:
                all_games = pd.json_normalize(games_data, max_level=1)
        except requests.RequestException as e:
            cls._log_error(f"Error fetching games from URL {url}: {e}")
        except (KeyError, TypeError, ValueError) as e:
            cls._log_error(f"Error processing games data from URL {url}: {e}")

        return all_games

    @classmethod
    def fetch_player_data(cls, player_name):
        """
        Fetches and returns all available data about a player from the Chess.com API.
        
        :param player_name: The player's username on Chess.com.
        :return: A dictionary containing all available data about the player.
        """
        url = f"{cls.BASE_URL}/player/{player_name}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            player_data = response.json()
            return player_data
        except requests.RequestException as e:
            cls._log_error(f"Error fetching player data from URL {url}: {e}")
            return None

    @staticmethod
    def _log_error(message):
        """
        Logs an error message.
        
        :param message: The error message to be logged.
        """
        print(f"Error: {message}")

