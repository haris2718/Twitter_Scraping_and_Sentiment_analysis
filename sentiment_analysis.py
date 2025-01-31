import pandas as pd
import nltk
from nltk.corpus import stopwords
from textblob import Word, TextBlob
import re
# Διάβασμα δεδομένων από το CSV αρχείο
df = pd.read_csv('euro.csv')
df.head()

# Καθορισμός λιστών με αναφορές στους Trump και Biden
trump_handle = ['DonaldTrump', 'Donald Trump', 'Donald', 'Trump', 'Trump\'s']
biden_handle = ['JoeBiden', 'Joe Biden', 'Joe', 'Biden', 'Biden\'s']

# Ορισμός συνάρτησης για αναγνώριση των ονομάτων σε tweets
def identify_subject(tweet, refs):
    flag = 0
    for ref in refs:
        if tweet.find(ref) != -1:
            flag = 1
    return flag

# Εφαρμογή της συνάρτησης για να βρούμε αν το tweet αναφέρεται στον Trump
df['Trump'] = df['Tweet'].apply(lambda x: identify_subject(x, trump_handle))

# Εφαρμογή της συνάρτησης για να βρούμε αν το tweet αναφέρεται στον Biden
df['Biden'] = df['Tweet'].apply(lambda x: identify_subject(x, biden_handle))

# Εμφάνιση των πρώτων δέκα γραμμών του DataFrame
df.head(10)


nltk.download('stopwords')
nltk.download('wordnet')
stop_words = stopwords.words('english')
custom_stopwords = ['RT', '#PresidentialDebate']

def preprocess_tweets(tweet, custom_stopwords):
    processed_tweet = re.sub(r'[^\w\s]', '', tweet)  # Χρήση re.sub για να αφαιρέσουμε μη αλφαριθμητικούς χαρακτήρες
    processed_tweet = " ".join(word for word in processed_tweet.split() if word not in stop_words)
    processed_tweet = " ".join(word for word in processed_tweet.split() if word not in custom_stopwords)
    processed_tweet = " ".join(Word(word).lemmatize() for word in processed_tweet.split())
    return processed_tweet

df['Processed Tweet'] = df['Tweet'].apply(lambda x: preprocess_tweets(x, custom_stopwords))
df.head()

print('Base review\n', df['Tweet'][0])
print('\n------------------------------------\n')
print('Cleaned and lemmatized review\n', df['Processed Tweet'][0])

# Υπολογισμός polarity
df['polarity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[0])
# Υπολογισμός subjectivity
df['subjectivity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[1])
# Εμφάνιση των πρώτων πέντε σειρών με συγκεκριμένες στήλες
df[['Processed Tweet', 'Biden', 'Trump', 'polarity', 'subjectivity']].head()

# Ομαδοποίηση και υπολογισμός στατιστικών για τα tweets που αναφέρονται στον Trump
display(df[df['Trump']==1][['Trump','polarity','subjectivity']].groupby('Trump').agg([np.mean, np.max, np.min, np.median]))

# Ομαδοποίηση και υπολογισμός στατιστικών για τα tweets που αναφέρονται στον Biden
df[df['Biden']==1][['Biden','polarity','subjectivity']].groupby('Biden').agg([np.mean, np.max, np.min, np.median])

