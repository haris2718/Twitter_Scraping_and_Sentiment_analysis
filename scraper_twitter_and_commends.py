import csv
import os
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver import FirefoxProfile, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from scroller import Scroller
from tweet import Tweet
import pandas as pd
from datetime import datetime
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
import time
tweet_cards=[]
data = []
global query

# Βρες όλα τα tweet card elements (καθε tweet εμφανίζεται σε ένα card element ) που δεν είναι απενεργοποιημένα και αποθηκευσέ τα  τα στην καθολική μεταβλητή tweet_cards
def get_tweet_cards(driver):
    global tweet_cards
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//article[@data-testid="tweet" and not(@disabled)]')))
    tweet_cards =driver.find_elements(By.XPATH, '//article[@data-testid="tweet" and not(@disabled)]')
    print(tweet_cards)
#αποθηκευσε τα  αποτελέσματα  σε ένα  csv
def save_to_csv():
    print("Saving Tweets to CSV...")
    now = datetime.now()
    folder_path = "./tweets/"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Created Folder: {}".format(folder_path))

    data1 = {
        "Name": [tweet[0] for tweet in data],
        "Handle": [tweet[1] for tweet in data],
        "Timestamp": [tweet[2] for tweet in data],
        "Verified": [tweet[3] for tweet in data],
        "Content": [tweet[4] for tweet in data],
        "Comments": [tweet[5] for tweet in data],
        "Retweets": [tweet[6] for tweet in data],
        "Likes": [tweet[7] for tweet in data],
        "Analytics": [tweet[8] for tweet in data],
        "Tags": [tweet[9] for tweet in data],
        "Mentions": [tweet[10] for tweet in data],
        "Emojis": [tweet[11] for tweet in data],
        "Profile Image": [tweet[12] for tweet in data],
        "Tweet Link": [tweet[13] for tweet in data],
        "Tweet ID": [f"tweet_id:{tweet[14]}" for tweet in data],
    }
    comments={
        "Tweet Link": [tweet[13] for tweet in data],
        "Tweet ID": [f"tweet_id:{tweet[14]}" for tweet in data],
    }

    if scraper_details["poster_details"]:
        data1["Tweeter ID"] = [f"user_id:{tweet[15]}" for tweet in data]
        data1["Following"] = [tweet[16] for tweet in data]
        data1["Followers"] = [tweet[17] for tweet in data]

    df = pd.DataFrame(data1)

    current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"{folder_path}{query}{current_time}_tweets_comments_1-{len(data1)}.csv"
    pd.set_option("display.max_colwidth", None)
    #ISO-8859-1
    df.to_csv(file_path, index=False, encoding="utf-8")

    print("CSV Saved: {}".format(file_path))

    pass


def get_tweets():
    global data
    return data

def scroll_down(driver):
    # αρχικοποιήσε τον scroller για να κατέβεις πιο κάτω στην σελίδα
    scroller = Scroller(driver)

    # όσο είναι ενεργός
    try:
        get_tweet_cards(driver)
        # Έλεγχος αν τα διαθέσιμα tweets είναι κάτω από 2
        if len(tweet_cards) < 2:
            print(f"Less than 2 tweets available. Number of tweets: {len(tweet_cards)}")
            for card in tweet_cards:
                print(card.text)
            print("I'm leaving")
            return

    except Exception as e:
        print("\n")
        print(f"Error scraping tweets: {e}")

    while scroller.scrolling:
        try:
            # μάζεψε τα tweet
            get_tweet_cards(driver)
            added_tweets = 0

            # Για τα τελευταία 15 tweet
            for card in tweet_cards[-3:]:
                try:
                    print(card.text)
                    tweet_id = str(card)

                    # εάν δεν τα έχεις ήδη επεξεργαστεί
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)

                        if not scraper_details["poster_details"]:
                            # κάνε scrool
                            driver.execute_script(
                                "arguments[0].scrollIntoView();", card
                            )
                        # αρχικοποίηση των tweet και συλλογή στοιχείων
                        tweet = Tweet(
                            card=card,
                            driver=driver,
                            actions=ActionChains(driver),
                            scrape_poster_details=scraper_details[
                                "poster_details"
                            ],
                        )

                        if tweet:
                            if not tweet.error and tweet.tweet is not None:
                                if not tweet.is_ad:
                                    data.append(tweet.tweet)
                                    added_tweets += 1
                                    # self.progress.print_progress(len(self.data))

                                    if len(data) >= max_tweets:
                                        scroller.scrolling = False
                                        break
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                except NoSuchElementException:
                    continue

            if len(data) >= max_tweets:
                break

            if added_tweets == 0:
                if empty_count >= 3:
                    if refresh_count >= 3:
                        print()
                        print("No more tweets to scrape")
                        break
                    refresh_count += 1
                empty_count += 1
                time.sleep(1)
            else:
                empty_count = 0
                refresh_count = 0
        except StaleElementReferenceException:
            time.sleep(2)
            continue
        except KeyboardInterrupt:
            print("\n")
            print("Keyboard Interrupt")
            interrupted = True
            break
        except Exception as e:
            print("\n")
            print(f"Error scraping tweets: {e}")
            break

    print("")

    if len(data) >= max_tweets:
        print("Scraping Complete")
    else:
        print("Scraping Incomplete")

    print("Tweets: {} out of {}\n".format(len(data), max_tweets))


# Δημιουργία αντικειμένου FirefoxOptions
options = Options()
options.binary_location = r'C:\Users\haris\AppData\Local\Mozilla Firefox\Firefox.exe'  # εισήγαγε την θέση εγκατάστασης του Firefox στον υπολογιστή σας



# Ορίστε την θέση   του geckodriver
service = Service(executable_path=r'C:\Users\haris\OneDrive\Desktop\scrap\geckodriver.exe')

# Δημιουργία Firefox WebDriver με το προσαρμοσμένο προφίλ και options
driver = webdriver.Firefox(service=service, options=options)

# Δημιουργία ενός Firefox Profile
#profile = FirefoxProfile()
#Το πρόσθετο ublock_origin χρησιμοποιείται για να μην εμφανίζινται οι διαφημίσεις
xpi_path = r'C:\Users\haris\OneDrive\Desktop\scrap\ublock_origin-1.57.2.xpi'
#rofile.add_extension(xpi_path)
driver.install_addon(xpi_path, temporary=True)
username="testihu139645"
password="baris1234wh123456"
query="Eurovision_advance_2_"#δηλωσε μερος του ονοματος για αποθηκευση
csv_to_scrape_comments=r'C:\Users\haris\OneDrive\Desktop\scrap\venv\splits\split_2.csv' #απο ποιο αρχείο θα πάρει τα post

#τα id των tweet, max_tweets = πόσα tweet θα φέρει, empty_count μεταβλητη που χρησιμοποιείται για την ανάκτηση των tweet
tweet_ids = set()
max_tweets=20000
empty_count=0
scraper_details = {
            "type": None,
            "username": None,
            "hashtag": None,
            "query": None,
            "tab": None,
            "poster_details": False,
        }
refresh_count=0
#πάνε σε αυτήν την διευθυνση
driver.get('https://twitter.com/i/flow/login')


#άνοιξε  τον browser σε μεγάλο παράθυρο
driver.maximize_window()
# Περιμένετε μέχρι να φορτώσει η σελίδα
time.sleep(5)

try:
    # Περίμενε  μέχρι το πεδίο εισαγωγής να είναι διαθέσιμο
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'text'))
    )

    # γράψε   το email στο πεδίο
    username_input.send_keys(username)
    # Πάτησε  το Enter
    username_input.send_keys(Keys.ENTER)
except Exception as e:
    print(f"Προέκυψε σφάλμα username: {e}")

try:
    # Περίμενε  μέχρι το πεδίο password να είναι διαθέσιμο
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'password'))
    )

    #γράψε  τον κωδικό πρόσβασης στο πεδίο
    password_input.send_keys(password)

    # Πάτησε  το Enter
    password_input.send_keys(Keys.ENTER)
except Exception as e:
    print(f"Προέκυψε σφάλμα password: {e}")

#επελεξε για cookies
element_to_click = WebDriverWait(driver, 20).until(
    #EC.element_to_be_clickable((By.CSS_SELECTOR, "div.r-18kxxzh:nth-child(2) > div:nth-child(1)"))
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Refuse non-essential cookies']"))
)
element_to_click.click()
try:
    # Διάβασε το CSV αρχείο
    df = pd.read_csv(csv_to_scrape_comments)

    # Εξαγωγή της στήλης "Tweet Link" σε μια λίστα
    tweet_links = df["Tweet Link"].tolist()
    # Περίμενε μέχρι το πεδίο αναζήτησης να είναι διαθέσιμο
    for link in tweet_links:
        driver.get(link)
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "accessible-list-0"))
        )
        scroll_down(driver)

except Exception as e:
    print(f"Προέκυψε σφάλμα query: {e}")




save_to_csv()

pass
