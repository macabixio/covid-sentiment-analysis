import nltk
import ast
import numpy as np
import pandas as pd

from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

# Abro el csv
test = pd.read_csv("./test_covid_tweets.csv")
train = pd.read_csv("./train_covid_tweets.csv")

# Combinar df en uno
combi = train.append(test, ignore_index=True)

# Creo la instancia de vector palabras -> apariciones
vectorized = CountVectorizer(
    analyzer='word',
    lowercase=False,
)

# Transformar stems de strings a lista
combi['stems'] = combi['stems'].apply(lambda x: ast.literal_eval(x))

# Transformar lista de stems a string
combi['stems'] = combi['stems'].apply(lambda x: ' '.join(x))

# Crear la BOW
bow = vectorized.fit_transform(combi['stems'])

# Separo el BOW de train y de test (sabiendo de antemano cuantos tweets de train hay)
train_bow = bow[:386, :]
test_bow = bow[386:, :]

# De mis tweets de training, separo algunos para entenar el modelo y otros pra validar que el modelo sea correcto
xtrain_bow, xvalid_bow, ytrain, yvalid = train_test_split(
    train_bow, train['score'], random_state=42, test_size=0.3)

# Creas y entrenas el modelo (con los tweets que separe antes para eso)
lreg = LogisticRegression()
lreg.fit(xtrain_bow, ytrain)

# Mido el score de mi modelo, comparando con el set de validacion
prediction = lreg.predict(xvalid_bow)
score = f1_score(yvalid, prediction, average="micro")

# Imprimir el score de mi modelo
print(score)

# Corro el modelo de prediccion, con mi datadset de prueba
test_pred = lreg.predict(test_bow)

# Guardo el score para cada tweet
test['score'] = test_pred


# Guardo el CSV con los scores actualizados
test.to_csv('covid_tweets_scored.csv', index=False)  # writing data to a CSV file
