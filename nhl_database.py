import csv
import datetime
from collections import defaultdict
import numpy as np
import os
import warnings
from nhl_helpers import backup_data_dir, generate_player_and_team_id
from nhl_defines import *
from nhl_classes import Skater
#from nhl_web_scrape import *


class Database():
    def __init__(self, configuration):
        self.id_set = set()
        self.data = {}
        self.configuration = configuration

    def add_id(self, item_id):
        self.id_set.add(item_id)

    def get_player(self, player_id):
        return self.data[player_id]


class SkaterDatabase(Database):
    def setup_database(self):
        self.add_bio_data()
        self.add_ind_data()
        self.add_on_ice_data()
        self.add_relative_data()
        self.add_experimental_data()

    def add_skater(self, skater):
        self.data[skater.bio['player_id']] = skater
        self.add_id(skater.bio['player_id'])

    def add_bio_data(self, input_csv=None):
        ''' Read bio-data from CSV-file and create Skater-object to store in SkaterDb '''
        if input_csv is None:
            input_csv = self.configuration['csvfiles']['skater_bio']

        for season_data in input_csv:
            with open(season_data, 'rt') as file_handle:
                reader = csv.reader(file_handle, delimiter=',')
                for row in reader:
                    if (row[1] != 'player_name') and (row[1] != 'Player'):
                        # NAME
                        # Create and store player-ID.
                        [player_id, team_id] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME],
                                                                           row[SKATER_DB_BIO_TEAM_ID])
                        # Only add new players
                        if player_id not in self.id_set:
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
                                bio_data['height'] = int(row[SKATER_DB_BIO_HEIGHT])*2.54 # Convert to centimeters.
                            # Weight
                            if str(row[SKATER_DB_BIO_WEIGHT]) == '-':
                                bio_data['weight'] = 0
                            else:
                                bio_data['weight'] = int(row[SKATER_DB_BIO_WEIGHT])*0.453592 # Convert to kilograms.
                            # Draft year
                            if str(row[SKATER_DB_BIO_DRAFT_YEAR]) == '-':
                                bio_data['draft_year'] = 0
                                #bio_data['draft_age'] = -1
                            else:
                                bio_data['draft_year'] = int(row[SKATER_DB_BIO_DRAFT_YEAR])
                                #if len(simulation_param['seasons']) > 1:
                                #bio_data['draft_age'] = -1
                                #else:
                                    #bio_data['draft_age'] = int(simulation_param['seasons'][0][:4])-bio_data['draft_year']
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
                        self.add_skater(Skater2(bio_data))

    def add_ind_data(self, input_csv=None, playform=None):
        ''' Class method to read individual data from stored .csv-file(s),
            and update Skater-object in Skater-database.

            @TODO:  If a value in a row is empty (or "-") the convertion to int/float will crash.
                    One possible solution would be to include this logic in stack()
        '''
        if playform is None:
            raise ValueError('Playform needs to be selected for individual data!')
        if input_csv is None:
            input_csv = self.configuration['csvfiles']['skater_es']

        for season_data in input_csv:
            with open(season_data, 'rt') as file_handle:
                reader = csv.reader(file_handle, delimiter=',')
                for row in reader:
                    if row[1] != 'Player':
                        # Only add players that are playing today.
                        if row[SKATER_DB_BIO_NAME] == 'Sebastian Aho':
                            [player_id, __] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME],
                                                                        row[SKATER_DB_BIO_TEAM_ID])
                        else:
                            [player_id, __] = generate_player_and_team_id(str(row[SKATER_DB_BIO_NAME]))
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
                            ind_data = stack(ind_data,
                                             attribute='toi',
                                             playform=playform,
                                             value=int(60*float(row[SKATER_DB_IND_TOI])))
                            # Goals
                            ind_data = stack(ind_data,
                                             attribute='gf',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_GOALS]))
                            # Assists
                            ind_data = stack(ind_data,
                                             attribute='assist',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_ASSIST]))
                            # Primary assist
                            ind_data = stack(ind_data,
                                             attribute='f_assist',
                                             playform='es',
                                             value=int(row[SKATER_DB_IND_FIRST_ASSIST]))
                            # Secondary assists
                            ind_data = stack(ind_data,
                                             attribute='s_assist',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_SECOND_ASSIST]))
                            # Individual shots taken
                            ind_data = stack(ind_data,
                                             attribute='sf',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_SF]))
                            # Individual Corsi
                            ind_data = stack(ind_data,
                                             attribute='icf',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_ICF]))
                            # Individual Fenwick
                            ind_data = stack(ind_data,
                                             attribute='iff',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_IFF]))
                            # Individual scoring chances
                            ind_data = stack(ind_data,
                                             attribute='iscf',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_ISCF]))
                            # Total penatlies taken
                            ind_data = stack(ind_data,
                                             attribute='pt',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_TOTAL_PENALTIES]))
                            # Total penalties drawn
                            ind_data = stack(ind_data,
                                             attribute='pd',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_PENALTIES_DRAWN]))
                            # Individual hits given
                            ind_data = stack(ind_data,
                                             attribute='hits',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_HITS]))
                            # Individual hits taken
                            ind_data = stack(ind_data,
                                             attribute='hits_taken',
                                             playform=playform,
                                             value=int(row[SKATER_DB_IND_HITS_TAKEN]))
                            # Individual expected goals forward
                            ind_data = stack(ind_data,
                                             attribute='ixgf',
                                             playform=playform,
                                             value=float(row[SKATER_DB_IND_IXG]))
                            # Update skater obejct
                            skater.add_ind_data(ind_data)

    def add_pp_data():
        pass

    def add_pk_data():
        pass

    def add_on_ice_data(self, input_csv=None):
        ''' Class method to read on-ice data from stored .csv-file(s), and update Skater-object in
            Skater-database.
        '''
        if input_csv is None:
            input_csv = self.configuration['csvfiles']['skater_on_ice']
        for season_data in input_csv:
            with open(season_data, 'rt') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if row[1] != 'player_name':
                        # Only add players that are playing today.
                        if row[SKATER_DB_BIO_NAME] == 'Sebastian Aho':
                            [player_id, __] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME],
                                                                        row[SKATER_DB_BIO_TEAM_ID])
                        else:
                            [player_id, __] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME])
                        if player_id in self.id_set:
                            skater = self.get_player(player_id)
                            on_ice_data = skater.get_on_ice_data()

                            # Game played
                            on_ice_data = stack(on_ice_data,
                                                attribute='gp',
                                                value=int(row[SKATER_DB_ON_ICE_GP]))
                            # Corsi forward
                            on_ice_data = stack(on_ice_data,
                                                attribute='cf',
                                                value=int(row[SKATER_DB_ON_ICE_CF]))
                            # Corsi against
                            on_ice_data = stack(on_ice_data,
                                                attribute='ca',
                                                value=int(row[SKATER_DB_ON_ICE_CA]))
                            # Goals forward
                            on_ice_data = stack(on_ice_data,
                                                attribute='gf',
                                                value=int(row[SKATER_DB_ON_ICE_GF]))
                            # Goals against
                            on_ice_data = stack(on_ice_data,
                                                attribute='ga',
                                                value=int(row[SKATER_DB_ON_ICE_GA]))
                            # Shots forward
                            on_ice_data = stack(on_ice_data,
                                                attribute='sf',
                                                value=int(row[SKATER_DB_ON_ICE_SF]))
                            # Shots against
                            on_ice_data = stack(on_ice_data,
                                                attribute='sa',
                                                value=int(row[SKATER_DB_ON_ICE_SA]))
                            # Expected goals forward
                            on_ice_data = stack(on_ice_data,
                                                attribute='xgf',
                                                value=float(row[SKATER_DB_ON_ICE_xGF]))
                            # Expected goals against
                            on_ice_data = stack(on_ice_data,
                                                attribute='xga',
                                                value=float(row[SKATER_DB_ON_ICE_xGA]))
                            # Scoring chances forward
                            on_ice_data = stack(on_ice_data,
                                                attribute='scf',
                                                value=int(row[SKATER_DB_ON_ICE_SCF]))
                            # Scoring chances against
                            on_ice_data = stack(on_ice_data,
                                                attribute='sca',
                                                value=int(row[SKATER_DB_ON_ICE_SCA]))
                            # High danger chances forward
                            on_ice_data = stack(on_ice_data,
                                                attribute='hdcf',
                                                value=int(row[SKATER_DB_ON_ICE_HDCF]))
                            # High danger chances against
                            on_ice_data = stack(on_ice_data,
                                                attribute='hdca',
                                                value=int(row[SKATER_DB_ON_ICE_HDCA]))
                            # Offensive zone starts
                            on_ice_data = stack(on_ice_data,
                                                attribute='ozs',
                                                value=int(row[SKATER_DB_ON_ICE_OZS]))
                            # Neutral zone starts
                            on_ice_data = stack(on_ice_data,
                                                attribute='nzs',
                                                value=int(row[SKATER_DB_ON_ICE_NZS]))
                            # Defensive zone starts
                            on_ice_data = stack(on_ice_data,
                                                attribute='dzs',
                                                value=int(row[SKATER_DB_ON_ICE_DZS]))
                            # Offensice zone face-offs
                            on_ice_data = stack(on_ice_data,
                                                attribute='ozfo',
                                                value=int(row[SKATER_DB_ON_ICE_OZFO]))
                            # Neutral zone face-offs
                            on_ice_data = stack(on_ice_data,
                                                attribute='nzfo',
                                                value=int(row[SKATER_DB_ON_ICE_NZFO]))
                            # Defensive zone face-offs
                            on_ice_data = stack(on_ice_data,
                                                attribute='dzfo',
                                                value=int(row[SKATER_DB_ON_ICE_DZFO]))
                            # Update Skater with on-ice data
                            skater.add_on_ice_data(on_ice_data)

    def add_relative_data(self, input_csv=None):
        ''' Add relative data to skater. Relative data cannot be staggered, hence data from only one season is used '''
        if input_csv is None:
            input_csv = self.configuration['csvfiles']['skater_relative']
        with open(input_csv) as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'player_name':
                    # Since relative data cannot be staggered, this special fix is neede
                    [is_aho, aho_id] = is_this_aho(row[SKATER_DB_RELATIVE_NAME], row[SKATER_DB_RELATIVE_TEAM_ID])
                    if is_aho:
                        player_id = aho_id
                    else:
                        [player_id, ] = generate_player_and_team_id(row[SKATER_DB_RELATIVE_NAME])

                    if player_id in self.id_set:
                        skater = self.get_player(player_id)
                        if str(row[SKATER_DB_RELATIVE_CF_PER_60]) == '-':
                            skater['on_ice']['rel_cf_per_60'] = 0
                        else:
                            skater['on_ice']['rel_cf_per_60'] = float(row[SKATER_DB_RELATIVE_CF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_CA_PER_60]) == '-':
                            skater['on_ice']['rel_ca_per_60'] = 0
                        else:
                            skater['on_ice']['rel_ca_per_60'] = float(row[SKATER_DB_RELATIVE_CA_PER_60])
                        '''
                        if str(row[SKATER_DB_RELATIVE_CF_PCG]) == '-':
                            player_data[player_id]['on_ice']['rel_cf_pcg'] = 0
                            player_data[player_id]['on_ice']['rel_cf_factor'] = 0
                            player_data[player_id]['on_ice']['rel_ca_factor'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_cf_pcg'] = float(row[SKATER_DB_RELATIVE_CF_PCG])
                            player_data[player_id]['on_ice']['rel_cf_factor'] = (player_data[player_id]['on_ice']['rel_cf_pcg']/200 + 1.0)  # Higher is better
                            player_data[player_id]['on_ice']['rel_ca_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_cf_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_FF_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_ff_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_ff_per_60'] = float(row[SKATER_DB_RELATIVE_FF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_FA_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_fa_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_fa_per_60'] = float(row[SKATER_DB_RELATIVE_FA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_FF_PCG]) == '-':
                            player_data[player_id]['on_ice']['rel_ff_pcg'] = 0
                            player_data[player_id]['on_ice']['rel_ff_factor'] = 0
                            player_data[player_id]['on_ice']['rel_fa_factor'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_ff_pcg'] = float(row[SKATER_DB_RELATIVE_FF_PCG])
                            player_data[player_id]['on_ice']['rel_ff_factor'] = (player_data[player_id]['on_ice']['rel_ff_pcg']/200 + 1.0)  # Higher is better
                            player_data[player_id]['on_ice']['rel_fa_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_ff_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_SF_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_sf_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_sf_per_60'] = float(row[SKATER_DB_RELATIVE_SF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_SA_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_sa_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_sa_per_60'] = float(row[SKATER_DB_RELATIVE_SA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_SF_PCG]) == '-':
                            player_data[player_id]['on_ice']['rel_sf_pcg'] = 0
                            player_data[player_id]['on_ice']['rel_sf_factor'] = 0
                            player_data[player_id]['on_ice']['rel_sa_factor'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_sf_pcg'] = float(row[SKATER_DB_RELATIVE_SF_PCG])
                            player_data[player_id]['on_ice']['rel_sf_factor'] = (player_data[player_id]['on_ice']['rel_sf_pcg']/200 + 1.0)  # Higher is better
                            player_data[player_id]['on_ice']['rel_sa_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_sf_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_GF_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_gf_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_gf_per_60'] = float(row[SKATER_DB_RELATIVE_GF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_GA_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_ga_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_ga_per_60'] = float(row[SKATER_DB_RELATIVE_GA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_GF_PCG]) == '-':
                            player_data[player_id]['on_ice']['rel_gf_pcg'] = 0
                            player_data[player_id]['on_ice']['rel_gf_factor'] = 0
                            player_data[player_id]['on_ice']['rel_ga_factor'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_gf_pcg'] = float(row[SKATER_DB_RELATIVE_GF_PCG])
                            player_data[player_id]['on_ice']['rel_gf_factor'] = (player_data[player_id]['on_ice']['rel_gf_pcg']/200 + 1.0)  # Higher is better
                            player_data[player_id]['on_ice']['rel_ga_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_gf_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_xGF_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_xgf_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_xgf_per_60'] = float(row[SKATER_DB_RELATIVE_xGF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_XGA_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_xga_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_xga_per_60'] = float(row[SKATER_DB_RELATIVE_XGA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_xGF_PCG]) == '-':
                            player_data[player_id]['on_ice']['rel_xgf_pcg'] = 0
                            player_data[player_id]['on_ice']['rel_xgf_factor'] = 0
                            player_data[player_id]['on_ice']['rel_xga_factor'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_xgf_pcg'] = float(row[SKATER_DB_RELATIVE_xGF_PCG])
                            player_data[player_id]['on_ice']['rel_xgf_factor'] = (player_data[player_id]['on_ice']['rel_xgf_pcg']/200 + 1.0)  # Higher is better
                            player_data[player_id]['on_ice']['rel_xga_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_xgf_pcg']/200)  # Lower is better

                        if str(row[SKATER_DB_RELATIVE_SCF_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_scf_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_scf_per_60'] = float(row[SKATER_DB_RELATIVE_SCF_PER_60])

                        if str(row[SKATER_DB_RELATIVE_SCA_PER_60]) == '-':
                            player_data[player_id]['on_ice']['rel_sca_per_60'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_sca_per_60'] = float(row[SKATER_DB_RELATIVE_SCA_PER_60])

                        if str(row[SKATER_DB_RELATIVE_SCF_PCG]) == '-':
                            player_data[player_id]['on_ice']['rel_scf_pcg'] = 0
                            player_data[player_id]['on_ice']['rel_scf_factor'] = 0
                            player_data[player_id]['on_ice']['rel_sca_factor'] = 0
                        else:
                            player_data[player_id]['on_ice']['rel_scf_pcg'] = float(row[SKATER_DB_RELATIVE_SCF_PCG])
                            player_data[player_id]['on_ice']['rel_scf_factor'] = (player_data[player_id]['on_ice']['rel_scf_pcg']/200 + 1.0)  # Higher is better
                            player_data[player_id]['on_ice']['rel_sca_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_scf_pcg']/200)  # Lower is better
                        '''
                    else:
                        if simulation_param['verbose']:
                            print(player_id + ' is not an active player!')
        return player_data

    def add_experimental_data(self):
        for player_id in self.id_set:
            skater = self.get_player(player_id)
            skater.add_experimental_ind_data()
            skater.add_experimental_on_ice_data()

class GoalieDatabase(Database):
    def add_goalie(self, goalie_id):
        pass

    def remove_goalie(self, goalie_id):
        pass


def create_databases(simulation_param):
    '''
    @TODO: The timeout functionality should be handled in the 'write_xxx_csv'-functions, with different degrees on the error functions.
    For instance, it's OK if the unavailable players timeout (set a warning), but an error should be set if the (e.g.) bio cannot be read
    '''
    global STATIC_DEFINES

    print('   Creating databases based on season(s) ' + str(simulation_param['seasons']))
    simulation_param['databases'] = {}
    # Create schedule database
    [team_schedules, season_schedule] = generate_schedule(simulation_param['csvfiles'])
    simulation_param['databases']['team_schedules'] = team_schedules
    simulation_param['databases']['season_schedule'] = season_schedule

    # Download new csv-files if current files are too ol
    data_dir = simulation_param['data_dir']
    mod_time_db = os.stat(simulation_param['csvfiles']['check_file']).st_mtime
    mod_time_db = datetime.datetime.fromtimestamp(mod_time_db)
    if simulation_param['skip_data_download'] is True:
        print('Skipping downloading of new data. Using bio-data file modified at ' + str(mod_time_db.strftime("%b-%d, %Y")))
    else:
        if mod_time_db.strftime("%y%m%d") != datetime.datetime.now().strftime("%y%m%d") or simulation_param['generate_fresh_databases']:
            print('Saving data backup to ' + simulation_param['backup_dir'])
            backup_data_dir(simulation_param['data_dir'], simulation_param['backup_dir'])
            print('Downloading new csv-files from www.naturalstattrick.com')
            print('   Downloading bio-data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['SKATER_BIO_BIT']] = write_skater_bio_csv(simulation_param['url_skater_bio'],os.path.join(data_dir,'Skater_Bio_201920.csv'))
            print('   Downloading individual ES data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['SKATER_ES_BIT']] = write_skater_ind_csv(simulation_param['url_skater_ind_es'],os.path.join(data_dir,'Skater_Individual_ES_201920.csv'))
            print('   Downloading individual PP data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['SKATER_PP_BIT']] = write_skater_ind_csv(simulation_param['url_skater_ind_pp'],os.path.join(data_dir,'Skater_Individual_PP_201920.csv'))
            print('   Downloading individual PK data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['SKATER_PK_BIT']] = write_skater_ind_csv(simulation_param['url_skater_ind_pk'],os.path.join(data_dir,'Skater_Individual_PK_201920.csv'))
            print('   Downloading on-ice data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['SKATER_ON_ICE_BIT']] = write_skater_on_ice_csv(simulation_param['url_skater_on_ice'],os.path.join(data_dir,'Skater_OnIce_201920.csv'))
            print('   Downloading relative data')
            STATIC_DEFINES['DATABASE_BIT_REGISTER'][STATIC_DEFINES['SKATER_RELATIVE_BIT']] = write_skater_relative_csv(simulation_param['url_skater_relative'],os.path.join(data_dir,'Skater_Relative_201819_201920.csv'))
            print('   Downloading goalie ES data')
            write_goalie_csv(simulation_param['url_goalie_201819_201920'], os.path.join(data_dir, 'Goalie_201819_201920.csv'))
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['GOALIE_ES_BIT']] = write_goalie_csv(simulation_param['url_goalie_es_201920'],os.path.join(data_dir,'Goalie_ES_201920.csv'))
            print('   Downloading goalie PP data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['GOALIE_PP_BIT']] = write_goalie_csv(simulation_param['url_goalie_pp_201920'],os.path.join(data_dir,'Goalie_PP_201920.csv'))
            print('   Downloading goalie PK data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['GOALIE_PK_BIT']] = write_goalie_csv(simulation_param['url_goalie_pk_201920'],os.path.join(data_dir,'Goalie_PK_201920.csv'))
            print('   Downloading ES team data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['TEAM_ES_BIT']] = write_team_csv(simulation_param['url_team_es'],os.path.join(data_dir,'Team_ES_201920.csv'))
            print('   Downloading PP team data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['TEAM_PP_BIT']] = write_team_csv(simulation_param['url_team_pp'],os.path.join(data_dir,'Team_PP_201920.csv'))
            print('   Downloading PK team data')
            STATIC_DEFINES['DATABASE_ERROR_REGISTER'][STATIC_DEFINES['TEAM_PK_BIT']] = write_team_csv(simulation_param['url_team_pk'],os.path.join(data_dir,'Team_PK_201920.csv'))
            print('   Downloading team data, home venue')
            STATIC_DEFINES['DATABASE_WARNING_REGISTER'][STATIC_DEFINES['TEAM_HOME_BIT']] = write_team_csv(simulation_param['url_team_home'],os.path.join(data_dir,'Team_Home_201819_1920.csv'))
            print('   Downloading team data, away venue')
            STATIC_DEFINES['DATABASE_WARNING_REGISTER'][STATIC_DEFINES['TEAM_AWAY_BIT']] = write_team_csv(simulation_param['url_team_away'],os.path.join(data_dir,'Team_Away_201819_1920.csv'))
            print('   Downloading unavailalbe players')
            STATIC_DEFINES['DATABASE_WARNING_REGISTER'][STATIC_DEFINES['UNAVAILABLE_PLAYERS_BIT']] = write_unavailable_players_csv(os.path.join(data_dir,'Unavailable_Players.csv'))
            print('   Downloading contract expiry data')
            STATIC_DEFINES['DATABASE_WARNING_REGISTER'][STATIC_DEFINES['CONTRACT_EXPIRY_BIT']] = write_ufas(os.path.join(data_dir,'Contract_Expiry_Data.csv'))
        else:
            print('Using local csv-files.')

    if sum(STATIC_DEFINES['DATABASE_ERROR_REGISTER'] != 0):
        raise ValueError('Cannot read skater information. Aborting.')

    if sum(STATIC_DEFINES['DATABASE_WARNING_REGISTER'] != 0):
        warnings.warning('Issues when creating databases. DATABASE_WARNING_REGISTER: ' + str(STATIC_DEFINES['DATABASE_WARNING_REGISTER']))

    # Create team and skater database.
    print('   Creating Team-DB')
    simulation_param['databases']['team_db'] = create_team_db(simulation_param)
    print('   Creating Skater-DB')
    simulation_param['databases']['skater_db'] = create_skater_db(simulation_param)
    print('   Creating Goalie-DB')
    simulation_param['databases']['goalie_db'] = create_goalie_db(simulation_param)
    DEFINES['ACTIVE_PLAYERS'] = STATIC_DEFINES['ACTIVE_SKATERS'].union(STATIC_DEFINES['ACTIVE_GOALIES'])
    old_rating, new_rating, diff_rating = {}, {}, {}

    # Find out who is available.
    if STATIC_DEFINES['DATABASE_WARNING_REGISTER'][STATIC_DEFINES['UNAVAILABLE_PLAYERS_BIT']] is True:
        players_to_remove = []
        simulation_param['databases']['unavailable_players'] = get_unavailable_players()
        for player_id in simulation_param['databases']['unavailable_players']:
            if (player_id not in simulation_param['databases']['skater_db']) and\
               (player_id not in simulation_param['databases']['goalie_db']):
                players_to_remove.append(player_id)
        for player_id in players_to_remove:
            simulation_param['databases']['unavailable_players'].remove(player_id)
    else:
        simulation_param['databases']['unavailable_players'] = set()

    print('   Modifying databases manually')
    simulation_param = modify_player_db(simulation_param)

    # Add experimental data - needs to be done after creation of SkaterDB (and GoalieDB).
    print('   Adding experimental data')
    simulation_param = add_experimental_data(simulation_param)

    for team_id in DEFINES['ACTIVE_TEAMS']:
        team = simulation_param['databases']['team_db'][team_id]
        old_rating[team_id] = team.get_ratings()[1]

    if simulation_param['include_offseason_moves'] is True:
        for team_id in DEFINES['ACTIVE_TEAMS']:
            team = simulation_param['databases']['team_db'][team_id]
            new_rating[team_id] = team.get_ratings()[1]
            diff_rating[team_id] = new_rating[team_id] - old_rating[team_id]

    simulation_param['databases']['starting_goalies'] = generate_starting_goalies()
    simulation_param['databases']['team_specific_db'] = create_team_specific_db(simulation_param)
    simulation_param['databases']['ufa'] = generate_ufa_database(simulation_param)

    # Create roster lists split up on team and position.
    roster_output, flt = {}, {}
    for team_id in DEFINES['ACTIVE_TEAMS']:
        flt['team_id'] = team_id
        flt['position'] = 'D'
        roster_output[str(team_id + '_D')] = create_player_list(simulation_param['databases']['skater_db'], flt)
        flt['position'] = 'F'
        roster_output[str(team_id + '_F')] = create_player_list(simulation_param['databases']['skater_db'], flt)
    simulation_param['databases']['team_rosters'] = roster_output

    return simulation_param


def download_old_season_data(seasons=None, data_dir='Data_download'):
    if seasons is None:
        raise ValueError('No seasons specified for download')
    for season in seasons:
        print('Downloading csv-files from www.naturalstattrick.com for season ' + season)
        orig_season_name = season
        # Transformation to fit the url-format at Natural Stat Trick.
        season = str(season[:-2]) + '20' + str(season[-2:])
        url_skater_bio = "http://naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        url_skater_ind_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        url_skater_ind_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v4&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        url_skater_ind_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=4v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        url_skater_on_ice = "http://naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=oi&rate=r&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        url_skater_relative = "http://naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=oi&rate=r&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        url_goalie_bio = "http://naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=G&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        url_goalie_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season +"&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        url_goalie_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v4&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        url_goalie_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season +"&stype=2&sit=4v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        # Individual data
        print('   Downloading skater bio data for season ' + season)
        write_skater_bio_csv(url_skater_bio, os.path.join(data_dir,
                                                          'Skater_Bio_' +
                                                          orig_season_name +
                                                          '.csv'))

        print('   Downloading individual ES data for season ' + season)
        write_skater_ind_csv(url_skater_ind_es, os.path.join(data_dir,
                                                             'Skater_Individual_ES_' +
                                                             orig_season_name +
                                                             '.csv'))

        print('   Downloading individual PP data for season ' + season)
        write_skater_ind_csv(url_skater_ind_pp, os.path.join(data_dir,
                                                             'Skater_Individual_PP_' +
                                                             orig_season_name +
                                                             '.csv'))

        print('   Downloading individual PK data for season ' + season)
        write_skater_ind_csv(url_skater_ind_pk, os.path.join(data_dir,
                                                             'Skater_Individual_PK_' +
                                                             orig_season_name +
                                                             '.csv'))

        # On ice data
        print('   Downloading on-ice data for season ' + season)
        write_skater_on_ice_csv(url_skater_on_ice, os.path.join(data_dir,
                                                                'Skater_OnIce_' +
                                                                orig_season_name +
                                                                '.csv'))

        # Relative data
        print('   Downloading relative data for season ' + season)
        write_skater_relative_csv(url_skater_relative, os.path.join(data_dir,
                                                                    'Skater_Relative_' +
                                                                    orig_season_name +
                                                                    '.csv'))

        # Goalie data
        print('   Downloading goalie bio data for season ' + season)
        write_skater_bio_csv(url_goalie_bio, os.path.join(data_dir,
                                                          'Goalie_Bio_' +
                                                          orig_season_name +
                                                          '.csv'))

        print('   Downloading goalie ES data for season ' + season)
        write_goalie_csv(url_goalie_es, os.path.join(data_dir,
                                                     'Goalie_ES_' +
                                                     orig_season_name +
                                                     '.csv'))

        print('   Downloading goalie PP data for season ' + season)
        write_goalie_csv(url_goalie_pp, os.path.join(data_dir,
                                                     'Goalie_PP_' +
                                                     orig_season_name +
                                                     '.csv'))

        print('   Downloading goalie PK data for season ' + season)
        write_goalie_csv(url_goalie_pk, os.path.join(data_dir,
                                                     'Goalie_PK_' +
                                                     orig_season_name +
                                                     '.csv'))


def create_skater_db(simulation_param):
    global DEFINES
    DEFINES['ACTIVE_SKATERS']
    output = {}
    player_data = add_bio_data(simulation_param)
    player_data = add_es_data(simulation_param, player_data)
    player_data = add_pp_data(simulation_param, player_data)
    player_data = add_pk_data(simulation_param, player_data)
    player_data = add_on_ice_data(simulation_param, player_data)
    player_data = add_relative_data(simulation_param, player_data)

    for player_id in player_data:
        player = player_data[player_id]
        if (player['ind'] is None) or (player['on_ice'] is None) or (player['ind']['toi'][0] == 0):
            warnings.warn('\nSkipping player ' + player_id)
            DEFINES['ACTIVE_SKATERS'].remove(player_id)
        else:
            output[player_id] = Skater(bio_data,
                                       player_data[player_id]['ind'],
                                       player_data[player_id]['on_ice'])
    return output


def add_bio_data_goalie(simulation_param):
    global DEFINES
    DEFINES['ACTIVE_GOALIES']
    player_data = {}
    for season_data in simulation_param['csvfiles']['goalie_bio']:
        with open(season_data, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'player_name':
                    # NAME
                    # Create and store player-ID.
                    [player_id, team_id] = generate_player_and_team_id(row[GOALIE_DB_NAME],row[GOALIE_DB_TEAM_ID])
                    # Only add new players
                    if player_id not in player_data.keys():
                        DEFINES['ACTIVE_GOALIES'].add(player_id)
                        # Initialize structs.
                        player_data[player_id] = {}

                        # Bio
                        player_data[player_id]['bio'] = {}
                        player_data[player_id]['bio']['name'] = player_id
                        player_data[player_id]['bio']['team_id'] = team_id
                        player_data[player_id]['bio']['position'] = 'G'

                        # Individual_GOALIE
                        player_data[player_id]['ind'] = {}
                        player_data[player_id]['ind']['toi'] = [0, 0, 0]
                        player_data[player_id]['ind']['toi_pcg'] = [0.0, 0.0, 0.0]
                        player_data[player_id]['ind']['sa'] = [0, 0, 0]
                        player_data[player_id]['ind']['sa_per_sec'] = [0, 0, 0]
                        player_data[player_id]['ind']['sv'] = [0, 0, 0]
                        player_data[player_id]['ind']['sv_pcg'] = [0, 0, 0]
                        player_data[player_id]['ind']['ga'] = [0, 0, 0]
                        player_data[player_id]['ind']['gaa'] = [0.0, 0.0, 0.0]
                        player_data[player_id]['ind']['gsaa'] = [0.0, 0.0, 0.0]
                        player_data[player_id]['ind']['xga'] = [0.0, 0.0, 0.0]
                        player_data[player_id]['ind']['avg_shot_dist'] = [0, 0, 0]
                        player_data[player_id]['ind']['avg_goal_dist'] = [0, 0, 0]

                        if str(row[SKATER_DB_BIO_AGE]) == '-':
                            player_data[player_id]['bio']['age'] = 0
                        else:
                            player_data[player_id]['bio']['age'] = int(row[SKATER_DB_BIO_AGE])
                        if str(row[SKATER_DB_BIO_HEIGHT]) == '-':
                            player_data[player_id]['bio']['height'] = 0
                        else:
                            player_data[player_id]['bio']['height'] = int(row[SKATER_DB_BIO_HEIGHT])*2.54  # Convert to centimeters.
                        if str(row[SKATER_DB_BIO_WEIGHT]) == '-':
                            player_data[player_id]['bio']['weight'] = 0
                        else:
                            player_data[player_id]['bio']['weight'] = int(row[SKATER_DB_BIO_WEIGHT])*0.453592  # Convert to kilograms.
                        # DRAFT
                        if str(row[SKATER_DB_BIO_DRAFT_YEAR]) == '-':
                            player_data[player_id]['bio']['draft_year'] = 0
                            player_data[player_id]['bio']['draft_age'] = -1
                        else:
                            player_data[player_id]['bio']['draft_year'] = int(row[SKATER_DB_BIO_DRAFT_YEAR])
                            if len(simulation_param['seasons']) > 1:
                                player_data[player_id]['bio']['draft_age'] = -1
                            else:
                                player_data[player_id]['bio']['draft_age'] = int(simulation_param['seasons'][0][:4])-player_data[player_id]['bio']['draft_year']
                        if str(row[SKATER_DB_BIO_DRAFT_TEAM]) == '-':
                            player_data[player_id]['bio']['draft_team'] = 'N/A'
                        else:
                            player_data[player_id]['bio']['draft_team'] = str(row[SKATER_DB_BIO_DRAFT_TEAM])
                        if str(row[SKATER_DB_BIO_DRAFT_ROUND]) == '-':
                            player_data[player_id]['bio']['draft_round'] = 7  # Default to last round
                        else:
                            player_data[player_id]['bio']['draft_round'] = int(row[SKATER_DB_BIO_DRAFT_ROUND])
                        if str(row[SKATER_DB_BIO_ROUND_PICK]) == '-':
                            player_data[player_id]['bio']['round_pick'] = 32    # Default to last pick
                        else:
                            player_data[player_id]['bio']['round_pick'] = int(row[SKATER_DB_BIO_ROUND_PICK])
                        if str(row[SKATER_DB_BIO_TOTAL_DRAFT_POS]) == '-':
                            player_data[player_id]['bio']['total_draft_pos'] = 225  # Default to one pick after last pick in the last round
                        else:
                            player_data[player_id]['bio']['total_draft_pos'] = int(row[SKATER_DB_BIO_TOTAL_DRAFT_POS])

    return player_data


def add_es_data_goalie(simulation_param, player_data):
    for season_data in simulation_param['csvfiles']['goalie_es']:
        with open(season_data, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'player_name':
                    # Only add players that are playing today.
                    [player_id, ] = generate_player_and_team_id(row[GOALIE_DB_NAME])
                    if player_id in ACTIVE_GOALIES:
                        if str(row[GOALIE_DB_TOI]) == '-':
                            player_data[player_id]['ind']['toi'][STAT_ES] += 0
                        else:
                            player_data[player_id]['ind']['toi'][STAT_ES] += int(60*float(row[GOALIE_DB_TOI]))

                        if str(row[GOALIE_DB_SA]) == '-':
                            player_data[player_id]['ind']['sa'][STAT_ES] += 0
                        else:
                            player_data[player_id]['ind']['sa'][STAT_ES] += int(row[GOALIE_DB_SA])

                        if str(row[GOALIE_DB_SV]) == '-':
                            player_data[player_id]['ind']['sv'][STAT_ES] += 0
                        else:
                            player_data[player_id]['ind']['sv'][STAT_ES] += int(row[GOALIE_DB_SV])

                        if str(row[GOALIE_DB_GA]) == '-':
                            player_data[player_id]['ind']['ga'][STAT_ES] += 0
                        else:
                            player_data[player_id]['ind']['ga'][STAT_ES] += int(row[GOALIE_DB_GA])

                        if str(row[GOALIE_DB_GSAA]) == '-':
                            player_data[player_id]['ind']['gsaa'][STAT_ES] += 0
                        else:
                            player_data[player_id]['ind']['gsaa'][STAT_ES] += float(row[GOALIE_DB_GSAA])

                        if str(row[GOALIE_DB_XGA]) == '-':
                            player_data[player_id]['ind']['xga'][STAT_ES] += 0
                        else:
                            player_data[player_id]['ind']['xga'][STAT_ES] += float(row[GOALIE_DB_XGA])

                        if str(row[GOALIE_DB_AVG_SHOT_DIST]) == '-':
                            player_data[player_id]['ind']['avg_shot_dist'][STAT_ES] += 0
                        else:
                            player_data[player_id]['ind']['avg_shot_dist'][STAT_ES] += int(row[GOALIE_DB_AVG_SHOT_DIST])

                        if str(row[GOALIE_DB_AVG_GOAL_DIST]) == '-':
                            player_data[player_id]['ind']['avg_goal_dist'][STAT_ES] += 0
                        else:
                            player_data[player_id]['ind']['avg_goal_dist'][STAT_ES] += int(row[GOALIE_DB_AVG_GOAL_DIST])
    return player_data


def add_pp_data(simulation_param, player_data):
    for season_data in simulation_param['csvfiles']['skater_pp']:
        with open(season_data, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'player_name':
                    if row[SKATER_DB_BIO_NAME] == 'Sebastian Aho':
                        [player_id, ] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME], row[SKATER_DB_BIO_TEAM_ID])
                    else:
                        [player_id, ] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME])
                    if player_id in ACTIVE_SKATERS:
                        if str(row[SKATER_DB_IND_TOI]) == '-':
                            player_data[player_id]['ind']['toi'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['toi'][STAT_PP] += int(60*float(row[SKATER_DB_IND_TOI]))

                        if str(row[SKATER_DB_IND_GOALS]) == '-':
                            player_data[player_id]['ind']['gf'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['gf'][STAT_PP] += int(row[SKATER_DB_IND_GOALS])

                        if str(row[SKATER_DB_IND_ASSIST]) == '-':
                            player_data[player_id]['ind']['assist'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['assist'][STAT_PP] += int(row[SKATER_DB_IND_ASSIST])

                        if str(row[SKATER_DB_IND_FIRST_ASSIST]) == '-':
                            player_data[player_id]['ind']['f_assist'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['f_assist'][STAT_PP] += int(row[SKATER_DB_IND_FIRST_ASSIST])

                        if str(row[SKATER_DB_IND_SECOND_ASSIST]) == '-':
                            player_data[player_id]['ind']['s_assist'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['s_assist'][STAT_PP] += int(row[SKATER_DB_IND_SECOND_ASSIST])

                        if str(row[SKATER_DB_IND_SF]) == '-':
                            player_data[player_id]['ind']['isf'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['isf'][STAT_PP] += int(row[SKATER_DB_IND_SF])

                        if str(row[SKATER_DB_IND_TOTAL_PENALTIES]) == '-':
                            player_data[player_id]['ind']['pt'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['pt'][STAT_PP] += int(row[SKATER_DB_IND_TOTAL_PENALTIES])

                        if str(row[SKATER_DB_IND_PENALTIES_DRAWN]) == '-':
                            player_data[player_id]['ind']['pd'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['pd'][STAT_PP] += int(row[SKATER_DB_IND_PENALTIES_DRAWN])

                        if str(row[SKATER_DB_IND_HITS]) == '-':
                            player_data[player_id]['ind']['hits'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['hits'][STAT_PP] += int(row[SKATER_DB_IND_HITS])

                        if str(row[SKATER_DB_IND_HITS_TAKEN]) == '-':
                            player_data[player_id]['ind']['hits_taken'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['hits_taken'][STAT_PP] += int(row[SKATER_DB_IND_HITS_TAKEN])
    return player_data


def add_pp_data_goalie(simulation_param, player_data):
    for season_data in simulation_param['csvfiles']['goalie_pp']:
        with open(season_data, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'player_name':
                    # Only add players that are playing today.
                    [player_id, ] = generate_player_and_team_id(row[GOALIE_DB_NAME])
                    if player_id in ACTIVE_GOALIES:
                        if str(row[GOALIE_DB_TOI]) == '-':
                            player_data[player_id]['ind']['toi'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['toi'][STAT_PP] += int(60*float(row[GOALIE_DB_TOI]))

                        if str(row[GOALIE_DB_SA]) == '-':
                            player_data[player_id]['ind']['sa'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['sa'][STAT_PP] += int(row[GOALIE_DB_SA])

                        if str(row[GOALIE_DB_SV]) == '-':
                            player_data[player_id]['ind']['sv'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['sv'][STAT_PP] += int(row[GOALIE_DB_SV])

                        if str(row[GOALIE_DB_GA]) == '-':
                            player_data[player_id]['ind']['ga'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['ga'][STAT_PP] += int(row[GOALIE_DB_GA])

                        if str(row[GOALIE_DB_SV_PCG]) == '-':
                            player_data[player_id]['ind']['sv_pcg'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['sv_pcg'][STAT_PP] += float(row[GOALIE_DB_SV_PCG])

                        if str(row[GOALIE_DB_GAA]) == '-':
                            player_data[player_id]['ind']['gaa'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['gaa'][STAT_PP] += float(row[GOALIE_DB_GAA])

                        if str(row[GOALIE_DB_GSAA]) == '-':
                            player_data[player_id]['ind']['gsaa'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['gsaa'][STAT_PP] += float(row[GOALIE_DB_GSAA])

                        if str(row[GOALIE_DB_XGA]) == '-':
                            player_data[player_id]['ind']['xga'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['xga'][STAT_PP] += float(row[GOALIE_DB_XGA])

                        if str(row[GOALIE_DB_AVG_SHOT_DIST]) == '-':
                            player_data[player_id]['ind']['avg_shot_dist'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['avg_shot_dist'][STAT_PP] += int(row[GOALIE_DB_AVG_SHOT_DIST])

                        if str(row[GOALIE_DB_AVG_GOAL_DIST]) == '-':
                            player_data[player_id]['ind']['avg_goal_dist'][STAT_PP] += 0
                        else:
                            player_data[player_id]['ind']['avg_goal_dist'][STAT_PP] += int(row[GOALIE_DB_AVG_GOAL_DIST])
    return player_data


def add_pk_data(simulation_param, player_data):
    for season_data in simulation_param['csvfiles']['skater_pk']:
        with open(season_data, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'player_name':
                    # Only add players that are playing today.
                    if row[SKATER_DB_BIO_NAME] == 'Sebastian Aho':
                        [player_id, ] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME],row[SKATER_DB_BIO_TEAM_ID])
                    else:
                        [player_id, ] = generate_player_and_team_id(row[SKATER_DB_BIO_NAME])
                    if player_id in ACTIVE_SKATERS:
                        team_id = player_data[player_id]['bio']['team_id']
                        #print('Adding pk-data to player ' + player_id + ' (' + team_id + ').')
                        if str(row[SKATER_DB_IND_TOI]) == '-':
                            player_data[player_id]['ind']['toi'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['toi'][STAT_PK] += int(60*float(row[SKATER_DB_IND_TOI]))

                        if str(row[SKATER_DB_IND_GOALS]) == '-':
                            player_data[player_id]['ind']['gf'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['gf'][STAT_PK] += int(row[SKATER_DB_IND_GOALS])

                        if str(row[SKATER_DB_IND_ASSIST]) == '-':
                            player_data[player_id]['ind']['assist'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['assist'][STAT_PK] += int(row[SKATER_DB_IND_ASSIST])

                        if str(row[SKATER_DB_IND_FIRST_ASSIST]) == '-':
                            player_data[player_id]['ind']['f_assist'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['f_assist'][STAT_PK] += int(row[SKATER_DB_IND_FIRST_ASSIST])

                        if str(row[SKATER_DB_IND_SECOND_ASSIST]) == '-':
                            player_data[player_id]['ind']['s_assist'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['s_assist'][STAT_PK] += int(row[SKATER_DB_IND_SECOND_ASSIST])

                        if str(row[SKATER_DB_IND_SF]) == '-':
                            player_data[player_id]['ind']['isf'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['isf'][STAT_PK] += int(row[SKATER_DB_IND_SF])

                        if str(row[SKATER_DB_IND_TOTAL_PENALTIES]) == '-':
                            player_data[player_id]['ind']['pt'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['pt'][STAT_PK] += int(row[SKATER_DB_IND_TOTAL_PENALTIES])

                        if str(row[SKATER_DB_IND_PENALTIES_DRAWN]) == '-':
                            player_data[player_id]['ind']['pd'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['pd'][STAT_PK] += int(row[SKATER_DB_IND_PENALTIES_DRAWN])

                        if str(row[SKATER_DB_IND_HITS]) == '-':
                            player_data[player_id]['ind']['hits'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['hits'][STAT_PK] += int(row[SKATER_DB_IND_HITS])

                        if str(row[SKATER_DB_IND_HITS_TAKEN]) == '-':
                            player_data[player_id]['ind']['hits_taken'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['hits_taken'][STAT_PK] += int(row[SKATER_DB_IND_HITS_TAKEN])
    return player_data


def add_pk_data_goalie(simulation_param, player_data):
    for season_data in simulation_param['csvfiles']['goalie_pk']:
        with open(season_data, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'player_name':
                    # Only add players that are playing today.
                    [player_id, ] = generate_player_and_team_id(row[GOALIE_DB_NAME])
                    if player_id in ACTIVE_GOALIES:
                        if str(row[GOALIE_DB_TOI]) == '-':
                            player_data[player_id]['ind']['toi'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['toi'][STAT_PK] += int(60*float(row[GOALIE_DB_TOI]))

                        if str(row[GOALIE_DB_SA]) == '-':
                            player_data[player_id]['ind']['sa'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['sa'][STAT_PK] += int(row[GOALIE_DB_SA])

                        if str(row[GOALIE_DB_SV]) == '-':
                            player_data[player_id]['ind']['sv'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['sv'][STAT_PK] += int(row[GOALIE_DB_SV])

                        if str(row[GOALIE_DB_GA]) == '-':
                            player_data[player_id]['ind']['ga'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['ga'][STAT_PK] += int(row[GOALIE_DB_GA])

                        if str(row[GOALIE_DB_SV_PCG]) == '-':
                            player_data[player_id]['ind']['sv_pcg'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['sv_pcg'][STAT_PK] += float(row[GOALIE_DB_SV_PCG])

                        if str(row[GOALIE_DB_GAA]) == '-':
                            player_data[player_id]['ind']['gaa'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['gaa'][STAT_PK] += float(row[GOALIE_DB_GAA])

                        if str(row[GOALIE_DB_GSAA]) == '-':
                            player_data[player_id]['ind']['gsaa'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['gsaa'][STAT_PK] += float(row[GOALIE_DB_GSAA])

                        if str(row[GOALIE_DB_XGA]) == '-':
                            player_data[player_id]['ind']['xga'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['xga'][STAT_PK] += float(row[GOALIE_DB_XGA])

                        if str(row[GOALIE_DB_AVG_SHOT_DIST]) == '-':
                            player_data[player_id]['ind']['avg_shot_dist'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['avg_shot_dist'][STAT_PK] += int(row[GOALIE_DB_AVG_SHOT_DIST])

                        if str(row[GOALIE_DB_AVG_GOAL_DIST]) == '-':
                            player_data[player_id]['ind']['avg_goal_dist'][STAT_PK] += 0
                        else:
                            player_data[player_id]['ind']['avg_goal_dist'][STAT_PK] += int(row[GOALIE_DB_AVG_GOAL_DIST])
    return player_data

def add_relative_data(simulation_param, player_data):
    with open(simulation_param['csvfiles']['skater_relative'], 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[1] != 'player_name':
                # Since relative data cannot be staggered, this special fix is neede
                [is_aho, aho_id] = is_this_aho(row[SKATER_DB_RELATIVE_NAME], row[SKATER_DB_RELATIVE_TEAM_ID])
                if is_aho:
                    player_id = aho_id
                else:
                    [player_id, ] = generate_player_and_team_id(row[SKATER_DB_RELATIVE_NAME])

                if player_id in ACTIVE_SKATERS:
                    if str(row[SKATER_DB_RELATIVE_CF_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_cf_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_cf_per_60'] = float(row[SKATER_DB_RELATIVE_CF_PER_60])

                    if str(row[SKATER_DB_RELATIVE_CA_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_ca_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_ca_per_60'] = float(row[SKATER_DB_RELATIVE_CA_PER_60])
                    if str(row[SKATER_DB_RELATIVE_CF_PCG]) == '-':
                        player_data[player_id]['on_ice']['rel_cf_pcg'] = 0
                        player_data[player_id]['on_ice']['rel_cf_factor'] = 0
                        player_data[player_id]['on_ice']['rel_ca_factor'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_cf_pcg'] = float(row[SKATER_DB_RELATIVE_CF_PCG])
                        player_data[player_id]['on_ice']['rel_cf_factor'] = (player_data[player_id]['on_ice']['rel_cf_pcg']/200 + 1.0)  # Higher is better
                        player_data[player_id]['on_ice']['rel_ca_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_cf_pcg']/200)  # Lower is better

                    if str(row[SKATER_DB_RELATIVE_FF_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_ff_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_ff_per_60'] = float(row[SKATER_DB_RELATIVE_FF_PER_60])

                    if str(row[SKATER_DB_RELATIVE_FA_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_fa_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_fa_per_60'] = float(row[SKATER_DB_RELATIVE_FA_PER_60])

                    if str(row[SKATER_DB_RELATIVE_FF_PCG]) == '-':
                        player_data[player_id]['on_ice']['rel_ff_pcg'] = 0
                        player_data[player_id]['on_ice']['rel_ff_factor'] = 0
                        player_data[player_id]['on_ice']['rel_fa_factor'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_ff_pcg'] = float(row[SKATER_DB_RELATIVE_FF_PCG])
                        player_data[player_id]['on_ice']['rel_ff_factor'] = (player_data[player_id]['on_ice']['rel_ff_pcg']/200 + 1.0)  # Higher is better
                        player_data[player_id]['on_ice']['rel_fa_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_ff_pcg']/200)  # Lower is better

                    if str(row[SKATER_DB_RELATIVE_SF_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_sf_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_sf_per_60'] = float(row[SKATER_DB_RELATIVE_SF_PER_60])

                    if str(row[SKATER_DB_RELATIVE_SA_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_sa_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_sa_per_60'] = float(row[SKATER_DB_RELATIVE_SA_PER_60])

                    if str(row[SKATER_DB_RELATIVE_SF_PCG]) == '-':
                        player_data[player_id]['on_ice']['rel_sf_pcg'] = 0
                        player_data[player_id]['on_ice']['rel_sf_factor'] = 0
                        player_data[player_id]['on_ice']['rel_sa_factor'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_sf_pcg'] = float(row[SKATER_DB_RELATIVE_SF_PCG])
                        player_data[player_id]['on_ice']['rel_sf_factor'] = (player_data[player_id]['on_ice']['rel_sf_pcg']/200 + 1.0)  # Higher is better
                        player_data[player_id]['on_ice']['rel_sa_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_sf_pcg']/200)  # Lower is better

                    if str(row[SKATER_DB_RELATIVE_GF_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_gf_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_gf_per_60'] = float(row[SKATER_DB_RELATIVE_GF_PER_60])

                    if str(row[SKATER_DB_RELATIVE_GA_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_ga_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_ga_per_60'] = float(row[SKATER_DB_RELATIVE_GA_PER_60])

                    if str(row[SKATER_DB_RELATIVE_GF_PCG]) == '-':
                        player_data[player_id]['on_ice']['rel_gf_pcg'] = 0
                        player_data[player_id]['on_ice']['rel_gf_factor'] = 0
                        player_data[player_id]['on_ice']['rel_ga_factor'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_gf_pcg'] = float(row[SKATER_DB_RELATIVE_GF_PCG])
                        player_data[player_id]['on_ice']['rel_gf_factor'] = (player_data[player_id]['on_ice']['rel_gf_pcg']/200 + 1.0)  # Higher is better
                        player_data[player_id]['on_ice']['rel_ga_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_gf_pcg']/200)  # Lower is better

                    if str(row[SKATER_DB_RELATIVE_xGF_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_xgf_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_xgf_per_60'] = float(row[SKATER_DB_RELATIVE_xGF_PER_60])

                    if str(row[SKATER_DB_RELATIVE_XGA_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_xga_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_xga_per_60'] = float(row[SKATER_DB_RELATIVE_XGA_PER_60])

                    if str(row[SKATER_DB_RELATIVE_xGF_PCG]) == '-':
                        player_data[player_id]['on_ice']['rel_xgf_pcg'] = 0
                        player_data[player_id]['on_ice']['rel_xgf_factor'] = 0
                        player_data[player_id]['on_ice']['rel_xga_factor'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_xgf_pcg'] = float(row[SKATER_DB_RELATIVE_xGF_PCG])
                        player_data[player_id]['on_ice']['rel_xgf_factor'] = (player_data[player_id]['on_ice']['rel_xgf_pcg']/200 + 1.0)  # Higher is better
                        player_data[player_id]['on_ice']['rel_xga_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_xgf_pcg']/200)  # Lower is better

                    if str(row[SKATER_DB_RELATIVE_SCF_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_scf_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_scf_per_60'] = float(row[SKATER_DB_RELATIVE_SCF_PER_60])

                    if str(row[SKATER_DB_RELATIVE_SCA_PER_60]) == '-':
                        player_data[player_id]['on_ice']['rel_sca_per_60'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_sca_per_60'] = float(row[SKATER_DB_RELATIVE_SCA_PER_60])

                    if str(row[SKATER_DB_RELATIVE_SCF_PCG]) == '-':
                        player_data[player_id]['on_ice']['rel_scf_pcg'] = 0
                        player_data[player_id]['on_ice']['rel_scf_factor'] = 0
                        player_data[player_id]['on_ice']['rel_sca_factor'] = 0
                    else:
                        player_data[player_id]['on_ice']['rel_scf_pcg'] = float(row[SKATER_DB_RELATIVE_SCF_PCG])
                        player_data[player_id]['on_ice']['rel_scf_factor'] = (player_data[player_id]['on_ice']['rel_scf_pcg']/200 + 1.0)  # Higher is better
                        player_data[player_id]['on_ice']['rel_sca_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_scf_pcg']/200)  # Lower is better
                else:
                    if simulation_param['verbose']:
                        print(player_id + ' is not an active player!')
    return player_data


def create_goalie_db(simulation_param):
    global DEFINES
    output = {}
    goalie_data = add_bio_data_goalie(simulation_param)
    goalie_data = add_es_data_goalie(simulation_param, goalie_data)
    goalie_data = add_pp_data_goalie(simulation_param, goalie_data)
    goalie_data = add_pk_data_goalie(simulation_param, goalie_data)
    for goalie_id in goalie_data:
        # @TODO: Make sure only goalies with TOI > 0 is adde
        output[goalie_id] = Goalie(goalie_data[goalie_id]['bio'], goalie_data[goalie_id]['ind'])

    # This guy is needed
    if simulation_param['add_average_goalies'] is not None:
        for i, team_id in enumerate(simulation_param['add_average_goalies']):
            average_goalie_bio = {}
            average_goalie_bio['name'] = str('AVERAGE_GOALIE_' + team_id + '_' + str(i))
            average_goalie_bio['position'] = 'G'
            average_goalie_bio['team_id'] = team_id
            average_goalie_ind = goalie_data['MARCUS_HOGBERG']['ind']  # This is very randomly selecte
            print('   Adding special (average) goalkeeper ' + average_goalie_bio['name'] + ' to ' + team_id)
            DEFINES['ACTIVE_GOALIES'].add(average_goalie_bio['name'])
            output[average_goalie_bio['name']] = Goalie(average_goalie_bio, average_goalie_ind)
    return output


def create_team_db(simulation_param):
    global TOTAL_GOALS_PER_GAME
    global TOTAL_POINTS_PER_GAME
    global PROBABILITY_FOR_OT
    output = {}

    fatigue_factors = generate_fatigue_factors()
    with open(simulation_param['csvfiles']['team_es'], 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        total_gp, total_otl, total_gf = 0, 0, 0
        for row in reader:
            if row[1] != 'team_name':
                # Get data from row.
                # @TODO: This is not nice
                [name,gp,team_toi_es,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
                reg_array = [gp,team_toi_es,w,l,otl,p,gf,ga,p_pcg]
                adv_array = [sf,sa,sf_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdcf,hdca,hdcf_pcg,sv_pcg,pdo]
                fatigue_info = get_fatigue_factor(fatigue_factors, name)
                total_gp += gp
                total_otl += otl
                total_gf += gf
                output[name] = Team(name, reg_array, adv_array, simulation_param['databases']['team_schedules'][name], fatigue_info)

    if DATABASE_BIT_REGISTER[TEAM_HOME_BIT] is True:
        with open(simulation_param['csvfiles']['team_home'], 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'team_name':
                    [name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
                    output[name].home_p_pcg = p_pcg
    else:
        for team_id in ACTIVE_TEAMS:
            output[name].home_p_pcg = 1.0

    if DATABASE_BIT_REGISTER[TEAM_AWAY_BIT] is True:
        with open(simulation_param['csvfiles']['team_away'], 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'team_name':
                    [name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
                    output[name].away_p_pcg = p_pcg
    else:
        for team_id in ACTIVE_TEAMS:
            output[name].away_p_pcg = 1.0

    with open(simulation_param['csvfiles']['team_pp'], 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[1] != 'team_name':
                [name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
                total_gf += gf
                output[name].team_toi_pp = team_toi
                output[name].team_gf_per_pp = 120*gf/team_toi  # This means how many goals per two minutes (120 seconds) of PP the team gets.
                output[name].team_toi_pp_per_gp = team_toi/gp

    with open(simulation_param['csvfiles']['team_pk'], 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[1] != 'team_name':
                [name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
                total_gf += gf
                output[name].team_toi_pk = team_toi
                output[name].team_ga_per_pp = 120*ga/team_toi  # This means how many goals per two minutes of PK the team gives up.
                if output[name].team_ga_per_pp == 0:
                    output[name].special_teams_rating = 0
                else:
                    output[name].special_teams_rating = output[name].team_gf_per_pp/output[name].team_ga_per_pp
                output[name].team_toi_pk_per_gp = team_toi/gp

    return output


def add_experimental_data(simulation_param):
    # For readability
    team_db = simulation_param['databases']['team_db']
    skater_db = simulation_param['databases']['skater_db']
    goalie_db = simulation_param['databases']['goalie_db']
    unavailable_players = simulation_param['databases']['unavailable_players']

    # Initialization
    sf_dict = defaultdict(list)
    gf_dict = defaultdict(list)
    cf_dict = defaultdict(list)
    ca_dict = defaultdict(list)
    scf_dict = defaultdict(list)
    sca_dict = defaultdict(list)
    hits_dict = defaultdict(list)
    hits_taken_dict = defaultdict(list)
    estimated_off_dict = defaultdict(list)
    estimated_def_dict = defaultdict(list)
    shots_against_dict = defaultdict(list)
    shots_saved_dict = defaultdict(list)
    gp_array = []

    # Update Skater data
    for skater_id in ACTIVE_SKATERS:
        skater = get_skater(skater_db, skater_id)
        skater.ind['toi_pcg'] = [0, 0, 0]
        skater.ind['toi_pcg'][STAT_ES] = skater.ind['toi_per_gp'][STAT_ES] / team_db[skater.bio['team_id']].team_toi_es_per_gp
        skater.ind['toi_pcg'][STAT_PP] = skater.ind['toi_per_gp'][STAT_PP] / team_db[skater.bio['team_id']].team_toi_pp_per_gp
        skater.ind['toi_pcg'][STAT_PK] = skater.ind['toi_per_gp'][STAT_PK] / team_db[skater.bio['team_id']].team_toi_pk_per_gp

        skater.on_ice['rel_gf_diff_per_60'] = skater.on_ice['gf_diff_per_60'] - team_db[skater.bio['team_id']].gf_diff_per_60

        # Estimate offensive and defensive capabilities. Different depending on the skater has played for multiple teams or not.
        estimated_off_metric = 'sc'
        estimated_off = skater.on_ice[estimated_off_metric + 'f'] * skater.on_ice['rel_' + estimated_off_metric + 'f_factor']
        estimated_def = skater.on_ice[estimated_off_metric + 'a'] * skater.on_ice['rel_' + estimated_off_metric + 'a_factor']

        # Not really sure if this code should be include..
        # If included, it is assumed that the player will perform in line with his new team (however, still taking the relative factor into account).
        # If excluded, the player might be "dragged down" by his previous club.
        '''
        if skater.bio['multiple_teams'] == True:
            estimated_off = team_db[skater.bio['team_id']].exp_data[estimated_off_metric + 'f_per_sec'] * skater.ind['toi'][STAT_ES] * skater.on_ice['rel_' + estimated_off_metric + 'f_factor']
            estimated_def = team_db[skater.bio['team_id']].exp_data[estimated_off_metric + 'a_per_sec'] * skater.ind['toi'][STAT_ES] * skater.on_ice['rel_' + estimated_off_metric + 'a_factor']
        '''
        skater.on_ice['estimated_off'] = estimated_off
        skater.on_ice['estimated_def'] = estimated_def
        skater.on_ice['estimated_off_diff'] = estimated_off - estimated_def
        if skater.ind['toi'][STAT_ES] == 0:
            skater.on_ice['estimated_off_per_sec'] = 0
            skater.on_ice['estimated_def_per_sec'] = 0
        else:
            skater.on_ice['estimated_off_per_sec'] = estimated_off / skater.ind['toi'][STAT_ES]
            skater.on_ice['estimated_def_per_sec'] = estimated_def / skater.ind['toi'][STAT_ES]
        skater.on_ice['estimated_off_per_60'] = skater.on_ice['estimated_off_per_sec']*3600
        skater.on_ice['estimated_def_per_60'] = skater.on_ice['estimated_def_per_sec']*3600
        skater.on_ice['estimated_off_per_60_diff'] = skater.on_ice['estimated_off_per_60'] - skater.on_ice['estimated_def_per_60']
        skater.on_ice['estimated_fun_factor'] = skater.on_ice['estimated_off_per_60'] + skater.on_ice['estimated_def_per_60']
        # Only use available players for the ranking data
        # Store estimated offensive and defensive capabilities per team.
        if skater_id not in unavailable_players:
            sf_dict[skater.bio['team_id']].append(skater.ind['isf'][STAT_ES])
            gf_dict[skater.bio['team_id']].append(skater.ind['gf'][STAT_ES])
            hits_dict[skater.bio['team_id']].append(skater.ind['hits'][STAT_ES])
            hits_taken_dict[skater.bio['team_id']].append(skater.ind['hits_taken'][STAT_ES])
            scf_dict[skater.bio['team_id']].append(skater.on_ice['scf'])
            sca_dict[skater.bio['team_id']].append(skater.on_ice['sca'])
            # Store estimated offensive and defensive capabilities per team.
            estimated_off_dict[skater.bio['team_id']].append(estimated_off)
            estimated_def_dict[skater.bio['team_id']].append(estimated_def)
        # Error/warning handling for weird input
        if (skater.on_ice['estimated_off_per_sec']+skater.on_ice['estimated_def_per_sec']) == 0:
            warnings.warn('Bad input for player ' + skater.bio['name'] + '. Setting value ESTIMATED_OFF_PCG to 0.')
            skater.on_ice['estimated_off_pcg'] = 0
        else:
            skater.on_ice['estimated_off_pcg'] = skater.on_ice['estimated_off_per_sec'] / (skater.on_ice['estimated_off_per_sec']+skater.on_ice['estimated_def_per_sec'])
        '''
        if skater.get_attribute('team_id') == 'SJS':
            print(skater_id)
            print('   5v5-TOI: {0:.1f} min. 5v5-TOI/GP: {1:.1f} min. 5v5-TOI%: {2:.1f}%'.format(skater.get_toi()/60,skater.get_attribute('toi_per_gp',STAT_ES)/60,100*skater.get_attribute('toi_pcg',STAT_ES)))
            print('   PP-TOI: {0:.1f} s. PP-TOI/GP: {1:.1f}. PP-TOI%: {2:.1f}%'.format(skater.get_toi(STAT_PP)/60,skater.get_attribute('toi_per_gp',STAT_PP)/60,100*skater.get_attribute('toi_pcg',STAT_PP)))
            print('   PK-TOI: {0:.1f} s. PK-TOI/GP: {1:.1f}. PK-TOI%: {2:.1f}%'.format(skater.get_toi(STAT_PK)/60,skater.get_attribute('toi_per_gp',STAT_PK)/60,100*skater.get_attribute('toi_pcg',STAT_PK)))
            print('   Off/60: {0:.1f}. Def/60: {1:.1f}. Off%: {2:.1f}%'.format(skater.get_attribute('estimated_off_per_60'),skater.get_attribute('estimated_def_per_60'),100*skater.get_attribute('estimated_off_pcg')))
            print('   PT/60: {0:.2f}. PD/60: {1:.2f}. PD diff/60: {2:.2f}'.format(skater.get_attribute('pt_per_60'),skater.get_attribute('pd_per_60'),skater.get_attribute('pd_diff_per_60')))
        '''
    # Add ranking data.
    values_dict = get_skater_values(skater_db)
    for skater_id in ACTIVE_SKATERS:
        skater_db[skater_id].rank['estimated_off_per_60'] = get_rank(skater_db[skater_id].on_ice['estimated_off_per_60'],
                                                                     values_dict['estimated_off_per_60'])
        skater_db[skater_id].rank['estimated_def_per_60'] = get_rank(skater_db[skater_id].on_ice['estimated_def_per_60'],
                                                                     values_dict['estimated_def_per_60'])
        skater_db[skater_id].rank['estimated_off_pcg'] = get_rank(skater_db[skater_id].on_ice['estimated_off_pcg'],
                                                                  values_dict['estimated_off_pcg'])
        skater_db[skater_id].rank['estimated_off_diff'] = get_rank(skater_db[skater_id].on_ice['estimated_off_diff'],
                                                                   values_dict['estimated_off_diff'])
        skater_db[skater_id].rank['primary_points_per_60'] = get_rank(skater_db[skater_id].ind['primary_points_per_60'][0],
                                                                      values_dict['primary_points_per_60'])
        skater_db[skater_id].rank['goal_scoring_rating'] = get_rank(skater_db[skater_id].ind['goal_scoring_rating'][0],
                                                                    values_dict['goal_scoring_rating'])
        if skater_db[skater_id].bio['position'] == 'F':
            weighted_scale = WS_FWD
        else:
            weighted_scale = WS_DEF
        skater_db[skater_id].rank['total'] = weighted_scale[0]*skater_db[skater_id].rank['estimated_off_diff'] +\
                                             weighted_scale[1]*skater_db[skater_id].rank['primary_points_per_60'] +\
                                             weighted_scale[2]*skater_db[skater_id].rank['goal_scoring_rating']
    # Update goalie data
    toi_dict = defaultdict(list)
    for g_id in goalie_db.keys():
        goalie = goalie_db[g_id]
        # Calculate total sa/ss per team, only if player is available
        if g_id not in unavailable_players:
            goalie = get_goalie(goalie_db, g_id)
            shots_against_dict[goalie.bio['team_id']].append(sum(goalie.ind['sa']))  # Using sum to get sa/sv for all strengths (EV/PP/PK)
            shots_saved_dict[goalie.bio['team_id']].append(sum(goalie.ind['sv']))
            toi_dict[goalie.bio['team_id']].append(goalie.ind['toi'][STAT_ES])

    for g_id in goalie_db.keys():
        goalie = goalie_db[g_id]
        goalie.ind['toi_pcg'][STAT_ES] = goalie.ind['toi'][STAT_ES] / sum(toi_dict[goalie.bio['team_id']])

    # Update team data
    for team_id in team_db.keys():
        gp_array.append(team_db[team_id].gp)
    avg_gp = np.mean(gp_array)
    if avg_gp > 20:
        avg_gp = 20

    print('\nTeam metrics (5v5):')
    for team_id in ACTIVE_TEAMS:
        team_sh_pcg = sum(gf_dict[team_id])/sum(sf_dict[team_id])
        team_sv_pcg = sum(shots_saved_dict[team_id])/sum(shots_against_dict[team_id])
        team_estimated_off = sum(estimated_off_dict[team_id])  # How much offense the team generates, based on the individual players.
        team_estimated_def = sum(estimated_def_dict[team_id])  # How much offense the team gives up, based on the individual players.
        team_scf = sum(scf_dict[team_id])
        team_sca = sum(sca_dict[team_id])
        team_db[team_id].exp_data['hits'] = sum(hits_dict[team_id])
        team_db[team_id].exp_data['hits_taken'] = sum(hits_taken_dict[team_id])
        team_db[team_id].exp_data['hits_diff'] = team_db[team_id].exp_data['hits'] - team_db[team_id].exp_data['hits_taken']
        team_db[team_id].exp_data['sh_pcg'] = team_sh_pcg
        team_db[team_id].exp_data['sv_pcg'] = team_sv_pcg
        team_db[team_id].exp_data['estimated_off'] = team_estimated_off*team_db[team_id].exp_data['sh_pcg']
        team_db[team_id].exp_data['estimated_def'] = team_estimated_def*(1-team_db[team_id].exp_data['sv_pcg'])
        team_db[team_id].exp_data['estimated_off_pcg'] = team_db[team_id].exp_data['estimated_off']/(team_db[team_id].exp_data['estimated_off']+team_db[team_id].exp_data['estimated_def'])

        team_db[team_id].exp_data['pdo'] = team_db[team_id].exp_data['sh_pcg']+team_db[team_id].exp_data['sv_pcg']
        team_db[team_id].exp_data['scf_per_60'] = (3600*team_scf/team_db[team_id].team_toi_es)/5  # Division by five to compare with in skater stat.
        team_db[team_id].exp_data['sca_per_60'] = (3600*team_sca/team_db[team_id].team_toi_es)/5  # Division by five to compare with in skater stat.
        team_db[team_id].exp_data['scf_pcg'] = (team_scf/(team_scf+team_sca))

        # Assign ratings. Different for pre_season or non_pre_season.
        team_db[team_id].exp_data['pre_season_rating'] = team_db[team_id].exp_data['estimated_off_pcg']
        team_db[team_id].exp_data['in_season_rating'] = (team_db[team_id].p_pcg*P_PCG_FACTOR*avg_gp/20) + team_db[team_id].exp_data['estimated_off_pcg']

        print('   {0}: Rating: {1:.3f}. "Goodness": {2:.3f}. Play-control: {3:.1f}%. PDO: {4:.3f}. Shooting: {5:.1f}%. Saving: {6:.1f}%'.format(team_id,team_db[team_id].exp_data['in_season_rating'],team_db[team_id].exp_data['estimated_off_pcg'],100*team_db[team_id].exp_data['scf_pcg'],team_db[team_id].exp_data['pdo'],100*team_db[team_id].exp_data['sh_pcg'],100*team_db[team_id].exp_data['sv_pcg']))

    # Add ranking data. This needs to be done in a separate for-loop because of 'estimated_off_pcg'
    # Get values for ranking
    values_dict = get_team_values(team_db)

    # Assign ranking(s)
    for team_id in ACTIVE_TEAMS:
        team_db[team_id].rank['p_pcg'] = get_rank(team_db[team_id].p_pcg, values_dict['p_pcg'])
        team_db[team_id].rank['gf_pcg'] = get_rank(team_db[team_id].gf_pcg, values_dict['gf_pcg'])
        team_db[team_id].rank['sf_pcg'] = get_rank(team_db[team_id].sf_pcg, values_dict['sf_pcg'])
        team_db[team_id].rank['cf_pcg'] = get_rank(team_db[team_id].cf_pcg, values_dict['cf_pcg'])
        team_db[team_id].rank['ff_pcg'] = get_rank(team_db[team_id].ff_pcg, values_dict['ff_pcg'])
        team_db[team_id].rank['xgf_pcg'] = get_rank(team_db[team_id].xgf_pcg, values_dict['xgf_pcg'])
        team_db[team_id].rank['scf_pcg'] = get_rank(team_db[team_id].scf_pcg, values_dict['scf_pcg'])
        team_db[team_id].rank['hdcf_pcg'] = get_rank(team_db[team_id].hdcf_pcg, values_dict['hdcf_pcg'])
        team_db[team_id].rank['sv_pcg'] = get_rank(team_db[team_id].sv_pcg, values_dict['sv_pcg'])
        team_db[team_id].rank['pdo'] = get_rank(team_db[team_id].pdo, values_dict['pdo'])
        team_db[team_id].rank['hits'] = get_rank(team_db[team_id].exp_data['hits'], values_dict['hits'])
        team_db[team_id].rank['hits_taken'] = get_rank(team_db[team_id].exp_data['hits_taken'], values_dict['hits_taken'])
        team_db[team_id].rank['hits_diff'] = get_rank(team_db[team_id].exp_data['hits_diff'], values_dict['hits_diff'])
        team_db[team_id].rank['estimated_off_pcg'] = get_rank(team_db[team_id].exp_data['estimated_off_pcg'], values_dict['estimated_off_pcg'])
        team_db[team_id].rank['in_season_rating'] = get_rank(team_db[team_id].exp_data['in_season_rating'], values_dict['in_season_rating'])

    # Store values for the return
    simulation_param['databases']['team_db'] = team_db
    simulation_param['databases']['skater_db'] = skater_db
    simulation_param['databases']['goalie_db'] = goalie_db
    simulation_param['databases']['unavailable_players'] = unavailable_players
    return simulation_param


def generate_schedule(csvfiles):
    schedule_per_team = defaultdict(list)
    schedule_per_date = defaultdict(list)
    with open(csvfiles['schedule'], 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            date = str(row[0])
            home_team_id = get_team_id(row[3])
            away_team_id = get_team_id(row[2])
            schedule_per_team[home_team_id].append(away_team_id)
            schedule_per_team[away_team_id].append(home_team_id)
            schedule_per_date[date].append([home_team_id, away_team_id])
    return [schedule_per_team, schedule_per_date]


def create_team_specific_db(simulation_param):
    output = defaultdict(dict)
    for skater_id in simulation_param['databases']['skater_db'].keys():
        skater = get_skater(simulation_param['databases']['skater_db'], skater_id)
        if skater_id not in simulation_param['databases']['unavailable_players']:
            output[skater.bio['team_id']][skater.bio['name']] = skater
    return output


def generate_ufa_database(simulation_param):
    ''' Generates a database (in the form of a list) of all Unrestricted Free Agents,
        based on the CSV-file downloaded and saved earlier. '''
    ufa_list = []
    with open(simulation_param['csvfiles']['contract_data'], 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        for raw_row in reader:
            str_row = str(raw_row[0])
            # Skip the first row.
            if str_row != 'player_id':
                # Only add players that played some in the NHL the valid season.
                if str_row in ACTIVE_PLAYERS:
                    ufa_list.append(str_row)
    return ufa_list


def get_row_values_for_team_db(row):
    # Strings
    if str(row[TEAM_DB_NAME_COL]) == '-':
        raise ValueError('Incorrect Team-ID')
    elif str(row[TEAM_DB_NAME_COL]) == 'St Louis Blues':  # Special case to fix descrepencies in worksheets
        name = 'STL'
    else:
        name = get_team_id(str(row[TEAM_DB_NAME_COL]))

    # Integers
    if str(row[TEAM_DB_GP_COL]) == '-':
        gp = 0
    else:
        gp = int(row[TEAM_DB_GP_COL])

    if str(row[TEAM_DB_TOI_COL]) == '-':
        team_toi = 0
    else:
        team_toi = int(60*float(row[TEAM_DB_TOI_COL]))

    if str(row[TEAM_DB_W_COL]) == '-':
        w = 0
    else:
        w = int(row[TEAM_DB_W_COL])

    if str(row[TEAM_DB_L_COL]) == '-':
        l = 0
    else:
        l = int(row[TEAM_DB_L_COL])

    if str(row[TEAM_DB_OTL_COL]) == '-':
        otl = 0
    else:
        otl = int(row[TEAM_DB_OTL_COL])

    if str(row[TEAM_DB_P_COL]) == '-':
        p = 0
    else:
        p = int(row[TEAM_DB_P_COL])

    if str(row[TEAM_DB_CF_COL]) == '-':
        cf = 0
    else:
        cf = int(row[TEAM_DB_CF_COL])

    if str(row[TEAM_DB_CA_COL]) == '-':
        ca = 0
    else:
        ca = int(row[TEAM_DB_CA_COL])

    if str(row[TEAM_DB_FF_COL]) == '-':
        ff = 0
    else:
        ff = int(row[TEAM_DB_FF_COL])

    if str(row[TEAM_DB_FA_COL]) == '-':
        fa = 0
    else:
        fa = int(row[TEAM_DB_FA_COL])

    if str(row[TEAM_DB_SF_COL]) == '-':
        sf = 0
    else:
        sf = int(row[TEAM_DB_SF_COL])

    if str(row[TEAM_DB_SA_COL]) == '-':
        sa = 0
    else:
        sa = int(row[TEAM_DB_SA_COL])

    if str(row[TEAM_DB_GF_COL]) == '-':
        gf = 0
    else:
        gf = int(row[TEAM_DB_GF_COL])

    if str(row[TEAM_DB_GA_COL]) == '-':
        ga = 0
    else:
        ga = int(row[TEAM_DB_GA_COL])

    if str(row[TEAM_DB_SCF_COL]) == '-':
        scf = 0
    else:
        scf = int(row[TEAM_DB_SCF_COL])

    if str(row[TEAM_DB_SCA_COL]) == '-':
        sca = 0
    else:
        sca = int(row[TEAM_DB_SCA_COL])

    if str(row[TEAM_DB_HDCF_COL]) == '-':
        hdcf = 0
    else:
        hdcf = int(row[TEAM_DB_HDCF_COL])

    if str(row[TEAM_DB_HDCA_COL]) == '-':
        hdca = 0
    else:
        hdca = int(row[TEAM_DB_HDCA_COL])

    # Floats
    if str(row[TEAM_DB_P_PCG_COL]) == '-':
        p_pcg = 0.0
    else:
        p_pcg = float(row[TEAM_DB_P_PCG_COL])

    if str(row[TEAM_DB_SF_PCG_COL]) == '-':
        sf_pcg = 0.0
    else:
        sf_pcg = float(row[TEAM_DB_SF_PCG_COL])/100

    if str(row[TEAM_DB_CF_PCG_COL]) == '-':
        cf_pcg = 0.0
    else:
        cf_pcg = float(row[TEAM_DB_CF_PCG_COL])/100

    if str(row[TEAM_DB_FF_PCG_COL]) == '-':
        ff_pcg = 0.0
    else:
        ff_pcg = float(row[TEAM_DB_FF_PCG_COL])/100

    if str(row[TEAM_DB_SCF_PCG_COL]) == '-':
        scf_pcg = 0.0
    else:
        scf_pcg = float(row[TEAM_DB_SCF_PCG_COL])/100

    if str(row[TEAM_DB_xGF_COL]) == '-':
        xgf = 0
    else:
        xgf = float(row[TEAM_DB_xGF_COL])

    if str(row[TEAM_DB_xGA_COL]) == '-':
        xga = 0
    else:
        xga = float(row[TEAM_DB_xGA_COL])

    if str(row[TEAM_DB_xGF_PCG_COL]) == '-':
        xgf_pcg = 0.0
    else:
        xgf_pcg = float(row[TEAM_DB_xGF_PCG_COL])/100

    if str(row[TEAM_DB_HDCF_PCG_COL]) == '-':
        hdcf_pcg = 0.0
    else:
        hdcf_pcg = float(row[TEAM_DB_HDCF_PCG_COL])/100

    if str(row[TEAM_DB_SV_PCG_COL]) == '-':
        sv_pcg = 0.0
    else:
        sv_pcg = float(row[TEAM_DB_SV_PCG_COL])/100

    if str(row[TEAM_DB_PDO_COL]) == '-':
        pdo = 0.0
    else:
        pdo = float(row[TEAM_DB_PDO_COL])

    return [name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo]


def modify_player_db(simulation_param):
    '''
    Manually update databases if neede
    Ex:
        simulation_param['databases'][skater_db] = ...
        simulation_param['databases'][goalie_db] = ...
    '''

    # ADD MODIFICATIONS TO DATABASE HERE

    return simulation_param


def update_new_team(db, player, new_team):
    global DEFINES
    if player not in DEFINES['ACTIVE_PLAYERS']:
        raise ValueError('Unknown player ' + player + '.')

    if new_team is None:
        del db[player]
        ACTIVE_PLAYERS.remove(player)
    else:
        if new_team == db[player].bio['team_id']:
            warnings.warn('Player ' + player + ' already playing for team ' + db[player].bio['team_id'])
        else:
            db[player].bio['team_id'] = new_team
            db[player].bio['multiple_teams'] = True
    return db


def add_unavailable_player(simulation_param, player_id):
    simulation_param['databases']['unavailable_players'].add(player_id)
    # Make sure to remove player from the team specific database.
    player = get_player(simulation_param, player_id)
    team_id = player.get_attribute('team_id')
    del simulation_param['databases']['team_specific_db'][team_id][player_id]
    return simulation_param


def get_unavailable_players():
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
        if attribute not in original_struct:
            original_struct[attribute] = value
        else:
            original_struct[attribute] += value
    else:
        if attribute not in original_struct:
            original_struct[attribute] = {}
            original_struct[attribute][playform] = value
        else:
            original_struct[attribute][playform] += value
    return original_struct

