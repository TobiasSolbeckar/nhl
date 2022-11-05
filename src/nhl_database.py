import csv
import datetime
from collections import defaultdict
import numpy as np
from nhl_helpers import generic_csv_reader, get_team_id
from .nhl_entities import Skater

class Database():
    """ Generic class to handle databases """
    def __init__(self, configuration):
        self.id_set = set()
        self.data = {}
        self._configuration = configuration
        self.setup_database()

    def add_id(self, item_id):
        self.id_set.add(item_id)

    def get_player(self, player_id):
        return self.data[player_id]

    def setup_database(self):
        raise ValueError("setup_database() has not been initiated")


class TeamDatabase(Database):
    def __init__(self, configuration):
        super().__init__(configuration)

    def setup_database(self):
        ''' Store all data from CSV-files into Team objects '''
        self.add_es_data()
        # self.add_pp_data()
        # self.add_pk_data()
        # self.add_home_data()
        # self.add_away_data()
        # self.add_team_schedule()
        # # @TODO: self.add_fattigue_information()
        # self.add_additional_data()

    def add_es_data(self):
        _csv_output = generic_csv_reader(self._configuration.csvfiles['team_es'], dict_key_attribute='team_name')
        team_es = {}
        for team_key, team_values in _csv_output.items():
            team_es[get_team_id(team_key)] = team_values


class SkaterDatabase(Database):
    def __init__(self, configuration):
        super().__init__(configuration)

    def setup_database(self):
        ''' Store all data from CSV-files into Skater objects '''
        self.add_players()
        # self.add_bio_data()
        # self.add_es_data()
        # self.setup_rankings()

    def add_players(self):
        _csv_output = generic_csv_reader(self._configuration.csvfiles['skater_bio'][0], dict_key_attribute='player_name')
        for player_key, player_values in _csv_output.items():
            print(player_key)
            self.data[player_key] = Skater(player_values)

    def add_bio_data(self):
        _csv_output = generic_csv_reader(self._configuration.csvfiles['skater_bio'][0], dict_key_attribute='player_name')
        for player_key, player_values in _csv_output.items():
            print(player_key + str(player_values))

    def add_es_data(self):
        _csv_output = generic_csv_reader(self._configuration.csvfiles['skater_es'][0], dict_key_attribute='player_name')
        for player_key, player_values in _csv_output.items():
            print(player_key + str(player_values))


class GoalieDatabase(Database):
    def __init__(self, configuration):
        super().__init__(configuration)

    def setup_database(self):
        ''' Store all data from CSV-files into Goalie objects '''
        pass
