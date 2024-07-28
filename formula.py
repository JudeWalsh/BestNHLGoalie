import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
full_df = pd.read_csv('formula.csv')

# Filter the DataFrame for goalies with at least 300 games started
df = full_df[full_df['gamesStarted'] >= 300]

# Define the columns for max and min calculations
columns_for_max = ['gamesStarted', 'shutouts', 'wins', 'qualityStart', 'qualityStartsPct', 'gamesRelievedWins']
columns_for_min = ['goalsAgainst', 'goalsAgainstAverage']

# Create a dictionary of extreme values (max and min)
extreme_values = {col: df[col].max() for col in columns_for_max}
extreme_values.update({col: df[col].min() for col in columns_for_min})

def goalieScore(row, extreme_values):
    # Example calculation using multiple columns
    vezinas = row['Vezina Trophies']
    stanley_cups = row['Stanley Cups']
    conn_smythes = row['Conn Smythe Trophies']
    jennings = row['William M. Jennings Trophies']

    # Your custom calculation
    accolade_score = (conn_smythes * 5) + (stanley_cups * 4) + (vezinas * 3) + (jennings * 2)
    stats_score = 0

    for i in extreme_values:
        if i == "goalsAgainst" or i == "goalsAgainstAverage":
            stats_score += extreme_values[i] / row[i]
        else:
            stats_score += row[i] / extreme_values[i]

    return accolade_score + stats_score


# Add the new column to the DataFrame using the custom function
df['Score'] = df.apply(goalieScore, axis=1, extreme_values=extreme_values)

plt.figure(figsize=(10, 6))
plt.hist(df['Score'], bins=20, color='blue', edgecolor='black')
plt.title('Histogram of Goalie Scores')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

df.to_csv('formula.csv')
