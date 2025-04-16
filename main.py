import pandas as pd
from collections import defaultdict
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings('ignore')

def clean_data(nba):
    """
    Clean and process the NBA dataset to extract rookie data.

    Parameters
    ----------
    nba : pandas.DataFrame
        A DataFrame containing NBA player data with columns including:
        'season', 'draft_year', and 'net_rating'.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing only rookie players data, with 'draft_year'
        and 'net_rating' appropriately adjusted.
    """
    # Extract the current season
    nba['season_year'] = nba['season'].str[:4].astype(int)

    # Replace "undrafted" with 0 in 'draft_year'
    nba['draft_year'] = nba['draft_year'].replace('Undrafted', 0)
    nba['draft_year'] = nba['draft_year'].astype(int)

    # Filter to extract rookies
    rookies = nba[nba['draft_year'] == nba['season_year']]

    # Replace negative net_rating values with 0
    rookies['net_rating'] = rookies['net_rating'].apply(lambda x: max(x, 0))

    return rookies

def calc_composite_score(rookies):
    """
    Calculate a composite performance score for each player.

    Parameters
    ----------
    rookies : pandas.DataFrame
        A DataFrame containing player statistics with at least the following columns:
        'pts', 'reb', 'ast', 'net_rating', 'ts_pct', 'usg_pct'.

    Returns
    --------
        None
    """
    # Replace any Nan value with 0
    rookies.fillna(0, inplace=True)

    # Select columns to normalize
    numeric_cols = ["pts", "reb", "ast", "net_rating", "ts_pct", "usg_pct"]
    scaler = MinMaxScaler()

    # Normalize
    normalized_vals = scaler.fit_transform(rookies[numeric_cols])
    normalized_df = pd.DataFrame(normalized_vals, columns=numeric_cols)

    # Ensure indices align
    normalized_df.index = rookies.index

    # Create a composite score by averaging the normalized values
    rookies['composite_performance_score'] = normalized_df.mean(axis=1)

def create_adj_list(data):
    """
    Create an adjacency list from a DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        A DataFrame containing the following columns:
        'college', 'team_abbreviation', 'player_name', 'composite_performance_score'

    Returns
    -------
    dict
        A dictionary representing the adjacency list. The keys are college names (str),
        and the values are lists of tuples. Each tuple contains:
        - str : NBA team abbreviation
        - str : player name
        - float : composite performance score
    """
    # Create a dictionary of lists to store the adjacency list
    adjacency_list = defaultdict(list)

    # Iterate
    for index, row in data.iterrows():
        college = row['college']
        team = row['team_abbreviation']
        player_name = row['player_name']
        score = row["composite_performance_score"]

        # Append the tuple the college's list
        adjacency_list[college].append((team, player_name, score))

    return adjacency_list

def get_node_connections(adjacency_list):
    """
    Calculate and sort the number of player connections for each college.

    Parameters
    ----------
    adjacency_list : dict
        A dictionary where each key is a college name and each value is a list of
        tuples. Each tuple represents a player's connection, containing:
        - str : NBA team abbreviation
        - str : player name
        - float : composite score

    Returns
    -------
    List[Tuple[str, int]]
        A list of tuples with the college name and the number of player connections,
        sorted in descending order of connections.
    """
    # Create a dictionary to count connections for colleges only
    college_connection_counts = defaultdict(int)

    # Iterate
    for college, connections in adjacency_list.items():
        # Count each player connection for the college
        college_connection_counts[college] += len(connections)

    # Sort the colleges by the number of connections in descending order
    sorted_college_connections = sorted(college_connection_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_college_connections

def top_colleges_by_team(adjacency_list, target_team):
    """
    Determine the number of players drafted from each college by a specific NBA team.

    Parameters
    ----------
    adjacency_list : dict
        A dictionary where the keys are college names (str) and the values are lists
        of tuples. Each tuple contains:
        - str : NBA team abbreviation
        - str : player name
        - float : composite score

    target_team : str
        The NBA team abbreviation to search for in the player lists.

    Returns
    -------
    List[Tuple[str, int]]
        A sorted list of tuples, each containing a college name and the count of players
        drafted by the specified team, sorted in descending order of count.
    """
    # Dictionary to store the count of players drafted from each college by the target team
    college_counts = defaultdict(int)

    # Iterate through dictionary
    for college, players in adjacency_list.items():
        # Iterate through list
        for team, player, composite_score in players:
            # If the team matches target_team, increment
            if team == target_team:
                college_counts[college] += 1

    # Sort the colleges
    sorted_colleges = sorted(college_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_colleges

def calc_average_composite(adjacency_list):
    """
    Calculate the average composite score for each college from an adjacency list.

    Parameters
    ----------
    adjacency_list : dict
        A dictionary where each key is a college, and each value is a
        list of tuples. Each tuple contains:
        - str : team abbreviation
        - str : player name
        - int : draft year
        - float : composite score

    Returns
    -------
    dict
        A dictionary with colleges as keys and their average composite scores
        as values. If a college has no players, the average score is stored
        as NaN.
    """
    # Dictionary to store total composite scores and counts for each college
    scores_data = defaultdict(lambda: {'total_score': 0.0, 'count': 0})

    # Iterate
    for college, players in adjacency_list.items():
        for _, _, composite_score in players:
            # Accumulate the composite scores and count of players per college
            scores_data[college]['total_score'] += composite_score
            scores_data[college]['count'] += 1

    # Calculate average composite scores for each college
    average_scores = {}
    for college, data in scores_data.items():
        if data['count'] > 0:
            average_scores[college] = data['total_score'] / data['count']
        else:
            average_scores[college] = float('nan')  # Handle no players scenario

    return average_scores

def main():
    # Read in data
    nba = pd.read_csv("all_seasons.csv")

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

        # It is assumed that input is valid from here onwards

        # Clean & prep our data
        rookies = clean_data(nba)
        # Create normalized composite score
        calc_composite_score(rookies)
        # Create network with an adjacency list
        adj_list = create_adj_list(rookies)

        # Respond to input
        if response == 1:
            sorted_nodes_with_connections = get_node_connections(adj_list)
            for node, count in sorted_nodes_with_connections:
                print(f"'{node}': {count}")
        elif response == 2:
            # Calculate and print average composite scores for each college
            average_scores = calc_average_composite(adj_list)
            for college, avg_score in average_scores.items():
                print(f"{college}: {avg_score:.4f}")
        elif response == 3:
            target_team = input("Enter NBA three letter team code: ")
            top_colleges = top_colleges_by_team(adj_list, target_team)
            for college, count in top_colleges:
                print(f"{college}: {count}")
        else:
            print("\nGoodbye!\n")
            break

if __name__ == "__main__":
    main()