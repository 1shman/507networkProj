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
        # Prompt user for input
        print("""1: Most successful colleges\n2: Determine average NBA rookie performance by college\n3: NBA draft history\n4: Exit""")

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