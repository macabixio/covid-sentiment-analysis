# - *- coding: utf- 8 - *-

import pandas as pd
from tqdm import tqdm
from langdetect import detect

# Abro el txt
df = pd.read_csv("./raw_tweets.csv", delimiter='|',
                 header=None, names=['user', 'location', 'timestamp', 'tweet'], error_bad_lines=False, warn_bad_lines=False)

#Elimino las filas vacías
df = df.dropna()

#Elimino filas con tweets duplicados
df = df.drop_duplicates()

#Elimno todos los tweets que son largos y la API lo trajo con URL`s
df = df[~df['tweet'].str.contains("https://", regex=False)]

#Reordeno los indices
df = df.reset_index()
df = df.drop(columns=['index'])

# Crear la barra de progreso de largo el dataframe
pbar = tqdm(total=len(df))

#Elimino los tweets que no esten en español
a=0
for x in df['tweet']:
    try:
        if (detect(x) != 'es'):
            df = df.drop([a])
    except:
        df = df.drop([a])

    a=a+1
    pbar.update(1)

df = df.reset_index()
df = df.drop(columns=['index'])

# Convertimos fecha y hora a formato datetime para trabajar con él
df['timestamp'] =  pd.to_datetime(df['timestamp'], format='%a %b %d %H:%M:%S %z %Y')

#Guardo un dataset ya limpio
df.to_csv('./clean_tweets.csv')
