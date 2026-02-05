import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ShopperDNA Visualization Module


# Set style for premium aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

csv_path = 'rfm_results.csv'
output_bar = 'segment_distribution.png'
output_scatter = 'rfm_scatter.png'

def create_visualizations():
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Run analysis first.")
        return

    df = pd.read_csv(csv_path)
    
    # Define order and colors for segments
    segment_order = [
        'Champions', 'Loyal Customers', 'Potential Loyalists', 
        'Recent Customers', 'At Risk', 'Lost Customers', 'Needs Attention'
    ]
    
    # Filter only segments that exist in the data to avoid seaborn errors if some are missing
    existing_segments = [s for s in segment_order if s in df['customer_segment'].unique()]
    
    # 1. Bar Chart: Customer Count per Segment
    plt.figure(figsize=(12, 6))
    sns.countplot(x='customer_segment', data=df, order=existing_segments, palette='viridis')
    plt.title('ShopperDNA: Customer Distribution by Segment', fontsize=16)
    plt.xlabel('Segment', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_bar)
    print(f"Saved bar chart to {output_bar}")
    
    # 2. Scatter Plot: Recency vs Frequency (colored by Segment)
    # Adding a small jitter to Frequency to see overlapping points better if needed, 
    # but for now standard scatter is fine.
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df, 
        x='recency_days', 
        y='frequency', 
        hue='customer_segment', 
        hue_order=existing_segments,
        palette='viridis',
        alpha=0.7
    )
    plt.title('ShopperDNA: Recency vs Frequency Intelligence', fontsize=16)
    plt.xlabel('Recency (Days since last purchase)', fontsize=12)
    plt.ylabel('Frequency (Total Orders)', fontsize=12)
    plt.legend(title='Segment')
    plt.tight_layout()
    plt.savefig(output_scatter)
    print(f"Saved scatter plot to {output_scatter}")

if __name__ == "__main__":
    create_visualizations()
