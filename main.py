import pandas as pd

def main():
    nba = pd.read_csv("all_seasons.csv")
    print(nba.head())

    # Option 1 Return a list of the most connected colleges - gives insights to the college with highest draft history (tie between MSU/UM)
    # Option 2 

if __name__ == "__main__":
    main()