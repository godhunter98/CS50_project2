import sqlite3
import yfinance as yf
from datetime import date
import tabulate
import sys

DB_PATH = 'portfolio.db'

def fetch_price(sec: str) -> float:
    ticker = yf.Ticker(sec.strip())
    data   = ticker.history(period="1d")
    if data.empty:
        raise ValueError(f"No price data available for {sec!r}")
    return round(float(data["Close"].iloc[-1]), 2)

def add_to_db(security: str, quantity: float, db_path: str = DB_PATH) -> dict:
    """
    Fetches the latest price for `security`, logs a trade of `quantity` shares
    into the SQLite DB, and returns a summary dictionary.
    """
    # 1. Open & init
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS portfolio (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker         TEXT    NOT NULL,
        current_price  REAL    NOT NULL,
        quantity       REAL    NOT NULL,
        total_position REAL    NOT NULL,
        date_added     TEXT    NOT NULL
      );
    """)
    con.commit()

    # 2. Compute
    price          = fetch_price(security)
    total_position = round(price * quantity, 2)
    today          = date.today().isoformat()

    # 3. Insert
    cur.execute("""
      INSERT INTO portfolio
        (ticker, current_price, quantity, total_position, date_added)
      VALUES
        (:ticker, :current_price, :quantity, :total_position, :date_added)
    """, {
      'ticker':          security.upper(),
      'current_price':   price,
      'quantity':        quantity,
      'total_position':  total_position,
      'date_added':      today
    })
    con.commit()

    new_id = cur.lastrowid
    con.close()

    # 4. Return a summary
    return {
      'id':             new_id,
      'ticker':         security.upper(),
      'current_price':  price,
      'quantity':       quantity,
      'total_position': total_position,
      'date_added':     today
    }

def fetch_portfolio(db_path: str):
    con = sqlite3.connect(db_path)

    try:
        cur = con.cursor()
        cur.execute("""
        SELECT 
            ticker,
            ROUND(AVG(current_price), 2) AS avg_price,
            SUM(quantity) AS total_qty,
            ROUND(SUM(total_position), 2) AS total_position
        FROM portfolio
        GROUP BY ticker;
        """)

        portfolio_data = cur.fetchall()
        total_portfolio = sum(row[3] for row in portfolio_data)
        headers = ['ticker', 'Avg_Price', 'Qty', 'Total_Position']
        portfolio_data = tabulate.tabulate(portfolio_data, tablefmt="grid", headers=headers)
        return portfolio_data, total_portfolio

    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            sys.exit("❌ The portfolio table does not exist. Please add a trade first.")
        else:
            sys.exit(f"❌ Database error: {e}")


def main():
    ticker   = input("Ticker to add: ").strip()
    quantity = float(input("Quantity: "))
    summary  = add_to_db(ticker, quantity)
    print(f"✔ Logged trade #{summary['id']}: "
          f"{summary['quantity']}× {summary['ticker']} @ "
          f"{summary['current_price']} each "
          f"(total {summary['total_position']}) on {summary['date_added']}")
    
if __name__ == "__main__":
    main()