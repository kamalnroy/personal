import socket
import sys
import requests
import requests_oauthlib
import json
import kafka
from kafka import KafkaProducer
import time
from kafka import SimpleProducer
from kafka import KafkaClient

###################################################
# My own access tokens
####################################################
ACCESS_TOKEN = '28778811-sw3jVlgjtS14kvquuo765rjaIYvCE0iMpTsDXdiRs'
ACCESS_SECRET = 'HBGjT0uixYSC6PXvyewvBuFmHv4FYtU6UmsDG98khY'
CONSUMER_KEY = '2VsrZwlSbtToGYbpHe42hmB36'
CONSUMER_SECRET = 'vuXhfCmMVMwecUzV3hwK8vvkGWZnAM5wtEDvzMMenq6rH8yFqe'

my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

time.sleep(10)
####################################################
# Kafka Producer
####################################################
twitter_topic="twitter_topic"
client = KafkaClient("10.142.0.2:9092")
producer = SimpleProducer(client)
#producer = kafka.KafkaProducer(bootstrap_servers='10.128.0.2:9092')

def get_tweets():
    print("#########################get_tweets called################################")
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    #query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#')]
    #query_data = [('language', 'en'), ('locations', '-3.7834,40.3735,-3.6233,40.4702'),('track','#')]
    query_data = [('language', 'en'), ('locations', '-3.7834,40.3735,-3.6233,40.4702'),('track','Madrid')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    #print("Query url is", query_url)
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response

def send_tweets_to_kafka(http_resp):
    print("########################send_tweets_to_kafka called#################################")
    for line in http_resp.iter_lines():
        print("reading tweets")
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['text']
            print("Tweet Text: " + tweet_text)
            print ("------------------------------------------")
            tweet_text = tweet_text + '\n'
            producer.send_messages(twitter_topic, tweet_text.encode())
            #producer.send(twitter_topic, tweet_text.encode())
            time.sleep(0.2)
        except:
            print("Error received")
            e = sys.exc_info()[0]
            print("Error: %s" % e)
    print("Done reading tweets")


resp = get_tweets()
send_tweets_to_kafka(resp)

