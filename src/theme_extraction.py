# src/theme_extraction.py
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    """Basic text cleaning: lowercase, remove punctuation, extra spaces."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_top_keywords(df, bank_name, n=10):
    """Extract top n keywords (unigrams + bigrams) using TF-IDF for a given bank."""
    subset = df[df['bank'] == bank_name].copy()
    subset['clean'] = subset['review'].apply(clean_text)
    # Remove empty strings
    subset = subset[subset['clean'].str.strip() != '']
    if len(subset) == 0:
        print(f"  No text available for {bank_name}")
        return []
    
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=n, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(subset['clean'])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    term_scores = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
    return term_scores

def assign_theme(text):
    """Assign a theme based on keyword matching."""
    text = text.lower()
    # Performance theme
    if any(word in text for word in ['slow', 'fast', 'crash', 'loading', 'freeze', 'speed', 'lag', 'hang', 'unresponsive']):
        return 'performance'
    # Authentication theme
    if any(word in text for word in ['login', 'otp', 'fingerprint', 'pin', 'password', 'biometric', 'authentication', 'sms']):
        return 'authentication'
    # Features theme
    if any(word in text for word in ['transfer', 'budget', 'ui', 'interface', 'notification', 'balance', 'feature', 'transaction']):
        return 'features'
    return 'other'

def main():
    # Load the CSV with sentiment labels (output from sentiment analysis)
    input_path = 'data/with_sentiment.csv'
    output_path = 'data/final_analysed_reviews.csv'
    
    print(f"Loading {input_path}...")
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} reviews.")
    
    # Extract and print top keywords per bank
    print("\n=== Top keywords per bank (TF-IDF) ===")
    for bank in df['bank'].unique():
        top_terms = extract_top_keywords(df, bank, n=10)
        print(f"\n{bank}:")
        if top_terms:
            for word, score in top_terms[:5]:
                print(f"  - {word}: {score:.3f}")
        else:
            print("  No keywords found.")
    
    # Assign themes to each review
    print("\n=== Assigning themes ===")
    df['theme'] = df['review'].apply(assign_theme)
    
    # Show theme distribution
    theme_counts = df['theme'].value_counts()
    print("\nTheme distribution (all banks):")
    for theme, count in theme_counts.items():
        print(f"  {theme}: {count} ({count/len(df)*100:.1f}%)")
    
    # Per-bank theme breakdown
    print("\nPer-bank theme breakdown:")
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        print(f"\n{bank}:")
        for theme in bank_df['theme'].value_counts().items():
            print(f"  {theme[0]}: {theme[1]} ({theme[1]/len(bank_df)*100:.1f}%)")
    
    # Save final dataset
    df.to_csv(output_path, index=False)
    print(f"\nSaved final analysed data to {output_path}")
    print("Columns now include: sentiment_label, sentiment_score, theme")

if name == "main":
    main()
