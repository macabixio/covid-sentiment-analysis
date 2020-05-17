# - *- coding: utf- 8 - *-

import re
import nltk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from wordcloud import WordCloud

# Abro el csv
df = pd.read_csv("./train_covid_tweets.csv")

# Obtener hashtags de tweet
def hashtag_extract(x):
    hashtags = []
    # Loop over the words in the tweet
    for i in x:
        ht = re.findall(r"#(\w+)", i)
        hashtags.append(ht)

    return hashtags

HT_neutral = hashtag_extract(df['tiny_tweet'][df['score'] == 0.5])
HT_positive = hashtag_extract(df['tiny_tweet'][df['score'] == 1])
HT_negative = hashtag_extract(df['tiny_tweet'][df['score'] == 0])

HT_neutral = sum(HT_neutral,[])
HT_negative = sum(HT_negative,[])
HT_positive = sum(HT_positive,[])

a = nltk.FreqDist(HT_positive)

d = pd.DataFrame({'Hashtag': list(a.keys()),
                  'Count': list(a.values())})

# Selecciono los 10 mas frecuentes
d = d.nlargest(columns="Count", n = 10)
plt.figure(figsize=(16,5))
ax = sns.barplot(data=d, x= "Hashtag", y = "Count")
ax.set(ylabel = 'Count')
plt.show()
