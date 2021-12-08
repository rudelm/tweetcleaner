import tweepy
import json
from datetime import datetime
import pytz
import sys
import argparse
import logging

import credentials

utc = pytz.UTC
delete_everything_before = utc.localize(datetime(2021, 12, 1))

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description='A tool for automated deletion of Twitter tweets before a given time'
)
parser.add_argument(
    '-v', '--verbose',
    help="Verbose logging",
    action="store_true"
)

args = parser.parse_args()
if args.verbose:  
    logging.basicConfig(level=logging.DEBUG)


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
        logger.error('Twitter archive not found in file ' + file)
        sys.exit(1)

def write_report_json(data):
    """
    writes a JSON report of the execution
    """
    timestring = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = 'report-' + timestring + '.json'
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, sort_keys=True, indent=4)
        return filename
    except Exception:
        logger.error('Could not write ' + filename)
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
        logger.debug('Tweet found to delete: ' + json.dumps(tweet))
        tweets_marked_old.append(tweet)

print(len(tweets_marked_old), 'tweets found and marked for deletion.')

# build list of marked status IDs
to_delete_ids = []
delete_count = 0
deleted_ids = []

failed_ids = []
failed_count = 0

report_data = {}

for tweet in tweets_marked_old:
   to_delete_ids.append(tweet['id'])

# delete marked tweets by status ID
for status_id in to_delete_ids:
    try:
        #api.destroy_status(status_id)
        logger.debug(status_id + ' deleted!')
        deleted_ids.append(status_id)
        delete_count += 1
    except tweepy.TweepyException as e:
        logger.error(status_id + ' could not be deleted, because ' + e)
    except tweepy.HTTPException as e:
        logger.error(status_id + ' could not be deleted, because ' + e.api_codes)
        failed_count += 1
        failed_ids.append(status_id)

print(delete_count, 'tweets deleted.')
print(failed_count, 'tweets unable to delete.')

report_data['deleted'] = deleted_ids
report_data['failed'] = failed_ids

print('A report of what happened can be found in ' + write_report_json(report_data))