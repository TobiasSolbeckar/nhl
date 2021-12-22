import csv
import numpy as np
import datetime
import time
import scipy.stats

from nhl_web_scrape import *


class Player():
    def __init__(self, url):
        self.data = PlayerData(url)
        self.meta_data = self.data.meta_data

    def print_data(self):
        for se in self.data.season_data.values():
            print(se)

    def print_nhle(self, seasons):
        for se in seasons:
            try:
                if self.data.season_data[se]["nhle_ppg"] != -1:
                    print(f'{se}: {self.data.season_data[se]["nhle_ppg"]:.3f}')
            except KeyError:
                print(f'No data for season {se}')
        print(f'Average NHLe: {self.data.nhle_avg:.3f}')

    def print_dob(self):
        print(self.meta_data["dob_raw"])


class PlayerData():
    def __init__(self, url):
        [self.meta_data, self.raw_data] = scrape_ep_player_info(url)
        self.split_seasons = []
        self.season_data = {}
        self.clean_meta_data()
        if self.meta_data != "G":
            self.clean_season_data()
            self.calculate_nhle()

    def clean_meta_data(self):
        # Make sure DOB is on the correct format
        dob_temp_array = self.meta_data["dob_raw"].replace(",","").split(" ")
        self.meta_data["dob"] = [None, None, None]
        self.meta_data["dob"][0] = int(dob_temp_array[2])
        self.meta_data["dob"][1] = MONTH_LOOKUP[dob_temp_array[0].upper()]
        self.meta_data["dob"][2] = int(dob_temp_array[1])
        name_array = self.meta_data["name_raw"].split("-")
        self.meta_data["name"] = name_array[0].upper() + "_" + name_array[-1].upper()
        if "D" in self.meta_data["pos_raw"]:
            self.meta_data["pos"] = "D"
        elif "G" in self.meta_data["pos_raw"]:
            self.meta_data["pos"] = "G"
        else:
            self.meta_data["pos"] = "F"

    def clean_season_data(self):
        # Clean up season data
        for season_key in self.meta_data["seasons_played"]:
            if season_key in self.meta_data["split_seasons"]:
                # Player played for one or more teams during the season
                self.combine_season_data(self.raw_data[season_key]["season"])
            else:
                self.season_data[season_key] = self.raw_data[season_key]
            self.season_data[season_key]["tp"] = self.season_data[season_key]["g"] + self.season_data[season_key]["a"]
            try:
                self.season_data[season_key]["ppg"] = self.season_data[season_key]["tp"] / self.season_data[season_key]["gp"]
            except ZeroDivisionError:
                self.season_data[season_key]["ppg"] = 0

    def get_seasons_from_year(self, value):
        op = []
        for season_data in self.raw_data.values():
            if season_data['season'] == value:
                op.append(season_data)
        return op

    def combine_season_data(self, season_key):
        list_of_seasons = self.get_seasons_from_year(season_key)
        combined_season = {}
        # Store data from season to normalize "against"
        combined_season["season"] = list_of_seasons[0]["season"]
        combined_season["league"] = list_of_seasons[0]["league"]
        combined_season["gp"] = list_of_seasons[0]["gp"]
        combined_season["g"] = list_of_seasons[0]["g"]
        combined_season["a"] = list_of_seasons[0]["a"]
        normalized_league = list_of_seasons[0]["league"]
        # Add data from season to normalize
        for season_data in list_of_seasons[1:]:
            try:
                norm_factor = LEAGUE_COEFF[season_data["league"].upper()] / LEAGUE_COEFF[normalized_league.upper()]
            except KeyError:
                norm_factor = None
            if norm_factor is not None:
                combined_season["gp"] += season_data["gp"]
                combined_season["g"] += season_data["g"] * norm_factor
                combined_season["a"] += season_data["a"] * norm_factor
        combined_season["tp"] = combined_season["g"] + combined_season["a"]
        self.season_data[season_key] = combined_season

    def calculate_nhle(self, N=3):
        ''' Calculate NHLe for each season '''
        nhles = []
        for se in self.season_data.values():
            # Calculate age coeffs based on 31st of December for the "starting year"
            # of the season
            season_year = int(se["season"].split("-")[0])
            d0 = datetime.date(self.meta_data["dob"][0], self.meta_data["dob"][1], self.meta_data["dob"][2])
            d1 = datetime.date(season_year, 12, 31)
            delta = d1 - d0  # How many days old is the player during the season
            age_coeff_to_use = get_daily_age_coeff(delta.days)
            try:
                se["nhle_ppg"] = se["ppg"] * LEAGUE_COEFF[se["league"].upper()] * age_coeff_to_use
                nhles.append(se["nhle_ppg"])
            except KeyError:
                # Skip the season if no data is available
                #  print("Could not find norm factor for league " + se["league"])
                se["nhle_ppg"] = -1
            se["nhle_tp"] = se["nhle_ppg"] * 82

        self.nhle_avg = np.mean(nhles[-N:])
        self.nhles = nhles


# Functions outside of classes
def generate_players_list(url, dob_th):
    ''' Generates a list of all players in a team '''
    _op, links = [], []
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    tables = soup.find_all('table')
    all_rows = tables[1].find_all('tr')
    for row in all_rows:
        link_entry = row.find('a', href=True)
        if link_entry is not None:
            dob_entry = row.find('td', {'class': 'date-of-birth'})
            if int(dob_entry.text.strip()) >= dob_th:
                tmp_a = link_entry.text.split(' ')
                first_name = tmp_a[0]
                last_name = tmp_a[1]
                player_name = first_name.upper() + '_' + last_name.upper()
                _op.append((player_name, link_entry['href']))
                links.append(link_entry['href'])

    # @TODO: Check the "In the system" page for more players.

    return _op


def get_daily_age_coeff(days_old_during_season):
    """ Calculate NHLe age compensation with daily granularity """
    season_years_of_age = np.floor(days_old_during_season/365)  # Ignore skip years
    if season_years_of_age < 16:
        return 0
    season_delta_days = days_old_during_season - season_years_of_age*365
    daily_coeff_delta = (AGE_COEFF[season_years_of_age + 1] - AGE_COEFF[season_years_of_age])/365
    return AGE_COEFF[season_years_of_age] + season_delta_days*daily_coeff_delta


def create_prospect_pool_analysis(url, dob_th=1997, nhle_th=0.25, nhl_gp_th=10, extended=False, verbose=False):
    ''' Creates analysis for team prospect pool
    @TODO: Sort out too old players earlier.
    @TODO: Possible to filter out based on position
    '''
    players_list = generate_players_list(url, dob_th=dob_th)
    nhles, nhlers = [], []
    i = 0
    for [name, link] in players_list:
        # To avoid spamming the servers
        time.sleep(2)
        if extended is True:
            create_prospect_analysis(link)
        else:
            if verbose:
                print(f"   Progress: {100*i/len(players_list):.1f}%")
            i += 1
            try:
                player = Player(link)
            except:
                print('Could not create analysis for player ' + name)
            if player.meta_data["pos"] == "F":
                nhle_th = 0.35
            elif player.meta_data["pos"] == "D":
                nhle_th = 0.23
            if player.meta_data["pos"] == "F" and player.meta_data["nhl_gps"] < nhl_gp_th and not np.isnan(player.data.nhle_avg):
                if verbose:
                    print(f"   Adding player {name} (NHLe: {player.data.nhle_avg:.3f}) to analysis")
                nhles.append(player.data.nhle_avg)
                if player.data.nhle_avg > nhle_th:
                    nhlers.append(name)
                    # print(f'\n {name}: {player.data.nhle_avg:.3f}')
                    # player.print_nhle(['2018-19', '2019-20', '2020-21'])
    if (extended is False) and (verbose is True):
        print(f'Team prospect pool:\n   Number of prospects: {len(nhles)}\n   Number of NHL-players: {len(nhlers)} ({nhlers})\n   total(NHLe): {sum(nhles):.1f}\n   mu(NHLe):    {np.mean(nhles):.3f}\n   sigma(NHLe): {np.std(nhles):.3f}')
    else:
        print(f'Team prospect pool:\n   Number of prospects: {len(nhles)}\n   Number of NHL-players: {len(nhlers)}\n   total(NHLe): {sum(nhles):.1f}\n   mu(NHLe):    {np.mean(nhles):.3f}\n   sigma(NHLe): {np.std(nhles):.3f}')


def create_prospect_analysis(player_url):
    ''' Calculate "success probabilities" for a prospect '''
    try:
        player = Player(player_url)
        print(f"\nAnalysing player {player.meta_data['name']}")
        # @TODO: Add some sort of weighting here?
        dist = scipy.stats.norm(np.mean(player.data.nhles), np.std(player.data.nhles))
        print(f"Success probabilities (based on NHLe: {player.data.nhles}):")
        print(f"   Probability for 1st line: {100*(1-dist.cdf(0.86)):.1f}%")
        print(f"   Probability for 2nd line: {100*(1-dist.cdf(0.59)):.1f}%")
        print(f"   Probability for 3rd line: {100*(1-dist.cdf(0.41)):.1f}%")
        print(f"   Probability for 4th line: {100*(1-dist.cdf(0.26)):.1f}%")
        player.print_nhle(['2018-19', '2019-20', '2020-21', '2021-22'])
    except:
        print('Could not create analysis from player URL ' + player_url)


def main():
    if True:
        team = "SJS"
        url = EP_TEAM_LINKS[team] + "/depth-chart"  # noqa: F405
        print(f"\n\nAnalysing {team}")
        create_prospect_pool_analysis(url,
                                      dob_th=1997,
                                      nhle_th=0.35,
                                      nhl_gp_th=10,
                                      extended=True,
                                      verbose=True)

    # write_player_team_info("TBL")
    # create_prospect_analysis("https://www.eliteprospects.com/player/333786/ivan-chekhovich")


if __name__ == "__main__":
    main()
