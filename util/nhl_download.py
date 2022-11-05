import os
import time

from util.nhl_web_scrape import WebScraper


class Downloader():
    """ Class to handle downloads from NST/eliteprospects """
    def __init__(self, year, force_download=False):
        self.data_dir = 'data'
        self.year = year
        self.scraper = WebScraper()
        self.setup_urls(year)
        #self._force_download = force_download
        self.get_new_data = force_download or self._new_data_needed()

    def _new_data_needed(self):
        """ Private method to decide if new data needs to be collected
            @TODO: Add check to see if data has been collected recently
        """
        fpath = os.path.join(self.data_dir, f'Skater_Individual_ES_{self.year}.csv')
        return not os.path.exists(fpath)

    def force_download(self, force_value=True):
        """ Update attribute to decide if data shall be downloaded """
        self.get_new_data = force_value

    def download_season_data(self, year=None, force_dowload=False):
        """ Public method to initiate download of data for a new season"""
        if year is None:
            year = self.year
        if self.get_new_data is True:
            self._download_season_data(year)
        else:
            print(f"Data for season {year} already available. Use 'force_download()' to override.")

    def setup_urls(self, year):
        """ Method to configure urls needed for download """
        self.url_skater_bio = f"https://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_goalie_bio = f"http://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=G&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_skater_ind_es = f"http://naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_skater_ind_pp = f"https://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=5v4&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        self.url_skater_ind_pk = f"https://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=4v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        self.url_skater_on_ice = f"https://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=5v5&score=all&stdoi=oi&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        self.url_goalie_es = f"https://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_goalie_pp = f"https://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=5v4&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_goalie_pk = f"https://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype=2&sit=4v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_team_es = f"https://www.naturalstattrick.com/teamtable.php?fromseason={year}&thruseason={year}&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
        self.url_team_pp = f"https://www.naturalstattrick.com/teamtable.php?fromseason={year}&thruseason={year}&stype=2&sit=5v4&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
        self.url_team_pk = f"https://www.naturalstattrick.com/teamtable.php?fromseason={year}&thruseason={year}&stype=2&sit=4v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="

    def _download_season_data(self, year):
        """ Download all data for a specific year, if needed """
        # In between each download we are sleeping for a while, to ensure not spamming the servers
        SLEEP_TIME = 3
        # For readability
        dd = self.data_dir
        print('   Downloading Skater bio-data')
        self.scraper.write_bio_csv(self.url_skater_bio, os.path.join(dd, f'Skater_Bio_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading Goalie bio-data')
        self.scraper.write_bio_csv(self.url_goalie_bio,
                                   os.path.join(dd, f'Goalie_Bio_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading individual ES data')
        self.scraper.write_skater_ind_csv(self.url_skater_ind_es,
                                          os.path.join(dd, f'Skater_Individual_ES_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading individual PP data')
        self.scraper.write_skater_ind_csv(self.url_skater_ind_pp,
                                          os.path.join(dd, f'Skater_Individual_PP_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading individual PK data')
        self.scraper.write_skater_ind_csv(self.url_skater_ind_pk,
                                          os.path.join(dd, f'Skater_Individual_PK_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading on-ice data')
        self.scraper.write_skater_on_ice_csv(self.url_skater_on_ice,
                                             os.path.join(dd, f'Skater_OnIce_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading goalie ES data')
        self.scraper.write_goalie_csv(self.url_goalie_es,
                                      os.path.join(dd, f'Goalie_ES_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading goalie PP data')
        self.scraper.write_goalie_csv(self.url_goalie_pp,
                                      os.path.join(dd, f'Goalie_PP_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading goalie PK data')
        self.scraper.write_goalie_csv(self.url_goalie_pk,
                                      os.path.join(dd, f'Goalie_PK_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading ES team data')
        self.scraper.write_team_csv(self.url_team_es,
                                    os.path.join(dd, f'Team_ES_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading PP team data')
        self.scraper.write_team_csv(self.url_team_pp,
                                    os.path.join(dd, f'Team_PP_{year}'))
        time.sleep(SLEEP_TIME)

        print('   Downloading PK team data')
        self.scraper.write_team_csv(self.url_team_pk,
                                    os.path.join(dd, f'Team_PK_{year}'))


if __name__ == '__main__':
    pass
