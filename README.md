# tweetcleaner
A twitter tweet cleaner written in python

Inspired by [this blog](https://pushpullfork.com/i-deleted-tweets/) post, [I've started to cleanup old tweets from my own account at the end of a year](https://centurio.net/2019/01/01/howto-mass-delete-old-tweets-on-twitter/). The code in this repo is based upon his code but is updated and refined to my needs.

First of all, the current twitter exports aren't anymore in CSV format. Therefore the python script needed some modification to work. It is now part of a JavaScript, but by removing the JavaScript assignment of `window.YTD.tweets.part0 = `, we'll get a valid JSON array of Hashes containing all relevant tweet data.

Second, there are some pitfalls with the twitter API I want to document. You'll need to create API credentials with `Read and Write` permissions, otherwise your script won't be able to delete anything at all.

# Changelog

## 2022
[Elon Musk bought Twitter on 27/10/2022](https://en.wikipedia.org/wiki/Acquisition_of_Twitter_by_Elon_Musk). Many people started to clean up their twitter accounts and moved over to [Mastodon](https://en.wikipedia.org/wiki/Mastodon_(software)). So I've decided to update this repo a little bit earlier this year, as the need for it will probably be large.

* The archive file containing all the tweet data is now named `tweets.js` instead of `tweet.js`
* The JavaScript assignment also changed to reflect on the changed filename

## 2021
* Updated tweepy library
* fixed bugfixes
* added better error handling and output
* added verbose mode
* added report.json

## 2020
* Initial release

# ToDos
* some tweets aren't deleted because they were retweets. Those need a special handling for "unretweeting"
* show progress n/x tweets deleted and/or failed
* show time used

# Requesting your Twitter archive
This step can take some time up to several days, so I recommend to start with this first.
* Go to [twitter.com](https://twitter.com)
* Open `More`
* Select `Settings and Privacy`
* Check if you've setup a valid phone number and valid email under `Your Account`, `Account information` - The phone number is required for getting developer credentials and the email is required for receiving a download link of the archive
* Return to `Your Account` (where you also found `Account information`) and select `Download an archive of your data`
* Click on `Request archive` to start the process of gathering your twitter data
* After some time (24h or longer can be normal) you'll receive an email with an download link as well as a notification in the mobile apps and/or in the web app
* Download the archive. Be aware, that this archive might be large and download speeds can be really slow (around 100kb/s)
* The download link can only be used once, so take care when you'll want to download the archive
* extract the archive next to the `tweetcleaner.py` script, so that you'll get two folders `data` and `assets` next to the `Your archive.html`. The tweetcleaner will search for the file `./data/tweets.js` relative to its position. You can also change the path to file to your liking

# Setup python3 environment
Clone this repo to your machine. You can setup a python3 virtual environment, if you want to keep things clean.

## Setting up a virtualenv
Do all of these things inside the repos folder:
```
virtualenv -p python3 myenv
source myenv/bin/activate
pip3 install -r requirements.txt
```

# Create Twitter developer credentials
* Go to [developer.twitter.com](https://developer.twitter.com).
* Open the `Developer Portal`
* Open `Project & Apps`, then `Overview`
* Create a new `Standalone App`
* Name your app like `yourusername-tweetcleaner`
* Copy the `API key`
* Copy the `API secret key`
* Go to `App Settings`
* Set the `App Permissions` from `Read` to `Read and Write` - This is important, otherwise you'll won't be able to delete tweets
* Go to `Keys and tokens`
* Generate `Access Tokens`
* Copy the `Access Token`
* Copy the `Access Token Secret`

# Setup tweetcleaner
* create a copy or rename `example.credentials.py` to `credentials.py`
* Insert the copied credentials at the top of the `credentials.py`
* Set the date for `delete_everything_before`. All old tweets before this date will be deleted 

# Execute tweetcleaner
By default, the script will only analyze your data without executing any deletion. If you're satisfied with the results, you can rerun the command with the `-d` or `--delete` parameter.

Execute the script by using `python3 tweetcleaner.py`.

Here's an example output:

```
...
1951 tweets deleted.
0 tweets unable to delete.
A report of what happened can be found in report-20211210-003341.json
```

## Error handling
Sometimes, tweets cannot be properly deleted. This might look like this output:

```
python3 tweetcleaner.py -d
1259 tweets found and marked for deletion.
1506536934700731337 could not be deleted, because 403 Forbidden
200 - Forbidden.
1258 tweets deleted.
1 tweets unable to delete.
A report of what happened can be found in report-20221029-143105.json
```

In this case, the `report-20221029-143105.json` will also contain the failed id, in case you've already closed your terminal and lost the output. You should manually open the tweet id under your twitter profile, like https://twitter.com/<twittername>/status/<tweetIDthatFailed>. Now you can decide what you want to do about that tweet. In most cases, its a retweet that could not be unretweeted. This is one of the open ToDos.
