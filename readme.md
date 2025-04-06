# 📊 Twitter Scraping για Eurovision 2024

## 🔍 Περιγραφή

Το παρόν project αφορά τη συλλογή και αποθήκευση σχολίων από το Twitter γύρω από τη Eurovision 2024. Εστιάσαμε σε posts από 1 έως 15 Μαΐου 2024, τα οποία σχετίζονται με τα queries **"Eurovision"**, **"EBU"**, και hashtags όπως:  
`#SBSEurovision`, `#fucktheEBU2024`, `#Eurovision2024`, `#eurovisiongr2024`, `#eurovissionfuns`.  

Αρχικά, έγινε χρήση του  του αρχείου **`advance_scraper.py`** για εντοπισμό σχετικών posts με τουλάχιστον 10 απαντήσεις. Το αποτέλεσμα ήταν το αρχείο `Advance2024-05-25_04-20-19_tweets_1-15.csv`, το οποίο περιείχε **1208 posts**.

Στη συνέχεια, τα URLs των posts μοιράστηκαν σε 5 csv αρχεία (για καλύτερη διαχείριση) και χρησιμοποιήθηκε το **`scraper_commends_from_post.py`** για τη συλλογή των απαντήσεων (tweets) κάθε post.

---

## ⚙️ Προϋποθέσεις για Εκτέλεση

Ο χρήστης πρέπει:

- Να έχει εγκατεστημένο τον **Firefox browser**.
- Να κατεβάσει και εγκαταστήσει το [**geckodriver**](https://github.com/mozilla/geckodriver/releases) και να ορίσει σωστά την τοποθεσία του.
- Να εγκαταστήσει το **uBlock Origin** για αποκλεισμό διαφημίσεων κατά την πλοήγηση:  
  [uBlock Origin Add-on](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/)
- Να έχει τα αρχεία `tweet.py` και `scroller.py` στον ίδιο φάκελο με τα κύρια scripts.
- Να δημιουργήσει η νά έχει έναν λογαριασμο στο twitter και να είσάγει το username και το password στια αντίσοιχες μεταβλητές του αρχείου  **`advance_scraper.py`** και **`scraper_commends_from_post.py`**

---

## 📁 Περιγραφή Αρχείων

### ✅ `advance_scraper.py`
Κάνει scrape τα αρχικά tweets με βάση την αναζήτηση:

1. **Αρχικοποίηση:** Εισαγωγή βιβλιοθηκών (`selenium`, `pandas`, `tweet.py`, `scroller.py`).
2. **get_tweet_cards:** Συλλογή tweet καρτελών από τη σελίδα.
3. **save_to_csv:** Αποθήκευση των tweets σε `.csv` αρχείο.
4. **get_tweets:** Επιστρέφει τα συλλεγμένα tweets.
5. **WebDriver:** Ρυθμίσεις για τον Firefox + geckodriver + uBlock.
6. **Login:** Είσοδος στο Twitter με username & password.
7. **Αναζήτηση:** Εισαγωγή ερωτήματος και ενεργοποίηση του Scroller.
8. **Αποθήκευση:** Εξαγωγή των αποτελεσμάτων σε αρχείο CSV.

### ✅ `scraper_commends_from_post.py`
Διαβάζει τα URLs από τα αρχικά δεδομένα και κάνει scrape τα σχόλια κάθε post.

### ✅ `tweet.py`
Συλλέγει δεδομένα (author, time, content) από κάθε tweet καρτέλα.

### ✅ `scroller.py`
Χειρίζεται το scroll down της σελίδας ώστε να φορτωθούν νέα tweets.

---

## ❗ Προβλήματα & Λύσεις

- 🔸 Οι στατικές σελίδες (π.χ. ελληνικοί στίχοι) δεν παρουσίασαν προβλήματα.
- 🔸 Οι διαφημίσεις σε αγγλικές σελίδες επιλύθηκαν με χρήση του **uBlock**.
- 🔸 Το Twitter, ως **δυναμική σελίδα**, απαίτησε scrolling μέσω του `scroller.py`.

---

## 📦 Αποτελέσματα

- Συλλέχθηκαν 1208 κύρια tweets.
- Μετά το scraping των απαντήσεων, δημιουργήθηκε ένα σύνολο δεδομένων ιδανικό για **ανάλυση συναισθήματος** ή **θέμα αναγνώρισης** στην Eurovision.

