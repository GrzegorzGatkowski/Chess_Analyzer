import datetime
import streamlit as st
import seaborn as sns
from matplotlib.backends.backend_agg import RendererAgg
from data_cleaner import ChessDataCleaner
from data_visualizer import ChessDataVisualizer
from fetch_games import ChessAPI

# Constants
SEABORN_STYLE = "whitegrid"
DEFAULT_USERNAMES = [
    "DanielNaroditsky",
    "Hikaru",
    "GothamChess",
    "nihalsarin",
    "Polish_fighter3000",
]
PAGE_TITLE = "Chess Analysis"


# Use underscores for variable naming for readability
_lock = RendererAgg.lock

# Set seaborn style
sns.set_style(SEABORN_STYLE)

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

    year = st.selectbox("Select a year", year_range)
    if year == current_year:
        month_range = ["{:02d}".format(i) for i in range(current_month, 0, -1)]
    else:
        # Allow all months if the joined year is not the current year
        month_range = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    month = st.selectbox("Select a month", month_range)

    # Create columns for header
    line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))

    with line1_1:
        st.header("Analyzing the Opponents' Ratings Distribution of: **{}**".format(player_name))

    # Fetch player's game data for the selected year and month
    df = ChessAPI.fetch_games(player_name, year, month)

    # Check if data is available
    if not df.empty:
        data_available = True
        cleaner = ChessDataCleaner(df, player_name)
        cleaned_data = cleaner.clean_data()

        # Create an instance of ChessDataVisualizer
        visualizer = ChessDataVisualizer(cleaned_data, player_name)

        st.write("")
        
        row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns((0.1, 1, 0.1, 1, 0.1))
        
    else:
        data_available = False

    # Create columns for the charts in the main content area
    with row3_1, _lock:
        ChessAPI.display_player_info(player_name)
        st.subheader("Overall Distribution")

        if data_available:
            # Visualize Win-Loss Distribution
            visualizer.print_kde(x="opponent's rating", hue='time_class', xlabel = 'Rating', ylabel = 'Density')
        else:
            st.write("No data available for the selected month. Please choose another month.")

    with row3_2, _lock:
        ChessAPI.display_player_stats(player_name)
        st.subheader("Games by time control")
        if data_available:
            visualizer.print_distribution(column='time_class', xlabel = "Game type", ylabel = 'Count')
        else:
            st.markdown("We do not have information to find out about your games.")
    # Create columns for header
    line2_spacer1, line2_1, line2_spacer2 = st.columns((0.1, 3.2, 0.1))

    with line2_1:
        total_games = cleaned_data.end_time.count()
        blitz_games = cleaned_data[cleaned_data.time_class == 'blitz'].shape[0]
        rapid_games = cleaned_data[cleaned_data.time_class == 'rapid'].shape[0]
        bullet_games = cleaned_data[cleaned_data.time_class == 'bullet'].shape[0]

        st.header(f"Games: **{player_name}**")
        st.markdown(f"It looks like {player_name} played a grand total of **{total_games}** games in {year}-{month}, including:")
        st.markdown(f"- **{blitz_games}** blitz games,")
        st.markdown(f"- **{rapid_games}** rapid game,")
        st.markdown(f"- **{bullet_games}** bullet game,")
    
    row4_1, row4_space1 = st.columns((2,0.1))

    with row4_1, _lock:
        st.subheader("Performance")
        visualizer.print_performance(data = cleaned_data)
    
    row5_1, row5_space1 = st.columns((2,0.1))

    with row5_1, _lock:
        st.subheader("Accuracy")
        fig = sns.lmplot(data=cleaned_data, x = "opponent's rating", y = player_name+" accuracy", col = 'time_class', scatter_kws={"color":"indigo","alpha":0.2,"s":10}, facet_kws=dict(sharex=False, sharey=False), col_wrap = 2)
        st.pyplot(fig)       

if __name__ == "__main__":
    main()
