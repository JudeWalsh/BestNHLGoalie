import requests
import pandas as pd
import json

# Load the CSV file into a DataFrame
df = pd.read_csv('goalieAgg.csv')


# Define the calculations for the new columns
def get_trophy_count(player_id, trophy_name):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    response = requests.get(url)
    data = response.json()
    print(data['firstName']['default'], data['lastName']['default'])

    try:
        for trophy in data['awards']:
            if trophy['trophy']['default'] == trophy_name:
                return len(trophy['seasons'])
    except KeyError:
        return 0

    return 0

def get_all_stars(playerName):
    return 0

def vezinas(player_id):
    return get_trophy_count(player_id, "Vezina Trophy")

def connsmythes(player_id):
    return get_trophy_count(player_id, "Conn Smythe Trophy")

def stanleycups(player_id):
    return get_trophy_count(player_id, "Stanley Cup")

def jennings(player_id):
    return get_trophy_count(player_id, 'William M. Jennings Trophy')


def allstardict():
    df = pd.read_csv('GoalieAllStars.csv')

    # Select the first two columns
    subset_df = df[['Name', 'GP']]

    # Update the dictionary
    name_gp_dict = subset_df.set_index('Name')['GP'].to_dict()

    return name_gp_dict

allStarDict = allstardict()

def allstars(playerName):
    try:
        return allStarDict[playerName]
    except KeyError:
        return 0


# Add the new columns to the DataFrame using the defined functions
# df['Vezina Trophies'] = df['playerId'].apply(vezinas)
# df['Stanley Cups'] = df['playerId'].apply(stanleycups)
# df['Conn Smythe Trophies'] = df['playerId'].apply(connsmythes)
# df['William M. Jennings Trophies'] = df['playerId'].apply(jennings)
df['All Stars'] = df['goalieFullName'].apply(allstars)

df.to_csv('accolades.csv', index=False)
