import csv

from selenium import webdriver
from selenium.webdriver import FirefoxProfile, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def saveResult(results):
    # Βρείτε όλα τα στοιχεία τίτλων και κάντε κλικ σε κάθε ένα
    # results = driver.find_elements(By.CSS_SELECTOR, "div.gs-title a.gs-title")

    visited_links = set()

    for result in results:
        #link = result.get_attribute('href')
        if result and result.text not in visited_links:
            visited_links.add(result.text)
            driver.execute_script("window.open(arguments[0]);", result)
            driver.switch_to.window(driver.window_handles[1])
            details = {}

            # Πηγαίνετε στη σελίδα του καλλιτέχνη
            try:
                # Περιμένετε μέχρι το στοιχείο να είναι φορτωμένο και επιλέξτε το όνομα χρήστη
                user_name = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="User-Name"] a'))
                )
                details['user'] = user_name.text
            except Exception as e:
                print("Καλλιτέχνης not found:", e)
                details['user'] = None


            try:
                # Χρήση WebDriverWait για να βεβαιωθείτε ότι το στοιχείο είναι φορτωμένο πριν προσπαθήσετε να το ανακτήσετε
                timestamp = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'time'))
                )
                details['timestamp'] = timestamp.text
            except Exception as e:
                details['timestamp'] = None

            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetText"]'))
                )
                tweet_text = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
                #lyrics = " ".join(element.text for element in lyrics_container if element.text)
                details['tweet'] = tweet_text.text
            except Exception as e:
                print("Στίχοι not found:", e)
                details['tweet'] = None

            # Κάντε εκτύπωση ή επεξεργαστείτε τα λεπτομερή περαιτέρω
            print(details)
            data_list.append(details)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

data_list = []
# Δημιουργία αντικειμένου FirefoxOptions
options = Options()
options.binary_location = r'C:\Users\haris\AppData\Local\Mozilla Firefox\Firefox.exe'  # Προσαρμόστε ανάλογα με την τοποθεσία εγκατάστασης του Firefox στον υπολογιστή σας



# Ορίστε την τοποθεσία του geckodriver
service = Service(executable_path=r'C:\Users\haris\OneDrive\Desktop\scrap\geckodriver.exe')

# Δημιουργία Firefox WebDriver με το προσαρμοσμένο προφίλ και options
driver = webdriver.Firefox(service=service, options=options)

# Δημιουργία ενός Firefox Profile
#profile = FirefoxProfile()
xpi_path = r'C:\Users\haris\OneDrive\Desktop\scrap\ublock_origin-1.57.2.xpi'  # Προσαρμόστε τη διαδρομή χωρίς διπλά backslashes
#rofile.add_extension(xpi_path)
driver.install_addon(xpi_path, temporary=True)
username=""
password=""
query="ClimateChangeUS"

driver.get('https://twitter.com/i/flow/login')
# Περιμένετε μέχρι να φορτώσει η σελίδα
time.sleep(5)

try:
    # Περιμένετε μέχρι το πεδίο εισαγωγής να είναι διαθέσιμο
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'text'))
    )

    # Εισάγετε το email στο πεδίο
    username_input.send_keys(username)
    # Πατήστε το Enter
    username_input.send_keys(Keys.ENTER)
except Exception as e:
    print(f"Προέκυψε σφάλμα username: {e}")

try:
    # Περιμένετε μέχρι το πεδίο password να είναι διαθέσιμο
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'password'))
    )

    # Εισάγετε τον κωδικό πρόσβασης στο πεδίο
    password_input.send_keys(password)

    # Πατήστε το Enter
    password_input.send_keys(Keys.ENTER)
except Exception as e:
    print(f"Προέκυψε σφάλμα password: {e}")

#επελεξε για cookies
element_to_click = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.r-18kxxzh:nth-child(2) > div:nth-child(1)"))
)
element_to_click.click()
try:
    # Περιμένετε μέχρι το πεδίο αναζήτησης να είναι διαθέσιμο
    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]'))
    )

    # Εισάγετε το κείμενο αναζήτησης στο πεδίο
    search_input.send_keys(query)

    # Πατήστε το Enter
    search_input.send_keys(Keys.ENTER)
except Exception as e:
    print(f"Προέκυψε σφάλμα query: {e}")

# Περιμένετε μέχρι το στοιχείο να είναι διαθέσιμο και κάντε κλικ
try:
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[3]/div/div/div/div/div[2]/div[2]/span[1]"))
    )
    element.click()
except Exception as e:
    print(f"Σφάλμα κατά την προσπάθεια κλικ: {e}")

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
# Εύρεση όλων των στοιχείων της λίστας που περιέχουν τα tweets
tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')

# Περιήγηση και κλικ σε κάθε στοιχείο της λίστας
for tweet in tweets:
    # Πάρε τον τίτλο ή το κείμενο του tweet αν χρειάζεται
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetText"]'))
    )
    tweet_text = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
    print(tweet_text)  # Εκτύπωση του κειμένου για επιβεβαίωση

    # Πατήστε στο tweet
    tweet.click()

    # Περίμενε ή χειρίσου την επόμενη σελίδα αν χρειάζεται
    # Περιμένετε μέχρι το στοιχείο να είναι ορατό
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-testid="primaryColumn"]'))
        )
        # Βρείτε όλα τα στοιχεία με τον συγκεκριμένο επιλογέα CSS
        elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="primaryColumn"]')

        # Εκτύπωση του κειμένου από κάθε στοιχείο
        for element in elements:
            print(element.text)
    except Exception as e:
        print(f"Σφάλμα κατά την προσπάθεια εύρεσης των στοιχείων: {e}")

with open('tweet'+query+'_.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
    writer.writeheader()
    for data in data_list:
        writer.writerow(data)
