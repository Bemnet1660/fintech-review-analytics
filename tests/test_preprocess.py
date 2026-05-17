import pytest
import pandas as pd
from src.preprocessing import clean_text, tokenize_and_lemmatize, preprocess_dataframe, robust_clean

def test_clean_text():
    # Check if symbols and numbers are removed
    assert "hello" in clean_text("Hello!")
    assert clean_text(None) == ""

def test_tokenize_and_lemmatize():
    text = "the cats are jumping"
    result = tokenize_and_lemmatize(text)
    # Stopwords like 'the' and 'are' should be gone
    assert "cat" in result
    assert "the" not in result

def test_preprocess_dataframe():
    df = pd.DataFrame({'review': ["I love this app!"] })
    df_processed = preprocess_dataframe(df, text_column='review')
    # Column names must match src/preprocessing.py
    assert 'clean_text' in df_processed.columns
    assert 'processed_content' in df_processed.columns

def test_robust_clean():
    df = pd.DataFrame({
        'review': ["Great", "Good", ""], # Row 3 is too short
        'rating': [5, 4, 1],
        'date': ["2023-01-01 10:00:00", "2023-02-01", "2023-03-01"]
    })
    df_cleaned = robust_clean(df)
    # Row with empty/short review should be dropped
    assert len(df_cleaned) == 2
    # Date should be normalized to YYYY-MM-DD
    assert df_cleaned['date'][0] == "2023-01-01"
