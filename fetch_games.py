import requests
import pandas as pd
import streamlit as st
import datetime

class ChessAPI:
    """
    A class to interact with the Chess.com API.
    """

    BASE_URL = "https://api.chess.com/pub"

    # Define a user-agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    @classmethod
    def fetch_games(cls, player_name=None, year=None, month=None, url=None):
        """
        Fetches and returns a DataFrame containing games either based on player_name, year, and month or a provided URL.

        :param player_name: The player's username on Chess.com (optional).
        :param year: The year for which to filter the games (optional).
        :param month: The month for which to filter the games (optional).
        :param url: The API URL to fetch games (optional, if provided, player_name, year, and month are ignored).
        :return: A pandas DataFrame containing the games.
        """
        if url:
            return cls._fetch_data_from_url(url)

        elif not player_name or not year or not month:
            raise ValueError("Either provide player_name, year, and month or provide a valid URL.")

        url = f"{cls.BASE_URL}/player/{player_name}/games/{year}/{month}"
        return cls._fetch_data_from_url(url)

    @classmethod
    def _fetch_data_from_url(cls, url):
        """
        Fetches and returns data from a provided URL.

        :param url: The API URL to fetch data from.
        :return: The fetched data.
        """
        data = None

        try:
            # Include the user-agent header in the request
            response = requests.get(url, headers=cls.headers)
            response.raise_for_status()
            games_data = response.json().get('games', [])

            if games_data:
                data = pd.json_normalize(games_data, max_level=1)
        except requests.RequestException as e:
            cls._log_error(f"Error fetching games from URL {url}: {e}")
        except (KeyError, TypeError, ValueError) as e:
            cls._log_error(f"Error processing games data from URL {url}: {e}")

        return data

    @classmethod
    def fetch_player_data(cls, player_name):
        """
        Fetches and returns all available data about a player from the Chess.com API.

        :param player_name: The player's username on Chess.com.
        :return: A dictionary containing all available data about the player.
        """
        url = f"{cls.BASE_URL}/player/{player_name}"

        try:
            # Include the user-agent header in the request
            response = requests.get(url, headers=cls.headers)
            response.raise_for_status()
            player_data = response.json()
            return player_data
        except requests.RequestException as e:
            cls._log_error(f"Error fetching player data from URL {url}: {e}")
            return None

    @classmethod
    def fetch_country_data(cls, country_url):
        """
        Fetches and returns data about a country from a given API URL.

        :param country_url: The API URL for the country data.
        :return: A dictionary containing data about the country.
        """
        try:
            # Include the user-agent header in the request
            response = requests.get(country_url, headers=cls.headers)
            response.raise_for_status()
            country_data = response.json()
            return country_data
        except requests.RequestException as e:
            cls._log_error(f"Error fetching country data from URL {country_url}: {e}")
            return None

    @classmethod
    def fetch_player_stats(cls, player_name):
        """
        Fetches and returns statistics for a player from the Chess.com API.

        :param player_name: The player's username on Chess.com.
        :return: A dictionary containing statistics for the player.
        """
        url = f"{cls.BASE_URL}/player/{player_name}/stats"
        player_stats = {}

        try:
            # Include the user-agent header in the request
            response = requests.get(url, headers=cls.headers)
            response.raise_for_status()
            player_stats = response.json()
        except requests.RequestException as e:
            cls._log_error(f"Error fetching player stats from URL {url}: {e}")

        return player_stats

    @staticmethod
    def _log_error(message):
        """
        Logs an error message.

        :param message: The error message to be logged.
        """
        print(f"Error: {message}")

    @classmethod
    def display_player_info(cls, player_name):
        """
        Fetches and displays player information in a Streamlit app.

        :param player_name: The player's username on Chess.com.
        """
        st.subheader("Player Information")

        player_info = cls.fetch_player_data(player_name)

        if player_info:
            st.write("Username: ", player_info['username'])

            # Handle the case where 'country' is another API link
            if 'country' in player_info and player_info['country']:
                country_data = cls.fetch_country_data(player_info['country'])
                if country_data:
                    st.write("Country: ", country_data.get('name'))
                else:
                    st.write("Country data not available.")
            else:
                st.write("Country data not available.")

            st.write("Followers: ", player_info['followers'])
            st.write("Status: ", player_info['status'])
            st.write("Joined Chess.com: ", datetime.datetime.fromtimestamp(player_info['joined']).strftime('%Y-%m-%d'))
            st.write("Last Online: ", datetime.datetime.fromtimestamp(player_info['last_online']).strftime('%Y-%m-%d %H:%M:%S'))
        else:
            st.write("Player not found or error fetching data.")

    @classmethod
    def display_player_stats(cls, player_name):
        """
        Fetches and displays player statistics in a Streamlit app.

        :param player_name: The player's username on Chess.com.
        """
        st.subheader("Player Statistics")

        player_stats = cls.fetch_player_stats(player_name)

        if player_stats:
            # Display the statistics (customize this based on the API response structure)
            st.write("Rapid Rating: ", player_stats.get('chess_rapid', {}).get('last', {}).get('rating'))
            st.write("Blitz Rating: ", player_stats.get('chess_blitz', {}).get('last', {}).get('rating'))
            st.write("Bullet Rating: ", player_stats.get('chess_bullet', {}).get('last', {}).get('rating'))
            # Display the best statistics
            st.write("Best Rapid Rating: ", player_stats.get('chess_rapid', {}).get('best', {}).get('rating'))
            st.write("Best Blitz Rating: ", player_stats.get('chess_blitz', {}).get('best', {}).get('rating'))
            st.write("Best Bullet Rating: ", player_stats.get('chess_bullet', {}).get('best', {}).get('rating'))

        else:
            st.write("Player statistics not found or error fetching data.")

    @classmethod
    def fetch_game_archives(cls, player_name):
        """
        Fetches and returns the game archives (list of available months) for a player from the Chess.com API.

        :param player_name: The player's username on Chess.com.
        :return: A list of available game archives (months) for the player.
        """
        url = f"{cls.BASE_URL}/player/{player_name}/games/archives"

        try:
            # Include the user-agent header in the request
            response = requests.get(url, headers=cls.headers)
            response.raise_for_status()
            game_archives = response.json().get('archives', [])
            return game_archives
        except requests.RequestException as e:
            cls._log_error(f"Error fetching game archives from URL {url}: {e}")
            return []

# Usage examples:
df = ChessAPI.fetch_games(player_name="DanielNaroditsky", year=2014, month='03')
print(df.columns)
# ChessAPI.fetch_games(url="https://example.com/api/endpoint")
# ChessAPI.display_player_info(player_name="example_player")
# ChessAPI.display_player_stats(player_name="example_player")
# ChessAPI.fetch_game_archives(player_name="example_player")
