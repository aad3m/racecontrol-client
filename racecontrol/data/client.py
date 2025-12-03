import pandas as pd

class F1Client:
    """
    Multi-season Formula 1 API Client using the Jolpica (Ergast-style) API.
    """

    def __init__(self, provider):
        self.provider = provider

    # ----------------------------------------------------
    # SCHEDULE
    # ----------------------------------------------------
    def get_schedule(self, season="current") -> pd.DataFrame:
        endpoint = f"f1/{season}.json"
        data = self.provider.fetch(endpoint)

        if not data:
            return pd.DataFrame()

        races = data["MRData"]["RaceTable"]["Races"]
        return pd.DataFrame(races)

    # ----------------------------------------------------
    # DRIVER STANDINGS
    # ----------------------------------------------------
    def get_driver_standings(self, season="current") -> pd.DataFrame:
        endpoint = f"f1/{season}/driverStandings.json"
        data = self.provider.fetch(endpoint)

        if not data:
            return pd.DataFrame()

        lists = data["MRData"]["StandingsTable"]["StandingsLists"]

        if not lists:
            return pd.DataFrame()

        return pd.DataFrame(lists[0]["DriverStandings"])

    # ----------------------------------------------------
    # CONSTRUCTOR STANDINGS
    # ----------------------------------------------------
    def get_constructor_standings(self, season="current") -> pd.DataFrame:
        endpoint = f"f1/{season}/constructorStandings.json"
        data = self.provider.fetch(endpoint)

        if not data:
            return pd.DataFrame()

        lists = data["MRData"]["StandingsTable"]["StandingsLists"]

        if not lists:
            return pd.DataFrame()

        return pd.DataFrame(lists[0]["ConstructorStandings"])

    # ----------------------------------------------------
    # RESULTS (single round)
    # ----------------------------------------------------
    def get_race_results(self, season="current", round_number=None) -> pd.DataFrame:
        if round_number is None:
            return pd.DataFrame()

        endpoint = f"f1/{season}/{round_number}/results.json"
        data = self.provider.fetch(endpoint)

        if not data:
            return pd.DataFrame()

        races = data["MRData"]["RaceTable"]["Races"]
        if not races:
            return pd.DataFrame()

        results = races[0]["Results"]
        return pd.DataFrame(results)

    # ----------------------------------------------------
    # RESULTS (up to round N)
    # ----------------------------------------------------
    def get_results_up_to(self, season="current", round_number=None) -> pd.DataFrame:
        """
        Get results for all rounds up to N (aggregated).
        """
        if round_number is None:
            return pd.DataFrame()

        all_results = []

        for r in range(1, round_number + 1):
            df = self.get_race_results(season, r)
            if not df.empty:
                df["round"] = r
                all_results.append(df)

        if not all_results:
            return pd.DataFrame()

        return pd.concat(all_results, ignore_index=True)

    # ----------------------------------------------------
    # RESULTS (all rounds)
    # ----------------------------------------------------
    def get_all_results(self, season="current"):
        """
        Fetch results for every completed round in the given season.
        """
        schedule = self.get_schedule(season)

        if schedule.empty:
            return pd.DataFrame()

        max_round = int(schedule["round"].max())
        return self.get_results_up_to(season, max_round)