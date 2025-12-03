import time
import requests

from racecontrolClient.utils.config import (
    HTTP_TIMEOUT,
    HTTP_RETRIES,
    HTTP_BACKOFF,
    USER_AGENT,
)

class HTTPError(RuntimeError):
    pass

def retry_get(url: str) -> requests.Response:
    """GET with retries + exponential backoff. Raises HTTPError on failure."""
    err: Exception | None = None
    for i in range(HTTP_RETRIES):
        try:
            r = requests.get(
                url,
                timeout=HTTP_TIMEOUT,
                headers={"User-Agent": USER_AGENT},
            )
            r.raise_for_status()
            return r
        except Exception as e:
            err = e
            if i < HTTP_RETRIES - 1:
                time.sleep(HTTP_BACKOFF * (2 ** i))
    raise HTTPError(str(err) if err else "Unknown network error")