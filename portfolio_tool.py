#!/Users/harsh/Desktop/cs50_project2/.venv/bin/python

import sys
import argparse
from database import fetch_price,add_to_db,fetch_portfolio

parser = argparse.ArgumentParser(
                    prog='sql_portfolio_db',
                    description='Sets up your portfolio in an SQLite databse, that you can query when needed',
                    epilog='Happy analysing! 📈 💸')

parser.add_argument("-a", help="Add the security to portfolio", type=str)
parser.add_argument("-q", help="Quantity you own", type=int)
parser.add_argument("-p", help="Fetch the price of a security", type=str)
parser.add_argument("-s", help="Show the current portfolio", action="store_true")
parser.add_argument("-e", help="Exit the program", action="store_true")
args = parser.parse_args()


def main():
    if args.a and args.q:
        security = args.a
        quantity = int(args.q)
        print(security,quantity)
        price = fetch_price(security)
        print(price)
        result = add_to_db(security,quantity,'portfolio.db')
        print(f"Trade id: {result['id']} for security {result['ticker']}, at price ${result['current_price']}, logged on {result['date_added']}!")
    elif args.a and not args.q:
        sys.exit("Please provide the quantity (-q) along with the security (-a).")

    elif args.s:
        table,total_portfolio = fetch_portfolio('portfolio.db')
        print(f'\n{table}')
        print(f'\n The porfolio is worth   ${total_portfolio}\n ')

    elif args.p:
        argument = str(args.p)
        if argument.endswith('.NS'):
            print(f"The stock, {args.p} currently trades at:- ₹{fetch_price(args.p)}")
        else:
            print(f"The stock, {args.p} currently trades at:- ${fetch_price(args.p)}")
    else:
        sys.exit("Please supply an argument!")


if __name__=='__main__':
    main()