import pandas as pd
import csv
from collections import defaultdict
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings('ignore')

def clean_data(nba):
    # Extract the first four characters of the 'season' column, convert to integer
    nba['season_year'] = nba['season'].str[:4].astype(int)

    # Replace "undrafted" with 0 in the 'draft_year' column
    nba['draft_year'] = nba['draft_year'].replace('Undrafted', 0)
    nba['draft_year'] = nba['draft_year'].astype(int)

    # Filter to extract all drafted rookies
    rookies = nba[nba['draft_year'] == nba['season_year']]

    # Replace negative net_rating values with 0
    rookies['net_rating'] = rookies['net_rating'].apply(lambda x: max(x, 0))

    return rookies

def calc_composite_score(rookies):
    # Ensure all values are numeric, filling NaNs with zero or an appropriate value if necessary
    rookies.fillna(0, inplace=True)  # Or choose a strategy like rookies.fillna(rookies.mean(), inplace=True)

    # Select only the columns to normalize
    numeric_cols = ["pts", "reb", "ast", "net_rating", "ts_pct", "usg_pct"]
    scaler = MinMaxScaler()

    # Normalize the selected columns
    normalized_vals = scaler.fit_transform(rookies[numeric_cols])
    normalized_df = pd.DataFrame(normalized_vals, columns=numeric_cols)

    # Ensure indices align between rookies and normalized_df
    normalized_df.index = rookies.index

    # Create a composite score by averaging the normalized values
    rookies['composite_performance_score'] = normalized_df.mean(axis=1)

def create_adj_list(data):
    # Create a dictionary of lists to store the adjacency list
    adjacency_list = defaultdict(list)

    # Iterate over each row in the data
    for index, row in data.iterrows():
        college = row['college']
        team = row['team_abbreviation']
        player_name = row['player_name']
        score = row["composite_performance_score"]

        # Append the tuple the college's list
        adjacency_list[college].append((team, player_name, score))

    return adjacency_list

def main():
    nba = pd.read_csv("all_seasons.csv")

    # Option 1 Return a list of the most connected colleges - gives insights to the college with highest draft history (tie between MSU/UM)
        # Done
        # Give option to visualize
        # (best team to get drafted from in general)
    # Option 2 For each college - NBA team, check their calculated composite score to give insights on athlete performance
        # Done
        # Give option to visualize
        # (best team to attend for rookie year performance)
    # Option 3 Return a list of colleges that are most historically drafted by an inputed NBA team
        # Give option to visualize
        # (if given a goal team to attend, return colleges that will increase your odds)

    response = 1

    while response:
        # Prompt user for input
        print("""1: Most successful colleges\n2: Determine average NBA rookie performance by college\n3: NBA draft history\n4: Exit\n""")

        # Error checking
        try:
            response = int(input("Please input an option: "))
        # If invalid input
        except ValueError:
            print("\nPlease input a valid input option\n")
        # Catch any other error
        except Exception:
            print("\nAn unexpected error occurred, please try again\n")
        # If input is valid but out of scope
        if response > 4 or response < 0:
            print("\nPlease input a valid input option\n")

        # It is assumed that data is valid from here onwards

        # Clean & prep our data
        rookies = clean_data(nba)
        # Create normalized composite score
        calc_composite_score(rookies)
        # Create network with an adjacency list
        adj_list = create_adj_list(rookies)

        # Valid input resonses below
        if response == 1:
            pass
        elif response == 2:
            pass
        elif response == 3:
            pass
        else:
            print("\nThank You!\n")
            break

if __name__ == "__main__":
    main()