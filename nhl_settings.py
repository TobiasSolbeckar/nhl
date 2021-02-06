import datetime
import os

from nhl_defines import *

class Settings():
    def __init__(self, seasons):
        # General
        self.seasons = seasons
        self.offseason = False
        self.include_offseason_moves = False

        # Gametime simulation settings
        self.number_of_periods = 3
        self.period_length = 1200
        self.shift_length = 45
        self.initial_wins = [[0, 0]]
        self.initial_time = 0
        self.initial_ht_goals = 0
        self.initial_at_goals = 0

        # General simulation settings
        self.days_rested = [[-1, -1]]
        self.simulation_date = datetime.datetime.today().strftime('%Y-%m-%d')
        self.down_sample = False
        self.simulation_mode = None
        self.number_of_simulations = [50000, 2500]

        # Output/print parameters
        self.write_to_gsheet = False  # Write information to Google Sheets
        self.print_time = False
        self.verbose = False

        # Database handling
        self.data_dir = 'Data'
        self.backup_dir = 'Data_backup'
        self.skip_data_dowload = False
        self.generate_fresh_databases = False  # Create new databases from www.naturalstattrick.com
        self.skip_data_download = True

        # Experimental team settings
        self.exp_team = None
        self.exp_team_attributes = None
        self.add_average_goalie = None
        self.exp_playform = None
        self.exp_position = ['F', 'D']

        # URLs for data download
        self.url_skater_bio_201819 = "https://www.naturalstattrick.com/playerteams.php?fromseason=20182019&thruseason=20182019&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_skater_bio = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_skater_ind_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        self.url_skater_ind_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v4&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        self.url_skater_ind_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=4v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        self.url_skater_on_ice = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=oi&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
        self.url_skater_relative = "http://naturalstattrick.com/playerteams.php?fromseason=20182019&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=oi&rate=r&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_goalie_201819_201920 = "https://www.naturalstattrick.com/playerteams.php?fromseason=20182019&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_goalie_es_201920 = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_goalie_pp_201920 = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v4&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_goalie_pk_201920 = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=4v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
        self.url_team_es = "https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
        self.url_team_pp = "https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v4&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
        self.url_team_pk = "https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=4v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
        self.url_team_home = "http://naturalstattrick.com/teamtable.php?fromseason=20182019&thruseason=20192020&stype=2&sit=5v5&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td="
        self.url_team_away = "http://naturalstattrick.com/teamtable.php?fromseason=20182019&thruseason=20192020&stype=2&sit=5v5&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td="
        # Create paths to data files.
        self.setup_csv_paths()

    def update_setting(self, attribute, value):
        if attribute not in self.__dict__:
            raise ValueError('Attribute "' + attribute + '" unknown!')
        self.__dict__[attribute] = value

    def setup_csv_paths(self):
        data_dir = self.data_dir
        self.csvfiles = {}
        self.csvfiles['schedule'] = os.path.join(data_dir, '2019_2020_NHL_Schedule.csv')
        self.csvfiles['team_es'] = os.path.join(data_dir, 'Team_ES_201920.csv')
        self.csvfiles['team_pp'] = os.path.join(data_dir, 'Team_PP_201920.csv')
        self.csvfiles['team_pk'] = os.path.join(data_dir, 'Team_PK_201920.csv')
        self.csvfiles['team_home'] = os.path.join(data_dir, 'Team_Home_201819_201920.csv')
        self.csvfiles['team_away'] = os.path.join(data_dir, 'Team_Away_201819_201920.csv')
        self.csvfiles['skater_old_bio'] = os.path.join(data_dir, 'Skater_Bio_201819.csv')
        self.csvfiles['contract_data'] = os.path.join(data_dir, 'Contract_Expiry_Data.csv')

        # Only use the first season for relative data
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

        # Make sure all CSV-files are availble
        for key in self.csvfiles:
            filepath = self.csvfiles[key]
            if isinstance(filepath, list) is True:
                for sub_path in filepath:
                    if os.path.exists(sub_path) is False:
                        print(os.path.basename(sub_path).split('.')[0])
                        raise ValueError('CSV file ' + sub_path + ' does not exist.')
            else:
                if os.path.exists(filepath) is False:
                    raise ValueError('CSV file ' + filepath + ' does not exist.')

    def set_starting_goalie(self, team, goalie_id):
        ''' Set starting goalie for a team '''
        if goalie_id not in ACTIVE_GOALIES:
            raise ValueError('Goalie ' + goalie_id + ' not included in database')
        self.databases['starting_goalies'][team_id] = goalie_id