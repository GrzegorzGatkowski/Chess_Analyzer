# Chess Analysis App

The Chess Analysis App is a Streamlit web application designed to analyze and visualize data from chess.com user profiles. It provides insights into a player's game performance, opponents' ratings distribution, game types, and more.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Chess Analysis App is a Python-based web application built using Streamlit, Seaborn, and Matplotlib. It allows users to input a chess.com username (or select from default usernames) and obtain detailed analytics about their game history.

## Features

- **User-Friendly Interface**: The app provides a simple and intuitive user interface, making it easy for anyone to access chess data insights.

- **Default Usernames**: Users can choose from a list of default usernames or input their own to fetch data.

- **Game Analysis**: Analyze game data for a selected year and month, including information about wins, losses, and draws.

- **Opponents' Ratings Distribution**: Visualize the distribution of opponents' ratings for the selected time period.

- **Game Type Distribution**: Explore the distribution of games by time control (blitz, rapid, bullet).

- **Performance Analysis**: Get insights into a player's performance based on their opponent's ratings.

- **Accuracy Analysis**: Visualize accuracy based on opponent's ratings for different game types.

## Getting Started

To get started with the Chess Analysis App, follow these steps:

1. Clone the repository to your local machine:
   ```shell
   git clone https://github.com/your-username/chess-analysis-app.git
2. Navigate to the project directory:
   ```shell
   cd chess-analysis-app
3. Install the required Python packages:
   ```shell
   pip install -r requirements.txt
4. Run the Streamlit app:
   ```shell
   streamlit run main.py
5. Open your web browser and access the app at http://localhost:8501.

## Usage
1. Upon launching the app, you will see an introduction and instructions on how to use it.

2. You can either select a default username from the dropdown list or input your own chess.com username.

3. Choose the year and month you want to analyze (data availability may vary).

4. The app will fetch and display various analytics and visualizations based on the selected criteria, including opponents' ratings distribution, game type distribution, performance analysis, and accuracy analysis.

5. Explore the insights and gain a deeper understanding of your chess game history.

## Contributing
Contributions to the Chess Analysis App are welcome! If you have ideas for improvements, bug fixes, or new features, please feel free to open an issue or submit a pull request. For major changes, please discuss your ideas in the issue tracker before making changes.

## License
See the LICENSE file for details.