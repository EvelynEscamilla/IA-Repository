import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

API_KEY = 'ZSay48KtBK1o4nQHdqOxQcbog'
API_SECRET = 'NwzVSptRA8bOdV2EP1RaESdU9R0R5Oi8dO30WF57OOLNpVFoB9'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMHkxQEAAAAAOr6afhqdTpiG64%2FyKs43zKK6%2F%2BY%3DjjUMp2sl7nYcAaeCk04FW9HJWCtPk4Oqzn5qPmI1uOAmTefjri'

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def buscar_tweets(query, max_tweets=100):
    tweets = []
    try:
        response = client.search_recent_tweets(
            query=query,
            tweet_fields=["text"],
            max_results=min(max_tweets, 100)
        )
        if response.data:
            for tweet in response.data:
                tweets.append(tweet.text)
    except tweepy.TweepyException as e:
        print(f"Error: {e}")
    return tweets

def main():
    palabra_clave = "Ley de Organismos Autónomos"
    resultados = buscar_tweets(palabra_clave, max_tweets=50)
    
    if resultados:
        df = pd.DataFrame(resultados, columns=["Texto del Tweet"])
        print("Primeros resultados:")
        print(df.head(10))
        
        df.to_csv("tweets_texto.csv", index=False)
    else:
        print("No se encontraron tweets.")

if __name__ == "__main__":
    main()
