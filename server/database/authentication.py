import os
import yaml
from requests_oauthlib import OAuth1, OAuth1Session


class Authentication:
    """
    Class to handle Twitter credentials to access the API.
    """

    def __init__(self):
        """
        Get app credentials from YAML file.
        """

        with open(r"credentials.yaml") as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)

        self.API_KEY = credentials["v2-app-credentials"]["API_KEY"]
        self.API_SECRET = credentials["v2-app-credentials"]["API_SECRET"]
        self.ACCESS_TOKEN = credentials["v2-app-credentials"]["ACCESS_TOKEN"]
        self.ACCESS_TOKEN_SECRET = credentials["v2-app-credentials"][
            "ACCESS_TOKEN_SECRET"
        ]
        self.BEARER_TOKEN = credentials["v2-app-credentials"]["BEARER_TOKEN"]

    def generate_oauth1(self):
        """
        Generate OAuth1 using app and user credentials.
        :return: OAuth1
        """

        return OAuth1(
            self.API_KEY,
            self.API_SECRET,
            self.ACCESS_TOKEN,
            self.ACCESS_TOKEN_SECRET,
            signature_method="HMAC-SHA1",
            signature_type="query",
        )

    def generate_oauth1_session(self):
        """
        Generate OAuth1 session using app credentials.
        :return: OAuth1 session.
        """

        return OAuth1Session(client_key=self.API_KEY, client_secret=self.API_SECRET)

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.BEARER_TOKEN}"
        r.headers["User-Agent"] = "v2TweetAnnotationsPython"
        return r

    def __str__(self):
        """
        Credentials. 
        :return: str, app and user credentials
        """

        return f"Consumer key: {self.API_KEY} \nConsumer secret: {self.API_SECRET} \nAccess token: {self.ACCESS_TOKEN} \nToken secret: {self.ACCESS_TOKEN_SECRET} \nBearer token: {self.BEARER_TOKEN}"
