import pandas as pd

def parse_schedule(raw: dict) -> pd.DataFrame:
    races = raw.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    if not races:
        return pd.DataFrame(columns=["round", "name", "circuit", "country", "local_date"])

    rows = []
    for r in races:
        rows.append(
            {
                "round": int(r.get("round", 0) or 0),
                "name": r.get("raceName", ""),
                "circuit": r.get("Circuit", {}).get("circuitName", ""),
                "country": (r.get("Circuit", {}).get("Location", {}) or {}).get("country", ""),
                "local_date": f"{r.get('date','')} {r.get('time','')}".strip(),
            }
        )
    df = pd.DataFrame(rows)
    return df.sort_values("round")

def parse_driver_standings(raw: dict) -> pd.DataFrame:
    lists = raw.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
    if not lists:
        return pd.DataFrame(
            columns=["position", "driver_code", "driver", "nationality", "team", "points", "wins"]
        )

    standings = lists[0].get("DriverStandings", [])
    rows = []
    for d in standings:
        drv = d.get("Driver", {}) or {}
        cons = (d.get("Constructors") or [{}])[0]
        rows.append(
            {
                "position": int(d.get("position", 0) or 0),
                "driver_code": drv.get("code", "") or "",
                "driver": f"{drv.get('givenName','')} {drv.get('familyName','')}".strip(),
                "nationality": drv.get("nationality", "") or "",
                "team": cons.get("name", "") or "",
                "points": float(d.get("points", 0.0) or 0.0),
                "wins": int(d.get("wins", 0) or 0),
            }
        )
    return pd.DataFrame(rows).sort_values("position", na_position="last")

def parse_constructor_standings(raw: dict) -> pd.DataFrame:
    lists = raw.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
    if not lists:
        return pd.DataFrame(
            columns=["position", "team", "nationality", "points", "wins"]
        )

    standings = lists[0].get("ConstructorStandings", [])
    rows = []
    for c in standings:
        cons = c.get("Constructor", {}) or {}
        rows.append(
            {
                "position": int(c.get("position", 0) or 0),
                "team": cons.get("name", "") or "",
                "nationality": cons.get("nationality", "") or "",
                "points": float(c.get("points", 0.0) or 0.0),
                "wins": int(c.get("wins", 0) or 0),
            }
        )
    return pd.DataFrame(rows).sort_values("position", na_position="last")

def parse_results_up_to(raw_rounds: list[dict]) -> pd.DataFrame:
    """Utility if you ever fetch multiple rounds at once."""
    # Not strictly needed for current flow; left as hook.
    return pd.DataFrame(raw_rounds)