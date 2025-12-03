import pandas as pd
import streamlit as st

from ..config import CACHE_TTL, DEFAULT_SEASON
from ..jolpica import JolpicaProvider

# Initialize the provider once
provider = JolpicaProvider()


def _fetch_json(path: str) -> dict:
    """
    Low-level wrapper using the JolpicaProvider (HttpClient underneath).
    path examples:
      "/current.json"
      "/2024/driverStandings.json"
    """
    data = provider.fetch(path)
    if not data:
        st.session_state["offline"] = True
        return {}
    return data


def init_session_flags():
    if "offline" not in st.session_state:
        st.session_state["offline"] = False
    if "last_error" not in st.session_state:
        st.session_state["last_error"] = ""


def clear_and_rerun():
    st.cache_data.clear()
    st.rerun()


@st.cache_data(ttl=CACHE_TTL)
def _schedule_json(season: str) -> dict:
    return _fetch_json(f"/{season}.json")


@st.cache_data(ttl=CACHE_TTL)
def _driver_standings_json(season: str) -> dict:
    return _fetch_json(f"/{season}/driverStandings.json")


@st.cache_data(ttl=CACHE_TTL)
def _constructor_standings_json(season: str) -> dict:
    return _fetch_json(f"/{season}/constructorStandings.json")


@st.cache_data(ttl=CACHE_TTL)
def _round_results_json(season: str, rnd: int) -> dict:
    return _fetch_json(f"/{season}/{rnd}/results.json")


@st.cache_data(ttl=CACHE_TTL)
def _last_results_json(season: str) -> dict:
    return _fetch_json(f"/{season}/last/results.json")


@st.cache_data(ttl=CACHE_TTL)
def get_completed_round(season: str) -> int:
    """
    Returns the latest completed round number for a season.
    """
    data = _last_results_json(season)
    races = (
        data.get("MRData", {})
        .get("RaceTable", {})
        .get("Races", [])
    )

    if not races:
        st.session_state["offline"] = True
        return 0

    try:
        return int(races[0].get("round", 0))
    except Exception:
        return 0


@st.cache_data(ttl=CACHE_TTL)
def get_schedule(season: str) -> pd.DataFrame:
    data = _schedule_json(season)
    races = (
        data.get("MRData", {})
        .get("RaceTable", {})
        .get("Races", [])
    )

    rows = []
    for r in races:
        round_num = int(r.get("round", 0) or 0)
        name = r.get("raceName", "")
        circuit = (r.get("Circuit") or {}).get("circuitName", "")
        loc = (r.get("Circuit") or {}).get("Location") or {}
        country = loc.get("country", "")
        city = loc.get("locality", "")
        date = r.get("date", "")
        time = r.get("time", "") or "00:00:00Z"

        dt_utc = pd.to_datetime(f"{date}T{time}", utc=True, errors="coerce")

        rows.append(
            {
                "round": round_num,
                "name": name,
                "circuit": circuit,
                "country": country,
                "city": city,
                "date": date,
                "time": time,
                "datetime_utc": dt_utc,
            }
        )

    if not rows:
        st.session_state["offline"] = True
        return pd.DataFrame()

    return pd.DataFrame(rows).sort_values("round").reset_index(drop=True)


@st.cache_data(ttl=CACHE_TTL)
def get_driver_standings(season: str) -> pd.DataFrame:
    data = _driver_standings_json(season)
    lists = (
        data.get("MRData", {})
        .get("StandingsTable", {})
        .get("StandingsLists", [])
    )

    if not lists:
        st.session_state["offline"] = True
        return pd.DataFrame()

    standings = lists[0].get("DriverStandings", [])
    rows = []

    for d in standings:
        drv = d.get("Driver") or {}
        cons_list = d.get("Constructors") or []
        cons = cons_list[0].get("name") if cons_list else ""

        rows.append(
            {
                "position": int(d.get("position", 0)),
                "driver": f"{drv.get('givenName', '')} {drv.get('familyName', '')}".strip(),
                "code": drv.get("code", ""),
                "number": drv.get("permanentNumber", ""),
                "nationality": drv.get("nationality", ""),
                "team": cons,
                "points": float(d.get("points", 0.0)),
                "wins": int(d.get("wins", 0)),
            }
        )

    return pd.DataFrame(rows).sort_values("position", na_position="last")


@st.cache_data(ttl=CACHE_TTL)
def get_constructor_standings(season: str) -> pd.DataFrame:
    data = _constructor_standings_json(season)
    lists = (
        data.get("MRData", {})
        .get("StandingsTable", {})
        .get("StandingsLists", [])
    )

    if not lists:
        st.session_state["offline"] = True
        return pd.DataFrame()

    standings = lists[0].get("ConstructorStandings", [])
    rows = []

    for c in standings:
        cons = c.get("Constructor") or {}

        rows.append(
            {
                "position": int(c.get("position", 0)),
                "team": cons.get("name", ""),
                "nationality": cons.get("nationality", ""),
                "points": float(c.get("points", 0.0)),
                "wins": int(c.get("wins", 0)),
            }
        )

    return pd.DataFrame(rows).sort_values("position", na_position="last")


@st.cache_data(ttl=CACHE_TTL)
def get_all_results_up_to(season: str, up_to_round: int) -> pd.DataFrame:
    rows = []

    for rnd in range(1, up_to_round + 1):
        data = _round_results_json(season, rnd)
        races = (
            data.get("MRData", {})
            .get("RaceTable", {})
            .get("Races", [])
        )

        if not races:
            continue

        race = races[0]
        race_name = race.get("raceName", "")
        results = race.get("Results", []) or []

        for res in results:
            drv = res.get("Driver") or {}
            cons = (res.get("Constructor") or {}).get("name", "")

            rows.append(
                {
                    "round": rnd,
                    "race": race_name,
                    "driver": f"{drv.get('givenName', '')} {drv.get('familyName', '')}".strip(),
                    "team": cons,
                    "position": res.get("position", ""),
                    "grid": res.get("grid", ""),
                    "points": float(res.get("points", 0.0)),
                    "status": res.get("status", ""),
                }
            )

    return pd.DataFrame(rows)


# -------- Optional OO wrapper to satisfy F1Client import --------

class F1Client:
    """
    Convenience wrapper around the functional API,
    bound to a single season (default = DEFAULT_SEASON).
    """

    def __init__(self, season: str = DEFAULT_SEASON):
        self.season = season

    def set_season(self, season: str):
        self.season = season

    def get_completed_round(self) -> int:
        return get_completed_round(self.season)

    def get_schedule(self) -> pd.DataFrame:
        return get_schedule(self.season)

    def get_driver_standings(self) -> pd.DataFrame:
        return get_driver_standings(self.season)

    def get_constructor_standings(self) -> pd.DataFrame:
        return get_constructor_standings(self.season)

    def get_all_results_up_to(self, up_to_round: int) -> pd.DataFrame:
        return get_all_results_up_to(self.season, up_to_round)