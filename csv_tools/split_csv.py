import pandas as pd
import os


def split_csv(file_path, num_splits, output_dir):
    # Ανάγνωση του CSV αρχείου
    df = pd.read_csv(file_path)

    # Ανάκτηση του header
    header = df.columns.tolist()

    # Υπολογισμός μεγέθους κάθε κομματιού
    num_rows = len(df)
    rows_per_split = num_rows // num_splits
    extra_rows = num_rows % num_splits

    # Δημιουργία του output directory αν δεν υπάρχει
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_idx = 0
    for i in range(num_splits):
        end_idx = start_idx + rows_per_split
        if i < extra_rows:
            end_idx += 1

        split_df = df.iloc[start_idx:end_idx]

        # Προσθήκη του header
        split_file_path = os.path.join(output_dir, f'split_{i + 1}.csv')
        split_df.to_csv(split_file_path, index=False, header=header)

        start_idx = end_idx

    print(f'File split into {num_splits} parts and saved to {output_dir}')


# Παράδειγμα χρήσης
file_path = 'C:/Users/haris/OneDrive/Desktop/scrap/venv/tweets/Advance2024-05-25_04-20-19_tweets_1-15.csv'  # Το μονοπάτι του αρχικού αρχείου
num_splits = 5  # Αριθμός κομματιών που θέλετε
output_dir = 'splits'  # Ο κατάλογος όπου θα αποθηκευτούν τα κομμάτια

split_csv(file_path, num_splits, output_dir)
