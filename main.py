import pandas as pd

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
        print("""1: Most successful colleges\n2: Determine average NBA rookie performance by college\n3: NBA draft history\n4: Exit""")
        try:
            response = int(input("Please input an option: "))
        except ValueError:
            print("\nPlease input a valid input option\n")
        if response == 4:
            print("\nThank You!\n")
            break

if __name__ == "__main__":
    main()