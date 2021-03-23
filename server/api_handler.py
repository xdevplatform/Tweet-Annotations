import requests


class ApiHandler:
    """
    Class for making requests to the Twitter API v2
    https://developer.twitter.com/en/docs/twitter-api/early-access
    """

    def __init__(self, path, authentication):
        """
        :param path: Endpoint path.
        :param authentication: Authentication object (see authentication.py).
        """

        base_url = "https://api.twitter.com/2/"

        self.url = base_url + path
        self.auth = authentication.bearer_oauth
        self.headers = {"Content-Type": "application/json"}

    def __call__(self, payload=None):
        """
        :param params: str
        :param payload: dict
        """
        return requests.request(
            "GET", url=self.url, auth=self.auth, headers=self.headers, params=payload,
        )
