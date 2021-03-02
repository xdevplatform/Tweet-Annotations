import json
from server.api_handler import (
    ApiHandler
)
from server.authentication import (
    Authentication
)

authentication = Authentication()

def get_topics_for_profiles():
    """
    Pass in a set of profiles (@handles) and get back topics of interest for each profile. 
    """ 
    pass

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