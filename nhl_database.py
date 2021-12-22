import csv
import datetime
from collections import defaultdict
import numpy as np
from nhl_helpers import *
from nhl_defines import *
from nhl_entities import Skater, Goalie, Team
# from nhl_web_scrape import *


class Database():
    def __init__(self, configuration):
        print('Creating a generic database')
        self.id_set = set()
        self.data = {}
        self._configuration = configuration

    def add_id(self, item_id):
        self.id_set.add(item_id)

    def get_player(self, player_id):
        return self.data[player_id]


class TeamDatabase():
    ''' Class to create and modify team database '''
    def __init__(self, configuration):
        ''' Constructor '''
        self.id_set = set()
        self.data = {}
        self._configuration = configuration
        self.setup_database()

    def setup_database(self):
        ''' Store all data from CSV-files into Team objects '''
        self.add_es_data()
        self.add_pp_data()
        self.add_pk_data()
        self.add_home_data()
        self.add_away_data()
        self.add_team_schedule()
        # @TODO: self.add_fattigue_information()
        self.add_additional_data()
        self.fix_seattle()

    def fix_seattle(self):
        """ Special fix to handle introduction of Seattle Kraken """
        kraken = self.get_team("MTL")
        kraken.name = "SEA"
        kraken.team_id = "SEA"
        kraken.set_division()
        self.data["SEA"] = kraken

    def add_es_data(self):
        ''' Adds ES-data for all teams '''
        with open(self._configuration.csvfiles['team_es'], 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            total_gp, total_otl, total_gf = 0, 0, 0
            for row in reader:
                if row[1] != 'team_name':
                    # Get data from row.
                    team_name = str(row[TEAM_DB_NAME_COL])
                    # Special case
                    if team_name == 'St Louis Blues':
                        team_name = 'St. Louis Blues'
                    team_id = get_team_id(team_name)
                    # Create a team if it doesn't already exists
                    if team_id not in self.id_set:
                        self.add_team(Team(team_id))
                    # Get team
                    team = self.get_team(team_id)

                    # Integers
                    if str(row[TEAM_DB_GP_COL]) == '-':
                        team.gp = 0
                    else:
                        team.gp = int(row[TEAM_DB_GP_COL])

                    if str(row[TEAM_DB_TOI_COL]) == '-':
                        team.team_toi_es = 0
                    else:
                        team.team_toi_es = int(60*float(row[TEAM_DB_TOI_COL]))

                    if str(row[TEAM_DB_W_COL]) == '-':
                        team.w = 0
                    else:
                        team.w = int(row[TEAM_DB_W_COL])

                    if str(row[TEAM_DB_L_COL]) == '-':
                        team.l = 0
                    else:
                        team.l = int(row[TEAM_DB_L_COL])

                    if str(row[TEAM_DB_OTL_COL]) == '-':
                        team.otl = 0
                    else:
                        team.otl = int(row[TEAM_DB_OTL_COL])

                    if str(row[TEAM_DB_P_COL]) == '-':
                        team.p = 0
                    else:
                        team.p = int(row[TEAM_DB_P_COL])

                    if str(row[TEAM_DB_CF_COL]) == '-':
                        team.cf = 0
                    else:
                        team.cf = int(row[TEAM_DB_CF_COL])

                    if str(row[TEAM_DB_CA_COL]) == '-':
                        team.ca = 0
                    else:
                        team.ca = int(row[TEAM_DB_CA_COL])

                    if str(row[TEAM_DB_FF_COL]) == '-':
                        team.ff = 0
                    else:
                        team.ff = int(row[TEAM_DB_FF_COL])

                    if str(row[TEAM_DB_FA_COL]) == '-':
                        team.fa = 0
                    else:
                        team.fa = int(row[TEAM_DB_FA_COL])

                    if str(row[TEAM_DB_SF_COL]) == '-':
                        team.sf = 0
                    else:
                        team.sf = int(row[TEAM_DB_SF_COL])

                    if str(row[TEAM_DB_SA_COL]) == '-':
                        team.sa = 0
                    else:
                        team.sa = int(row[TEAM_DB_SA_COL])

                    if str(row[TEAM_DB_GF_COL]) == '-':
                        team.gf = 0
                    else:
                        team.gf = int(row[TEAM_DB_GF_COL])

                    if str(row[TEAM_DB_GA_COL]) == '-':
                        team.ga = 0
                    else:
                        team.ga = int(row[TEAM_DB_GA_COL])

                    if str(row[TEAM_DB_SCF_COL]) == '-':
                        team.scf = 0
                    else:
                        team.scf = int(row[TEAM_DB_SCF_COL])

                    if str(row[TEAM_DB_SCA_COL]) == '-':
                        team.sca = 0
                    else:
                        team.sca = int(row[TEAM_DB_SCA_COL])

                    if str(row[TEAM_DB_HDCF_COL]) == '-':
                        team.hdcf = 0
                    else:
                        team.hdcf = int(row[TEAM_DB_HDCF_COL])

                    if str(row[TEAM_DB_HDCA_COL]) == '-':
                        team.hdca = 0
                    else:
                        team.hdca = int(row[TEAM_DB_HDCA_COL])

                    # Floats
                    if str(row[TEAM_DB_P_PCG_COL]) == '-':
                        team.p_pcg = 0.0
                    else:
                        team.p_pcg = float(row[TEAM_DB_P_PCG_COL])

                    if str(row[TEAM_DB_SF_PCG_COL]) == '-':
                        team.sf_pcg = 0.0
                    else:
                        team.sf_pcg = float(row[TEAM_DB_SF_PCG_COL])/100

                    if str(row[TEAM_DB_CF_PCG_COL]) == '-':
                        team.cf_pcg = 0.0
                    else:
                        team.cf_pcg = float(row[TEAM_DB_CF_PCG_COL])/100

                    if str(row[TEAM_DB_FF_PCG_COL]) == '-':
                        team.ff_pcg = 0.0
                    else:
                        team.ff_pcg = float(row[TEAM_DB_FF_PCG_COL])/100

                    if str(row[TEAM_DB_SCF_PCG_COL]) == '-':
                        team.scf_pcg = 0.0
                    else:
                        team.scf_pcg = float(row[TEAM_DB_SCF_PCG_COL])/100

                    if str(row[TEAM_DB_xGF_COL]) == '-':
                        team.xgf = 0
                    else:
                        team.xgf = float(row[TEAM_DB_xGF_COL])

                    if str(row[TEAM_DB_xGA_COL]) == '-':
                        team.xga = 0
                    else:
                        team.xga = float(row[TEAM_DB_xGA_COL])

                    if str(row[TEAM_DB_xGF_PCG_COL]) == '-':
                        team.xgf_pcg = 0.0
                    else:
                        team.xgf_pcg = float(row[TEAM_DB_xGF_PCG_COL])/100

                    if str(row[TEAM_DB_HDCF_PCG_COL]) == '-':
                        team.hdcf_pcg = 0.0
                    else:
                        team.hdcf_pcg = float(row[TEAM_DB_HDCF_PCG_COL])/100

                    if str(row[TEAM_DB_SV_PCG_COL]) == '-':
                        team.sv_pcg = 0.0
                    else:
                        team.sv_pcg = float(row[TEAM_DB_SV_PCG_COL])/100

                    if str(row[TEAM_DB_PDO_COL]) == '-':
                        team.pdo = 0.0
                    else:
                        team.pdo = float(row[TEAM_DB_PDO_COL])

                    total_gp += team.gp
                    total_otl += team.otl
                    total_gf += team.gf

    def add_home_data(self):
        ''' Adds home-ice data to all teams '''
        with open(self._configuration.csvfiles['team_pp'], 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'team_name':
                    # Get data from row.
                    team_name = str(row[TEAM_DB_NAME_COL])
                    # Special case
                    if team_name == 'St Louis Blues':
                        team_name = 'St. Louis Blues'
                    team_id = get_team_id(team_name)

                    # Make sure the team exists
                    if team_id not in self.id_set:
                        raise ValueError('Team ' + team_id + ' not previously added!')

                    # Get team
                    team = self.get_team(team_id)

                    # Update team with Home-ice-data
                    if str(row[TEAM_DB_P_PCG_COL]) == '-':
                        team.home_p_pcg = 0.0
                    else:
                        team.home_p_pcg = float(row[TEAM_DB_P_PCG_COL])

    def add_away_data(self):
        ''' Adds away-ice data to all teams '''
        with open(self._configuration.csvfiles['team_pp'], 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'team_name':
                    # Get data from row.
                    team_name = str(row[TEAM_DB_NAME_COL])
                    # Special case
                    if team_name == 'St Louis Blues':
                        team_name = 'St. Louis Blues'
                    team_id = get_team_id(team_name)

                    # Make sure the team exists
                    if team_id not in self.id_set:
                        raise ValueError('Team ' + team_id + ' not previously added!')

                    # Get team
                    team = self.get_team(team_id)

                    # Update team with Home-ice-data
                    if str(row[TEAM_DB_P_PCG_COL]) == '-':
                        team.away_p_pcg = 0.0
                    else:
                        team.away_p_pcg = float(row[TEAM_DB_P_PCG_COL])

    def add_pp_data(self):
        ''' Adds powerplay data to all teams '''
        with open(self._configuration.csvfiles['team_pp'], 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'team_name':
                    # Get data from row.
                    team_name = str(row[TEAM_DB_NAME_COL])
                    # Special case
                    if team_name == 'St Louis Blues':
                        team_name = 'St. Louis Blues'
                    team_id = get_team_id(team_name)

                    # Make sure the team exists
                    if team_id not in self.id_set:
                        raise ValueError('Team ' + team_id + ' not previously added!')

                    # Get team
                    team = self.get_team(team_id)

                    # Update team with PP-data
                    if str(row[TEAM_DB_TOI_COL]) == '-':
                        team.team_toi_pp = 0
                        team.team_gf_per_pp = 0
                    else:
                        team.team_toi_pp = int(60*float(row[TEAM_DB_TOI_COL]))
                        team.team_gf_per_pp = 120*int(row[TEAM_DB_GF_COL])/team.team_toi_pp  # Goals scored per two minutes (120 seconds) of PP.

                    if team.gp == 0:
                        team.team_toi_pp_per_gp = 0
                    else:
                        team.team_toi_pp_per_gp = team.team_toi_pp/team.gp

    def add_pk_data(self):
        ''' Adds penalty killing data to all teams '''
        with open(self._configuration.csvfiles['team_pk'], 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'team_name':
                    # Get data from row.
                    team_name = str(row[TEAM_DB_NAME_COL])
                    # Special case
                    if team_name == 'St Louis Blues':
                        team_name = 'St. Louis Blues'
                    team_id = get_team_id(team_name)

                    # Make sure the team exists
                    if team_id not in self.id_set:
                        raise ValueError('Team ' + team_id + ' not previously added!')

                    # Get team
                    team = self.get_team(team_id)

                    # Update team with PK-data
                    if str(row[TEAM_DB_TOI_COL]) == '-':
                        team.team_toi_pk = 0
                        team.team_ga_per_pk = 0
                    else:
                        team.team_toi_pk = int(60*float(row[TEAM_DB_TOI_COL]))
                        team.team_ga_per_pk = 120*int(row[TEAM_DB_GA_COL])/team.team_toi_pk  # Goals allowed per two minutes (120 seconds) of PK

                    if team.gp == 0:
                        team.team_toi_pk_per_gp = 0
                    else:
                        team.team_toi_pk_per_gp = team.team_toi_pk/team.gp

                    # Add data on combined special teams (@TODO: this should probably not be done here)
                    if team.team_ga_per_pk == 0:
                        team.special_teams_rating = 0
                    else:
                        team.special_teams_rating = team.team_gf_per_pp/team.team_ga_per_pk

    def add_team_schedule(self):
        ''' Add information about team scehdule '''
        for team_id in self.id_set:
            team = self.get_team(team_id)
            team.schedule = self._configuration.databases['team_schedules'][team_id]
            team.remaining_schedule = team.schedule[team.gp:]
            team.game_index = team.gp

    def add_additional_data(self):
        ''' Add additional data not stored in the CSV-files '''
        for team_id in self.id_set:
            team = self.get_team(team_id)
            team.add_additional_data()

    def get_team(self, team_id):
        ''' Return a given team based on its team-id/name '''
        return self.data[team_id]

    def add_team(self, team):
        ''' Add team to database '''
        if isinstance(team, Team) is not True:
            raise ValueError('Can only add object of type "Team" to TeamDatabase')
        self.data[team.name] = team
        self.id_set.add(team.name)


class SkaterDatabase():
    ''' Class to handle skater data
    #TODO: This should inherit from the class Database
    '''
    def __init__(self, configuration):
        ''' SkaterDatabase constructor '''
        self.id_set = set()
        self.data = {}
        self._configuration = configuration
        self.setup_database()

    def setup_database(self):
        ''' Method to parse information from csv-files '''
        self.add_bio_data()
        self.add_contract_data()
        self.add_ind_data(playform='es')
        self.add_ind_data(playform='pp')
        self.add_ind_data(playform='pk')
        self.add_on_ice_data()
        self.add_relative_data()
        self.add_additional_data()

    def add_skater(self, skater):
        ''' Add skater to database '''
        if isinstance(skater, Skater) is not True:
            raise ValueError('Can only add object of type "Skater" to SkaterDatabase')
        else:
            self.data[skater.bio['player_id']] = skater
            self.id_set.add(skater.bio['player_id'])

    def remove_skater(self, skater):
        ''' Remove skater from database. This  '''
        if isinstance(skater, Skater) is not True:
            raise ValueError('Can only add object of type "Skater" to SkaterDatabase')
        else:
            del self.data[skater.bio['player_id']]
            self.id_set.remove(skater.bio['player_id'])

    def get_player(self, player_id):
        ''' Return player from database '''
        return self.data[player_id]

    def add_bio_data(self, input_csv=None):
        ''' Create Skater-instance and store in database '''
        _settings = self._configuration
        ''' Read bio-data from CSV-file and create Skater-object to store in SkaterDb '''
        if input_csv is None:
            input_csv = _settings.csvfiles['skater_bio']
        player_team_db = generic_csv_reader(_settings.csvfiles['player_team_info'], dict_key_attribute='player_id')
        for season_data in input_csv:
            with open(season_data, 'rt') as file_handle:
                reader = csv.reader(file_handle, delimiter=',')
                for row in reader:
                    if (row[1] != 'player_name') and (row[1] != 'Player'):
                        # Create and store player-ID.
                        player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
                        try:
                            team_id = player_team_db[player_id]["team_id"]
                        except KeyError:
                            # This means that the player has no active contract
                            team_id = None

                        # Only add new players, that has an active contract
                        if player_id not in self.id_set and team_id is not None:
                            # Bio
                            bio_data = {}
                            bio_data['name'] = player_id
                            bio_data['player_id'] = player_id
                            bio_data['team_id'] = team_id
                            # Position
                            if str(row[SKATER_DB_BIO_POSITION]) == '-':
                                raise ValueError('Incorrect Player position')
                            else:
                                position = str(row[SKATER_DB_BIO_POSITION])
                                bio_data['position'] = position
                                if ('C' in position) or ('L' in position) or ('R' in position):
                                    bio_data['position'] = 'F'
                            # Age
                            if str(row[SKATER_DB_BIO_AGE]) == '-':
                                bio_data['age'] = 0
                            else:
                                bio_data['age'] = int(row[SKATER_DB_BIO_AGE])
                            # Height
                            if str(row[SKATER_DB_BIO_HEIGHT]) == '-':
                                bio_data['height'] = 0
                            else:
                                bio_data['height'] = int(row[SKATER_DB_BIO_HEIGHT])*2.54  # Convert to centimeters.
                            # Weight
                            if str(row[SKATER_DB_BIO_WEIGHT]) == '-':
                                bio_data['weight'] = 0
                            else:
                                bio_data['weight'] = int(row[SKATER_DB_BIO_WEIGHT])*0.453592  # Convert to kilograms.
                            # Draft year
                            if str(row[SKATER_DB_BIO_DRAFT_YEAR]) == '-':
                                bio_data['draft_year'] = 0
                            else:
                                bio_data['draft_year'] = int(row[SKATER_DB_BIO_DRAFT_YEAR])
                            # Draft team
                            if str(row[SKATER_DB_BIO_DRAFT_TEAM]) == '-':
                                bio_data['draft_team'] = 'N/A'
                            else:
                                bio_data['draft_team'] = str(row[SKATER_DB_BIO_DRAFT_TEAM])
                            # Draft round
                            if str(row[SKATER_DB_BIO_DRAFT_ROUND]) == '-':
                                bio_data['draft_round'] = 7  # Default to last round
                            else:
                                bio_data['draft_round'] = int(row[SKATER_DB_BIO_DRAFT_ROUND])
                            # Draft position
                            if str(row[SKATER_DB_BIO_TOTAL_DRAFT_POS]) == '-':
                                bio_data['total_draft_pos'] = 225  # Default to one pick after last pick in the last round
                            else:
                                bio_data['total_draft_pos'] = int(row[SKATER_DB_BIO_TOTAL_DRAFT_POS])
                            self.add_skater(Skater(bio_data))

    def add_ind_data(self, input_csv=None, playform=None):
        ''' Class method to read individual data from stored .csv-file(s),
            and update Skater-object in Skater-database.

            @TODO:  If a value in a row is empty (or "-") the convertion to int/float will crash.
                    One possible solution would be to include this logic in stack()
        '''
        if playform is None:
            raise ValueError('Playform needs to be selected for individual data!')
        if input_csv is None:
            input_csv = self._configuration.csvfiles['skater_' + playform]

        for season_data in input_csv:
            with open(season_data, 'rt') as file_handle:
                reader = csv.reader(file_handle, delimiter=',')
                for row in reader:
                    if row[1].upper() != 'PLAYER_NAME':
                        # Only add players that are playing today.
                        if row[SKATER_DB_BIO_NAME] == 'Sebastian Aho':
                            """
                            [player_id, __] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME],
                                                                        row[SKATER_DB_BIO_TEAM_ID])
                            """
                            player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
                            print("WE NEED TO TALK ABOUT SEBASTIAN AHO")
                        else:
                            player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
                        if player_id in self.id_set:
                            skater = self.get_player(player_id)
                            ind_data = skater.get_ind_data()
                            if str(row[SKATER_DB_IND_TEAM_ID]) == '-':
                                raise ValueError('Incorrect team_id ' + str(row[SKATER_DB_IND_TEAM_ID]))
                            else:
                                ind_data['multiple_teams'] = False
                                if len(str(row[SKATER_DB_IND_TEAM_ID]).split(',')) > 1:
                                    ind_data['multiple_teams'] = True
                            # Time on ice
                            ind_data = stack(ind_data, attribute='toi', playform=playform, value=int(60*float(row[SKATER_DB_IND_TOI])))
                            # Goals
                            ind_data = stack(ind_data, attribute='goals', playform=playform, value=int(row[SKATER_DB_IND_GOALS]))
                            # Assists
                            ind_data = stack(ind_data, attribute='assists',playform=playform, value=int(row[SKATER_DB_IND_ASSIST]))
                            # Primary assist
                            ind_data = stack(ind_data, attribute='primary_assists', playform=playform, value=int(row[SKATER_DB_IND_FIRST_ASSIST]))
                            # Secondary assists
                            ind_data = stack(ind_data, attribute='secondary_assists', playform=playform, value=int(row[SKATER_DB_IND_SECOND_ASSIST]))
                            # Individual shots taken
                            ind_data = stack(ind_data, attribute='sf', playform=playform, value=int(row[SKATER_DB_IND_SF]))
                            # Individual Corsi
                            ind_data = stack(ind_data, attribute='icf', playform=playform, value=int(row[SKATER_DB_IND_ICF]))
                            # Individual Fenwick
                            ind_data = stack(ind_data, attribute='iff', playform=playform, value=int(row[SKATER_DB_IND_IFF]))
                            # Individual scoring chances
                            ind_data = stack(ind_data, attribute='iscf', playform=playform, value=int(row[SKATER_DB_IND_ISCF]))
                            # Total penatlies taken
                            ind_data = stack(ind_data, attribute='pt', playform=playform, value=int(row[SKATER_DB_IND_TOTAL_PENALTIES]))
                            # Total penalties drawn
                            ind_data = stack(ind_data, attribute='pd', playform=playform, value=int(row[SKATER_DB_IND_PENALTIES_DRAWN]))
                            # Individual hits given
                            ind_data = stack(ind_data, attribute='hits', playform=playform, value=int(row[SKATER_DB_IND_HITS]))
                            # Individual hits taken
                            ind_data = stack(ind_data, attribute='hits_taken', playform=playform, value=int(row[SKATER_DB_IND_HITS_TAKEN]))
                            # Individual expected goals forward
                            ind_data = stack(ind_data, attribute='ixgf', playform=playform, value=float(row[SKATER_DB_IND_IXG]))
                            # Update skater object
                            skater.add_ind_data(ind_data)
                        else:
                            # print('Player ' + player_id + ' not included in BIO-data')
                            pass

    def add_on_ice_data(self, input_csv=None):
        ''' Class method to read on-ice data from stored .csv-file(s), and update Skater-object in
            Skater-database.
        '''
        if input_csv is None:
            input_csv = self._configuration.csvfiles['skater_on_ice']
        for season_data in input_csv:
            with open(season_data, 'rt') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if row[1] != 'player_name':
                        # Only add players that are playing today.
                        if row[SKATER_DB_BIO_NAME] == 'Sebastian Aho':
                            """
                            [player_id, __] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME],
                                                                        row[SKATER_DB_BIO_TEAM_ID])
                            """
                            player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
                            print("WE NEED TO TALK ABOUT SEBASTIAN AHO")
                        else:
                            player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
                        if player_id in self.id_set:
                            skater = self.get_player(player_id)
                            on_ice_data = skater.get_on_ice_data()

                            # Game played
                            on_ice_data = stack(on_ice_data, attribute='gp', value=int(row[SKATER_DB_ON_ICE_GP]))
                            # Corsi forward
                            on_ice_data = stack(on_ice_data, attribute='cf', value=int(row[SKATER_DB_ON_ICE_CF]))
                            # Corsi against
                            on_ice_data = stack(on_ice_data, attribute='ca', value=int(row[SKATER_DB_ON_ICE_CA]))
                            # Goals forward
                            on_ice_data = stack(on_ice_data, attribute='gf', value=int(row[SKATER_DB_ON_ICE_GF]))
                            # Goals against
                            on_ice_data = stack(on_ice_data, attribute='ga', value=int(row[SKATER_DB_ON_ICE_GA]))
                            # Shots forward
                            on_ice_data = stack(on_ice_data, attribute='sf', value=int(row[SKATER_DB_ON_ICE_SF]))
                            # Shots against
                            on_ice_data = stack(on_ice_data, attribute='sa', value=int(row[SKATER_DB_ON_ICE_SA]))
                            # Expected goals forward
                            if player_id == "ERIK_KARLSSON":
                                print(f"{player_id}: Stacking value {float(row[SKATER_DB_ON_ICE_xGF])}")
                            on_ice_data = stack(on_ice_data, attribute='xgf', value=float(row[SKATER_DB_ON_ICE_xGF]))
                            # Expected goals against
                            on_ice_data = stack(on_ice_data, attribute='xga', value=float(row[SKATER_DB_ON_ICE_xGA]))
                            # Scoring chances forward
                            on_ice_data = stack(on_ice_data, attribute='scf', value=int(row[SKATER_DB_ON_ICE_SCF]))
                            # Scoring chances against
                            on_ice_data = stack(on_ice_data, attribute='sca', value=int(row[SKATER_DB_ON_ICE_SCA]))
                            # High danger chances forward
                            on_ice_data = stack(on_ice_data, attribute='hdcf', value=int(row[SKATER_DB_ON_ICE_HDCF]))
                            # High danger chances against
                            on_ice_data = stack(on_ice_data, attribute='hdca', value=int(row[SKATER_DB_ON_ICE_HDCA]))
                            # Offensive zone starts
                            on_ice_data = stack(on_ice_data, attribute='ozs', value=int(row[SKATER_DB_ON_ICE_OZS]))
                            # Neutral zone starts
                            on_ice_data = stack(on_ice_data, attribute='nzs', value=int(row[SKATER_DB_ON_ICE_NZS]))
                            # Defensive zone starts
                            on_ice_data = stack(on_ice_data, attribute='dzs', value=int(row[SKATER_DB_ON_ICE_DZS]))
                            # Offensice zone face-offs
                            on_ice_data = stack(on_ice_data, attribute='ozfo', value=int(row[SKATER_DB_ON_ICE_OZFO]))
                            # Neutral zone face-offs
                            on_ice_data = stack(on_ice_data, attribute='nzfo', value=int(row[SKATER_DB_ON_ICE_NZFO]))
                            # Defensive zone face-offs
                            on_ice_data = stack(on_ice_data, attribute='dzfo', value=int(row[SKATER_DB_ON_ICE_DZFO]))
                            # Update Skater with on-ice data
                            skater.add_on_ice_data(on_ice_data)

    def add_relative_data(self, input_csv=None):
        '''
        Add relative data to skater. Relative data cannot be staggered, hence data from only one season is used.
        '''
        if input_csv is None:
            input_csv = self._configuration.csvfiles['skater_relative']
        with open(input_csv) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'player_name':
                    # Since relative data cannot be staggered, this special fix is neede
                    [is_aho, aho_id] = is_this_aho(row[SKATER_DB_RELATIVE_NAME], row[SKATER_DB_RELATIVE_TEAM_ID])
                    if is_aho:
                        player_id = aho_id
                    else:
                        player_id = generate_player_id(row[SKATER_DB_RELATIVE_NAME])

                    if player_id in self.id_set:
                        skater = self.get_player(player_id)
                        if str(row[SKATER_DB_RELATIVE_CF_PER_60]) == '-':
                            skater.on_ice['rel_cf_per_60'] = 0
                        else:
                            skater.on_ice['rel_cf_per_60'] = float(row[SKATER_DB_RELATIVE_CF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_CA_PER_60]) == '-':
                            skater.on_ice['rel_ca_per_60'] = 0
                        else:
                            skater.on_ice['rel_ca_per_60'] = float(row[SKATER_DB_RELATIVE_CA_PER_60])
                        if str(row[SKATER_DB_RELATIVE_CF_PCG]) == '-':
                            skater.on_ice['rel_cf_pcg'] = 0
                            skater.on_ice['rel_cf_factor'] = 0
                            skater.on_ice['rel_ca_factor'] = 0
                        else:
                            skater.on_ice['rel_cf_pcg'] = float(row[SKATER_DB_RELATIVE_CF_PCG])
                            skater.on_ice['rel_cf_factor'] = (skater.on_ice['rel_cf_pcg']/200 + 1.0)  # Higher is better
                            skater.on_ice['rel_ca_factor'] = (1.0 - skater.on_ice['rel_cf_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_FF_PER_60]) == '-':
                            skater.on_ice['rel_ff_per_60'] = 0
                        else:
                            skater.on_ice['rel_ff_per_60'] = float(row[SKATER_DB_RELATIVE_FF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_FA_PER_60]) == '-':
                            skater.on_ice['rel_fa_per_60'] = 0
                        else:
                            skater.on_ice['rel_fa_per_60'] = float(row[SKATER_DB_RELATIVE_FA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_FF_PCG]) == '-':
                            skater.on_ice['rel_ff_pcg'] = 0
                            skater.on_ice['rel_ff_factor'] = 0
                            skater.on_ice['rel_fa_factor'] = 0
                        else:
                            skater.on_ice['rel_ff_pcg'] = float(row[SKATER_DB_RELATIVE_FF_PCG])
                            skater.on_ice['rel_ff_factor'] = (skater.on_ice['rel_ff_pcg']/200 + 1.0)  # Higher is better
                            skater.on_ice['rel_fa_factor'] = (1.0 - skater.on_ice['rel_ff_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_SF_PER_60]) == '-':
                            skater.on_ice['rel_sf_per_60'] = 0
                        else:
                            skater.on_ice['rel_sf_per_60'] = float(row[SKATER_DB_RELATIVE_SF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_SA_PER_60]) == '-':
                            skater.on_ice['rel_sa_per_60'] = 0
                        else:
                            skater.on_ice['rel_sa_per_60'] = float(row[SKATER_DB_RELATIVE_SA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_SF_PCG]) == '-':
                            skater.on_ice['rel_sf_pcg'] = 0
                            skater.on_ice['rel_sf_factor'] = 0
                            skater.on_ice['rel_sa_factor'] = 0
                        else:
                            skater.on_ice['rel_sf_pcg'] = float(row[SKATER_DB_RELATIVE_SF_PCG])
                            skater.on_ice['rel_sf_factor'] = (skater.on_ice['rel_sf_pcg']/200 + 1.0)  # Higher is better
                            skater.on_ice['rel_sa_factor'] = (1.0 - skater.on_ice['rel_sf_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_GF_PER_60]) == '-':
                            skater.on_ice['rel_gf_per_60'] = 0
                        else:
                            skater.on_ice['rel_gf_per_60'] = float(row[SKATER_DB_RELATIVE_GF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_GA_PER_60]) == '-':
                            skater.on_ice['rel_ga_per_60'] = 0
                        else:
                            skater.on_ice['rel_ga_per_60'] = float(row[SKATER_DB_RELATIVE_GA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_GF_PCG]) == '-':
                            skater.on_ice['rel_gf_pcg'] = 0
                            skater.on_ice['rel_gf_factor'] = 0
                            skater.on_ice['rel_ga_factor'] = 0
                        else:
                            skater.on_ice['rel_gf_pcg'] = float(row[SKATER_DB_RELATIVE_GF_PCG])
                            skater.on_ice['rel_gf_factor'] = (skater.on_ice['rel_gf_pcg']/200 + 1.0)  # Higher is better
                            skater.on_ice['rel_ga_factor'] = (1.0 - skater.on_ice['rel_gf_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_xGF_PER_60]) == '-':
                            skater.on_ice['rel_xgf_per_60'] = 0
                        else:
                            skater.on_ice['rel_xgf_per_60'] = float(row[SKATER_DB_RELATIVE_xGF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_XGA_PER_60]) == '-':
                            skater.on_ice['rel_xga_per_60'] = 0
                        else:
                            skater.on_ice['rel_xga_per_60'] = float(row[SKATER_DB_RELATIVE_XGA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_xGF_PCG]) == '-':
                            skater.on_ice['rel_xgf_pcg'] = 0
                            skater.on_ice['rel_xgf_factor'] = 0
                            skater.on_ice['rel_xga_factor'] = 0
                        else:
                            skater.on_ice['rel_xgf_pcg'] = float(row[SKATER_DB_RELATIVE_xGF_PCG])
                            skater.on_ice['rel_xgf_factor'] = (skater.on_ice['rel_xgf_pcg']/200 + 1.0)  # Higher is better
                            skater.on_ice['rel_xga_factor'] = (1.0 - skater.on_ice['rel_xgf_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_SCF_PER_60]) == '-':
                            skater.on_ice['rel_scf_per_60'] = 0
                        else:
                            skater.on_ice['rel_scf_per_60'] = float(row[SKATER_DB_RELATIVE_SCF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_SCA_PER_60]) == '-':
                            skater.on_ice['rel_sca_per_60'] = 0
                        else:
                            skater.on_ice['rel_sca_per_60'] = float(row[SKATER_DB_RELATIVE_SCA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_SCF_PCG]) == '-':
                            skater.on_ice['rel_scf_pcg'] = 0
                            skater.on_ice['rel_scf_factor'] = 0
                            skater.on_ice['rel_sca_factor'] = 0
                        else:
                            skater.on_ice['rel_scf_pcg'] = float(row[SKATER_DB_RELATIVE_SCF_PCG])
                            skater.on_ice['rel_scf_factor'] = (skater.on_ice['rel_scf_pcg']/200 + 1.0)  # Higher is better
                            skater.on_ice['rel_sca_factor'] = (1.0 - skater.on_ice['rel_scf_pcg']/200)  # Lower is better
                    else:
                        if self._configuration.verbose is True:
                            print(player_id + ' is not an active player!')

    def add_contract_data(self, input_csv=None):
        '''
        Adds (very) basic contract information from CapFriendlly
        '''
        if input_csv is None:
            input_csv = self._configuration.csvfiles['contract_data']
        ufas = []
        with open(input_csv, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[0] != 'player_id':
                    ufas.append(row[0])

        for player_id in self.id_set:
            skater = self.get_player(player_id)
            if player_id in ufas:
                skater.bio["ufa"] = True
            else:
                skater.bio["ufa"] = False

    def add_additional_data(self):
        '''
        Adds additional data to database.
        @TODO: This function should probably change name, since it does more than adding data
        '''
        players_to_remove = []
        for player_id in self.id_set:
            skater = self.get_player(player_id)
            if skater.ind == {}:
                players_to_remove.append(skater.bio['name'])
            else:
                skater.add_additional_ind_data()
                skater.add_additional_on_ice_data()
                # There might be a difference between the season data used for relative data and all other data, hence
                # a check to see if all players have been assigned relative data is needed.
                skater.validate_relative_data()

        # Remove players which only have bio-data.
        for player_id in players_to_remove:
            self.remove_skater(self.get_player(player_id))

    def get_players_rank(self, player_id, attribute, reverse=True):
        ''' Finds a certain players ranking based on a specified attribute. Sorts ascending as default. '''
        skater = self.get_player(player_id)
        attribute_value = skater.get_attribute(attribute)
        lst = []
        for s_id in self.id_set:
            lst.append(self.get_player(s_id).get_attribute(attribute))
        lst.sort(reverse=reverse)
        return lst.index(attribute_value) + 1

    def get_data_dict(self, attributes):
        ''' Return dictionary of lists for each specified attribute '''
        data_dict = defaultdict(list)
        if isinstance(attributes, list) is False:
            attributes = [attributes]
        for player_id in self.id_set:
            player = self.get_player(player_id)
            for attribute in attributes:
                data_dict[attribute].append(player.get_attribute(attribute))
        return data_dict


class GoalieDatabase():
    ''' Class to handle Goalies (not Martin Jones) '''
    def __init__(self, configuration):
        ''' GoalieDatabase constructor '''
        self.id_set = set()
        self.data = {}
        self._configuration = configuration
        self.setup_database()

    def setup_database(self):
        ''' Method to parse information from csv-files '''
        self.add_bio_data()
        self.add_ind_data(playform='es')
        self.add_ind_data(playform='pp')
        self.add_ind_data(playform='pk')
        self.add_additional_data()

    def add_goalie(self, goalie):
        ''' Add instance to database '''
        if isinstance(goalie, Goalie) is not True:
            raise ValueError('Can only add object of type "Goalie" to GoalieDatabase')
        else:
            self.data[goalie.bio['player_id']] = goalie
            self.id_set.add(goalie.bio['player_id'])

    def get_player(self, player_id):
        ''' Return player from database '''
        return self.data[player_id]

    def add_bio_data(self, input_csv=None):
        ''' Create Goalie-instance and store in database '''
        _settings = self._configuration
        # Read bio-data from CSV-file and create Goalie object to store in GoalieDb
        if input_csv is None:
            input_csv = _settings.csvfiles['goalie_bio']
        player_team_db = generic_csv_reader(_settings.csvfiles['player_team_info'], dict_key_attribute='player_id')
        for season_data in input_csv:
            with open(season_data, 'rt') as file_handle:
                reader = csv.reader(file_handle, delimiter=',')
                for row in reader:
                    if (row[1] != 'player_name') and (row[1] != 'Player'):
                        # Create and store player-ID.
                        player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
                        try:
                            team_id = player_team_db[player_id]["team_id"]
                        except KeyError:
                            # This means that the player has no active contract
                            team_id = None

                        # Only add new players
                        if player_id not in self.id_set and team_id is not None:
                            # Bio
                            bio_data = {}
                            bio_data['name'] = player_id
                            bio_data['player_id'] = player_id
                            bio_data['team_id'] = team_id
                            bio_data['position'] = 'G'

                            self.add_goalie(Goalie(bio_data))

    def add_ind_data(self, input_csv=None, playform=None):
        ''' Class method to read individual data from stored .csv-file(s),
            and update Goalie object in Goalie-database.

            @TODO:  If a value in a row is empty (or "-") the convertion to int/float will crash.
                    One possible solution would be to include this logic in stack()
        '''
        if playform is None:
            raise ValueError('Playform needs to be selected for individual data!')
        if input_csv is None:
            input_csv = self._configuration.csvfiles['goalie_' + playform]

        for season_data in input_csv:
            with open(season_data, 'rt') as file_handle:
                reader = csv.reader(file_handle, delimiter=',')
                for row in reader:
                    if row[1] != 'Player':
                        player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
                        if player_id in self.id_set:
                            goalie = self.get_player(player_id)
                            ind_data = goalie.get_ind_data()
                            if str(row[SKATER_DB_IND_TEAM_ID]) == '-':
                                raise ValueError('Incorrect team_id ' + str(row[SKATER_DB_IND_TEAM_ID]))
                            else:
                                ind_data['multiple_teams'] = False
                                if len(str(row[SKATER_DB_IND_TEAM_ID]).split(',')) > 1:
                                    ind_data['multiple_teams'] = True
                            # Time on ice
                            ind_data = stack(ind_data, attribute='toi', playform=playform, value=int(60*float(row[GOALIE_DB_TOI])))
                            # Goals
                            ind_data = stack(ind_data, attribute='sa', playform=playform, value=int(row[GOALIE_DB_SA]))
                            # Assists
                            ind_data = stack(ind_data, attribute='sv', playform=playform, value=int(row[GOALIE_DB_SV]))
                            # Primary assist
                            ind_data = stack(ind_data, attribute='ga', playform=playform, value=int(row[GOALIE_DB_GA]))
                            # Secondary assists
                            ind_data = stack(ind_data, attribute='gsaa', playform=playform, value=float(row[GOALIE_DB_GSAA]))
                            # Individual shots taken
                            ind_data = stack(ind_data, attribute='xga', playform=playform, value=float(row[GOALIE_DB_XGA]))
                            # Individual Corsi
                            ind_data = stack(ind_data, attribute='avg_shot_dist', playform=playform, value=float(row[GOALIE_DB_AVG_SHOT_DIST]))
                            # Individual Fenwick
                            ind_data = stack(ind_data, attribute='avg_goal_dist', playform=playform, value=float(row[GOALIE_DB_AVG_GOAL_DIST]))

                            # Update skater object
                            goalie.add_ind_data(ind_data)

    def add_additional_data(self):
        '''
        Adds additional data to database.
        '''
        players_to_remove = []
        for player_id in self.id_set:
            goalie = self.get_player(player_id)
            if goalie.ind == {}:
                players_to_remove.append(goalie.bio['name'])
            else:
                goalie.add_additional_ind_data()
        # Remove players which only have bio-data.
        for player_id in players_to_remove:
            self.remove_skater(self.get_player(player_id))

def create_metrics(team_db, skater_db, goalie_db={}, unavailable_players={}):
    ''' Create metrics and rankings for teams and player (skaters and goalies) '''
    # @TODO: This function REALLY needs an overhaul
    # Initialization
    sf_dict = defaultdict(list)
    gf_dict = defaultdict(list)
    ixgf_dict = defaultdict(list)
    scf_dict = defaultdict(list)
    sca_dict = defaultdict(list)
    estimated_off_dict = defaultdict(list)
    estimated_def_dict = defaultdict(list)
    shots_against_dict = defaultdict(list)
    shots_saved_dict = defaultdict(list)
    toi_dict_skater = defaultdict(list)
    goals_saved_above_expected_dict = defaultdict(list)
    xgf_per_sec, xga_per_sec = defaultdict(list), defaultdict(list)
    gp_array = []

    # Update Skater data
    for skater_id in skater_db.id_set:
        skater = skater_db.get_player(skater_id)
        skater.ind['toi_pcg'] = {}
        if skater.bio["team_id"] == "SEA":
            if datetime.datetime.now().month not in [8, 9, 10]:
                raise ValueError("This needs to be updated")
            skater.ind['toi_pcg']['es'] = skater.ind['toi_per_gp']['es'] / team_db.data["MTL"].team_toi_es_per_gp
            skater.ind['toi_pcg']['pp'] = skater.ind['toi_per_gp']['pp'] / team_db.data["MTL"].team_toi_pp_per_gp
            skater.ind['toi_pcg']['pk'] = skater.ind['toi_per_gp']['pk'] / team_db.data["MTL"].team_toi_pk_per_gp
            skater.on_ice['rel_gf_diff_per_60'] = skater.on_ice['gf_diff_per_60'] - team_db.data["MTL"].gf_diff_per_60  # MTL is very average...
        else:
            skater.ind['toi_pcg']['es'] = skater.ind['toi_per_gp']['es'] / team_db.data[skater.bio['team_id']].team_toi_es_per_gp
            skater.ind['toi_pcg']['pp'] = skater.ind['toi_per_gp']['pp'] / team_db.data[skater.bio['team_id']].team_toi_pp_per_gp
            skater.ind['toi_pcg']['pk'] = skater.ind['toi_per_gp']['pk'] / team_db.data[skater.bio['team_id']].team_toi_pk_per_gp
            skater.on_ice['rel_gf_diff_per_60'] = skater.on_ice['gf_diff_per_60'] - team_db.data[skater.bio['team_id']].gf_diff_per_60

        # Estimate offensive and defensive capabilities. Different depending on the skater has played for multiple teams or not.
        # Per 2021-05-08: xgf
        estimated_off_metric = 'xg'
        estimated_off = skater.on_ice[estimated_off_metric + 'f'] * skater.on_ice['rel_' + estimated_off_metric + 'f_factor']
        estimated_def = skater.on_ice[estimated_off_metric + 'a'] * skater.on_ice['rel_' + estimated_off_metric + 'a_factor']

        # Not really sure if this code should be included..
        # If included, it is assumed that the player will perform in line with his new team (however, still taking the relative factor into account).
        # If excluded, the player might be "dragged down" by his previous club.
        '''
        if skater.bio['multiple_teams'] == True:
            estimated_off = team_db[skater.bio['team_id']].exp_data[estimated_off_metric + 'f_per_sec'] * skater.ind['toi']['es'] * skater.on_ice['rel_' + estimated_off_metric + 'f_factor']
            estimated_def = team_db[skater.bio['team_id']].exp_data[estimated_off_metric + 'a_per_sec'] * skater.ind['toi']['es'] * skater.on_ice['rel_' + estimated_off_metric + 'a_factor']
        '''
        skater.on_ice['estimated_off'] = estimated_off
        skater.on_ice['estimated_def'] = estimated_def
        skater.on_ice['estimated_off_diff'] = estimated_off - estimated_def
        if skater.ind['toi']['es'] == 0:
            skater.on_ice['xgf_per_sec'] = 0
            skater.on_ice['xga_per_sec'] = 0
            skater.on_ice['estimated_off_per_sec'] = 0
            skater.on_ice['estimated_def_per_sec'] = 0
        else:
            skater.on_ice['xgf_per_sec'] = (skater.on_ice['xgf']) / skater.ind['toi']['es']
            skater.on_ice['xga_per_sec'] = (skater.on_ice['xga']) / skater.ind['toi']['es']
            skater.on_ice['estimated_off_per_sec'] = estimated_off / skater.ind['toi']['es']
            skater.on_ice['estimated_def_per_sec'] = estimated_def / skater.ind['toi']['es']
        skater.on_ice['estimated_off_per_60'] = skater.on_ice['estimated_off_per_sec']*3600
        skater.on_ice['estimated_def_per_60'] = skater.on_ice['estimated_def_per_sec']*3600
        skater.on_ice['xgf_per_60'] = skater.on_ice['xgf_per_sec']*3600
        skater.on_ice['xga_per_60'] = skater.on_ice['xga_per_sec']*3600
        skater.on_ice['estimated_off_per_60_diff'] = skater.on_ice['estimated_off_per_60'] - skater.on_ice['estimated_def_per_60']
        skater.on_ice['estimated_fun_factor'] = skater.on_ice['estimated_off_per_60'] + skater.on_ice['estimated_def_per_60']
        # Only use available players for the ranking data
        # Store estimated offensive and defensive capabilities per team.
        if skater_id not in unavailable_players:
            sf_dict[skater.bio['team_id']].append(skater.ind['isf']['es'])
            gf_dict[skater.bio['team_id']].append(skater.ind['goals']['es'])
            ixgf_dict[skater.bio['team_id']].append(skater.ind['ixgf']['es'])
            scf_dict[skater.bio['team_id']].append(skater.on_ice['scf'])
            sca_dict[skater.bio['team_id']].append(skater.on_ice['sca'])

            # Store estimated offensive and defensive capabilities per team.
            xgf_per_sec[skater.bio['team_id']].append(skater.on_ice['xgf_per_sec'])
            xga_per_sec[skater.bio['team_id']].append(skater.on_ice['xga_per_sec'])
            estimated_off_dict[skater.bio['team_id']].append(estimated_off)
            estimated_def_dict[skater.bio['team_id']].append(estimated_def)
            toi_dict_skater[skater.bio['team_id']].append(skater.ind['toi']['es'])
        # Error/warning handling for weird input
        if (skater.on_ice['estimated_off_per_sec'] + skater.on_ice['estimated_def_per_sec']) == 0:
            raise ValueError('Bad input for player ' + skater.bio['name'])
        else:
            skater.on_ice['estimated_off_pcg'] = skater.on_ice['estimated_off_per_sec'] / (skater.on_ice['estimated_off_per_sec']+skater.on_ice['estimated_def_per_sec'])

    # Update goalie data
    toi_dict_goalies = defaultdict(list)
    for g_id, goalie in goalie_db.data.items():
        # Calculate total sa/ss per team, only if player is available
        if g_id not in unavailable_players:
            shots_against_dict[goalie.bio['team_id']].append(goalie.get_attribute('sa', playform_index=-1))
            shots_saved_dict[goalie.bio['team_id']].append(goalie.get_attribute('sv', playform_index=-1))
            toi_dict_goalies[goalie.bio['team_id']].append(goalie.ind['toi']['es'])
            goals_saved_above_expected_dict[goalie.bio['team_id']].append(goalie.ind['gsax']['es'])
    # This loop needs to happen, since the total toi_dict_goalies is created in the previous one.
    for g_id in goalie_db.id_set:
        goalie = goalie_db.get_player(g_id)
        goalie.ind['toi_pcg'] = {}
        goalie.ind['toi_pcg']['es'] = goalie.ind['toi']['es'] / sum(toi_dict_goalies[goalie.bio['team_id']])

    # Update team data
    for team_id in team_db.id_set:
        gp_array.append(team_db.data[team_id].gp)
    avg_gp = np.mean(gp_array)
    games_needed = 15
    if avg_gp > games_needed:
        avg_gp = games_needed

    # Special fix to handle inlcusion of Seattle
    team_db.data["SEA"] = team_db.data["MTL"]
    if datetime.datetime.now().month not in [8, 9, 10]:
        raise ValueError("This must be updated")

    tmp_team_data = []
    for team_id in ACTIVE_TEAMS:
        for g_id, goalie in goalie_db.data.items():
            # goalie = goalie_db.data[g_id]
            if goalie.bio['team_id'] == team_id:
                sv_pcg = 100*goalie.ind["sv"]["es"]/goalie.ind["sa"]["es"]
        team_sh_pcg = sum(gf_dict[team_id])/sum(sf_dict[team_id])
        team_sv_pcg = sum(shots_saved_dict[team_id])/sum(shots_against_dict[team_id])
        team_estimated_off = sum(estimated_off_dict[team_id])  # How much offense the team generates, based on the individual players.
        team_estimated_def = sum(estimated_def_dict[team_id])  # How much offense the team gives up, based on the individual players.
        team_db.data[team_id].exp_data['sh_pcg'] = team_sh_pcg
        team_db.data[team_id].exp_data['sv_pcg'] = team_sv_pcg
        team_db.data[team_id].exp_data['team_off'] = team_estimated_off
        team_db.data[team_id].exp_data['team_def'] = team_estimated_def
        team_db.data[team_id].exp_data['team_off_pcg'] = team_estimated_off/(team_estimated_off+team_estimated_def)

        team_db.data[team_id].exp_data['estimated_off'] = team_estimated_off*team_db.data[team_id].exp_data['sh_pcg']
        team_db.data[team_id].exp_data['estimated_def'] = team_estimated_def*(1-team_db.data[team_id].exp_data['sv_pcg'])
        team_db.data[team_id].exp_data['estimated_off_pcg'] = team_db.data[team_id].exp_data['estimated_off']/(team_db.data[team_id].exp_data['estimated_off']+team_db.data[team_id].exp_data['estimated_def'])
        team_db.data[team_id].exp_data['pdo'] = team_db.data[team_id].exp_data['sh_pcg']+team_db.data[team_id].exp_data['sv_pcg']


        # Assign ratings. Different for pre_season or non_pre_season.
        # Special construction to blur effects of an exceptionally bad/good player changing teams
        pre_season_off = team_db.data[team_id].exp_data['team_off']
        pre_season_def = team_db.data[team_id].exp_data['team_def']
        team_db.data[team_id].exp_data['pre_season_rating'] = pre_season_off/(pre_season_off + pre_season_def)
        team_db.data[team_id].exp_data['in_season_rating'] = (team_db.data[team_id].p_pcg*P_PCG_FACTOR*avg_gp/games_needed) + team_db.data[team_id].exp_data['estimated_off_pcg']
        # print('   {0}: Rating: {1:.3f}. "Goodness": {2:.3f}. Play-control: {3:.1f}%. PDO: {4:.3f}. Shooting: {5:.1f}%. Saving: {6:.1f}%'.format(team_id,
        #                                                                                                                                         team_db.data[team_id].exp_data['in_season_rating'],
        #                                                                                                                                         team_db.data[team_id].exp_data['estimated_off_pcg'],
        #                                                                                                                                         100*team_db.data[team_id].exp_data['scf_pcg'],
        #                                                                                                                                         team_db.data[team_id].exp_data['pdo'],
        #                                                                                                                                         100*team_db.data[team_id].exp_data['sh_pcg'],
        #                                                                                                                                         100*team_db.data[team_id].exp_data['sv_pcg']))

        # New approach to team ratings
        team_gsvax_per_60 = 0
        for gid in goalie_db.id_set:
            goalie = goalie_db.get_player(gid)
            if goalie.bio["team_id"] == team_id:
                ind_gsvax_per_60 = 3600*goalie.ind['gsax']['es']/goalie.ind['toi']['es']
                #print(f'   {gid}: Individual GSAX/60: {ind_xgf_per_60:.2f}. TOI-weighted: {goalie.ind["toi_pcg"]["es"] * ind_xgf_per_60:.2f}')
                team_gsvax_per_60 += goalie.ind['toi_pcg']['es'] * ind_gsvax_per_60

        team_db.data[team_id].exp_data['gsax_per_60'] = 3600*sum(goals_saved_above_expected_dict[team_id])/sum(toi_dict_goalies[team_id])
        team_db.data[team_id].exp_data['xgf_per_60'] = 3600*sum(xgf_per_sec[team_id])
        team_db.data[team_id].exp_data['xga_per_60'] = 3600*sum(xga_per_sec[team_id])
        # How effective is the overall team compared to expected goals?
        team_gfs = sum(gf_dict[team_id])
        team_ixgfs = sum(ixgf_dict[team_id])
        goal_scoring_factor = team_gfs/team_ixgfs
        gsax_60 = team_db.data[team_id].exp_data['gsax_per_60']
        # N is the number of players per team
        N = len(xgf_per_sec[team_id])
        xgf_60 = team_db.data[team_id].exp_data['xgf_per_60']
        xga_60 = team_db.data[team_id].exp_data['xga_per_60']
        # Expected goals forward per 60 minutes (5v5)
        xgf_60_5v5 = xgf_60/N
        # Expected goals against per 60 minutes (5v5)
        xga_60_5v5 = xga_60/N

        xgf_60_5v5_comp = xgf_60_5v5*goal_scoring_factor
        xga_60_5v5_comp = xga_60_5v5 - gsax_60

        xgf_pcg_no_g = xgf_60_5v5/(xgf_60_5v5 + xga_60_5v5)
        xgf_pcg = xgf_60_5v5_comp/(xgf_60_5v5_comp+xga_60_5v5_comp)
        tmp_team_data.append((100*xgf_pcg, team_id))


        print(f"{team_id}: GSAx: {gsax_60:.2f}. 5v5-XGF60: {xgf_60_5v5_comp:.2f} GoalScoring: {goal_scoring_factor:.2f}. 5v5-XGA60: {xga_60_5v5_comp:.2f} XGF%: {100*xgf_pcg:.2f}% XGF-no-goalie%: {100*xgf_pcg_no_g:.2f}%")
        """
        for sid in skater_db.id_set:
            skater = skater_db.get_player(sid)
            if skater.bio["team_id"] == team_id:
                s_xgf_pcg = skater.on_ice['xgf_per_60'] / (skater.on_ice['xgf_per_60'] + skater.on_ice['xga_per_60'])
                # gscax = 3600*(skater.ind["gf_above_xgf"]["es"] / skater.ind['toi']['es'])
                if skater.ind["goals"]["es"] == 0:
                    gscax = 1
                else:
                    gscax = skater.ind["goals"]["es"] / skater.ind["ixgf"]["es"]
                print(f"   {sid:20} (xGF: {100*s_xgf_pcg:.2f}%) (GScaX-quota: {gscax:.2f})")
        for gid in goalie_db.id_set:
            goalie = goalie_db.get_player(gid)
            if goalie.bio["team_id"] == team_id:
                print(f"   {gid} (GSaX/60: {goalie.ind['gsax_per_60']['es']:.2f})")
        """
    sort_and_print(tmp_team_data, reversed=True)

    return [team_db, skater_db, goalie_db]


def create_rankings(team_db, skater_db, goalie_db):
    """ Create rankings for Teams, Skaters and Goalies """

    # @TODO: This really needs an update
    values_dict = get_skater_values(skater_db)
    for skater_id in skater_db.id_set:
        skater_db.data[skater_id].rank['estimated_off_per_60'] = get_rank(skater_db.data[skater_id].on_ice['estimated_off_per_60'],
                                                                          values_dict['estimated_off_per_60'])
        skater_db.data[skater_id].rank['estimated_def_per_60'] = get_rank(skater_db.data[skater_id].on_ice['estimated_def_per_60'],
                                                                          values_dict['estimated_def_per_60'])
        skater_db.data[skater_id].rank['estimated_off_pcg'] = get_rank(skater_db.data[skater_id].on_ice['estimated_off_pcg'],
                                                                       values_dict['estimated_off_pcg'])
        skater_db.data[skater_id].rank['estimated_off_diff'] = get_rank(skater_db.data[skater_id].on_ice['estimated_off_diff'],
                                                                        values_dict['estimated_off_diff'])
        skater_db.data[skater_id].rank['primary_points_per_60'] = get_rank(skater_db.data[skater_id].ind['primary_points_per_60']['es'],
                                                                           values_dict['primary_points_per_60'])
        skater_db.data[skater_id].rank['goal_scoring_rating'] = get_rank(skater_db.data[skater_id].ind['goal_scoring_rating']['es'],
                                                                         values_dict['goal_scoring_rating'])
        if skater_db.data[skater_id].bio['position'] == 'F':
            weighted_scale = WS_FWD
        else:
            weighted_scale = WS_DEF
        skater_db.data[skater_id].rank['total'] = weighted_scale[0]*skater_db.data[skater_id].rank['estimated_off_diff'] + weighted_scale[1]*skater_db.data[skater_id].rank['primary_points_per_60'] + weighted_scale[2]*skater_db.data[skater_id].rank['goal_scoring_rating']


    # Add team ranking data.
    # Get values for ranking
    values_dict = get_team_values(team_db)
    rankings = ["p_pcg",
                "gf_pcg",
                "sf_pcg",
                "cf_pcg",
                "ff_pcg",
                "xgf_pcg",
                "scf_pcg",
                "hdcf_pcg",
                "sv_pcg",
                "pdo"]
    # Assign ranking(s)
    for team_id in ACTIVE_TEAMS:
        for rank in rankings:
            team_db.data[team_id].rank[rank] = get_rank(team_db.data[team_id].__dict__[rank], values_dict[rank])
        for key in team_db.data[team_id].exp_data:
            team_db.data[team_id].rank[key] = get_rank(team_db.data[team_id].exp_data[key], values_dict[key])

    return team_db, skater_db, goalie_db


def create_team_specific_db(simulation_param):
    output = defaultdict(dict)
    for skater_id in simulation_param['databases']['skater_db'].keys():
        skater = get_skater(simulation_param['databases']['skater_db'], skater_id)
        if skater_id not in simulation_param['databases']['unavailable_players']:
            output[skater.bio['team_id']][skater.bio['name']] = skater
    return output


def add_unavailable_player(simulation_param, player_id):
    ''' Add a player as unavailable '''
    simulation_param['databases']['unavailable_players'].add(player_id)
    # Make sure to remove player from the team specific database.
    player = get_player(simulation_param, player_id)
    team_id = player.get_attribute('team_id')
    del simulation_param['databases']['team_specific_db'][team_id][player_id]
    return simulation_param


def get_unavailable_players():
    ''' Return list of all unavailable players '''
    unavailable_players = defaultdict(list)
    dict_output = generic_csv_reader('Data/Unavailable_Players.csv', dict_key_attribute='team_id')
    for team_id in ACTIVE_TEAMS:
        if dict_output[team_id]['unavailable_players'] == '[]':
            unavailable_players[team_id] = []
        else:
            str_array = dict_output[team_id]['unavailable_players'][1:-1]
            str_array = str_array.replace("'", "")
            str_array = str_array.replace(' ', '')
            names = str_array.split(',')
            for name in names:
                unavailable_players[team_id].append(name)  # This output is not used at the moment.

    all_unavailable_players = set()
    for team_id in unavailable_players.keys():
        for player_id in unavailable_players[team_id]:
            if player_id == 'DAN_DEKEYSER':
                player_id = 'DANNY_DEKEYSER'

            all_unavailable_players.add(player_id)
    return all_unavailable_players


def stack(original_struct, attribute=None, value=None, playform=None):
    ''' Check if a key is present in a struct.
    Creates a new entry if key is not there; adds value if key _is_ there
    '''

    if attribute is None or value is None:
        raise ValueError('Please provide attribute and value to be added')

    if playform is None:
        # playform == None means that no playform is applicable for the current case, e.g. on-ice data.
        if attribute not in original_struct:
            original_struct[attribute] = value
        else:
            original_struct[attribute] += value
    else:
        if attribute not in original_struct:
            # The attribute has not yet been added
            original_struct[attribute] = {}
            original_struct[attribute][playform] = value
            if playform == 'es':
                original_struct[attribute]['pp'] = 0
                original_struct[attribute]['pk'] = 0
                other_playforms = ['pp', 'pk']
            elif playform == 'pp':
                original_struct[attribute]['es'] = 0
                original_struct[attribute]['pk'] = 0
                other_playforms = ['es', 'pk']
            else:
                original_struct[attribute]['es'] = 0
                original_struct[attribute]['pp'] = 0
        else:
            original_struct[attribute][playform] += value
    return original_struct

