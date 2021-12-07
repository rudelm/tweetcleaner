import tweepy
import json
from datetime import datetime
import pytz
import sys

import credentials

utc = pytz.UTC
delete_everything_before = utc.localize(datetime(2021, 12, 1))

def read_json(file):
    """
    reads a JSON file into a list dictionaries
    """
    try:
        with open(file, encoding = 'utf-8') as jsonfile:
            file_content = jsonfile.read()

            # the Twitter tweet.js is a JavaScript file and cannot be parsed as json directly
            # remove the variable assignment first before its loaded into a json dictionary
            json_content = file_content.strip('window.YTD.tweet.part0 = ')

            json_list = json.loads(json_content)
        return(json_list)
    except Exception:
        print('Twitter archive not found in file ', file)
        sys.exit(1)

tweets = read_json('./data/tweet.js')

auth = tweepy.OAuthHandler(credentials.api_key, credentials.api_secret_key)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)
api = tweepy.API(auth)
# Get the User object for twitter...
user = api.get_user(screen_name='twitter')
print("Authenticated as: %s" % user.screen_name)

tweets_marked_old = []
retweets_marked_old = []

for entry in tweets:
    tweet = entry['tweet']
    created_at = tweet['created_at']
    # parse string into datetime, e.g. "Mon Jul 15 09:34:01 +0000 2013"
    created_at_datetime = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
    if (created_at_datetime < delete_everything_before):
        print('Tweet found to delete:')
        #print(json.dumps(tweet))
        tweets_marked_old.append(tweet)

print(len(tweets_marked_old), 'tweets marked for deletion.')

for tweet in tweets_marked_old:
   print(json.dumps(tweet))

# build list of marked status IDs
to_delete_ids = []
delete_count = 0

failed_ids = []
failed_count = 0

for tweet in tweets_marked_old:
   to_delete_ids.append(tweet['id'])

# delete marked tweets by status ID
for status_id in to_delete_ids:
    try:
        #api.destroy_status(status_id)
        print(status_id, 'deleted!')
        delete_count += 1
    except tweepy.TweepyException as e:
        print(status_id, 'could not be deleted, because ', e)
    except tweepy.HTTPException as e:
        print(status_id, 'could not be deleted, because ', e.api_codes)
        failed_count += 1
        failed_ids.append(tweepy['id'])

print(delete_count, 'tweets deleted.')
print(failed_count, 'tweets unable to delete.')
print('full list of failed IDs:')
print(*failed_ids, sep = ", ") 
