import csv
import datetime
import os

from collections import defaultdict

from src.nhl_defines import *
from nhl_helpers import *


class Settings():
    ''' Class to handle all settings '''
    def __init__(self, seasons):
        # General
        self.seasons = seasons
        self.offseason = False
        self.include_offseason_moves = False
        self.write_to_gsheet = False  # Write information to Google Sheets
        self.print_time = False
        self.verbose = False
        self.init_database_settings()
        self.init_gametime_settings()
        self.init_simulation_settings()
        self.init_analytics_parameters()
        self.setup_csv_paths()
        # self.generate_schedule()

    def init_database_settings(self):
        ''' Initiate database settings '''
        self.databases = {}
        self.data_dir = 'Data'
        self.backup_dir = 'Data_backup'
        self.skip_data_dowload = False
        self.generate_fresh_databases = False  # Create new databases from www.naturalstattrick.com
        self.skip_data_download = True

    def init_gametime_settings(self):
        ''' Initiate game time settings '''
        self.number_of_periods = 3
        self.period_length = 1200
        self.shift_length = 45
        self.initial_wins = [[0, 0]]
        self.initial_time = 0
        self.initial_ht_goals = 0
        self.initial_at_goals = 0

    def init_simulation_settings(self):
        ''' Initiate general simulation settings '''
        self.games_to_simulate = [['DAL', 'CGY'], ['SJS', 'COL']]
        self.add_average_goalie = None
        self.days_rested = [[-1, -1]]
        self.simulation_date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.down_sample = False
        self.simulation_mode = None
        self.number_of_simulations = [50000, 2500]

    def init_analytics_parameters(self):
        ''' Initiate parameters connected to analytics settings '''
        self.team_plots = False
        self.exp_min_toi = 100
        self.exp_list_length = 1
        self.exp_weighted_scale = 'WS_FWD'
        self.exp_temp_attributes = ['primary_points_per_60']
        self.exp_additional_players = ['JOE_THORNTON']
        self.exp_team = None
        self.exp_team_attributes = None
        self.exp_playform = None
        self.exp_position = ['F', 'D']

    def update_setting(self, setting, value):
        ''' Method to update/set setting in Settings object'''
        if setting not in self.__dict__:
            raise ValueError('Setting "' + setting + '" unknown. ' + str(self.__dict__.keys()))
        self.__dict__[setting] = value

    def add_setting(self, setting, value):
        ''' Method to add new setting to Settings object '''
        self.__dict__[setting] = value

    def get_settings(self, setting):
        ''' Method to get a setting from a Settings object'''
        if setting not in self.__dict__:
            raise ValueError('Setting "' + setting + '" unknown!')
        return self.__dict__[setting]

    def setup_csv_paths(self):
        ''' Construct the paths to CSV-files '''
        data_dir = self.data_dir
        self.csvfiles = {}
        self.csvfiles['schedule'] = os.path.join(data_dir, 'nhl-202021-asplayed.csv')
        self.csvfiles['team_home'] = os.path.join(data_dir, 'Team_Home_201819_201920.csv')
        self.csvfiles['team_away'] = os.path.join(data_dir, 'Team_Away_201819_201920.csv')
        self.csvfiles['skater_old_bio'] = os.path.join(data_dir, 'Skater_Bio_201819.csv')
        self.csvfiles['contract_data'] = os.path.join(data_dir, 'Contract_Expiry_Data.csv')
        self.csvfiles['player_team_info'] = os.path.join(data_dir, 'player_team_info.csv')

        # Only use one season for relative data
        self.csvfiles['skater_relative'] = os.path.join(data_dir, 'Skater_Relative_201819_201920.csv')

        self.csvfiles['skater_bio'] = []
        self.csvfiles['skater_es'] = []
        self.csvfiles['skater_pp'] = []
        self.csvfiles['skater_pk'] = []
        self.csvfiles['skater_on_ice'] = []
        self.csvfiles['goalie_bio'] = []
        self.csvfiles['goalie_es'] = []
        self.csvfiles['goalie_pp'] = []
        self.csvfiles['goalie_pk'] = []
        for season in self.seasons:
            self.csvfiles['skater_bio'].append(os.path.join(data_dir, 'Skater_Bio_' + season + '.csv'))
            self.csvfiles['skater_es'].append(os.path.join(data_dir, 'Skater_Individual_ES_' + season + '.csv'))
            self.csvfiles['skater_pp'].append(os.path.join(data_dir, 'Skater_Individual_PP_' + season + '.csv'))
            self.csvfiles['skater_pk'].append(os.path.join(data_dir, 'Skater_Individual_PK_' + season + '.csv'))
            self.csvfiles['skater_on_ice'].append(os.path.join(data_dir, 'Skater_OnIce_' + season + '.csv'))
            self.csvfiles['goalie_bio'].append(os.path.join(data_dir, 'Goalie_Bio_' + season + '.csv'))
            self.csvfiles['goalie_es'].append(os.path.join(data_dir, 'Goalie_ES_' + season + '.csv'))
            self.csvfiles['goalie_pp'].append(os.path.join(data_dir, 'Goalie_PP_' + season + '.csv'))
            self.csvfiles['goalie_pk'].append(os.path.join(data_dir, 'Goalie_PK_' + season + '.csv'))
        self.csvfiles['check_file'] = os.path.join(data_dir, 'Skater_Bio_201920.csv')  # Use this file to check if new databases are needed.
        self.csvfiles['team_es'] = os.path.join(data_dir, 'Team_ES_' + season + '.csv')
        self.csvfiles['team_pp'] = os.path.join(data_dir, 'Team_PP_' + season + '.csv')
        self.csvfiles['team_pk'] = os.path.join(data_dir, 'Team_PK_' + season + '.csv')

        # Make sure all CSV-files are availble
        for key in self.csvfiles:
            filepath = self.csvfiles[key]
            if isinstance(filepath, list) is True:
                for sub_path in filepath:
                    if os.path.exists(sub_path) is False:
                        print(os.path.basename(sub_path).split('.')[0])
                        raise FileNotFoundError('CSV file ' + sub_path + ' does not exist.')
            else:
                if os.path.exists(filepath) is False:
                    raise FileNotFoundError('CSV file ' + filepath + ' does not exist.')

    def generate_schedule(self):
        ''' Create team specific schedules, for simulation purpose '''
        schedule_per_team = defaultdict(list)
        schedule_per_date = defaultdict(list)
        with open(self.csvfiles['schedule'], 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                date = str(row[0])
                home_team_id = get_team_id(row[5])
                away_team_id = get_team_id(row[3])
                schedule_per_team[home_team_id].append(away_team_id)
                schedule_per_team[away_team_id].append(home_team_id)
                schedule_per_date[date].append([home_team_id, away_team_id])
        self.databases['team_schedules'] = schedule_per_team
        self.databases['season_schedule'] = schedule_per_date


class CsvHandler():
    """ Class to handle data stored in csv-files """
    def __init__(self):
        """ Constructor for CsvHandler """
        data_dir = "data"
        self.schedule = os.path.join(data_dir, 'nhl-202021-asplayed.csv')