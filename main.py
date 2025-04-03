import pandas as pd

def main():
    nba = pd.read_csv("all_seasons.csv")

    print(nba.head())

if __name__ == "__main__":
    main()