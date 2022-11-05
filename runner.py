from src.nhl_database import TeamDatabase, SkaterDatabase, GoalieDatabase
from util.nhl_download import Downloader
# from src.nhl_simulation import GameSimulation, SeasonSimulation
from nhl_settings import Settings


class Runner():
    def __init__(self, seasons):
        self.settings = Settings(seasons)

    def update_data(self, force=False):
        # Use "download_old_season_data" to download older seasons data
        for season in self.settings.seasons:
            d = Downloader(season)
            if force is True:
                d.force_download()
            d.download_season_data()

    def create_databases(self):
        # tdb = TeamDatabase(self.settings)
        sdb = SkaterDatabase(self.settings)
        # gdb = GoalieDatabase(self.settings)

if __name__ == '__main__':
    rn = Runner(["20212022"])
    rn.update_data()
    rn.create_databases()
