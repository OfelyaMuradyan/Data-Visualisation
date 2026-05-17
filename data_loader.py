import pandas as pd
import os

file_path = 'netflix_titles.csv'
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    print("Warning: netflix_titles.csv not found locally.")
    df = pd.DataFrame(columns=['type', 'country', 'date_added', 'release_year', 'rating', 'duration', 'listed_in'])

df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
df['year_added'] = df['date_added'].dt.year
df = df.dropna(subset=['year_added']) 
df['country'] = df['country'].fillna('Unknown')