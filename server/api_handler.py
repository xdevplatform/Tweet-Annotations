import requests

class User_Lookup: 
    """
    https://api.twitter.com/2/users/by
    https://developer.twitter.com/en/docs/twitter-api/users/lookup/introduction 
    """

    def __init__(self, authentication):
        """
        :param authentication: Authentication object (see authentication.py)     
        """
        self.url = "https://api.twitter.com/2/users/by"
        self.auth = authentication.bearer_oauth
        self.headers = {"Content-Type": "application/json"}
    
    def __call__(self, usernames):
        """
        :param query: str (one or multiple usernames, comma separated with no whitespace)
        :return: User object for given user(s).
        """
        payload = {"usernames": usernames}
        return requests.request(
            "GET",
            url=self.url,
            auth=self.auth,
            headers=self.headers,
            params=payload,
        ) 

class User_Tweet_Timeline: 
    """
    GET /2/users/:id/tweets
    https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/introduction 
    """

    def __init__(self, authentication):
        """
        :param authentication: Authentication object (see authentication.py)     
        """
        self.auth = authentication.bearer_oauth
        self.headers = {"Content-Type": "application/json"}

    def __call__(self, user_id):
        """
        :param user_id: str
        :return: List of recent activity (Tweets, retweets, quote Tweets, replies) for given user. 
        """ 
        url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        return requests.request(
            "GET",
            url=url,
            auth=self.auth,
            headers=self.headers
        )

class Follows_Lookup: 
    """
    GET /2/users/:id/followers
    https://developer.twitter.com/en/docs/twitter-api/users/follows/introduction 
    """

    def __init__(self, authentication):
        """
        :param authentication: Authentication object (see authentication.py)     
        """
        self.auth = authentication.bearer_oauth
        self.headers = {"Content-Type": "application/json"}

    def __call__(self, user_id):
        """
        :param user_id: str
        :return: List of followers for given user. 
        """ 
        url = f"https://api.twitter.com/2/users/{user_id}/followers"
        return requests.request(
            "GET",
            url=url,
            auth=self.auth,
            headers=self.headers
        )

class Recent_Search: 
    """
    GET /2/tweets/search/recent
    https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction 
    """

    def __init__(self, authentication):
        """
        :param authentication: Authentication object (see authentication.py)     
        """
        self.url = "https://api.twitter.com/2/tweets/search/recent"
        self.auth = authentication.bearer_oauth
        self.headers = {"Content-Type": "application/json"}

    def __call__(self, query, next_token=None):
        """
        :param query: str
        :param next_token: str (optional)
        :return: Tweet payload and annotations data for results matching query in previous 7 days.
        """
        
        payload = {"query": query, "tweet.fields": "context_annotations,entities", "max_results": "100"}
        if next_token != None:
            payload.update(next_token=next_token)
        return requests.request(
            "GET",
            url=self.url,
            auth=self.auth,
            headers=self.headers,
            params=payload,
        )
