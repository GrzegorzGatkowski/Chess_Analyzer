import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.figure import Figure

class ChessDataVisualizer:
    def __init__(self, dataframe, player_name):
        self.dataframe = dataframe
        self.player_name = player_name

        # Set custom Seaborn style
        sns.set_theme(style="whitegrid")
        sns.set_palette("pastel")

    def _set_aesthetics(self, title, xlabel, ylabel):
        """
        Set aesthetics for the plots.
        """
        plt.title(title, fontsize=18, fontweight="bold")
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

    def print_kde(self, x, hue, fill=True, xlabel=None, ylabel=None):
        """
        Plot univariate distributions using kernel density estimation.
        """
        fig = Figure()
        ax = fig.subplots()
        sns.kdeplot(data=self.dataframe, x=x, hue=hue, fill=fill, ax=ax)
        self._set_aesthetics("Kernel Density Estimation", xlabel, ylabel)
        st.pyplot(fig)

    def print_distribution(self, column, xlabel=None, ylabel=None):
        """
        Show the counts of observations in each categorical bin using bars.
        """
        fig = Figure()
        ax = fig.subplots()
        sns.countplot(data=self.dataframe, y=column, order=self.dataframe[column].value_counts().index, ax=ax)
        self._set_aesthetics("Distribution of " + column, xlabel, ylabel)
        st.pyplot(fig)

    def print_performance(self, data, xlabel=None, ylabel=None):
        """
        Show performance over time using a line plot.
        """
        fig = Figure()
        ax = fig.subplots()
        sns.lineplot(data=data, ax=ax)
        self._set_aesthetics("Performance Over Time", xlabel, ylabel)
        st.pyplot(fig)

    def print_rating(self, data_series):
        """
        Print information about opponent's summary statistics.
        """
        avg_opp_rating = data_series.mean().round()
        max_opp_rating = data_series.max()
        st.markdown(
            f"**Average Opponent Rating:** {avg_opp_rating}\n"
            f"**Highest Opponent Rating:** {max_opp_rating}"
        )

