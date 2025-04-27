# Sentiment Analysis of Greece and Israel Tweets Related to Eurovision 2024

Introduction

This study focuses on sentiment analysis of tweets related to Greece and Israel during the Eurovision Song Contest 2024. Data were collected through Twitter scraping, processed with Python and the TextBlob library, and stored in CSV format on Google Drive.

Israel was included in the analysis due to its heightened media presence following the outbreak of the Gaza conflict. The study aims to capture the emotional dynamics reflected on social media, with full acknowledgment of the seriousness of the events.

## Overview

This project focuses on the collection and sentiment analysis of Twitter data related to Eurovision 2024, with a specific emphasis on discussions involving Greece and Israel.
Data was collected between May 1st and May 15th, 2024, and processed using Python and the TextBlob library for sentiment classification.
Data Collection
Keywords & Hashtags

    "Eurovision", "EBU"

    #SBSEurovision, #fucktheEBU2024, #Eurovision2024, #eurovisiongr2024, #eurovissionfuns

Initially, the ```advance_scraper.py``` script was used to locate relevant posts with at least 10 replies. This process generated the file ```Advance2024-05-25_04-20-19_tweets_1-15.csv```, containing 1208 posts.

Subsequently, the URLs of these posts were split into five CSV files for easier management. The ```scraper_comments_from_post.py``` script was then utilized to scrape the replies (tweets) associated with each post.



---

## Prerequisites for Execution

The user must:

- Have the **Firefox browser** installed.
- Download and install **[geckodriver](https://github.com/mozilla/geckodriver/releases)** and properly configure its location.
- Install **uBlock Origin** for blocking ads during navigation:  
  [uBlock Origin Add-on](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/)
- Have the files `tweet.py` and `scroller.py` in the same folder as the main scripts.
- Have a Twitter account.
- Insert their account details (username/email and password) in the appropriate sections of the **advance_scraper.py** and **scraper_comments_from_post.py** files.

---

## File Description

###  `advance_scraper.py`
It finds the URLs of posts that have more than 10 tweets.


### `scraper_commends_from_post.py`
It reads the URLs from the initial data and scrapes the comments of each post.

###  `tweet.py`
It collects data (author, time, content) from each tweet card.

###  `scroller.py`
It handles the page scroll down to load new tweets.

---

### Part Β

### Sentiment Analysis of Tweets for Greece and Israel in Eurovision 2024


#### 1. Data Loading

Google Colab was used to access Google Drive and read the combined_unique_eurovision_valid.csv file. Then, a list of dictionaries was created containing the tweets and their timestamps.

```python
from google.colab import drive
drive.mount('/content/drive')

query = pd.read_csv('/content/drive/MyDrive/combined_unique_eurovision_valid.csv')
tweets = [{'Tweet': row['Content'], 'Timestamp': row['Timestamp']} for index, row in query.iterrows()]
```

---

#### 2. Creating the DataFrame and Cleaning the Data

The tweets were imported into a DataFrame. ```NaN``` values were replaced with empty strings to prevent errors.

```python
df = pd.DataFrame.from_dict(tweets)
df['Tweet'] = df['Tweet'].fillna('')
```

---

#### 3. Defining Keywords

Two lists of keywords related to Greece and Israel (such as "Athens," "Greek culture," "Tel Aviv," "Gaza," etc.) were created. These lists were used to identify whether a tweet referred to either of the two countries.

---

#### 4. Topic Identification

A function named ```identify_subject()``` was defined to check if a tweet contains any of the specified keywords.

```python
def identify_subject(tweet, refs):
    flag = 0
    for ref in refs:
        if ref.lower() in tweet.lower():
            flag = 1
    return flag

df['Israel'] = df['Tweet'].apply(lambda x: identify_subject(x, Israel_handle))
df['Greece'] = df['Tweet'].apply(lambda x: identify_subject(x, Greece_handle))
```

---

#### 5. Sentiment Analysis with TextBlob

For each tweet, the sentiment polarity was calculated using the TextBlob library. Polarity values range from -1 (negative sentiment) to +1 (positive sentiment).
```python
from textblob import TextBlob
df['polarity'] = df['Tweet'].apply(lambda x: TextBlob(x).sentiment.polarity)
```

---

#### 6. Timestamp Conversion and Grouping by Date

Timestamps were converted into date format, and a new column with the corresponding dates was created. Tweets were then filtered to include only those from May 1, 2024, onwards.

```python
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Date'] = df['Timestamp'].dt.date
start_date = pd.to_datetime('2024-05-01').date()
df = df[df['Date'] >= start_date]
```

---

#### 7. Daily Sentiment Calculation & Rolling Average

For each country:
  - Tweets related to the country were filtered.
  - Tweets were grouped by date.
  - The daily average sentiment polarity was calculated.
  - A rolling mean (with a 3-day window) was also computed.

```python
Greece = df[df['Greece']==1][['Date', 'polarity']].groupby('Date').mean().reset_index()
Greece['MA Polarity'] = Greece.polarity.rolling(3, min_periods=1).mean()

Israel = df[df['Israel']==1][['Date', 'polarity']].groupby('Date').mean().reset_index()
Israel['MA Polarity'] = Israel.polarity.rolling(3, min_periods=1).mean()
```

 <p align="left">
  <img src="https://github.com/haris2718/Sentiment_analysis/blob/main/assets/Grece_Polarity.png" width="80%" hspace="10" />  
 </p>
<p align="left">
  <img src="assets/Israel_Polarity.png" width="80%" hspace="10" />  
 </p>
---

#### 8. Visualization of Results

A line chart was created to show the trend of the average daily sentiment polarity and its variation over time.


```python
plt.plot(Greece['Date'], Greece['MA Polarity'], label='Greece MA Polarity', color='blue')
plt.plot(Israel['Date'], Israel['MA Polarity'], label='Israel MA Polarity', color='red')
plt.title('Sentiment Polarity Over Time (from May 1st)')
plt.xlabel('Date')
plt.ylabel('Moving Average Polarity')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```


---

#### Conclusions

From the above analysis, it is possible to track the public’s emotional reaction to events related to the two countries during the competition.
This methodology can be extended to include more countries or time periods and can incorporate advanced NLP techniques for a more accurate understanding of sentiment.

# Sentiment Dynamics Analysis (May 1st – May 26th, 2024)


<p align="left">
  <img src="assets/sentiment_analysis.png" width="100%" hspace="10" />  
 </p>


This figure presents the progression of the 3-day moving average of sentiment polarity for Greece and Israel throughout the period from May 1st to May 26th, 2024, capturing trends and fluctuations in public emotional response as reflected through Twitter data.

Subsequently, major events that occurred within this timeframe are outlined, offering context to the observed variations in sentiment.

---

## 🇬🇷 Greece – Key Events and Analysis

| Date | Event | Link | Correlation with Graph |
|-----------|---------|-----------|------------------------|
| **06/05** | [Announcements about Marina Satti (Eurovision)](https://www.radiotimes.com/tv/entertainment/marina-satti-greece-eurovision-2024-profile-age-instagram/) | 📎 | Upward trend in positive sentiment polarity. |
| **07/05** | [	Eurovision Semi-final A ](https://program.ert.gr/details.asp?pid=3953653&chid=9) | 📎 | 	Peak in positive sentiment polarity (~0.14). |
| **09/05** | [	Eurovision Semi-final B – Greece’s participation](https://press.ert.gr/grafeio-typou-ert/eurovision-2024-me-tin-ellada-kai-ti-marina-satti-ston-v-imiteliko-pempti-9-ma-oy-2024-stis-22-00/) | 📎 | 	Gradual decline. |
| **10/05** | [	Viral reaction of Satti to Israeli representative](https://www.enikos.gr/media/eurovision-2024-marina-satti-oi-gkrimatses-to-chasmourito-kai-o-ypnos-tin-ora-pou-milouse-i-ekprosopos-tou-israil/2155051/) | 📎 | Increase in positive sentiment polarity. |
| **11/05** | [Eurovision Final – Greece finished 11th](https://www.protothema.gr/life-style/article/1496616/eurovision-2024-megalos-telikos-apotelesmata/) | 📎 |Drop in positive sentiment polarity. |
| **12/05** | [Reactions to Marina Satti’s dancers](https://www.protothema.gr/life-style/article/1496813/eurovision-suggnomi-zitoun-oi-horeutes-tis-marinas-satti-meta-tis-adidraseis-gia-ti-dilosi-tous-gia-tin-tourkia/) | 📎 | Significant drop in positive sentiment. |
| **After 16/05** | — | — | Gradual decline / stagnation in sentiment polarity. |

---

## 🇮🇱 Israel – Key Events and Analysis

| Date | Event | Link | Correlation with Graph |
|-----------|---------|-----------|------------------------|
| **06/05** | [Israeli invasion of Rafah	](https://www.cnn.gr/kosmos/story/418037/rafa-me-to-daxtylo-sti-skandali-to-israil-nea-eksodos-xiliadon-amaxon) | 📎 |Small drop or stagnation in sentiment polarity.  |
| **13/05** | [Memorial Day ](https://www.timesofisrael.com/liveblog_entry/israels-ny-consul-at-memorial-day-event-every-single-household-knows-a-victim/) | 📎 | Small increase due to collective sentiment. |
| **17/05** | [Recovery of 3 hostages by IDF](https://www.bankingnews.gr/index.php?id=738200) / [Israel Hayom](https://www.israelhayom.com/2024/05/17/israeli-forces-recover-bodies-of-3-captives-in-daring-gaza-raid/) | 📎 | Noticeable rise in sentiment polarity (emotion – national unity). |
| **20/05** | [Helicopter crash of Iranian President Raisi – Israeli statement	](https://www.ieidiseis.gr/kosmos/247461/israil-den-riksame-emeis-to-elikoptero-oyte-dakry-gia-ton-raisi) | 📎 | Noticeable drop in sentiment polarity. |
| **24/05** | [Recovery of another 3 hostages ](https://www.bbc.com/news/articles/cjrr9wqjnveo) | 📎 | New rise in sentiment polarity – intense emotion. |

---

## 📌 Conclusions

- **Greece** showed a peak in **positive sentiment on May 6-7** due to Eurovision. This was followed by a **decline** due to negative reactions to the aftermath.
- **Israel** exhibited contradictory trends: negative events such as the **Rafah invasion, war, and helicopter crash caused a drop** in sentiment polarity, while a **significant rise was observed on dates when the recovery of hostages was announced** (May 17 & 24), likely due to patriotic pride and relief.
- The graph reflects the cultural influence in Greece’s case and the emotional intensity due to war in Israel’s case.






## Problems & Solutions

- Issues caused by ads during scraping were resolved by using uBlock. **uBlock**.
-  Twitter, being a **dynamic page**, required scrolling through the scroller.py. `scroller.py`.

---

## Results

- 1208 posts and 32,134 unique tweets were collected.
- After scraping the replies, a dataset ideal for **sentiment analysis** was created.


