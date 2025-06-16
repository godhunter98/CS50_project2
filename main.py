import sqlite3
import sys
import argparse
from database import fetch_price,add_to_db

parser = argparse.ArgumentParser(
                    prog='sql_portfolio_db',
                    description='Sets up your portfolio in an SQLite databse, that you can query when needed',
                    epilog='Happy analysing! 📈 💸')

parser.add_argument("-a",help = "Add the security to portfolio",type=str)
parser.add_argument("-p",help = "Fetch the price of a single security ",type=str)
parser.add_argument("-q",help = "What quantity do you own?",type=int)
parser.add_argument("-s",help = "Show the current portfolio",action="store_true")
parser.add_argument("-e",help = "Exit the program",action='store_true')
args = parser.parse_args()


if args.a and args.q:
    security = args.a
    quantity = int(args.q)
    print(security,quantity)
    price = fetch_price(security)
    print(price)
    result = add_to_db(security,quantity,'portfolio.db')
    print(f'Trade id: {result['id']} for security {result['ticker']}, at price ${result['current_price']}, logged on {result['date_added']}!')

elif args.p:
    argument = str(args.p)
    if argument.endswith('.NS'):
        print(f'The stock, {args.p} currently trades at:- ₹{fetch_price(args.p)}')
    else:
        print(f'The stock, {args.p} currently trades at:- ${fetch_price(args.p)}')

else:
    pass