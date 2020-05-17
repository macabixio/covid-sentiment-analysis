import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Secretos de Twitter API
ckey = "ckey"
csecret = "csecret"
atoken = "atoken"
asecret = "asecret"

# Coordenada de Uruguay (https://boundingbox.klokantech.com/)
uruguay=[-58.6,-34.99,-53.01,-29.98]

# Creamos archivo para guardar tweets
file = open('./raw_tweets.csv',  'a')

class listener(StreamListener):
    def on_connect(self):
        print ("Conectado!")

    def on_data(self, data):
        # Twitter retorna la data en formato JSON, necesitamos decodificarlo
        try:
            decoded = json.loads(data)
        except Exception as e:
            print (e)
            return True

        # Si tweet contiene la data de la coordenada, la incluimos
        if decoded.get('geo') is not None:
            location = decoded.get('geo').get('coordinates')
        else:
            location = '[,]'

        # Removemos saltos de lineas
        text = decoded['text'].replace('\n',' ')

        # Codificamos autor de tweet
        user = '@' + decoded.get('user').get('screen_name')

        # Obtenemos fecha de tweet
        created = decoded.get('created_at')

        # Creamos fila de tweet
        tweet = '%s|%s|%s|%s\n' % (user,location,created,text)

        # Escribimos el tweet en el archivo
        file.write(tweet)

        return True

    def on_error(self, status):
        print (status)

if __name__ == '__main__':
    print ('Starting')

    # Autenticacion a twitter
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    # Nos quedamos escuchando y guardando tweets
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=uruguay)
