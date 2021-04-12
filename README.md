# Tweet Annotations 

This sample code shows you how you might build a demo web app with Python and [Flask](https://flask.palletsprojects.com/en/1.1.x/) and exemplifies some of the features and functionality available with the [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api/early-access) and [Tweet Annotations](https://developer.twitter.com/en/docs/twitter-api/annotations). 

## Set up 

* In the root directory, rename `credentials.yaml.template` to `credentials.yaml` and insert your Twitter App credentials. Note that you must use the credentials belonging to a [Twitter Developer App](https://developer.twitter.com/en/docs/apps/overview) with access to the Twitter API v2.

* Don't forget to add `credentials.yaml` to your `.gitignore` file to avoid compromising your App credentials.

## Running the web app locally

Follow these steps to run the web app on your local machine: 
* From the root directory in the command line type: `export FLASK_ENV=development`. (On Windows, use `set` instead of `export`.)
* Then type `flask run`. 
* The web app is now running on your local host (usually something like `http://127.0.0.1:5000/`).
* Further information on configuring your Flask app can be found [here](https://flask.palletsprojects.com/en/1.1.x/config/).

## Functionality

This web app illustrates the following functionality: 

1. Get topics of interest for a profile (including top Tweet Annotations associated with a profile's Tweets and top most used emojis by this profile). 
2. Get topics of interest for a profile's followers. Same functionality as above, but for a user profile's follower base. 
3. For a given topic, get a list of users who recently Tweeted about this topic.
4. For a given topic, get resonance metrics (including number of Tweets sent within the past 7 days, and aggregate engagement metrics, such as retweets, quote Tweets, likes, and replies).