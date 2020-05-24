from urllib.parse import urljoin

import os
import requests


class Eventbrite(requests.Session):
    base_url = "https://www.eventbriteapi.com/v3/"

    def __init__(self):
        super().__init__()
        self._set_header_token()

    def request(self, method, url, *args, **kwargs):
        """Send the request after generating the complete URL."""
        url = self.create_url(url)
        print(url)
        return super().request(method, url, *args, **kwargs)

    def create_url(self, url):
        """Create the URL based off this partial path."""
        return urljoin(self.base_url, url)

    def _set_header_token(self):
        token = os.environ.get("EVENTBRITE_TOKEN", None)
        if not token:
            raise ValueError("EVENTBRITE_TOKEN environmental variable not set")
        self.headers.update({"Authorization": f"Bearer {token}"})
