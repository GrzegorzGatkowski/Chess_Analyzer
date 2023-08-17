import requests
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib.figure import Figure


### Helper Methods ###

def get_archives(player_name):
    """
    Fetches and returns a list of URLs for monthly archives of games for a given player from Chess.com API.
    
    :param player_name: The username of the player.
    :return: A list of URLs for monthly archives.
    """
    base_url = f"https://api.chess.com/pub/player/{player_name}/games/archives"
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        archives_urls = data.get("archives", [])
        return archives_urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching archives for player {player_name}: {e}")
        return []
    except ValueError as ve:
        print(f"Error parsing JSON response: {ve}")
        return []


def get_years_list(player_name):
    """
    Fetches a list of years from a player's game archives on Chess.com.
    
    :param player_name: The username of the player.
    :return: A list of years as strings, or None if an error occurs.
    """
    try:
        response = requests.get(f"https://api.chess.com/pub/player/{player_name}/games/archives")
        response.raise_for_status()

        if response.status_code == 200:
            try:
                year = response.json()["archives"][0][-7:-3]
                first_year = int(year)
                list_year = [str(x) for x in range(first_year, 2023)]
                return list_year
            except (KeyError, TypeError, ValueError):
                return None
    except requests.RequestException:
        return None


def get_games(monthly_games, year):
    """
    Fetches and returns a DataFrame containing all games for a given year from a list of monthly game URLs.
    
    :param monthly_games: List of URLs for monthly game archives.
    :param year: The year for which to filter the games.
    :return: A pandas DataFrame containing the games for the specified year.
    """
    all_games = pd.DataFrame()
    
    for url in monthly_games:
        if url[-7:-3] == year:
            try:
                response = requests.get(url)
                response.raise_for_status()
                games_data = response.json().get('games', [])
                
                if games_data:
                    month_df = pd.json_normalize(games_data, max_level=1)
                    all_games = pd.concat([all_games, month_df], ignore_index=True)
            except requests.RequestException as e:
                print(f"Error fetching games from URL {url}: {e}")
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error processing games data from URL {url}: {e}")
    
    return all_games

def print_kde(DataFrame, x, hue, fill=True, xlabel=None, ylabel=None):
    """
    Plot univariate distributions of opponents rating using kernel density estimation.
    """
    fig = Figure()
    ax = fig.subplots()
    sns.kdeplot(data=DataFrame, x=x, hue=hue, fill=fill, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)


def print_distribution(DataFrame, column, xlabel=None, ylabel=None):
    """
    Show the counts of observations in each categorical bin using bars.
    """        
    fig = Figure()
    ax = fig.subplots()
    sns.countplot(data=DataFrame, y=column, order=DataFrame[column].value_counts().index, palette='pastel', ax=ax)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    st.pyplot(fig)


def print_performance(data, xlabel=None, ylabel=None):
    """
    Show the counts of observations in each categorical bin using bars.
    """ 
    fig = Figure()
    ax = fig.subplots()
    sns.lineplot(data, ax=ax, dashes=False, palette='pastel')
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    st.pyplot(fig) 


def print_rating(DataSeries):
    """
    Printing informations about opponents summary statistics.
    """
    avg_opp_rating = DataSeries.mean().round()
    max_opp_rating = DataSeries.max()
    st.markdown(
        '''Average opponent rating: **{}**.  
        The highest opponent rating: **{}**.'''.format(
            avg_opp_rating,
            max_opp_rating,
            unsafe_allow_html=True
        )
    )
