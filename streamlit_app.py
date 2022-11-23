import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
import seaborn as sns
import streamlit as st
import numpy as np
from handlers import get_archives, get_games, print_kde, print_rating, get_years_list, print_performance, print_distribution


st.set_page_config(layout="wide")

_lock = RendererAgg.lock

sns.set_style("darkgrid")
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 0.6, 0.1)
)

row0_1.title("Analyzing Chess.com profile.")

with row0_2:
    st.write("")

row0_2.subheader(
    "Streamlit App by [Grzegorz Gątkowski](https://www.linkedin.com/in/grzegorz-g-811727125/)"
)

row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

with row1_1:
    st.markdown(
        "Hey there! Welcome to Chess Analysis App. This app analyzes data about your chess.com account, and looking at the distribution of the opponents rating."
    )
    st.markdown(
        "**To begin, please enter the [chess.com](https://www.chess.com/) username (or just use mine!).** 👇"
    )

row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))
with row2_1:
    default_username = st.selectbox(
        "Select one and press 'ENTER'",
        (
            "grzegorzgatkowski",
            "Hikaru",
            "MagnusCarlsen",
            "DanielNaroditsky"
        ),
    )
    st.markdown("**or**")
    user_input = st.text_input(
        "Input your own Name and press 'ENTER'"
    )
    if not user_input:
        user_input = f"{default_username}"
    
    default_year = st.selectbox(
        "Select one year and press 'ENTER'",
        (get_years_list(user_input)          
        ),
    )
    
player = user_input

line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))

with line1_1:
    st.header("Analyzing the opponents ratings distrubution of: **{}**".format(player))


### Data Import ###
data = get_archives(player_name = player)
all_months = get_games(data, default_year)

### Data Cleaning ###
all_months.drop([ 'url', 'pgn', 'tcn', 'uuid', 'initial_setup', 'fen', 'white.@id', 'white.uuid', 'black.@id', 'black.uuid'], axis = 1, inplace = True)
all_months[player+"'s rating"] = np.where(all_months['white.username']==player,all_months['white.rating'],all_months['black.rating'])
all_months["opponent's rating"] = np.where(all_months['white.username']!=player,all_months['white.rating'],all_months['black.rating'])
if 'accuracies.white' in all_months:
    all_months[player+" accuracy"] = np.where(all_months['white.username']==player,all_months['accuracies.white'],all_months['accuracies.black'])
    all_months["Opponent accuracy"] = np.where(all_months['white.username']!=player,all_months['accuracies.white'],all_months['accuracies.black'])
    has_accuracy = True
else:
    has_accuracy = False

all_months.end_time = pd.to_datetime(all_months.end_time,unit='s')
has_records = any(all_months['end_time'])
st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row3_1, _lock:
    st.subheader("Overall distribution")
    if has_records:
        print_kde(DataFrame = all_months, x = "opponent's rating", hue = 'time_class', fill = True, xlabel = 'Rating', ylabel = 'Density')
        print_rating(all_months["opponent's rating"])
    else:
        st.markdown("We do not have information to find out about your games.")

with row3_2, _lock:
    st.subheader("Games played by time control")
    if has_records:
        print_distribution(DataFrame=all_months, column='time_class')
    else:
        st.markdown("We do not have information to find out about your games.")
    
    st.markdown(
        "It looks like you've played a grand total of **{}** games, including:".format(all_months.end_time.count())
        )
    st.markdown(
        "- **{}** blitz games,".format(all_months[all_months.time_class == 'blitz'].shape[0])
        )
    st.markdown(
        "- **{}** rapid game,".format(all_months[all_months.time_class == 'rapid'].shape[0])
        )
    st.markdown(
        "- **{}** bullet game,".format(all_months[all_months.time_class == 'bullet'].shape[0])
        )
    st.markdown(
        "- **{}** daily games.".format(all_months[all_months.time_class == 'daily'].shape[0])
        )

    st.write("")
row4_1, row4_space2 = st.columns(
    (2,0.1)
)


with row4_1, _lock:
    st.subheader("Performance")
    df = all_months.groupby('time_class').resample('3D', on = 'end_time')[[player+"'s rating"]].mean().reset_index()
    df_wide = df.pivot("end_time", "time_class", player+"'s rating")
    df_wide = df_wide.fillna(method="bfill")
    df_wide = df_wide.fillna(method="ffill")
    if has_records:
        print_performance(data=df_wide, xlabel = 'Time', ylabel = 'Rating') 




    st.write("")
row5_1, row5_space2 = st.columns(
    (2,0.1)
)


with row5_1, _lock:
    st.subheader("Accuracy")
    if has_accuracy:
        fig = sns.lmplot(data=all_months, x = "opponent's rating", y = player+" accuracy", col = 'time_class', scatter_kws={"color":"indigo","alpha":0.2,"s":10}, facet_kws=dict(sharex=False, sharey=False), col_wrap = 2)

    else:
        st.markdown("You did not played any games with accuracy analysis.")
