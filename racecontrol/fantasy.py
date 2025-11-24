import pandas as pd

class FantasyService:
    def __init__(self, provider):
        self.provider = provider

    def get_fantasy_scores(self):
        data = self.provider.fetch("f1/current/driverStandings.json")
        if not data:
            return pd.DataFrame()

        drivers = (
            data["MRData"]["StandingsTable"]["StandingsLists"][0]
            ["DriverStandings"]
        )

        df = pd.DataFrame(drivers)
        df["fantasy_score"] = df["points"].astype(float) * 1.4

        return df.sort_values("fantasy_score", ascending=False)