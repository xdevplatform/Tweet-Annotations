import json
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
    payload = {"tweet.fields": "context_annotations,entities", "start_time": "2021-02-01T15:00:00Z"} 
    # payload = {"tweet.fields": "context_annotations,entities"} 
    response = user_tweet_timeline(payload)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
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
                    print("Error:", response.status_code)
                    break
                data = json.loads(response.text)
                if "data" in data:
                    if tweet in data["data"]:
                        tweets.append(tweet)
                    else: 
                        print("DATA", data)
                        print("RESPONSE CODE", response.status_code)
                        pass
                    request_count += 1
            print("Request count:", request_count)
            print("Code:", response.status_code)
    return tweets, response.status_code

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

        # [To Do -- Figure out how to unpack items from dictionaries below]
        # domain_frequency_ordered = {**domain_frequency_ordered} # Create a shallow copy, to avoid "RuntimeError: dictionary changed size during iteration"
        # print("HEY", domain_frequency_ordered)
        # for k,v in domain_frequency_ordered.items():
        #     if v < 5:
        #         domain_frequency_ordered.pop(k,v)

        # entity_frequency_ordered = {**entity_frequency_ordered}
        # for k,v in entity_frequency_ordered.items():
        #     if v < 5: 
        #         entity_frequency_ordered.pop(k,v)
        
        # person_frequency_ordered = {**person_frequency_ordered}
        # for k,v in person_frequency_ordered.items(): 
        #     if v < 5:
        #         person_frequency_ordered.pop(k,v)
                
        # place_frequency_ordered = {**place_frequency_ordered} 
        # for k,v in place_frequency_ordered.items():
        #     if v < 5:
        #         place_frequency_ordered.pop(k,v)

        # person_frequency_ordered = {**product_frequency_ordered}
        # for k,v in product_frequency_ordered.items():
        #     if v < 5:
        #         product_frequency_ordered.pop(k,v)

        # organization_frequency_ordered = {**organization_frequency_ordered}
        # for k,v in organization_frequency_ordered.items():
        #     if v < 5:
        #         organization_frequency_ordered.pop(k,v)
        
        # other_frequency_ordered = {**other_frequency_ordered}
        # for k,v in other_frequency_ordered.items():
        #     if v < 5:
        #         organization_frequency_ordered.pop(k,v)

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

    return tweet_count, domain_frequency_ordered, entity_frequency_ordered, person_frequency_ordered, place_frequency_ordered, product_frequency_ordered, organization_frequency_ordered, other_frequency_ordered
    print("domain_frequency_ordered", domain_frequency_ordered)

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