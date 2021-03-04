import os
from flask import Flask, render_template, redirect
from server.main import get_user_details, get_user_tweet_timeline, get_annotations
from forms import GetUsername

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/GetTopicsForProfiles', methods=["post", "get"])
def get_topics_profile():
    form = GetUsername()
    response_code = None
    tweet_count = None
    annotations_data = None
    domain = None 
    entity = None 
    person = None 
    place = None 
    product = None 
    organization = None 
    other = None
    if form.validate_on_submit():
        username = form.username.data
        username, user_id = get_user_details(username)
        if user_id == None:
            annotations_data = 0
        else: 
            user_timeline_tweets, response_code = get_user_tweet_timeline(user_id)
            if response_code != 200: 
                annotations_data = 1
            else: 
                tweet_count, domain, entity, person, place, product, organization, other = get_annotations(user_timeline_tweets)
    
    # domains_count = 0
    # entities_count = 0

    # for i in domains: 
    #     domains_count += 1
    
    # for i in entities: 
    #     entities_count += 1
        
    return render_template('get_topics_for_profiles.html', form=form, annotations_data=annotations_data, tweet_count=tweet_count, domain=domain, entity=entity, person=person, place=place, product=product, organization=organization, other=other, response_code=response_code, methods=["post", "get"])

@app.route('/GetTopicsForProfileFollowers', methods=["post", "get"])
def get_topics_follower_base():
    return render_template('get_topics_for_profile_followers.html', methods=["post", "get"])

@app.route('/GetProfilesForTopic', methods=["post", "get"])
def get_profiles():
    return render_template('get_profiles_for_topic.html', methods=["post", "get"])

@app.route('/GetTweetMetricsForTopic', methods=["post", "get"])
def get_metrics():
    return render_template('get_tweet_metrics_for_topic.html', methods=["post", "get"])

@app.route("/Results", methods=["get"])
def error_page():
    return render_template('results.html', methods=["post", "get"])

# @app.route("/Error", methods=["get"])
# def error_page():
#     return render_template('error.html', methods=["post", "get"])