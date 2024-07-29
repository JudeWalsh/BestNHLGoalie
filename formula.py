import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
full_df = pd.read_csv('formula.csv')

# Filter the DataFrame for goalies with at least 300 games started
df = full_df[full_df['gamesStarted'] >= 300]
print(df.shape)

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
    accolade_score = (conn_smythes * 0.75) + (stanley_cups * 0.5) + (vezinas * 0.25) + (jennings * 0.125)
    stats_score = 0

    for i in extreme_values:
        if i in ["goalsAgainst", "goalsAgainstAverage"]:
            stats_score += extreme_values[i] / row[i]
        else:
            stats_score += row[i] / extreme_values[i]

    return accolade_score + stats_score


# Add the new column to the DataFrame using the custom function
df['Score'] = df.apply(goalieScore, axis=1, extreme_values=extreme_values)

# Apply log transformation to the 'Score' column
df['Log_Score'] = np.log1p(df['Score'])

sorted_df = df.sort_values(by='Score', ascending=False)
print(sorted_df.head(5))

sorted_df = df.sort_values(by='Log_Score', ascending=False)
print(sorted_df.head(5))

# Plot a histogram of the transformed 'Score' column
plt.figure(figsize=(10, 6))
plt.hist(df['Log_Score'], bins=30, color='blue', edgecolor='black')
plt.title('Histogram of Log-Transformed Goalie Scores')
plt.xlabel('Log-Transformed Score')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Save the updated DataFrame to a CSV file
df.to_csv('updated_formula.csv', index=False)
