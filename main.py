import pandas as pd

def main():
    nba = pd.read_csv("all_seasons.csv")
    print(nba.head())

    # Option 1 Return a list of the most connected colleges - gives insights to the college with highest draft history (tie between MSU/UM)
        # Give option to visualize
    # Option 2 For each college - NBA team, check their calculated composite score to give insights on athlete performance
        # Give option to visualize
    # Option 3 Return a list of colleges that are most historically drafted by an inputted NBA team
        # Give option to visualize

if __name__ == "__main__":
    main()