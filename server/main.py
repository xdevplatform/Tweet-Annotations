import json
import random
from server.api_handler import (
    ApiHandler
)
from server.authentication import (
    Authentication
)

authentication = Authentication()

def get_user_details(username):
    
    username = username.lstrip("@")

    user_lookup = ApiHandler("users/by", authentication)
    response = user_lookup(payload={"usernames": username})
    
    if response.status_code != 200:
        print("Could not load user. Error code:", response.status_code)
        user_id = None
    else: 
        data = json.loads(response.text)
        user_id = data["data"][0]["id"]
    
    return username, user_id

def get_user_tweet_timeline(user_id):

    tweets = []
    user_tweet_timeline = ApiHandler(f"users/{user_id}/tweets", authentication)
    #To return all 3200 available activities for the user, remove the start_time parameter from the payload below:
    payload = {"tweet.fields": "context_annotations,entities", "max_results": "100", "start_time": "2021-03-04T12:00:00Z"}
    response = user_tweet_timeline(payload)
    if response.status_code != 200:
        print("Response", response.status_code, response.text)
    else:
        data = json.loads(response.text)
        request_count = 1
        if "data" in data:
            for tweet in data["data"]:
                tweets.append(tweet)
            while "next_token" in data["meta"]:
                pagination_token = data["meta"]["next_token"]
                payload.update(pagination_token=pagination_token)
                response = user_tweet_timeline(payload)
                if response.status_code != 200:
                    print("Response:", response.status_code)
                    break
                data = json.loads(response.text)
                request_count += 1
                if "data" in data:
                    for tweet in data["data"]:
                        tweets.append(tweet)
            print("Request count:", request_count)
            print("Code:", response.status_code)
    
    return tweets, response.status_code

def get_user_tweet_timeline_no_pagination(user_id):
    
    tweets = []
    user_tweet_timeline = ApiHandler(f"users/{user_id}/tweets", authentication)
    payload = {"tweet.fields": "context_annotations,entities", "max_results": "10"}
    response = user_tweet_timeline(payload)
    if response.status_code != 200:
        print("Response", response.status_code, response.text)
    else:
        data = json.loads(response.text)
        if "data" in data:
            for tweet in data["data"]:
                tweets.append(tweet)
    
    return tweets, response.status_code

def get_user_followers(user_id):
    
    followers = []
    user_followers = ApiHandler(f"users/{user_id}/followers", authentication)
    payload = {"max_results": "1000", "user.fields": "public_metrics"}
    response = user_followers(payload)
    if response.status_code != 200:
        print("Response:", response.status_code, response.text)
    else: 
        data = json.loads(response.text)
        request_count = 1 
        if "data" in data:
            for follower in data["data"]:
                followers.append(follower)
            while "next_token" in data["meta"]:
                pagination_token = data["meta"]["next_token"]
                payload.update(pagination_token=pagination_token)
                response = user_followers(payload)
                if response.status_code != 200:
                    print("Response:", response.status_code)
                    break
                data = json.loads(response.text)
                request_count += 1
                if "data" in data:
                    for follower in data["data"]:
                        followers.append(follower)
            print("Request count:", request_count) 
    
    return followers, response.status_code

def random_selection(followers, follower_count):
    
    # Randomly select 50 followers, from whom to analyze annotations data.
    if follower_count > 50: 
        # .seed() method makes the random selection deterministic
        random.seed(56)
        selection = random.sample(followers, k=50)
    else: 
        selection = followers
    
    return selection

def get_annotations(tweets):
    
    domain = []
    entity = []
    person = []
    place = []
    product = []
    organization = []
    other = []

    tweet_count = 0

    try: 
        for tweet in tweets:
            tweet_count += 1

            if "context_annotations" in tweet:
                for annotation in tweet["context_annotations"]: 
                    domain.append(annotation["domain"]["name"])
                    entity.append(annotation["entity"]["name"])
                    
            if "entities" in tweet:
                if "annotations" in tweet["entities"]:
                    for annotation in tweet["entities"]["annotations"]:
                        if annotation["probability"] >= 0.5:
                            if annotation["type"] == "Person":
                                person.append(annotation["normalized_text"])
                            elif annotation["type"] == "Place":
                                place.append(annotation["normalized_text"])
                            elif annotation["type"] == "Product":
                                product.append(annotation["normalized_text"])
                            elif annotation["type"] == "Organization":
                                organization.append(annotation["normalized_text"])
                            elif annotation["type"] == "Other":
                                other.append(annotation["normalized_text"])
                            else:
                                pass

        domain_frequency = {d:domain.count(d) for d in domain} 
        entity_frequency = {e:entity.count(e) for e in entity} 

        domain_frequency_ordered = {k: v for k, v in sorted(domain_frequency.items(), key=lambda item: item[1], reverse=True)}
        entity_frequency_ordered = {k: v for k, v in sorted(entity_frequency.items(), key=lambda item: item[1], reverse=True)} 

        person_frequency = {i:person.count(i) for i in person}
        place_frequency = {i:place.count(i) for i in place}
        product_frequency = {i:product.count(i) for i in product} 
        organization_frequency = {i:organization.count(i) for i in organization}
        other_frequency = {i:other.count(i) for i in other}

        person_frequency_ordered = {k: v for k, v in sorted(person_frequency.items(), key=lambda item: item[1], reverse=True)}
        place_frequency_ordered = {k: v for k, v in sorted(place_frequency.items(), key=lambda item: item[1], reverse=True)}
        product_frequency_ordered = {k: v for k, v in sorted(product_frequency.items(), key=lambda item: item[1], reverse=True)}
        organization_frequency_ordered = {k: v for k, v in sorted(organization_frequency.items(), key=lambda item: item[1], reverse=True)}
        other_frequency_ordered = {k: v for k, v in sorted(other_frequency.items(), key=lambda item: item[1], reverse=True)}

        # Only returns annotations and entities that are present in at least 2+ Tweets.
        domain_list_top = {k: v for k, v in domain_frequency_ordered.items() if v >= 2}
        entity_list_top = {k: v for k, v in entity_frequency_ordered.items() if v >= 2}
        person_list_top = {k: v for k, v in person_frequency_ordered.items() if v >= 2}
        place_list_top = {k: v for k, v in place_frequency_ordered.items() if v >= 2}
        product_list_top = {k: v for k, v in product_frequency_ordered.items() if v >= 2}
        organization_list_top = {k: v for k, v in organization_frequency_ordered.items() if v >= 2}
        other_list_top = {k: v for k, v in other_frequency_ordered.items() if v >= 2} 


    except:
        print(f"""
        No topics data to analyse for @{username} in the past week
        """)
        domain_frequency_ordered = None
        entity_frequency_ordered = None
        person_frequency_ordered = None
        place_frequency_ordered = None
        product_frequency_ordered = None 
        organization_frequency_ordered = None
        other_frequency_ordered = None

    print(f"""
    Total number of Tweets returned: {tweet_count}
    """)

    return tweet_count, domain_list_top, entity_list_top, person_list_top, place_list_top, product_list_top, organization_list_top, other_list_top 

def update_annotations(dict1, dict2):

    for k, v in dict2.items():
        if k in dict1:
            dict1[k] += v
        else:
            dict1[k] = v

    return dict1

def get_topics_for_profile_followers():
    """
    Understand topics of interest for a profile’s followers. 
    I.e. What activities and topics are the profile’s followers Tweeting about and engaging with?
    """
    pass

def get_profiles_for_topic():
    """
    Pass in a given topic and get back a list of users who are interested in the topic.
    E.g. Surface a set of profiles who are enthusiastic about skiing.
    """
    pass

def get_tweet_metrics_for_topic():
    """
    Pass in a given topic and get back Tweet metrics for each topic.
    I.e. how often (or not) is a given topic mentioned on the platform?. 
    The full Tweet text is also returned and displayed with associated metrics.
    """
    pass