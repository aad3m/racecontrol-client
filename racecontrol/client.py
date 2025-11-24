import pandas as pd

class F1Client:
    def __init__(self, provider):
        self.provider = provider

    # ---------- SCHEDULE ----------
    def get_schedule(self):
        data = self.provider.fetch("f1/current.json")
        if not data:
            return pd.DataFrame()

        races = data["MRData"]["RaceTable"]["Races"]
        return pd.DataFrame(races)

    # ---------- DRIVER STANDINGS ----------
    def get_driver_standings(self):
        data = self.provider.fetch("f1/current/driverStandings.json")
        if not data:
            return pd.DataFrame()

        standings = (
            data["MRData"]["StandingsTable"]
            ["StandingsLists"][0]["DriverStandings"]
        )
        return pd.DataFrame(standings)

    # ---------- RESULTS ----------
    def get_race_results(self, round_number: int):
        data = self.provider.fetch(f"f1/current/{round_number}/results.json")
        if not data:
            return pd.DataFrame()

        results = (
            data["MRData"]["RaceTable"]["Races"][0]["Results"]
        )
        return pd.DataFrame(results)