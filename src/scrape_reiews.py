import pandas as pd
from google_play_scraper import reviews, Sort
import time

def scrape_fintech_reviews(app_dict, count=200, retries=3):
    """
    ERROR HANDLING: Scraper Robustness
    Moves the live scraping logic into a modular function. -  a Retry + Backoff strategy.
    """
    all_reviews = []
    for name, pkg in app_dict.items():
        success = False
        for attempt in range(retries):
            try:
                res, _ = reviews(pkg, lang='en', country='us', sort=Sort.NEWEST, count=count)
                if not res:
                    raise ValueError(f'Empty response for {name}')
                
                for r in res:
                    all_reviews.append({
                        'app': name,
                        'review': r['content'],
                        'rating': r['score'],
                        'date': r['at'],
                        'thumbs': r['thumbsUpCount']
                    })
                print(f'  Scraped {len(res)} reviews for {name}')
                success = True
                break
            except Exception as e:
                print(f'  [Attempt {attempt+1}/{retries}] Failed to scrape {name}: {e}')
                time.sleep(2) # Backoff
        
        if not success:
            print(f' Critical Failure: Could not collect data for {name} after {retries} attempts.')
            
    return pd.DataFrame(all_reviews)
