import time
import requests
import streamlit as st

from ..config import HTTP_TIMEOUT, HTTP_RETRIES, HTTP_BACKOFF, USER_AGENT


class HttpClient:
    def __init__(self, base_url: str = ""):
        # Base API URL, like "https://api.jolpi.ca/ergast/f1"
        self.base_url = base_url.rstrip("/")

    def get(self, endpoint: str):
        """
        Perform a GET request with retries and return parsed JSON or None.
        endpoint is joined to base_url.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._retry_get(url)

    def _retry_get(self, url: str):
        err = None
        for i in range(HTTP_RETRIES):
            try:
                r = requests.get(
                    url,
                    timeout=HTTP_TIMEOUT,
                    headers={"User-Agent": USER_AGENT},
                )
                r.raise_for_status()
                return r.json()
            except Exception as e:
                err = e
                if i < HTTP_RETRIES - 1:
                    time.sleep(HTTP_BACKOFF * (2 ** i))

        # mark offline in session_state
        st.session_state["last_error"] = f"{err}" if err else "Unknown network error"
        st.session_state["offline"] = True
        return None