import sqlite3
import sys
import argparse

parser = argparse.ArgumentParser(
                    prog='sql_portfolio_db',
                    description='Sets up your portfolio in an SQLite databse, that you can query when needed',
                    epilog='Text at the bottom of help')

parser.add_argument("-a",help = "Add the security to portfolio",type=str)
parser.add_argument("-q",help = "What quantity do you own?",type=int)
parser.add_argument("-s",help = "Show the current portfolio")
parser.add_argument("e",help = "Exit the program")
args = parser.parse_args()

while True:
    if args.a and args.q:
        print(args)
    elif args.e:
        sys.exit("Exiting the program!")
    else:
        print('You need to input something!')




# # setting up our db connection and a cursor to execute queries
# con = sqlite3.connect('portfolio.db')
# cur = con.cursor()

# def main():
#     print("Hello from cs50-project2!")


# if __name__ == "__main__":
#     main()
