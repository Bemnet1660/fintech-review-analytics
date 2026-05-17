# src/plot_sentiment.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_sentiment_distribution(input_path='data/final_analysed_reviews.csv', output_path='sentiment_plot.png'):
    """
    Loads the analysed reviews (with sentiment_label column) and creates a stacked bar chart
    showing sentiment distribution per bank.
    """
    # Load data
    df = pd.read_csv(input_path)
    
    # Check required columns
    if 'sentiment_label' not in df.columns:
        print("Error: 'sentiment_label' column not found. Run sentiment analysis first.")
        return
    
    # Create cross-tabulation: bank vs sentiment_label
    sentiment_counts = df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0)
    
    # Reorder columns for consistent legend (positive, neutral, negative)
    desired_order = ['positive', 'neutral', 'negative']
    existing = [col for col in desired_order if col in sentiment_counts.columns]
    sentiment_counts = sentiment_counts[existing]
    
    # Plot
    ax = sentiment_counts.plot(kind='bar', stacked=True, figsize=(8,5), colormap='viridis', edgecolor='black')
    plt.title('Sentiment Distribution per Bank', fontsize=14)
    plt.xlabel('Bank', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    # Add value labels on bars (optional)
    for container in ax.containers:
        ax.bar_label(container, label_type='center', fontsize=9)
    
    # Save plot
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {output_path}")
    plt.show()

if name == "main":
    plot_sentiment_distribution()
