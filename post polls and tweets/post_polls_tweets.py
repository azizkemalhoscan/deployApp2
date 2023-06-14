import tweepy,os,json
import asyncio
import random
from time import sleep
import openai
from telegram import Bot
from html import unescape

# from telegram.ext import ApplicationBuilder, PollHandler, ContextTypes, filters, MessageHandler,CallbackQueryHandler
openai.api_key = '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'
model_engine = "text-davinci-003"

def generate_response(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=90, # Set maximum number of tokens to 286
        n=1,
        stop=None,
        temperature=0.75,
        )
    message = completions.choices[0].text
    return message


def get_client():
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAGuymQEAAAAAxnpN93qcaMSTskKN7iKtDHKBKug%3DWCq7GSMddig30x3wyMNyDXBP8r2rMLe5jEmzSqQE10XdLmcP3l"
    consumer_key = 'eZDrQmfG51xwqSj4itv5LMOWk'
    consumer_key_secret = 'Dp1IELfDlbssXVAfxJsn0FgRDthNy1UWVmjxHwvZIaQGFjpdTq'
    access_token = '1237878915793702912-yAdaYFWHmpGTNEoMqMFupSsgJKM8Nj'
    access_token_secret = '6bMxUH94pss9bVy8fC6r4pguev6tSt424iYP3mfO3nwok'
    client = tweepy.Client(bearer_token,consumer_key,consumer_key_secret,access_token,access_token_secret)
    return client


async def handle_new_tweet(tweet,bot):
    text = tweet.text
    text = unescape(text)
    words = text.split()
    for word in words[:]:
        if '@' in word:
            words.remove(word)
    message = ' '.join(words)
    message = message.strip().strip()
    listOfTones = ["Sarcasm", "Satiric", "Playful", "Humorous"]
    randomListOfTones = random.choice(listOfTones)
    new_tweet_string = generate_response(f'Tweet: "{message}"\nAI, please paraphrase the tweet with an "{randomListOfTones}"" tone. Translate it into Turkish and add great hashtags. Provide me with the final result.')
    await bot.send_poll(chat_id=-977935709, question=new_tweet_string,options=['Post it',"Don't post it"],open_period=100)


def handle_previous(client):
    with open('results.json','r')as fp:
        results=json.load(fp)
    if results:
        result = results.pop()
        if result['shoot']>result['hold']:
            print(result['Question'])
            client.create_tweet(text =  result['Question'])


def main():
    client =  get_client()
    bot = Bot(token='5942564261:AAHAxGhNQVlWQlfEh7HvuOV563EN4oukPG4')

    me =client.get_me().data

    list_id = client.get_owned_lists(me.id).data[0].id

    tweets =  client.get_list_tweets(list_id,user_auth=True,max_results=1)
    if "since_id.txt" not in os.listdir():
        with open('since_id.txt','w') as f:
            f.write(str(1))
    with open('since_id.txt','r') as f:
        since_id = f.read().strip()
    for tweet in tweets.data:
        if (str(tweet.id) > since_id) and tweet.text[:2] != 'RT' :
            asyncio.run(handle_new_tweet(tweet,bot))
            with open('since_id.txt','w') as f:
                f.write(str(tweet.id))
            break
    handle_previous(client)
if __name__ == '__main__':
    main()
