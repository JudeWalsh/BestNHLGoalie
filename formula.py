import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Load the CSV file into a DataFrame
full_df = pd.read_csv('formula.csv')

# Filter the DataFrame for goalies with at least 300 games started
df = full_df[full_df['gamesStarted'] >= 300]
print(df.shape)

# Define the columns for max and min calculations
columns_for_max = ['gamesStarted', 'shutouts', 'wins', 'qualityStart', 'qualityStartsPct', 'gamesRelievedWins',
                   'Vezina Trophies', 'Stanley Cups', 'Conn Smythe Trophies', 'William M. Jennings Trophies', 'All Stars',
                   'goalsAgainst', 'goalsAgainstAverage']
# columns_for_min = ['goalsAgainst', 'goalsAgainstAverage']

# Create a dictionary of extreme values (max and min)
extreme_values = {col: df[col].max() for col in columns_for_max}
# extreme_values.update({col: df[col].min() for col in columns_for_min})

def goalieScore(row, extreme_values):
    # Example calculation using multiple columns
    vezinas = row['Vezina Trophies']
    stanley_cups = row['Stanley Cups']
    conn_smythes = row['Conn Smythe Trophies']
    jennings = row['William M. Jennings Trophies']
    allStars = row['All Stars']

    # Your custom calculation
    accolade_score = 0
    stats_score = 0

    for i in extreme_values:
        if i in ["goalsAgainst", "goalsAgainstAverage"]:
            stats_score += (extreme_values[i] - row[i]) / extreme_values[i]
        elif i in ['gamesStarted', 'shutouts', 'wins', 'qualityStart', 'qualityStartsPct', 'gamesRelievedWins']:
            stats_score += row[i] / extreme_values[i]
        elif i in ['Vezina Trophies', 'Stanley Cups', 'Conn Smythe Trophies', 'William M. Jennings Trophies', 'All Stars']:
            if i == 'Vezina Trophies':
                accolade_score += 0.4 * (vezinas / extreme_values[i])
            elif i == 'Stanley Cups':
                accolade_score += 0.3 * (stanley_cups / extreme_values[i])
            elif i == 'Conn Smythe Trophies':
                accolade_score += 0.2 * (conn_smythes / extreme_values[i])
            elif i == 'William M. Jennings Trophies':
                accolade_score += 0.1 * (jennings / extreme_values[i])
            elif i == 'All Stars':
                accolade_score += 0.05 * (allStars / extreme_values[i])

    return (accolade_score + 1) * stats_score


# Add the new column to the DataFrame using the custom function
df['Score'] = df.apply(goalieScore, axis=1, extreme_values=extreme_values)

# Apply log transformation to the 'Score' column
df['Log_Score'] = np.log1p(df['Score'])

sorted_df = df.sort_values(by='Log_Score', ascending=False)
print(sorted_df[['goalieFullName', 'Log_Score']].head(5))

sorted_df = df.sort_values(by='Score', ascending=False)
print(sorted_df[['goalieFullName', 'Score']].head(5))

# Plot a histogram of the transformed 'Score' column
plt.figure(figsize=(10, 6))
plt.hist(df['Log_Score'], bins=15, color='blue', edgecolor='black')
plt.title('Histogram of Log-Transformed Goalie Scores')
plt.xlabel('Log-Transformed Score')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

score_series = df['Score']

# Calculate summary statistics
average = score_series.mean()
standard_deviation = score_series.std()
variance = score_series.var()
median = score_series.median()
minimum = score_series.min()
maximum = score_series.max()

# Print summary statistics
print(f"Average: {average}")
print(f"Standard Deviation: {standard_deviation}")
print(f"Variance: {variance}")
print(f"Median: {median}")
print(f"Minimum: {minimum}")
print(f"Maximum: {maximum}")

# Save the updated DataFrame to a CSV file
sorted_df.to_csv('updated_formula.csv', index=False)
