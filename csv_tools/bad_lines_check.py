import pandas as pd

# Διαδρομή του αρχείου
file_path = 'C:/Users/haris/OneDrive/Desktop/scrap/venv/eurovision/combined_unique_eurovision.csv'

# Διαδρομές για τα αρχεία εξόδου
valid_output_file_path = 'C:/Users/haris/OneDrive/Desktop/scrap/venv/eurovision/valid_rows.csv'
invalid_output_file_path = 'C:/Users/haris/OneDrive/Desktop/scrap/venv/eurovision/invalid_rows.csv'

# Ανάγνωση του αρχείου CSV
df = pd.read_csv(file_path)

# Έλεγχος για μη έγκυρες γραμμές
valid_rows = []
invalid_rows = []

# Εύρεση της στήλης 'Tweet ID'
tweet_id_index = df.columns.get_loc('Tweet ID')

for index, row in df.iterrows():
    tweet_id_value = row['Tweet ID']
    if isinstance(tweet_id_value, str) and tweet_id_value.startswith('tweet_id:'):
        valid_rows.append(row)
    else:
        invalid_rows.append(row)

# Δημιουργία DataFrame για τις έγκυρες και μη έγκυρες γραμμές
valid_df = pd.DataFrame(valid_rows, columns=df.columns)
invalid_df = pd.DataFrame(invalid_rows, columns=df.columns)

# Αποθήκευση των έγκυρων γραμμών σε ένα νέο αρχείο CSV
valid_df.to_csv(valid_output_file_path, index=False)

# Αποθήκευση των μη έγκυρων γραμμών σε ένα ξεχωριστό αρχείο CSV
invalid_df.to_csv(invalid_output_file_path, index=False)

print(f"Οι έγκυρες γραμμές αποθηκεύτηκαν ως {valid_output_file_path}")
print(f"Οι μη έγκυρες γραμμές αποθηκεύτηκαν ως {invalid_output_file_path}")
