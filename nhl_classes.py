import random
from collections import defaultdict

from nhl_defines import *
from nhl_simulation import simulate_ind_game

'''
Definitions:
Corsi: shots + blocks + misses
Fenwick: shots + misses
Shots: shots
'''


class Skater():
    ''' Class for holding information about Skaters
        @TODO: Make sure the experimental data is added somewhere
    '''

    def __init__(self, bio, ind=None, on_ice=None):
        ''' Constructor '''
        self.bio = bio
        self.initialize_ranking_data()

        if ind is None:
            self.ind = {}
        else:
            self.add_ind_data(ind)

        if on_ice is None:
            self.on_ice = {}
        else:
            self.add_on_ice_data(on_ice)

    def get_ind_data(self):
        ''' Getter for ind-data '''
        return self.ind

    def add_ind_data(self, ind):
        ''' Add/update data regarding individual performance '''

        # Special case for storing the "multiple_teams" attribute
        self.bio['multiple_teams'] = ind['multiple_teams']

        # Store data directly from input source (www.naturalstattrick.com)
        for attribute in ind:
            if attribute not in ['multiple_teams']:
                self.ind[attribute] = ind[attribute]

    def add_experimental_ind_data(self):
        ''' Add special/experimental individual data which is not available from source '''
        self.ind['toi_per_gp'] = {}  # Time on ice per game
        self.ind['points'] = {}  # Total points
        self.ind['primary_points'] = {}  # Primary points
        self.ind['gf_above_xgf'] = {}  # Goals scored above (individual) expected goals
        self.ind['points_per_60'] = {}  # Total points scored per 60 min
        self.ind['primary_points_per_60'] = {}  # Primary points scored per 60 min
        self.ind['isf_per_sec'] = {}  # Individual shots forward per second
        self.ind['isf_per_60'] = {}  # Individual shots forward per 60 min
        self.ind['pt_per_sec'] = {}  # Penalties taken per second
        self.ind['pd_per_sec'] = {}  # Peanlties draw per second
        self.ind['pt_per_60'] = {}  # Penalties taken per 60 min
        self.ind['pd_per_60'] = {}  # Penalties draw per 60 min
        self.ind['pd_diff_per_60'] = {}  # Difference between penalties drawn and taken per 60 min. Higher is better.
        self.ind['pd_pcg'] = {}  # Quota between penalties drawn and taken. Higher number is better.
        self.ind['ixgf_per_60'] = {}  # Individual expected goals forward per 60 min.
        self.ind['icf_per_60'] = {}  # Individual CF per 60 min
        self.ind['iff_per_60'] = {}  # Individual FF per 60 min
        self.ind['iscf_per_60'] = {}  # Individual SCF per 60 min
        self.ind['ish_pcg'] = {}  # Individual shooting percentage
        self.ind['part_primary'] = {}  # Quota of totals points that is primary points. Higher number is better.
        self.ind['icf_pcg'] = {}  # "Shooting percentage", for individual CF.
        self.ind['ixgf_pcg'] = {}  # Quota between individual expected goals and goals scored.
        self.ind['goal_scoring_rating'] = {}  # Metric showing goal scoring potential.
        self.ind['i_blocked_against'] = {}
        self.ind['isf'] = self.ind['sf']  # Legacy
        for index in PLAYFORMS:
            self.ind['points'][index] = self.ind['gf'][index] + self.ind['assist'][index]
            self.ind['primary_points'][index] = self.ind['gf'][index] + self.ind['f_assist'][index]
            # Store TOI for readability
            toi = self.ind['toi'][index]
            if toi == 0:
                self.ind['points_per_60'][index] = 0
                self.ind['primary_points_per_60'][index] = 0
                self.ind['isf_per_sec'][index] = 0
                self.ind['pt_per_sec'][index] = 0
                self.ind['pd_per_sec'][index] = 0
                self.ind['pt_per_60'][index] = 0
                self.ind['pd_per_60'][index] = 0
                self.ind['isf_per_60'][index] = 0
                self.ind['icf_per_60'][index] = 0
                self.ind['iff_per_60'][index] = 0
                self.ind['iscf_per_60'][index] = 0
                self.ind['ixgf_per_60'][index] = 0
            else:
                self.ind['points_per_60'][index] = (self.ind['points'][index]/toi) * 3600
                self.ind['primary_points_per_60'][index] = (self.ind['gf'][index] + self.ind['f_assist'][index]/toi) * 3600
                self.ind['isf_per_sec'][index] = self.ind['isf'][index]/toi
                self.ind['pt_per_sec'][index] = self.ind['pt'][index]/toi
                self.ind['pd_per_sec'][index] = self.ind['pd'][index]/toi
                self.ind['pt_per_60'][index] = self.ind['pt_per_sec'][index] * 3600
                self.ind['pd_per_60'][index] = self.ind['pd_per_sec'][index] * 3600
                self.ind['isf_per_60'][index] = self.ind['isf_per_sec'][index] * 3600
                self.ind['icf_per_60'][index] = (self.ind['icf'][index]/toi) * 3600
                self.ind['iff_per_60'][index] = (self.ind['iff'][index]/toi) * 3600
                self.ind['iscf_per_60'][index] = (self.ind['iscf'][index]/toi) * 3600
                self.ind['ixgf_per_60'][index] = (self.ind['ixgf'][index]/toi) * 3600

            if self.ind['points'][index] == 0:
                self.ind['part_primary'][index] = 0
            else:
                self.ind['part_primary'][index] = self.ind['primary_points'][index]/self.ind['points'][index]

            if self.ind['isf'][index] == 0:
                self.ind['ish_pcg'][index] = 0
            else:
                self.ind['ish_pcg'][index] = self.ind['gf'][index]/self.ind['isf'][index]

            if self.ind['icf'][index] == 0:
                self.ind['icf_pcg'][index] = 0
            else:
                self.ind['icf_pcg'][index] = self.ind['gf'][index]/self.ind['icf'][index]

            if self.ind['pt_per_60'][index] + self.ind['pd_per_60'][index] == 0:
                self.ind['pd_pcg'][index] = 0
            else:
                self.ind['pd_pcg'][index] = self.ind['pd_per_60'][index] /\
                                            (self.ind['pd_per_60'][index]+self.ind['pt_per_60'][index])

            if self.ind['gf'][index] + self.ind['ixgf'][index] == 0:
                self.ind['ixgf_pcg'][index] = 0
            else:
                self.ind['ixgf_pcg'][index] = self.ind['gf'][index]/(self.ind['gf'][index]+self.ind['ixgf'][index])


            self.ind['i_blocked_against'][index] = self.ind['icf'][index] - self.ind['iff'][index]
            self.ind['gf_above_xgf'][index] = self.ind['gf'][index] - self.ind['ixgf'][index]
            self.ind['pd_diff_per_60'][index] = self.ind['pd_per_60'][index] - self.ind['pt_per_60'][index]
            self.ind['goal_scoring_rating'][index] = self.ind['ixgf_pcg'][index] * self.ind['icf_per_60'][index]

            # This will only work if "add_on_ice_data" already has been performed
            if self.on_ice['gp'] == 0:
                self.ind['toi_per_gp'][index] = 0
            else:
                self.ind['toi_per_gp'][index] = toi/self.on_ice['gp']


    def add_on_ice_data(self, on_ice):
        ''' Add on-ice data '''

        # Store data directly from input source
        for attribute in on_ice:
            self.on_ice[attribute] = on_ice[attribute]

    def get_on_ice_data(self):
        ''' Return on-ice data '''
        return self.on_ice

    def add_experimental_on_ice_data(self):
        ''' Add special/experimental on-ice data which is not availble from source '''

        for char in ['c', 's', 'g', 'xg', 'sc', 'hdc']:
            char_f = str(char + 'f')
            char_a = str(char + 'a')
            if self.on_ice[char_f] + self.on_ice[char_a] == 0:
                self.on_ice[char_f + '_pcg'] = 0
            else:
                self.on_ice[char_f + '_pcg'] = self.on_ice[char_f]/(self.on_ice[char_f] + self.on_ice[char_a])
            if self.ind['toi']['es'] == 0:
                self.on_ice[char_f + '_per_sec'] = 0
                self.on_ice[char_a + '_per_sec'] = 0
            else:
                self.on_ice[char_f + '_per_sec'] = self.on_ice[char_f]/self.ind['toi']['es']
                self.on_ice[char_a + '_per_sec'] = self.on_ice[char_a]/self.ind['toi']['es']
            self.on_ice[char_f + '_per_60'] = 3600*self.on_ice[char_f + '_per_sec']
            self.on_ice[char_a + '_per_60'] = 3600*self.on_ice[char_a + '_per_sec']
            self.on_ice[char_f + '_diff_per_60'] = self.on_ice[char_f + '_per_60'] - self.on_ice[char_a + '_per_60']

        if (self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs']) == 0:
            self.on_ice['ozs_pcg'] = 0
            self.on_ice['nzs_pcg'] = 0
            self.on_ice['dzs_pcg'] = 0
        else:
            self.on_ice['ozs_pcg'] = self.on_ice['ozs']/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs'])
            self.on_ice['nzs_pcg'] = self.on_ice['nzs']/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs'])
            self.on_ice['dzs_pcg'] = self.on_ice['dzs']/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs'])
        if (self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo']) == 0:
            self.on_ice['ozfo_pcg'] = 0
            self.on_ice['nzfo_pcg'] = 0
            self.on_ice['dzfo_pcg'] = 0
        else:
            self.on_ice['ozfo_pcg'] = self.on_ice['ozfo']/(self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
            self.on_ice['nzfo_pcg'] = self.on_ice['nzfo']/(self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
            self.on_ice['dzfo_pcg'] = self.on_ice['dzfo']/(self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
        if (self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs']+self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo']) == 0:
            self.on_ice['oz_pcg'] = 0
            self.on_ice['nz_pcg'] = 0
            self.on_ice['dz_pcg'] = 0
        else:
            self.on_ice['oz_pcg'] = (self.on_ice['ozs'] + self.on_ice['ozfo']) /\
                                    (self.on_ice['ozs'] +
                                     self.on_ice['nzs'] +
                                     self.on_ice['dzs'] +
                                     self.on_ice['ozfo'] +
                                     self.on_ice['nzfo'] +
                                     self.on_ice['dzfo'])
            self.on_ice['nz_pcg'] = (self.on_ice['nzs'] + self.on_ice['nzfo']) /\
                                    (self.on_ice['ozs'] +
                                     self.on_ice['nzs'] +
                                     self.on_ice['dzs'] +
                                     self.on_ice['ozfo'] +
                                     self.on_ice['nzfo'] +
                                     self.on_ice['dzfo'])
            self.on_ice['dz_pcg'] = (self.on_ice['dzs'] + self.on_ice['dzfo']) /\
                                    (self.on_ice['ozs'] +
                                     self.on_ice['nzs'] +
                                     self.on_ice['dzs'] +
                                     self.on_ice['ozfo'] +
                                     self.on_ice['nzfo'] +
                                     self.on_ice['dzfo'])
        self.on_ice['non_dz_pcg'] = self.on_ice['oz_pcg'] + self.on_ice['nz_pcg']
        self.on_ice['non_oz_pcg'] = self.on_ice['dz_pcg'] + self.on_ice['nz_pcg']
        self.on_ice['non_nz_pcg'] = self.on_ice['oz_pcg'] + self.on_ice['dz_pcg']
        self.on_ice['avg_zone_start'] = (self.on_ice['oz_pcg']*3 +
                                         self.on_ice['nz_pcg']*2 +
                                         self.on_ice['dz_pcg']*1)-2

        # All "estimated_off/def" attributes need to be added after the construction,
        # as they depend on the overall team
        self.on_ice['estimated_off_per_sec'] = 0
        self.on_ice['estimated_def_per_sec'] = 0
        self.on_ice['estimated_off_per_60'] = 0
        self.on_ice['estimated_def_per_60'] = 0
        self.on_ice['estimated_def_per_60_diff'] = 0
        self.on_ice['estimated_off_pcg'] = 0

    def initialize_ranking_data(self):
        self.rank = {}
        self.rank['estimated_off_per_60'] = 0
        self.rank['estimated_off_per_60'] = 0
        self.rank['estimated_off_pcg'] = 0
        self.rank['estimated_off_diff'] = 0
        self.rank['primary_points_per_60'] = 0
        self.rank['goal_scoring_rating'] = 0
        self.rank['total'] = 0

    def print_player(self, playform='es'):
        ''' Print player information '''
        print('\nInformation for player {0} ({1})'.format(self.bio['name'], self.bio['team_id']))


        # Print estimated offense/defense
        print('   Estimated offense/60: {0:.1f}. Estimated defense/60: {1:.1f}. Estimated offense%: {2:.1f}'
              .format(self.on_ice['estimated_off_per_60'],
                      self.on_ice['estimated_def_per_60'],
                      100*self.on_ice['estimated_off_pcg']))


        # Print points/goalscoring abilities
        print('   Points/60: {0:.2f}. Goals above expected: {1:.2f}. GF/ixGF-quote: {2:.2f}'
              .format(self.ind['points_per_60'][playform],
                      self.ind['gf_above_xgf'][playform],
                      self.ind['ixgf_pcg'][playform]))
        '''
        # Print rankings
        print('   Rank-Off%: {0:.0f}. Rank-Primary points/60: {1:.0f}. Rank-Goal scoring: {2:.0f}'
              .format(self.rank['estimated_off_pcg'],
                      self.rank['primary_points_per_60'],
                      self.rank['goal_scoring_rating']))
        '''

        # Print deployment information
        print('   TOI/GP: {0:.1f}. Penalty difference/60: {1:.2f}. Avg. zone start: {2:.2f}'
              .format(self.ind['toi_per_gp'][playform]/60,
                      self.ind['pd_diff_per_60'][playform],
                      self.on_ice['avg_zone_start']))

    def get_attribute(self, attribute, playform_index='es'):
        ''' Class function to get player attribute '''
        if playform_index == 'ranking':
            return self.rank[attribute]
        if attribute in self.bio:
            return self.bio[attribute]
        elif attribute in self.ind:
            return self.ind[attribute][playform_index]
        elif attribute in self.on_ice:
            return self.on_ice[attribute]
        else:
            raise ValueError('Unknown attribute ' + attribute)

    def get_toi(self, playform_index='es'):
        ''' Special function to get time on ice. Possible to get time on ice for different playforms '''
        return self.get_attribute('toi', playform_index)


class Goalie():
    ''' Goalie class '''
    def __init__(self, bio, ind):
        # Bio-data
        self.bio = bio

        # Ind
        self.ind = {}
        for attribute in ind.keys():
            self.ind[attribute] = ind[attribute]

        # Special attributes
        self.ind['sv_pcg'] = [None, None, None]
        self.ind['sa_per_sec'] = [None, None, None]
        self.ind['gsaa_per_60'] = [None, None, None]
        self.ind['gsax'] = [None, None, None]
        self.ind['gsax_per_60'] = [None, None, None]
        for index in [STAT_ES, STAT_PP, STAT_PK]:
            self.ind['gsax'][index] = ind['xga'][index] - ind['ga'][index]
            if ind['toi'][index] == 0:
                self.ind['gaa'][index] = 0
                self.ind['sa_per_sec'][index] = 0
                self.ind['gsaa_per_60'][index] = 0
                self.ind['gsax_per_60'][index] = 0
            else:
                self.ind['gaa'][index] = 3600*ind['ga'][index]/ind['toi'][index]
                self.ind['sa_per_sec'][index] = ind['sa'][index]/ind['toi'][index]
                self.ind['gsaa_per_60'][index] = 3600*(ind['gsaa'][index])/ind['toi'][index]
                self.ind['gsax_per_60'][index] = 3600*(self.ind['gsax'][index])/ind['toi'][index]
            if ind['sa'][index] == 0:
                self.ind['sv_pcg'][index] = 0
            else:
                self.ind['sv_pcg'][index] = ind['sv'][index]/ind['sa'][index]

        # Simulated stats
        self.in_game_stats = defaultdict(int)

    def get_attribute(self, attribute, playform_index=None):
        ''' Get specific attribute for a goalie '''
        if playform_index is None:
            playform_index = STAT_ES
        if attribute in self.bio.keys():
            return self.bio[attribute]
        elif attribute in self.ind.keys():
            return self.ind[attribute][playform_index]
        else:
            raise ValueError('Unknown attribute ' + attribute)

    def get_toi(self, playform_index=None):
        ''' Get time on ice for a goalie '''
        if playform_index is None:
            playform_index = STAT_ES
        return self.get_attribute('toi', playform_index)

    def print_player(self):
        ''' Print player information for a goalie '''
        print('Information for player ' + self.bio['name'])
        print(' 5v5:')
        print('     Shots against: {0:.0f}. \
                    Goals against: {1:.0f}. \
                    Save%: {2:.1f}'
              .format(self.ind['sa'][0],
                      self.ind['ga'][0],
                      100*self.ind['sv_pcg'][0]))

        print('     TOI: {0:.0f}. Goals against average (GAA): {1:.2f}.'.format(self.ind['toi'][0], self.ind['gaa'][0]))
        print('     Goals saved above average: {0:.1f}. Goals saved above xGA: {1:.1f}.'.format(self.ind['gsaa'][0], self.ind['gsax'][0]))
        print('     Goals saved above average/60: {0:.1f}. Goals saved above xGA/60: {1:.1f}.'.format(self.ind['gsaa_per_60'][0], self.ind['gsax_per_60'][0]))
        print(' PP:')
        print('     Shots against: {0:.1f}. Goals against: {1:.1f}. Save%: {2:.1f}'.format(self.ind['sa'][1], self.ind['ga'][1], 100*self.ind['sv_pcg'][1]))
        print('     TOI: {0:.0f}. Goals against average (GAA): {1:.2f}.'.format(self.ind['toi'][1], self.ind['gaa'][1]))
        print('     Goals saved above average: {0:.1f}. Goals saved above xGA: {1:.1f}.'.format(self.ind['gsaa'][1], self.ind['gsax'][1]))
        print('     Goals saved above average/60: {0:.1f}. Goals saved above xGA/60: {1:.1f}.'.format(self.ind['gsaa_per_60'][1], self.ind['gsax_per_60'][1]))
        print(' PK:')
        print('     Shots against: {0:.1f}. Goals against: {1:.1f}. Save%: {2:.1f}'.format(self.ind['sa'][2], self.ind['ga'][2], 100*self.ind['sv_pcg'][2]))
        print('     TOI: {0:.0f}. Goals against average (GAA): {1:.2f}.'.format(self.ind['toi'][2], self.ind['gaa'][2]))
        print('     Goals saved above average: {0:.1f}. Goals saved above xGA: {1:.1f}.'.format(self.ind['gsaa'][2], self.ind['gsax'][2]))
        print('     Goals saved above average/60: {0:.1f}. Goals saved above xGA/60: {1:.1f}.'.format(self.ind['gsaa_per_60'][2], self.ind['gsax_per_60'][2]))


class Team():
    def __init__(self, name, reg_array, adv_array, team_schedule, fatigue_info):

        self.name = name        # name = team_id
        [self.conference, self.division] = self.get_division(self.name)

        self.gp = reg_array[0]
        self.team_toi_es = reg_array[1]
        self.team_toi_es_per_gp = self.team_toi_es / self.gp
        self.wins = reg_array[2]
        self.losses = reg_array[3]
        self.otl = reg_array[4]
        self.p = reg_array[5]
        self.gf = reg_array[6]
        self.ga = reg_array[7]
        if self.gf + self.ga == 0:
            self.gf_pcg = 0
        else:
            self.gf_pcg = self.gf/(self.gf+self.ga)
        self.gf_per_60 = 3600*self.gf/self.team_toi_es
        self.ga_per_60 = 3600*self.ga/self.team_toi_es
        self.gf_diff_per_60 = self.gf_per_60 - self.ga_per_60
        self.p_pcg = reg_array[8]

        # This is directly accessed in the create_team_db()
        self.team_toi_pp = 0
        self.team_toi_pk = 0
        self.team_toi_pp_per_gp = 0
        self.team_toi_pk_per_gp = 0
        self.team_gf_per_pp = 0
        self.team_ga_per_pp = 0
        self.home_p_pcg = 0
        self.away_p_pcg = 0

        self.sf = adv_array[0]
        self.sa = adv_array[1]
        self.sf_pcg = adv_array[2]
        self.sf_per_sec = self.sf/self.team_toi_es
        self.sa_per_sec = self.sa/self.team_toi_es
        self.sf_per_60 = 3600*self.sf_per_sec
        self.sa_per_60 = 3600*self.sa_per_sec
        self.cf = adv_array[3]
        self.ca = adv_array[4]
        self.cf_pcg = adv_array[5]
        self.cf_per_sec = self.cf/self.team_toi_es
        self.ca_per_sec = self.ca/self.team_toi_es
        self.cf_per_60 = 3600*self.cf_per_sec
        self.ca_per_60 = 3600*self.ca_per_sec
        self.ff = adv_array[6]
        self.fa = adv_array[7]
        self.ff_pcg = adv_array[8]
        self.ff_per_sec = self.ff/self.team_toi_es
        self.fa_per_sec = self.fa/self.team_toi_es
        self.ff_per_60 = 3600*self.ff_per_sec
        self.fa_per_60 = 3600*self.fa_per_sec
        self.blocked_against = self.cf-self.ff
        self.xgf = adv_array[9]
        self.xga = adv_array[10]
        self.xgf_pcg = adv_array[11]
        self.xgf_per_sec = self.xgf/self.team_toi_es
        self.xga_per_sec = self.xga/self.team_toi_es
        self.xgf_per_60 = 3600*self.xgf_per_sec
        self.xga_per_60 = 3600*self.xga_per_sec
        self.scf = adv_array[12]
        self.sca = adv_array[13]
        self.scf_pcg = adv_array[14]
        self.scf_per_sec = self.scf/self.team_toi_es
        self.sca_per_sec = self.sca/self.team_toi_es
        self.scf_per_60 = 3600 * self.scf_per_sec
        self.sca_per_60 = 3600 * self.sca_per_sec
        self.hdcf = adv_array[15]
        self.hdca = adv_array[16]
        self.hdcf_pcg = adv_array[17]
        self.hdcf_per_sec = self.hdcf/self.team_toi_es
        self.hdca_per_sec = self.hdca/self.team_toi_es
        self.hdcf_per_60 = 3600*self.hdcf_per_sec
        self.hdca_per_60 = 3600*self.hdca_per_sec
        self.sv_pcg = adv_array[18]
        self.pdo = adv_array[19]

        self.schedule = team_schedule
        self.remaining_schedule = self.schedule[self.gp:]
        self.game_index = self.gp
        self.simulated_wins = 0
        self.simulated_po_div_final = 0
        self.simulated_po_conf_final = 0
        self.simulated_po_conf_champ = 0
        self.simulated_po_sc_champ = 0
        #if self.game_index >= 0:
        #   self.previous_opponent = self.schedule[self.game_index]
        #else:
        #   self.previous_opponent = 'N/A'
        if self.game_index == 82:
            self.next_opponent = 'N/A'
        self.gf_in_simulated_game = 0
        self.sf_in_simulated_game = 0
        self.exp_data = {}
        self.exp_data['sf_per_sec'] = self.sf_per_sec
        self.exp_data['sa_per_sec'] = self.sa_per_sec
        self.exp_data['cf_per_sec'] = self.cf_per_sec
        self.exp_data['ca_per_sec'] = self.ca_per_sec
        self.exp_data['ff_per_sec'] = self.ff_per_sec
        self.exp_data['fa_per_sec'] = self.fa_per_sec
        self.exp_data['xgf_per_sec'] = self.xgf_per_sec
        self.exp_data['xga_per_sec'] = self.xga_per_sec
        self.exp_data['scf_per_sec'] = self.scf_per_sec
        self.exp_data['sca_per_sec'] = self.sca_per_sec
        self.exp_data['hdcf_per_sec'] = self.hdcf_per_sec
        self.exp_data['hdca_per_sec'] = self.hdca_per_sec
        self.exp_data['hits_per_game'] = 0
        self.exp_data['team_sf_in_simulated_game'] = 0
        self.exp_data['in_season_rating'] = 0
        self.exp_data['pre_season_rating'] = 0
        self.exp_data['total_made_playoffs'] = 0
        self.exp_data['mean_made_playoffs'] = 0
        self.exp_data['total_simulated_points'] = 0
        self.exp_data['mean_simulated_points'] = 0

        self.rank = {}
        self.rank['p_pcg'] = 0
        self.rank['gf_pcg'] = 0
        self.rank['sf_pcg'] = 0
        self.rank['cf_pcg'] = 0
        self.rank['ff_pcg'] = 0
        self.rank['xgf_pcg'] = 0
        self.rank['scf_pcg'] = 0
        self.rank['hdcf_pcg'] = 0
        self.rank['sv_pcg'] = 0
        self.rank['pdo'] = 0
        self.rank['hits'] = 0
        self.rank['hits_diff'] = 0

        self.fatigue = fatigue_info

    def get_division(self, team_id):
        atlantic, metro, central, pacific = set(), set(), set(), set()
        atlantic.update(['BOS'], ['BUF'], ['DET'], ['FLA'], ['MTL'], ['OTT'], ['TBL'], ['TOR'])
        metro.update(['CAR'], ['CBJ'], ['NJD'], ['NYI'], ['NYR'], ['PHI'], ['PIT'], ['WSH'])
        central.update(['CHI'], ['COL'], ['DAL'], ['MIN'], ['NSH'], ['STL'], ['WPG'])
        pacific.update(['ANA'], ['ARI'], ['CGY'], ['EDM'], ['LAK'], ['SJS'], ['VAN'], ['VGK'])

        if team_id in atlantic:
            return ['E', 'A']
        elif team_id in metro:
            return ['E', 'M']
        elif team_id in central:
            return ['W', 'C']
        elif team_id in pacific:
            return ['W', 'P']
        else:
            raise ValueError('Unknown team-ID: ' + str(team_id))

    def add_points(self, p_to_add):
        self.p += p_to_add

    def get_ratings(self):
        return [self.exp_data['in_season_rating'], self.exp_data['pre_season_rating']]

    def print_team(self):
        print(self.name)
        print('   CF:   {0:.0f}. CA:   {1:.0f}. CF%:   {2:.1f}%.'.format(self.cf, self.ca, 100*self.cf_pcg))
        print('   FF:   {0:.0f}. FA:   {1:.0f}. FF%:   {2:.1f}%.'.format(self.ff, self.fa, 100*self.ff_pcg))
        print('   SF:   {0:.0f}. SA:   {1:.0f}. SF%:   {2:.1f}%.'.format(self.sf, self.sa, 100*self.sf_pcg))
        print('   GF:   {0:.0f}. GA:   {1:.0f}. GF%:   {2:.1f}%.'.format(self.gf, self.ga, 100*self.gf_pcg))
        print('   xGF:  {0:.0f}. xGA:  {1:.0f}. xGF%:  {2:.1f}%.'.format(self.xgf, self.xga, 100*self.xgf_pcg))
        print('   SCF:  {0:.0f}. SCA:  {1:.0f}. SCF%:  {2:.1f}%.'.format(self.scf, self.sca, 100*self.scf_pcg))
        print('   HDCF: {0:.0f}. HDCA: {1:.0f}. HDCF%: {2:.1f}%.'.format(self.hdcf, self.hdca, 100*self.hdcf_pcg))

    def update_score(self, key):
        if key == 'w':
            self.p += 2
            self.wins += 1
            self.simulated_wins += 1
        elif key == 'l':
            self.p += 0
            self.losses += 1
        elif key == 'otl':
            self.p += 1
            self.otl += 1
        else:
            raise ValueError('Unknown key "' + str(key) + '". Key needs to be "w", "l" or "otl"')

    def reset_schedule(self):
        self.gp = 0
        self.wins = 0
        self.losses = 0
        self.otl = 0
        self.p = 0
        self.gf = 0
        self.ga = 0
        self.p_pcg = 0
        self.exp_data['in_season_rating'] = self.exp_data['pre_season_rating']
        self.remaining_schedule = (self.schedule).copy()

    def simulate_game(self, opponent, simulation_param, data_param=[]):
        simulation_param['ht_id'] = self.name
        simulation_param['at_id'] = opponent.name

        # Update game data
        self.gp += 1
        opponent.gp += 1
        # Update points
        if simulation_param['simulation_mode'] == SIMULATION_LIGHT:
            # Simplified simulation, based on team-stats.

            # New version of calculating "rating". Old version would be: distribution = self.rating/(self.rating+opponent.rating)
            distribution = self.exp_data['in_season_rating']/(self.exp_data['in_season_rating']+opponent.exp_data['in_season_rating'])

            self.gf_in_simulated_game = distribution*TOTAL_GOALS_PER_GAME
            opponent.gf_in_simulated_game = (1-distribution)*TOTAL_GOALS_PER_GAME
            if random.uniform(0, 1) < PROBABILITY_FOR_OT:  # this is not correct.
                if random.uniform(0, 1) < distribution:
                    self.update_score('w')
                    opponent.update_score('otl')
                else:
                    self.update_score('otl')
                    opponent.update_score('w')
            else:
                if random.uniform(0, 1) < distribution:
                    self.update_score('w')
                    opponent.update_score('l')
                else:
                    self.update_score('l')
                    opponent.update_score('w')
        else:
            # Advanced (and time demanding) simulation, based on player stats.
            # Simulate the game
            game_output = simulate_ind_game(simulation_param, data_param)

            # Update score and stats
            self.gf_in_simulated_game = game_output['ht_goals']
            opponent.gf_in_simulated_game = game_output['at_goals']
            self.sf_in_simulated_game = game_output['ht_shots']
            self.exp_data['team_sf_in_simulated_game'] = game_output['ht_exp_shots']
            opponent.sf_in_simulated_game = game_output['at_shots']
            opponent.exp_data['team_sf_in_simulated_game'] = game_output['at_exp_shots']
            if game_output['ht_points'] == 2:
                self.update_score('w')
                if game_output['at_points'] == 1:
                    opponent.update_score('otl')
                else:
                    opponent.update_score('l')
            elif game_output['ht_points'] == 1:
                self.update_score('otl')
                opponent.update_score('w')
            else:
                self.update_score('l')
                opponent.update_score('w')

    def simulate_game_in_season(self, opponent, simulation_param, data_param=[]):
        # Simulate one game
        self.simulate_game(opponent, simulation_param, data_param)

        # Update schedule
        self.remaining_schedule = self.remaining_schedule[1:]
        if len(self.remaining_schedule) > 0:
            self.next_opponent = self.remaining_schedule[0]
        else:
            self.next_opponent = 'N/A'
        # Remove game from remaining schedule
        try:
            opponent.remaining_schedule.remove(self.name)
        except Exception as ex:
            raise ValueError('Schedule mis-match with the game between ' +
                             self.name + ' (HOME) and ' + opponent.name + ' (AWAY): ' + ex)
