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

def get_node_connections(adjacency_list):
    # Create a dictionary to count connections for colleges only
    college_connection_counts = defaultdict(int)

    # Iterate over each college in the adjacency list
    for college, connections in adjacency_list.items():
        # Count each player connection for the college
        college_connection_counts[college] += len(connections)

    # Sort the colleges by the number of connections in descending order
    sorted_college_connections = sorted(college_connection_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_college_connections

def top_colleges_by_team(adjacency_list, target_team):
    # Dictionary to store the count of players drafted from each college by the target team
    college_counts = defaultdict(int)

    # Iterate through the adjacency list
    for college, players in adjacency_list.items():
        # Iterate through each player's data
        for team, player, composite_score in players:
            # If the team matches the target_team, increment the count for this college
            if team == target_team:
                college_counts[college] += 1

    # Sort the colleges by the number of players drafted by the target team in descending order
    sorted_colleges = sorted(college_counts.items(), key=lambda x: x[1], reverse=True)

    # Return the top three colleges or fewer if less than three exist
    top_three_colleges = sorted_colleges

    return top_three_colleges

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

    while True:
        response = 0
        # Prompt user for input
        print("""\nPlease select an input:\n1: Most successful colleges\n2: Determine average NBA rookie performance by college\n3: NBA draft history\n4: Exit\n""")

        # Error checking
        try:
            response = int(input("Please input an option: "))
        # If invalid input
        except ValueError:
            print("\nPlease input a valid input option\n")
            continue
        # Catch any other error
        except Exception:
            print("\nAn unexpected error occurred, please try again\n")
            continue
        # If input is valid but out of scope
        if response > 4 or response < 0:
            print("\nPlease input a valid input option\n")
            continue

        # It is assumed that data is valid from here onwards

        # Clean & prep our data
        rookies = clean_data(nba)
        # Create normalized composite score
        calc_composite_score(rookies)
        # Create network with an adjacency list
        adj_list = create_adj_list(rookies)

        # Valid input responses below
        if response == 1:
            sorted_nodes_with_connections = get_node_connections(adj_list)
            for node, count in sorted_nodes_with_connections:
                print(f"'{node}': {count}")
            print("\n")
        elif response == 2:
            pass
        elif response == 3:
            target_team = input("Enter NBA three letter team code: ")
            top_colleges = top_colleges_by_team(adj_list, target_team)
            # Print out the results
            for college, count in top_colleges:
                print(f"{college}: {count}")
        else:
            print("\nThank You!\n")
            break

if __name__ == "__main__":
    main()