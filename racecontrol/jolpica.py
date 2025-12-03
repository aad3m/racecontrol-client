from .utils.http import HttpClient
from .config import ERGAST_BASE


class JolpicaProvider:
    """
    Thin provider around HttpClient, targeting the Jolpica Ergast-compatible API.
    """
    BASE_URL = ERGAST_BASE  # e.g. "https://api.jolpi.ca/ergast/f1"

    def __init__(self, base_url: str | None = None):
        self.http = HttpClient(base_url or self.BASE_URL)

    def fetch(self, endpoint: str):
        """
        Fetch JSON from an endpoint like:
          "/current.json"
          "/2024/driverStandings.json"
        """
        return self.http.get(endpoint)