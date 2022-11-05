''' Module for handling downloading of data, mostly from www.naturalstattrick.com '''
# Import modules
import requests
import cfscrape
import csv
import time

from bs4 import BeautifulSoup
from collections import defaultdict
from src.nhl_defines import *

# @TODO: All fnuctions named like "write_X_csv" shouldn't need to take *.csv
# into the filename argument


def translate_web_name(web_name):
    ''' Fix for incompatible team names '''
    if web_name == "N.Y. Islanders":
        team_name = 'New York Islanders'
    elif web_name == 'N.Y. Rangers':
        team_name = 'New York Rangers'
    else:
        team_name = web_name
    return team_name


class WebScraper():
    """ Class for handling web scraping """
    def __init__(self):
        pass

    def write_bio_csv(self, url, filename):
        ''' Download and write bio data from www.naturalstattrick.com '''
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        tables = soup.find_all('table')
        data_table = tables[0].find_all('td')
        data_length = SKATER_DB_BIO_LENGTH  # noqa
        number_of_players = int(len(data_table)/data_length)
        with open(f'{filename}.csv', mode='w', newline='') as csv_file:
            fieldnames = ['id', 'player_name', 'team', 'position', 'age', 'dob', 'birth_city', 'birth_state', 'birth_country', 'nationality', 'height', 'weight', 'draft_year', 'draft_team', 'draft_round', 'draft_round_pick', 'total_draft_pick']  # noqa
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(number_of_players):
                player_dict = {}
                player_dict['id'] = str(data_table[0+i*data_length].contents[0])
                player_dict['player_name'] = str(data_table[1+i*data_length].find('a').contents[0])
                player_dict['team'] = str(data_table[2+i*data_length].contents[0])
                player_dict['position'] = str(data_table[3+i*data_length].contents[0])
                player_dict['age'] = str(data_table[4+i*data_length].contents[0])
                player_dict['dob'] = str(data_table[5+i*data_length].contents[0])
                player_dict['birth_city'] = '-' # str(data_table[6+i*data_length].contents[0])
                player_dict['birth_state'] = '-'  # str(data_table[7+i*data_length].contents[0])
                player_dict['birth_country'] = "-" # str(data_table[8+i*data_length].contents[0])
                player_dict['nationality'] = '-'  # str(data_table[9+i*data_length].contents[0])
                player_dict['height'] = str(data_table[10+i*data_length].contents[0])
                player_dict['weight'] = str(data_table[11+i*data_length].contents[0])
                player_dict['draft_year'] = str(data_table[12+i*data_length].contents[0])
                player_dict['draft_team'] = str(data_table[13+i*data_length].contents[0])
                player_dict['draft_round'] = str(data_table[14+i*data_length].contents[0])
                player_dict['draft_round_pick'] = str(data_table[15+i*data_length].contents[0])
                player_dict['total_draft_pick'] = str(data_table[16+i*data_length].contents[0])
                writer.writerow(player_dict)

    def write_skater_ind_csv(self, url, filename):
        ''' Download and write individual skater data from www.naturalstattrick.com '''
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            tables = soup.find_all('table')
            data_table = tables[0].find_all('td')
            data_length = SKATER_DB_IND_LENGTH  # noqa
            number_of_players = int(len(data_table)/data_length)
            with open(f'{filename}.csv', mode='w', newline='') as csv_file:
                fieldnames = ['id', 'player_name', 'team', 'position', 'gp', 'toi', 'goals', 'assist', 'first_assist', 'second_assist', 'total_points', 'ipp', 'sf', 'sh_pcg', 'ixg', 'icf', 'iff', 'iscf', 'ihdcf', 'rush_attempts', 'rebounds_created', 'pim', 'total_penalties', 'minor', 'major', 'misconduct', 'penalties_drawn', 'giveaways', 'takeaways', 'hits', 'hits_taken', 'shots_blocked', 'faceoffs_won', 'faceoffs_lost', 'faceoffs_won_pcg']  # noqa
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(number_of_players):
                    player_dict = {}
                    for j, field in enumerate(fieldnames):
                        if j == 1:
                            name_item = data_table[1+i*data_length]
                            player_dict['player_name'] = str(name_item.find('a').contents[0])
                        else:
                            player_dict[field] = str(data_table[j+i*data_length].contents[0])
                    writer.writerow(player_dict)
        except Exception as ex:
            print('Could not download individual data from ' + url)
            print(ex)
            return False
        return True

    def write_skater_on_ice_csv(self, url, filename):
        ''' Download and write on-ice skater data from www.naturalstattrick.com '''
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            tables = soup.find_all('table')
            data_table = tables[0].find_all('td')
            fieldnames = ['id', 'player_name', 'team', 'position', 'gp', 'toi', 'cf', 'ca', 'cf_pcg', 'ff', 'fa', 'ff_pcg', 'sf', 'sa', 'sf_pcg', 'goals', 'ga', 'gf_pcg', 'xgf', 'xga', 'xgf_pcg', 'scf', 'sca', 'scf_pcg', 'hdcf', 'hdca', 'hdcf_pcg', 'hdgf', 'hdga', 'hdgf_pcg', 'mdcf', 'mdca', 'mdcf_pcg', 'mdgf', 'mdga', 'mdgf_pcg', 'ldcf', 'ldca', 'ldcf_pcg', 'ldgf', 'ldga', 'ldgf_pcg', 'on_ice_sh_pcg', 'on_ice_sv_pcg', 'pdo', 'ozs', 'nzs', 'dzs', 'on_the_fly_starts', 'ofz_pcg', 'ozfo', 'nzfo', 'dzfo', 'ozfo_ocg']  # noqa
            number_of_players = int(len(data_table)/len(fieldnames))
            with open(f'{filename}.csv', mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(number_of_players):
                    player_dict = {}
                    for j, field in enumerate(fieldnames):
                        if j == 1:
                            name_item = data_table[1+i*len(fieldnames)]
                            player_dict['player_name'] = str(name_item.find('a').contents[0])
                        else:
                            player_dict[field] = str(data_table[j+i*len(fieldnames)].contents[0])
                    writer.writerow(player_dict)
        except Exception as ex:
            print('Could not download on-ice data from ' + url)
            print(ex)
            return False
        return True


    def write_skater_relative_csv(self, url, filename):
        ''' Download and write relative skater data from www.naturalstattrick.com '''
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            tables = soup.find_all('table')
            data_table = tables[0].find_all('td')
            fieldnames = ['id', 'player_name', 'team', 'position', 'gp', 'toi', 'toi_per_gp', 'cf_60_rel', 'ca_60_rel', 'cf_pcg_rel', 'ff_60_rel', 'fa_60_rel', 'ff_pcg_rel', 'sf_60_rel', 'sa_60_rel', 'sf_pcg_rel', 'gf_60_rel', 'ga_60_rel', 'gf_pcg_rel', 'xgf_60_rel', 'xga_60_rel', 'xgf_pcg_rel', 'scf_60_rel', 'sca_60_rel', 'scf_pcg_rel', 'hdcf_60_rel', 'hdca_60_rel', 'hdcf_pcg_rel', 'hdgf_60_rel', 'hdga_60_rel', 'hdgf_pcg_rel', 'mdcf_60_rel', 'mdca_60_rel', 'mdcf_pcg_rel', 'mdgf_60_rel', 'mdga_60_rel', 'mdgf_pcg_rel', 'ldcf_60_rel', 'ldca_60_rel', 'ldcf_pcg_rel', 'ldgf_60_rel', 'ldga_60_rel', 'ldgf_pcg_rel', 'on_ice_sh_pcg', 'on_ice_sv_pcg', 'pdo', 'ozs_60', 'nzs_60', 'dzs_60', 'on_the_fly_starts_60', 'ozs_pcg', 'ozfo_60', 'nzfo_60', 'dzfo_60', 'ozfo_pcg']  # noqa
            number_of_players = int(len(data_table)/len(fieldnames))
            with open(f'{filename}.csv', mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(number_of_players):
                    player_dict = {}
                    for j, field in enumerate(fieldnames):
                        if j == 1:
                            name_item = data_table[1+i*len(fieldnames)]
                            player_dict['player_name'] = str(name_item.find('a').contents[0])
                        else:
                            player_dict[field] = str(data_table[j+i*len(fieldnames)].contents[0])
                    writer.writerow(player_dict)
        except Exception as ex:
            print('Could not download relative data from ' + url)
            print(ex)
            return False
        return True


    def write_team_csv(self, url, filename):
        ''' Download and write team data from www.naturalstattrick.com '''
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            tables = soup.find_all('table')
            headers = soup.find('thead')
            headers = headers.find('tr').find_all('th')
            fieldnames = []
            for entry in headers:
                if entry.contents != []:
                    header_str = str(entry.contents[0])
                    header_str = header_str.lower()
                    header_str = header_str.replace(' ', '')
                    header_str = header_str.replace('%', '_pcg')
                    header_str = header_str.replace('team', 'team_name')
                    fieldnames.append(header_str)
                else:
                    fieldnames.append('id')
            data_table = tables[0].find_all('td')
            data_length = TEAM_DB_LENGTH  # noqa
            number_of_teams = int(len(data_table)/data_length)
            with open(f'{filename}.csv', mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(number_of_teams):
                    team_dict = {}
                    for j, field in enumerate(fieldnames):
                        team_dict[field] = str(data_table[j+i*data_length].contents[0])
                    writer.writerow(team_dict)
        except Exception as ex:
            print('Could not download team data from ' + url)
            print(ex)
            return False
        return True


    def write_unavailable_players_csv(self, filename):
        ''' Download and information about unavailable players from www.naturalstattrick.com '''
        try:
            with open(f'{filename}.csv', mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=', ')
                unavailable_players = defaultdict(list)
                writer.writerow(['team_id', 'unavailable_players'])      # Write header manually.
                for team_id in ACTIVE_TEAMS:
                    url = get_daily_fo_url(team_id)
                    scraper = cfscrape.create_scraper()
                    html = scraper.get(url).content
                    soup = BeautifulSoup(html, 'html.parser')
                    ir_container = soup.find("div", {"id": "ir-container"})
                    try:
                        ir_players = ir_container.find_all("td")
                        for i in range(len(ir_players)):
                            name_content = ir_players[i].contents[2].find_all("span")[1].contents[0]
                            unavailable_players[team_id].append(generate_player_id(name_content))
                    except:
                        unavailable_players[team_id] = []
                        print('Could not read injury reserve for ' + team_id)
                    writer.writerow([team_id, unavailable_players[team_id]])
        except Exception as ex:
            print('Could not download information about unavailable players from ' + url)
            print(ex)
            return False
        return True


    def write_goalie_csv(self, url, filename):
        ''' Download and write goalie data from www.naturalstattrick.com '''
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            tables = soup.find_all('table')
            data_table = tables[0].find_all('td')
            fieldnames = ['id', 'player_name', 'team', 'gp', 'toi', 'sa', 'sv', 'ga', 'sv_pcg', 'gaa', 'gsaa', 'xga', 'hdsa', 'hdsv', 'hdga', 'hdsv_pcg', 'hdgaa', 'hdgsaa', 'mdsa', 'mdsv', 'mdga', 'mdsv_pcg', 'mdgaa', 'mdgsaa', 'ldsa', 'ldsv', 'ldga', 'ldsv_pcg', 'ldgaa', 'ldgsaa', 'rush_attempts_against', 'rebound_attempts_against', 'avg_shot_dist', 'avg_goal_dist']  # noqa
            data_length = len(fieldnames)
            number_of_players = int(len(data_table)/data_length)
            with open(f'{filename}.csv', mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(number_of_players):
                    player_dict = {}
                    for j, field in enumerate(fieldnames):
                        if j == 1:
                            name_item = data_table[1+i*data_length]
                            player_dict['player_name'] = str(name_item.find('a').contents[0])
                        else:
                            player_dict[field] = str(data_table[j+i*data_length].contents[0])
                    writer.writerow(player_dict)
        except Exception as ex:
            print(ex)
            return False
        return True


    def write_ufas(self, filename):
        ''' Take information from CapFriendly regarding the UFAs '''
        name_list = set()
        try:
            with open(f'{filename}.csv', mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(['player_id'])      # Write header manually.
                for i in range(15):  # 50 players per page, i.e 'range(15)' means maximum of 15*50=750 players.
                    url = "https://www.capfriendly.com/browse/free-agents/2022/caphit/all/all/ufa/?pg=" + str(i+1)
                    scraper = cfscrape.create_scraper()
                    html = scraper.get(url).content
                    soup = BeautifulSoup(html, 'html.parser')
                    ufa_container = soup.find("table", {"id": "brwt"})
                    ufa_players = ufa_container.find_all("a")
                    for i in range(len(ufa_players)):
                        name_content = str(ufa_players[i].contents[0])
                        [player_id, __] = generate_player_and_team_id(name_content)
                        if (name_content[0] != "<") and (player_id != "NO_QO") and (player_id != "GROUP_6"):
                            if player_id == 'EVGENI_DADONOV':
                                player_id = 'EVGENII_DADONOV'
                            if player_id == 'PATRICK_MAROON':
                                player_id = 'PAT_MAROON'
                            player_id = player_id.replace('Å', 'A')
                            player_id = player_id.replace('Ä', 'A')
                            player_id = player_id.replace('Ö', 'O')
                            player_id = player_id.replace('Í', 'I')
                            player_id = player_id.replace('Á', 'A')
                            player_id = player_id.replace('Ü', 'U')
                            player_id = player_id.replace('É', 'E')
                            name_list.add(player_id)
                            writer.writerow([player_id])
        except Exception as ex:
            print('Could not download UFA information from ' + url)
            print(ex)
        return True

    def scrape_cf(self, team_id, url):
        ''' Download information from CapFriendly to decide which player belongs to what team '''
        op_ = {}
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        tables = soup.find_all('table')
        tr_classes = ["odd c", "even c"]
        for tr_class in tr_classes:
            tr_entries = tables[1].find_all('tr', {'class': tr_class})
            for tr in tr_entries:
                name_entry = tr.find('a')
                name_str = str(name_entry.text).replace(" ", "")
                name_str_array = name_str.split(",")
                player_id = name_str_array[1].upper() + "_" + name_str_array[0].upper()
                player_id = clean_cf_string(player_id)
                op_[player_id] = team_id
        return op_


    def clean_cf_string(self, player_id):
        """ Remove 'weird' characters from player_id, and match names from NaturalStatTrick """
        player_id = player_id.replace("'", "")
        player_id = player_id.replace(".", "_")
        player_id = player_id.replace("Á", "A")
        player_id = player_id.replace("É", "E")
        player_id = player_id.replace("Í", "I")
        player_id = player_id.replace("Ū", "U")
        player_id = player_id.replace("Å", "A")
        player_id = player_id.replace("Ä", "A")
        player_id = player_id.replace("Ö", "O")

        # Synchronize player names
        if player_id == "PATRICK_MAROON":
            player_id = "PAT_MAROON"
        elif player_id == "EVGENII_DADONOV":
            player_id = "EVGENI_DADONOV"
        elif player_id == "MICHAEL_MATHESON":
            player_id = "MIKE_MATHESON"
        elif player_id == "NICOLAS_PETAN":
            player_id = "NIC_PETAN"
        elif player_id == "JOSHUA_MORRISSEY":
            player_id = "JOSH_MORRISSEY"
        elif player_id == "ZACHARY_SANFORD":
            player_id = "ZACH_SANFORD"
        elif player_id == "ALEXANDER_WENNBERG":
            player_id = "ALEX_WENNBERG"
        elif player_id == "ANTHONY_DEANGELO":
            player_id = "TONY_DEANGELO"
        elif player_id == "LOUIS_BELPEDIO":
            player_id = "LOUIE_BELPEDIO"
        elif player_id == "SAMUEL_BLAIS":
            player_id = "SAMMY_BLAIS"
        elif player_id == "NICK_MERKLEY":
            player_id = "NICHOLAS_MERKLEY"
        elif player_id == "ZACHARY_WERENSKI":
            player_id = "ZACH_WERENSKI"
        elif player_id == "JEFFREY_TRUCHON-VIEL":
            player_id = "JEFFREY_VIEL"
        elif player_id == "MAXIME_COMTOIS":
            player_id = "MAX_COMTOIS"
        elif player_id == "JOSHUA_NORRIS":
            player_id = "JOSH_NORRIS"
        elif player_id == "ALEX_TRUE":
            player_id = "ALEXANDER_TRUE"
        elif player_id == "JOSEPH_VELENO":
            player_id = "JOE_VELENO"
        elif player_id == "JOSHUA_DUNNE":
            player_id = "JOSH_DUNNE"
        elif player_id == "AJ_GREER":
            player_id = "A_J__GREER"
        elif player_id == "NICHOLAS_CAAMANO":
            player_id = "NICK_CAAMANO"
        elif player_id == "DANIEL_RENOUF":
            player_id = "DAN_RENOUF"
        elif player_id == "MICHAEL_ANDERSON":
            player_id = "MIKEY_ANDERSON"
        elif player_id == "YEGOR_ZAMULA":
            player_id = "EGOR_ZAMULA"
        elif player_id == "ZACHARY_JONES":
            player_id = "ZAC_JONES"

        return player_id

    def write_player_team_info(self, filepath, team=None, verbose=True):
        ''' Update the CSV-file keeping track on which team each player is contracted to.
        Based on data from CapFriendly '''
        # Select which teams to go through
        if team is None:
            _iter = CF_TEAM_LINKS
        else:
            _iter = {team: CF_TEAM_LINKS[team]}

        # Loop through the selected teams
        all_players = {}
        for team_id, link in _iter.items():
            if verbose is True:
                print(f"Adding players to team {team_id}")
            # Add sleep in order to not spam servers
            time.sleep(1)
            # Scrape CF for the selected team
            players_in_team = scrape_cf(team_id, link)
            # Store information in struct holding all players
            for player_id in players_in_team:
                all_players[player_id] = players_in_team[player_id]

        # Write information to CSV-file
        with open(filepath, mode='w', newline='') as csv_file:
            fieldnames = ["player_id", "team_id"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for player_id in all_players:
                writer.writerow({"player_id": player_id, "team_id": all_players[player_id]})


def scrape_ep_player_info(url):
    # Declarations
    season_data, meta_data = {}, {}
    meta_data["split_seasons"], meta_data["seasons_played"] = [], []
    meta_data["nhl_gps"] = 0
    # EP request
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    # Find all tables
    tables = soup.find_all('table')
    # Get player-card information for meta data
    player_card = soup.find('div', {'class': 'ep-list'})
    # Sort out infomration about DOB, position and name
    dob_entry = player_card.find('div', {'class': "col-xs-12 col-17 text-right p-0 ep-text-color--black"})
    meta_data["dob_raw"] = dob_entry.text.strip()
    pos_entry = player_card.find('div', {'class': "col-xs-12 col-18 text-right p-0 ep-text-color--black"})
    meta_data["pos_raw"] = pos_entry.text.strip()
    meta_data["name_raw"] = url.split("/")[-1]  # This is not really correct - but maybe close enough...
    # Get total number of NHL-games played.
    total_stats = soup.find('div', {'id': 'total-stats'})  # @TODO: This should probably not be stored in "meta-data"
    na_trs = total_stats.find_all('tr', {'class': 'team-continent-NA'})
    for entry in na_trs:
        link_entry = entry.find("a", href=True)
        if link_entry.text.strip() == "NHL":
            try:
                meta_data["nhl_gps"] = int(entry.find('td', {'class': 'regular gp'}).text)
            except ValueError:
                meta_data["nhl_gps"] = 0

    # Find all information about the seasons played
    season_data_table = tables[1].find_all('td', {'class': 'season sorted'})
    team_data_table = tables[1].find_all('td', {'class': 'team'})
    league_data_table = tables[1].find_all('td', {'class': 'league'})
    gp_data_table = tables[1].find_all('td', {'class': 'regular gp'})
    g_data_table = tables[1].find_all('td', {'class': 'regular g'})
    a_data_table = tables[1].find_all('td', {'class': 'regular a'})
    if meta_data['pos_raw'] != "G":
        # Loop through each season
        for idx, season in enumerate(season_data_table):
            season_output = {}
            team_entry = team_data_table[idx]
            league_entry = league_data_table[idx]
            gp_entry = gp_data_table[idx]
            g_entry = g_data_table[idx]
            a_entry = a_data_table[idx]
            season_str = str(season.text).strip()
            # Store information weather or not a season is "split" (i.e. played for at least two different teams)
            if season_str in season_data.keys():
                dict_key = season_str + "__" + str(idx)
                if season_str not in meta_data["split_seasons"]:
                    meta_data["split_seasons"].append(season_str)
            else:
                dict_key = season_str

            season_output['season'] = season_str
            season_output['league'] = league_entry.text.strip()
            try:
                # Only add season data if at least 5 games are played.
                # As per 2022-03-15 Eliteprospects also adds a prediction of total points scored based
                # on current scoring rate. This "ghost season" needs to be removed
                if int(gp_entry.text) > 4 and team_entry.text.strip().upper() != "PROJECTED":
                    season_output['team'] = team_entry.text.strip()
                    season_output['gp'] = int(gp_entry.text)
                    season_output['g'] = int(g_entry.text)
                    season_output['a'] = int(a_entry.text)
                    season_data[dict_key] = season_output
                    if season_str not in meta_data["seasons_played"]:
                        meta_data["seasons_played"].append(season_str)
                # else:
                #     print(f"Ignoring season {season_str} due to too few games played")
            except ValueError:
                pass
    return [meta_data, season_data]


if __name__ == '__main__':
    pass