import pandas as pd
import sqlite3
import os

db_path = 'ecommerce.db'
csv_path = 'superstore.csv'

def load_data():
    print(f"Loading {csv_path} into {db_path}...")
    
    # Try reading with different encodings
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 decode error, trying 'windows-1252'...")
        df = pd.read_csv(csv_path, encoding='windows-1252')

    # Clean column names for easier SQL querying
    df.columns = [c.replace(' ', '_').replace('-', '_').lower() for c in df.columns]
    
    # Convert date columns to datetime objects (pandas will store as ISO strings in sqlite)
    date_cols = ['order_date', 'ship_date']
    for col in date_cols:
        if col in df.columns:
            # infer_datetime_format is deprecated in newer pandas but helpful, 
            # or just let pd.to_datetime handle it.
            df[col] = pd.to_datetime(df[col], format='mixed', dayfirst=False)
    
    print("Columns found:", df.columns.tolist())

    conn = sqlite3.connect(db_path)
    df.to_sql('orders', conn, if_exists='replace', index=False)
    conn.close()
    
    print("Database setup complete. Table 'orders' created.")

if __name__ == "__main__":
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
    else:
        load_data()
