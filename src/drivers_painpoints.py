import pandas as pd

df = pd.read_csv('data/final_analysed_reviews.csv')
pos = df[df['sentiment_label'] == 'positive']
neg = df[df['sentiment_label'] == 'negative']

for bank in df['bank'].unique():
    print(f"\n===== {bank} =====")
    print("Drivers (positive themes):", pos[pos['bank'] == bank]['theme'].value_counts().head(3).to_dict())
    print("Pain points (negative themes):", neg[neg['bank'] == bank]['theme'].value_counts().head(3).to_dict())
