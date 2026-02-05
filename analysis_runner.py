import sqlite3
import pandas as pd
import os

db_path = 'ecommerce.db'
sql_path = 'rfm_analysis.sql'
output_csv = 'rfm_results.csv'

def run_analysis():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found!")
        return
    
    conn = sqlite3.connect(db_path)
    
    with open(sql_path, 'r') as f:
        # We need to split the script if we want to run multiple statements, 
        # but pandas read_sql usually expects a single query.
        # Our script has 1 main select but precedes with comments/checks.
        # The complex query is one big statement starting with WITH.
        # We'll just read the whole file, but we might encounter issues if we send multiple statements.
        # Let's extract just the final big query if possible, or use executescript for setup and read_sql for the final.
        
        # Actually our SQL file has a "SELECT * FROM orders LIMIT 10;" at the top.
        # We should parse it or just execute the big query directly in python for safety/clarity in this runner.
        # Or I can modify the SQL file to only contain the query.
        # Let's read the content and split by semicolon.
        sql_script = f.read()

    statements = sql_script.split(';')
    
    # We assume the LAST statement is the main query we want results from.
    # We exclude empty statements resulting from trailing newlines/semicolons.
    queries = [s.strip() for s in statements if s.strip()]
    
    print(f"Found {len(queries)} SQL statements.")
    
    for i, query in enumerate(queries):
        if i == len(queries) - 1:
            # Main Analysis Query
            print("Executing final RFM analysis query...")
            try:
                df = pd.read_sql_query(query, conn)
                print("Analysis complete.")
                print("-" * 30)
                
                # Summary Metrics
                print("Segment Summary:")
                summary = df.groupby('customer_segment').agg(
                    customer_count=('customer_id', 'count'),
                    total_revenue=('monetary_value', 'sum')
                ).sort_values('total_revenue', ascending=False)
                summary['total_revenue'] = summary['total_revenue'].map('${:,.2f}'.format)
                print(summary)
                print("-" * 30)
                
                print("Top 5 Champions:")
                print(df[df['customer_segment'] == 'Champions'].head())
                print("-" * 30)
                print(f"Saving results to {output_csv}...")
                df.to_csv(output_csv, index=False)
                print("Done.")
            except Exception as e:
                print("Error executing query:", e)
                print("Query was:", query)
        else:
            # Inspection/Setup queries (run but don't save)
            print(f"Executing setup/inspection query {i+1}...")
            try:
                conn.execute(query)
            except Exception as e:
                print(f"Warning on query {i+1}: {e}")

    conn.close()

if __name__ == "__main__":
    run_analysis()
