import os
import pandas as pd

# Φάκελος που περιέχει τα αρχεία CSV
folder_path = 'C:/Users/haris/OneDrive/Desktop/scrap/venv/eurovision'  # Αντικαταστήστε με τη σωστή διαδρομή

# Λίστα για να αποθηκεύσουμε τα δεδομένα από όλα τα CSV αρχεία
all_data = []

# Διατρέχουμε όλα τα αρχεία στον φάκελο
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        print(f"Διαβάζοντας το αρχείο {file_path}")
        df = pd.read_csv(file_path)
        all_data.append(df)

# Ενοποίηση όλων των δεδομένων σε ένα DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Αφαίρεση των διπλότυπων βάσει του πεδίου 'tweet_id'
unique_df = combined_df.drop_duplicates(subset='Tweet ID')

# Αποθήκευση του συνενωμένου DataFrame σε ένα νέο αρχείο CSV
output_file_path = 'C:/Users/haris/OneDrive/Desktop/scrap/venv/eurovision/combined_unique_eurovision.csv'  # Αντικαταστήστε με τη σωστή διαδρομή
unique_df.to_csv(output_file_path, index=False)

print(f"Το νέο αρχείο CSV αποθηκεύτηκε ως {output_file_path}")
