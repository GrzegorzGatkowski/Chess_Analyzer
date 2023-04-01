import requests
import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib.figure import Figure


### Helper Methods ###

def get_archives(player_name):
    """
    Get list of URLs for monthly archives games for player.
    """
    try:
        response = requests.get(f"https://api.chess.com/pub/player/{player_name}/games/archives")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        archives = response.json()
        return archives["archives"]
    except (KeyError, TypeError, ValueError):
        return None


def get_years_list(player_name):
    try:
        response = requests.get(f"https://api.chess.com/pub/player/{player_name}/games/archives")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        year = response.json()["archives"][0][-7:-3]
        first_year = int(year)
        list_year = [*range(first_year, 2023)]
        str_list = [str(x) for x in list_year]
        return str_list
    except (KeyError, TypeError, ValueError):
        return None  


def get_games(monthly_games, year):
    """
    Get Dataframe with all games by year.
    """
    all_months = pd.DataFrame()
    for url in monthly_games:
        if url[-7:-3] == year:
            response = requests.get(url).json()['games']
            all_months = pd.concat([all_months, pd.json_normalize(response, max_level=1)])
    return all_months


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
