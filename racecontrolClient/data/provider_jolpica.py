from racecontrolClient.utils.config import ERGAST_BASE
from racecontrolClient.utils.http import retry_get

def fetch_json(path: str) -> dict:
    url = f"{ERGAST_BASE}{path}"
    r = retry_get(url)
    try:
        return r.json()
    except Exception:
        return {}

class JolpicaProvider:
    """Thin Jolpica/Ergast-compatible data provider."""

    def schedule_json(self, season: str):
        return fetch_json(f"/{season}.json")

    def driver_standings_json(self, season: str):
        return fetch_json(f"/{season}/driverStandings.json")

    def constructor_standings_json(self, season: str):
        return fetch_json(f"/{season}/constructorStandings.json")

    def round_results_json(self, season: str, rnd: int):
        return fetch_json(f"/{season}/{rnd}/results.json")

    def last_results_json(self, season: str):
        return fetch_json(f"/{season}/last/results.json")