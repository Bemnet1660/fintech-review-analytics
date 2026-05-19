import pandas as pd
import psycopg2

# CHANGE THIS LINE to your actual password
DB_PASSWORD = "your_password"

# Connection settings (do not change unless you used different values)
DB_NAME = "fintech_reviews"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

def main():
    # 1. Read the CSV
    df = pd.read_csv('data/final_analysed_reviews.csv')
    print(f"Loaded {len(df)} reviews from CSV")

    # 2. Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    # 3. Insert bank names into 'banks' table
    banks = df['bank'].unique()
    for bank in banks:
        cur.execute("INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) ON CONFLICT (bank_name) DO NOTHING",
                    (bank, f"{bank} Mobile App"))
    conn.commit()
    print(f"Inserted {len(banks)} banks")

    # 4. Get bank_id for each bank name
    cur.execute("SELECT bank_name, bank_id FROM banks")
    bank_map = {row[0]: row[1] for row in cur.fetchall()}

    # 5. Insert each review
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date,
                                 sentiment_label, sentiment_score, theme, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['review_id'],
            bank_map[row['bank']],
            row['review'],
            row['rating'],
            row['date'],
            row['sentiment_label'],
            row['sentiment_score'],
            row['theme'],
            row['source']
        ))
        # Print progress every 100 rows
        if index % 100 == 0:
            print(f"Inserted {index} reviews...")

    conn.commit()
    cur.close()
    conn.close()
    print(f"Successfully inserted {len(df)} reviews into the database.")

if __name__ == "main":
    main()
