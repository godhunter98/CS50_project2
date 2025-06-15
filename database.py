import sqlite3
import yfinance as yf
from datetime import date

# setup


def fetch_price(sec: str) -> float:
    ticker = yf.Ticker(sec.strip())
    data = ticker.history(period="1d")

    if data.empty:
        raise ValueError(f"No price data available for {sec!r}") from None
    
    price = data["Close"].iloc[-1]
    return round(float(price), 2)

def main():

    # STEP 1
    # setting up our db connection and a cursor to execute queries
    con = sqlite3.connect('portfolio.db')
    cur = con.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL, 
                current_price REAL NOT NULL,
                quantity REAL NOT NULL,
                total_position REAL NOT NULL,
                date_added TEXT NOT NULL
            )
    """)

    con.commit()

    # STEP 2
    security = input(
'''What security do you want to add to porfolio?: 
Press 3 to see available tickers...\n''').strip()
    
    quantity = int(input('How much do you own?\n'))

    # STEP 3
    price = fetch_price(security)

    total_position = (price * quantity).__round__(2)

    # STEP 4
    cur.execute('''INSERT INTO portfolio
                (ticker, current_price, quantity, total_position, date_added)
                VALUES (:ticker,:current_price,:quantity,:total_position,:date_added)''',
                {'ticker':security,'current_price':price,'quantity':quantity,
                 'total_position':total_position,'date_added':date.today()})
    con.commit()

    cur.execute("SELECT * FROM portfolio")
    
    print(cur.fetchall())

    con.close()

if __name__ == '__main__':
    main()