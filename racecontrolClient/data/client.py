from typing import List, Dict

import pandas as pd

from racecontrolClient.data.provider_jolpica import JolpicaProvider
from racecontrolClient.services.results import (
    parse_schedule,
    parse_driver_standings,
    parse_constructor_standings,
)
from racecontrol.services.fantasy import (
    summarize_driver_form,
    compute_fantasy_score,
)

_provider = JolpicaProvider()

# ---------- Core data fetchers ----------

def get_completed_round(season: str) -> int:
    data = _provider.last_results_json(season)
    races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    if not races:
        return 0
    r = races[0]
    try:
        return int(r.get("round", 0) or 0)
    except Exception:
        return 0

def get_schedule(season: str) -> List[Dict]:
    raw = _provider.schedule_json(season)
    df = parse_schedule(raw)
    return df.to_dict(orient="records")

def get_driver_standings(season: str) -> List[Dict]:
    raw = _provider.driver_standings_json(season)
    df = parse_driver_standings(raw)
    return df.to_dict(orient="records")

def get_constructor_standings(season: str) -> List[Dict]:
    raw = _provider.constructor_standings_json(season)
    df = parse_constructor_standings(raw)
    return df.to_dict(orient="records")

def get_all_results_up_to(season: str, round_inclusive: int) -> List[Dict]:
    if round_inclusive <= 0:
        return []

    results: list[dict] = []
    for rnd in range(1, round_inclusive + 1):
        data = _provider.round_results_json(season, rnd)
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        if not races:
            continue
        r = races[0]
        round_num = int(r.get("round", rnd))
        race_name = r.get("raceName", f"Round {rnd}")
        for res in r.get("Results", []):
            drv = res.get("Driver", {}) or {}
            cons = res.get("Constructor", {}) or {}
            grid = None
            gr = res.get("grid", None)
            if gr not in (None, ""):
                try:
                    grid = int(gr)
                except Exception:
                    grid = None
            results.append(
                {
                    "round": round_num,
                    "race": race_name,
                    "driver": f"{drv.get('givenName','')} {drv.get('familyName','')}".strip(),
                    "driver_code": drv.get("code", "") or "",
                    "team": cons.get("name", "") or "",
                    "finish": res.get("positionText", "") or "",
                    "grid": grid,
                    "status": res.get("status", "") or "",
                    "points": float(res.get("points", 0.0) or 0.0),
                }
            )

    results_df = pd.DataFrame(results)
    if results_df.empty:
        return []
    results_df = results_df.sort_values(["round", "points"], ascending=[True, False])
    return results_df.to_dict(orient="records")

def get_fantasy_scores(
    season: str,
    round_inclusive: int,
    last_n: int,
    w_recent: float,
    w_season: float,
    vol_penalty: float,
) -> List[Dict]:
    """High-level helper that matches your original Fantasy tab."""
    raw_results = get_all_results_up_to(season, round_inclusive)
    df_results = pd.DataFrame(raw_results)
    form = summarize_driver_form(df_results, last_n=last_n)
    scores = compute_fantasy_score(form, w_recent=w_recent, w_season=w_season, vol_penalty=vol_penalty)
    return scores.to_dict(orient="records")