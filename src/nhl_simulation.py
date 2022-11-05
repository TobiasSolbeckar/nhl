from src.nhl_defines import *


class Simulation():
    def __init__(self):
        self.name = "hej"


class Game(Simulation):
    def __init__(self):
        super().__init__()
        pass


class GameStatus():
    def __init__(self):
        self.game_active = False
        self.time = 0
        self.current_period = 0
        self.players_in_box = []
        self.gameplay_state = GAMEPLAY_ES
        self.gameplay_changed = False
        self.previous_gameplay_state = GAMEPLAY_ES

    def simulate_game(self):
        '''
        Simulating one game between 'ht_id' and 'at_id', based on content in 'settings'
        '''
        # Set up games status parameters
        game_status = {}
        game_status['goal_scored'] = [False, False]
        game_status['active_penalties'] = [0, 0]
        game_status['ht_line_values'], game_status['at_line_values'] = {}, {}
        game_status['ht_goalie_in_net'], game_status['at_goalie_in_net'] = True, True
        game_status['ht_pp'], game_status['ht_pk'], game_status['at_pp'], game_status['at_pk'] = False, False, False, False
        game_status['ht_goalie'] = self.ht_goalie
        game_status['at_goalie'] = self.at_goalie
        game_status['ht_goals'] = self.ht_initial_goals
        game_status['at_goals'] = self.at_initial_goals
        game_status['ht_points'], game_status['at_points'], game_status['ht_shots'], game_status['at_shots'] = 0, 0, 0, 0
        game_status['game_active'] = False
        game_status['goal_scored'] = [False, False]
        game_status['ht_penalty'], game_status['at_penalty'] = defaultdict(int), defaultdict(int)
        game_status['active_penalties'] = [0, 0]
        game_status['current_period'] = 0
        game_status['ht_number_of_skaters'], game_status['at_number_of_skaters'] = [], []  # [def, fwd]
        game_status['ht_on_ice_db'], game_status['at_on_ice_db'] = {}, {}
        game_status['ht_line_values'], game_status['at_line_values'] = {}, {}
        game_status['players_in_pbox'] = []
        game_status['previous_gameplay_state'] = GAMEPLAY_ES
        game_status['gameplay_changed'] = False
        game_status['gameplay_state'] = GAMEPLAY_ES
        game_status['ht_goalie_in_net'], game_status['at_goalie_in_net'] = True, True
        game_status['ht_goalscorers'], game_status['at_goalscorers'] = [], []  # Is this even used?
        game_status['ht_pp'], game_status['ht_pk'], game_status['at_pp'], game_status['at_pk'] = False, False, False, False
        game_status['period_length'] = 1200
        game_status['time'] = 0


class SeasonSimulation(Simulation):
    def __init__(self):
        super().__init__()
        pass
