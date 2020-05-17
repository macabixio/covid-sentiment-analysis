# - *- coding: utf- 8 - *-

import re
import nltk
import numpy as np
import pandas as pd

from nltk.stem.snowball import SpanishStemmer

# Abro el csv
df = pd.read_csv("./clean_tweets.csv")

# Elimina una expresion regular de una cadena de texto
def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt


# Elimina autor del tweet
df = df.drop(columns=['user'])

# Elimina usernames del tweet
df['tiny_tweet'] = np.vectorize(remove_pattern)(df['tweet'], "@[\w]*")

# Eliminar puntuacion, numeros y caracteres especiales
df['tiny_tweet'] = df['tiny_tweet'].str.replace("[^a-zA-Z#]", " ")

# Elimina palabras cortas (menos de 3 caracteres)
df['tiny_tweet'] = df['tiny_tweet'].apply(
    lambda x: ' '.join([w for w in x.split() if len(w) > 3]))

# Tokenizar tweets
df['tokens'] = df['tiny_tweet'].apply(lambda x: x.lower().split())

# Stemming
stemmer = SpanishStemmer()
df['stems'] = df['tokens'].apply(lambda x: [stemmer.stem(i) for i in x])

# Guardo un dataset ya limpio
df.to_csv('./processed_tweets.csv', index=False)
