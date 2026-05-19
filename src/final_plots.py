import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/final_analysed_reviews.csv')
df['date'] = pd.to_datetime(df['date'])

# 1. Sentiment distribution
sentiment_counts = df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0)
sentiment_counts.plot(kind='bar', stacked=True, figsize=(8,5))
plt.title('Sentiment Distribution per Bank')
plt.tight_layout()
plt.savefig('plot_sentiment.png')
plt.close()

# 2. Rating boxplot
plt.figure(figsize=(8,5))
sns.boxplot(x='bank', y='rating', data=df)
plt.title('Rating Distribution per Bank')
plt.savefig('plot_ratings.png')
plt.close()

# 3. Top themes per bank
for bank in df['bank'].unique():
    subset = df[df['bank'] == bank]
    theme_counts = subset['theme'].value_counts().head(5)
    plt.figure(figsize=(6,4))
    theme_counts.plot(kind='barh')
    plt.title(f'Top Themes - {bank}')
    plt.tight_layout()
    plt.savefig(f'plot_themes_{bank}.png')
    plt.close()

# 4. Sentiment trend (monthly)
df['month'] = df['date'].dt.to_period('M')
trend = df.groupby(['month', 'sentiment_label']).size().unstack(fill_value=0)
if len(trend) > 1:
    trend.plot(kind='line', figsize=(10,5))
    plt.title('Sentiment Trend Over Time')
    plt.savefig('plot_trend.png')
    plt.close()

print("All plots saved.")
