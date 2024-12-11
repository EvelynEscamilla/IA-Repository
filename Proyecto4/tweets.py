import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

API_KEY = 'Kwt3OMhgmm80w5f0dnWGx1Lxw'
API_SECRET = 'vlCgfZitIRE0fzDAsfAZOUhVdY61qUTSWSganmoSeKZZV85yTc'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAAT2xQEAAAAAiIPZds3FG9frc4ehwZ7IR6T2pZk%3DTGWZmFIti64nWImDgu21nBIYbvkEAG5t2zYp7G9ldD1yNac13L'

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
    palabra_clave = "reforma judicial México"
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
