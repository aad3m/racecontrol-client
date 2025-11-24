from .http import HttpClient

class JolpicaProvider:
    BASE_URL = "https://api.jolpica.com/ergast"

    def __init__(self):
        self.http = HttpClient(self.BASE_URL)

    def fetch(self, endpoint: str):
        return self.http.get(endpoint)