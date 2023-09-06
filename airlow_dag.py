from fetch_games import ChessAPI
from data_cleaner import ChessDataCleaner
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sqlite3

DEFAULT_USERNAMES = [
    "DanielNaroditsky",
    "Hikaru",
    "GothamChess",
    "nihalsarin",
    "Polish_fighter3000",
]

# Define default_args and DAG configuration
default_args = {
    'owner': 'Grzegorz',
    'start_date': datetime(2023, 9, 6),
    'retries': 1,
}

dag = DAG(
    'chess_data_etl',
    default_args=default_args,
    schedule_interval=None,  # Set your desired schedule interval here
    catchup=False,
)

def fetch_and_save_chess_data(player_name, url=None):
    # Fetch data using ChessAPI class
    df = ChessAPI.fetch_games(player_name=player_name, url=url)
    cleaner = ChessDataCleaner(df, player_name)
    cleaned_data = cleaner.clean_data()

    # Save data to SQLite
    if cleaned_data is not None:
        conn = sqlite3.connect('data/chess.db')
        table_name = player_name

        # Use 'replace' or 'append' based on your requirement
        if_exists_option = 'append'

        cleaned_data.to_sql(table_name, conn, index=False, if_exists=if_exists_option)
        conn.close()
    else:
        print(f"No data retrieved from ChessAPI for {player_name}.")

def fetch_and_save_chess_data_for_all_players():
    for player_name in DEFAULT_USERNAMES:
        archive_url = ChessAPI.fetch_game_archives(player_name)
        for archive in archive_url:
            fetch_and_save_chess_data(player_name=player_name, url=archive)

fetch_chess_data_task = PythonOperator(
    task_id='fetch_chess_data',
    python_callable=fetch_and_save_chess_data_for_all_players,
    dag=dag,
)

if __name__ == "__main__":
    fetch_and_save_chess_data_for_all_players()
