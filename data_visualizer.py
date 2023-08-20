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

    def _set_aesthetics(self, ax, title, xlabel, ylabel):
        """
        Set aesthetics for the plots.
        """
        ax.set_title(title, fontsize=18, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=14)
        ax.set_ylabel(ylabel, fontsize=14)
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)

    def print_kde(self, x, hue, fill=True, xlabel=None, ylabel=None):
        """
        Plot univariate distributions using kernel density estimation.
        """
        fig = Figure()
        ax = fig.subplots()

        # Normalize the KDE to represent percentages
        sns.kdeplot(data=self.dataframe, x=x, hue=hue, fill=fill, ax=ax, common_norm=True)

        self._set_aesthetics(ax, "Chess Opponent Ratings Distribution", xlabel, ylabel)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        st.pyplot(fig)
    
    def print_histogram(self, x, hue, xlabel=None, ylabel=None, bins=10):
        """
        Plot a histogram of the data.
        """
        fig = Figure()
        ax = fig.subplots()
        sns.histplot(data=self.dataframe, x=x, hue=hue, bins=bins, ax=ax)
        self._set_aesthetics(ax, "Histogram", xlabel, ylabel)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        st.pyplot(fig)


    def print_distribution(self, column, xlabel=None, ylabel=None, chart_type='pie'):
        """
        Show the counts of observations in each categorical bin using either bars (default) or a pie chart.
        """
        if chart_type == 'countplot':
            fig = Figure()
            ax = fig.subplots()
            sns.countplot(data=self.dataframe, x=column, order=self.dataframe[column].value_counts().index, ax=ax)
            self._set_aesthetics(ax, "Distribution of " + column, xlabel, ylabel)
            ax.set_ylabel(ylabel)
            ax.set_xlabel(xlabel)
            st.pyplot(fig)
        elif chart_type == 'pie':
            counts = self.dataframe[column].value_counts()
            labels = counts.index
            sizes = counts.values

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            plt.title("Distribution of " + column)
            st.pyplot(fig)
        else:
            st.write("Invalid chart_type. Supported types: 'countplot', 'pie'")

    def print_performance(self, data, xlabel=None, ylabel=None):
        """
        Plot a line plot for ratings over time.
        """
        fig = Figure()
        ax = fig.subplots()
        sns.lineplot(data=self.dataframe, x='end_time', y=f"{self.player_name}'s rating", ax=ax, hue = 'time_class')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        self._set_aesthetics(ax, f"{self.player_name}'s Rating Over Time", "Date", "Rating")        
        ax.legend()
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
