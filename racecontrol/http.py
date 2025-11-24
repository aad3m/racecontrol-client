import requests

class HttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get(self, path: str):
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None  # dashboard handles empty DataFrame gracefully