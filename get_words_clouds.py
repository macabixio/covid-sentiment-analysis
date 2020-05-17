# - *- coding: utf- 8 - *-

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Abro el csv
df = pd.read_csv("./train_covid_tweets.csv")


all_words = [text.lower() for text in df['tiny_tweet'][df['score'] == 1]]

words_string = ' '.join(all_words)

wordcloud = WordCloud(width=1200, height=800, random_state=21, max_font_size=110).generate(words_string)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()
