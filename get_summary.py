import pandas as pd

try:
    df = pd.read_csv('rfm_results.csv')
    summary = df.groupby('customer_segment').agg(
        count=('customer_id', 'count'), 
        revenue=('monetary_value', 'sum')
    ).sort_values('revenue', ascending=False)
    
    summary['revenue'] = summary['revenue'].map('${:,.2f}'.format)
    
    with open('summary.txt', 'w') as f:
        f.write(summary.to_string())
    
    print("Summary saved to summary.txt")
except Exception as e:
    print(e)
