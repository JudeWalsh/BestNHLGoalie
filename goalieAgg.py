import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

class GoalieAgg:

    def __init__(self, base_url='https://api-web.nhle.com/', stats_url='https://api.nhle.com/stats/rest'):
        """

        base_url: Base URL for main NHL API
        stats_url: Base URL for stats NHL API
        """
        self.base_url = base_url
        self.stats_url = stats_url
        self.curr_season_id = 0
        self.current_season = self.get_current_season()
        self.ID_dict = {}
        self.create_ID_dict()

    """
    Ping the NHL API for the current season
    """

    def get_current_season(self):
        url = self.base_url + 'v1/season'
        response = requests.get(url)
        if response.status_code == 200:
            season = response.json()
            self.curr_season_id = season[-1]
            curr_season = int(str(season[-1])[:4])
            return curr_season
        else:
            return [response.status_code, response.text]

    def create_ID_dict(self):
        '''
        Populates the ID dictionary
        Maps player names to their unique identifier
        '''

        # Iterate over the range of pages (assuming there are 8 pages)
        url = self.stats_url + f"/en/skater/goalie?limit=-1&start=0&sort=playerId&cayenneExp=seasonId={self.curr_season_id}%20and%20gameTypeId=2"

        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            stats = data.get('data', [])  # Get the 'data' list from the response

            # Use a list comprehension to create a list of (skater_full_name, player_id) tuples
            skater_id_pairs = [(player_data.get('playerId'), player_data.get('skaterFullName')) for player_data in
                               stats]

            # Update the id_dict with the pairs from the current page
            self.ID_dict.update(skater_id_pairs)
        else:
            # Print an error message if the request was not successful
            return [response.status_code, response.text]

    def get_everything(self):

        reports = [
            "summary",
            "advanced",
            "bios",
            "savesByStrength",
            "startedVsRelieved"
        ]

        all_data = []

        for report in reports:
            url = f"https://api.nhle.com/stats/rest/en/goalie/{report}?isAggregate=true&limit=-1&start=0&sort=playerId&cayenneExp=seasonId%3E=19551956%20and%20seasonId%3C=20232024%20and%20gameTypeId=2"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', [])
                all_data.extend(stats)

        if not all_data:
            return pd.DataFrame()  # Return an empty DataFrame if no data is retrieved

            # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(all_data)

        # Drop duplicate columns resulting from concatenation
        df = df.loc[:, ~df.columns.duplicated()]

        # Set playerId as index if needed
        df.set_index('playerId', inplace=True)

        # Group by playerId and concatenate the rows
        grouped_df = df.groupby('playerId').apply(lambda x: x.ffill().bfill().iloc[0])

        columns_to_drop = ["goals", "lastName", "birthCity", "birthCountryCode", "birthDate", "birthStateProvince",
                           "draftOverall", "draftRound", "draftYear", "height", "nationalityCode", "weight"]
        grouped_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

        grouped_df = grouped_df.sort_values(by="gamesStarted", ascending=False)

        return grouped_df.reset_index()

obj = GoalieAgg()
goalie_df = obj.get_everything()

with sqlite3.connect('goalies.db') as conn:
    goalie_df.to_sql('goalies', conn, if_exists='replace', index=False)
    goalie_df.to_csv('goalieAgg.csv')

# Connect to the database
conn = sqlite3.connect('goalies.db')

'''
query for all goalies with at least 300 games started
sort by:
wins
shutouts
save percentage
'''

sort = input("Sort by: ")

# Query the database and load the result into a DataFrame
df = pd.read_sql_query(f"SELECT * FROM goalies WHERE gamesStarted >= 300 ORDER BY {sort} DESC", conn)

df.to_csv(f"sorted_by_{sort}.csv", index=False)

brodeur = df.index[df['goalieFullName'] == 'Martin Brodeur'].tolist()
gump = df.index[df['goalieFullName'] == 'Gump Worsley'].tolist()
roy = df.index[df['goalieFullName'] == 'Patrick Roy'].tolist()
hasek = df.index[df['goalieFullName'] == 'Dominik Hasek'].tolist()
osgood = df.index[df['goalieFullName'] == 'Chris Osgood'].tolist()
hank = df.index[df['goalieFullName'] == 'Henrik Lundqvist'].tolist()

print("Martin Brodeur ranks: ", brodeur)
print("Gump Worsley ranks: ", gump)
print("Patrick Roy ranks: ", roy)
print("Dominik Hasek ranks: ", hasek)
print("Chris Osgood ranks: ", osgood)
print("Henrik Lundqvist ranks: ", hank)

# Select the top 5 rows after sorting
top_5 = df.head(5)

# Create a horizontal bar chart
plt.figure(figsize=(20, 6))
bars = plt.barh(top_5['goalieFullName'], top_5[sort], color='skyblue')
plt.xlabel(sort)
plt.title(f"Top 5 Goalies by {sort.capitalize()}")
plt.gca().invert_yaxis()  # Invert y-axis to have the highest value at the top

# Add value labels at the end of each bar
for bar in bars:
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f'{bar.get_width():.4f}',  # Format the value to 2 decimal places
        va='center'
    )

# plt.xlim(left=0.918, right=0.925)

plt.show()

print("Amount of goalies: ", len(df))

# Close the connection
conn.close()

# Return the DataFrame
# print(df)