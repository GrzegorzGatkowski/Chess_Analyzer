import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
import warnings
from data_cleaner import ChessDataCleaner
from data_visualizer import ChessDataVisualizer
from fetch_games import ChessAPI
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Analyzing Chess.com Profile", page_icon=":chess_pawn:", layout="wide")
SEABORN_STYLE = "whitegrid"
DEFAULT_USERNAMES = [
    "DanielNaroditsky",
    "Hikaru",
    "GothamChess",
    "nihalsarin",
    "Polish_fighter3000",
]


st.title(" :chess_pawn: Chess.com profile stats")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

def main():
    
    # Create columns for the main content
    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((0.1, 2, 0.2, 0.6, 0.1))

    # Title of the app
    row0_1.title("Analyzing Chess.com Profile")

    # Subheader with app creator's information
    with row0_2:
        st.write("")

    row0_2.subheader("Streamlit App by [Grzegorz Gątkowski](https://www.linkedin.com/in/grzegorzgatkowski/)")

    # Create columns for the main content
    row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

    # Introduction and input instructions
    with row1_1:
        st.markdown(
            "Hey there! Welcome to the Chess Analysis App. This app analyzes data about your chess.com account and looks at the distribution of the opponents' ratings."
        )
        st.markdown(
            "**To begin, please enter the [chess.com](https://www.chess.com/) username (or use one of the default usernames).** 👇"
        )

    # Create columns for user input
    row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))

    # Default usernames and user input field
    default_username = st.selectbox("Select a default username", DEFAULT_USERNAMES)
    st.markdown("**or**")
    user_input = st.text_input("Input your own username")

    # Fetch player data and date-related variables
    if not user_input:
        player_name = default_username
    else:
        player_name = user_input

    player_info = ChessAPI.fetch_player_data(player_name)
    joined_date = datetime.datetime.fromtimestamp(player_info['joined'])
    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    year_range = list(range(current_year, joined_date.year - 1, -1))
    col1, col2 = st.columns((2))
    with col1:
        date1 = st.date_input("Start Date", min_value=joined_date, max_value=current_date)
    with col2:
        date1 = st.date_input("End Date", min_value=joined_date, max_value=current_date)
    year = st.selectbox("Select a year", year_range)
    if year == current_year:
        month_range = ["{:02d}".format(i) for i in range(current_month, 0, -1)]
    else:
        # Allow all months if the joined year is not the current year
        month_range = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    month = st.selectbox("Select a month", month_range)

if __name__ == "__main__":
    main()
    