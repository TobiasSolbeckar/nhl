import random
from collections import defaultdict

from nhl_defines import *
from nhl_simulation import simulate_ind_game


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

    def add_additional_ind_data(self):
        ''' Add special/additional individual data which is not available from source '''
        self.ind['toi_per_gp'] = {}  # Time on ice per game
        self.ind['points'] = {}  # Total points
        self.ind['primary_points'] = {}  # Primary points
        self.ind['gf_above_xgf'] = {}  # Goals scored above (individual) expected goals
        self.ind['gf_above_xgf_per_60'] = {}  # Goals scored above (individual) expected goals
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
        self.ind['ixgf_per_icf'] = {}
        if 'sf' not in self.ind:
            self.ind['isf'] = {}
        else:
            self.ind['isf'] = self.ind['sf']  # Legacy
        for index in PLAYFORMS:
            self.ind['points'][index] = self.ind['goals'][index] + self.ind['assists'][index]
            self.ind['primary_points'][index] = self.ind['goals'][index] + self.ind['primary_assists'][index]
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
                self.ind['primary_points_per_60'][index] = (self.ind['goals'][index] + self.ind['primary_assists'][index]/toi) * 3600
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
                self.ind['ish_pcg'][index] = self.ind['goals'][index]/self.ind['isf'][index]

            if self.ind['icf'][index] == 0:
                self.ind['icf_pcg'][index] = 0
            else:
                self.ind['icf_pcg'][index] = self.ind['goals'][index]/self.ind['icf'][index]

            if self.ind['pt_per_60'][index] + self.ind['pd_per_60'][index] == 0:
                self.ind['pd_pcg'][index] = 0
            else:
                self.ind['pd_pcg'][index] = self.ind['pd_per_60'][index] /\
                                            (self.ind['pd_per_60'][index]+self.ind['pt_per_60'][index])

            if self.ind['goals'][index] + self.ind['ixgf'][index] == 0:
                self.ind['ixgf_pcg'][index] = 0
            else:
                self.ind['ixgf_pcg'][index] = self.ind['goals'][index]/(self.ind['goals'][index]+self.ind['ixgf'][index])  # Higher means better goalscorer

            if self.ind['icf_per_60'][index] == 0:
                self.ind['ixgf_per_icf'][index] = 0
            else:
                self.ind['ixgf_per_icf'][index] = self.ind['ixgf_per_60'][index] / self.ind['icf_per_60'][index]

            self.ind['i_blocked_against'][index] = self.ind['icf'][index] - self.ind['iff'][index]
            self.ind['gf_above_xgf'][index] = self.ind['goals'][index] - self.ind['ixgf'][index]
            self.ind['pd_diff_per_60'][index] = self.ind['pd_per_60'][index] - self.ind['pt_per_60'][index]
            self.ind['goal_scoring_rating'][index] = self.ind['ixgf_pcg'][index] * self.ind['isf_per_60'][index]

            if self.ind["toi"][index] == 0:
                self.ind['gf_above_xgf_per_60'][index] = 0
            else:
                self.ind['gf_above_xgf_per_60'][index] = 3600 * self.ind['gf_above_xgf'][index] / self.ind["toi"][index]

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

    def add_additional_on_ice_data(self):
        ''' Add special/additional on-ice data which is not availble from source '''

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

    def validate_relative_data(self):
        ''' Check if a player has been assigned relative data. If not, assume the player is a perfect Average Joe '''
        if 'rel_cf_per_60' not in self.on_ice:
            for entry in ['c', 'f', 's', 'g', 'xg', 'sc']:
                self.on_ice['rel_' + entry + 'f_per_60'] = 0
                self.on_ice['rel_' + entry + 'a_per_60'] = 0
                self.on_ice['rel_' + entry + 'f_pcg'] = 0
                self.on_ice['rel_' + entry + 'f_factor'] = 1
                self.on_ice['rel_' + entry + 'a_factor'] = 1

    def initialize_ranking_data(self):
        ''' Initialize ranking data '''
        self.rank = {}
        self.rank['estimated_off_per_60'] = 0
        self.rank['estimated_off_per_60'] = 0
        self.rank['estimated_off_pcg'] = 0
        self.rank['estimated_off_diff'] = 0
        self.rank['primary_points_per_60'] = 0
        self.rank['goal_scoring_rating'] = 0
        self.rank['total'] = 0

    def _print(self, playform=None):
        ''' Print player information '''
        print('\nInformation for player {0} ({1})'.format(self.bio['name'], self.bio['team_id']))

        if playform is None:
            for playform in PLAYFORMS:
                # Print points/goalscoring abilities
                print('   [{0}] Points/60: {1:.2f}. Primary points per game: {2:.2f}. Goals above expected: {3:.2f}. GF/ixGF-quote: {4:.2f}'
                    .format(playform.upper(),
                            self.ind['points_per_60'][playform],
                            self.ind['primary_points'][playform]/self.on_ice['gp'],
                            self.ind['gf_above_xgf'][playform],
                            self.ind['ixgf_pcg'][playform]))

                print('   [{0}] Points: {1:.0f}. Goals: {2:.0f}. Assists: {3:.0f}'
                    .format(playform.upper(),
                            self.ind['points'][playform],
                            self.ind['goals'][playform],
                            self.ind['assists'][playform]))

        # Print estimated offense/defense
        print('   Estimated offense/60: {0:.1f}. Estimated defense/60: {1:.1f}. Estimated offense%: {2:.1f}'
              .format(self.on_ice['estimated_off_per_60'],
                      self.on_ice['estimated_def_per_60'],
                      100*self.on_ice['estimated_off_pcg']))
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
            # If -1, summarize all playforms
            if playform_index == -1:
                tmp_ = 0
                for playform in PLAYFORMS:
                    tmp_ += self.ind[attribute][playform]
                return tmp_
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
    def __init__(self, bio, ind=None):
        # Bio-data
        self.bio = bio
        if ind is None:
            self.ind = {}
        else:
            self.add_ind_data(ind)

    def add_ind_data(self, ind):
        ''' Add/update data regarding individual performance. Store data directly from input source (www.naturalstattrick.com)'''
        for attribute in ind:
            self.ind[attribute] = ind[attribute]

    def add_additional_ind_data(self):
        ''' Add additional data which is not directly stored in the csv-file '''
        self.ind['gsax'] = {}  # Goals saved above expected per 60 min
        self.ind['gsaa_per_60'] = {}  # Goals saved above average per 60 min
        self.ind['gsax_per_60'] = {}  # Goals saved above expected per 60 min

        for index in PLAYFORMS:  # noqa
            toi = self.ind['toi'][index]
            self.ind['gsax'][index] = self.ind['xga'][index] - self.ind['ga'][index]
            if toi == 0:
                self.ind['gsaa_per_60'][index] = 0
                self.ind['gsax_per_60'][index] = 0
            else:
                self.ind['gsaa_per_60'][index] = (self.ind['gsaa'][index]/toi) * 3600
                self.ind['gsax_per_60'][index] = (self.ind['gsax'][index]/toi) * 3600

    def get_ind_data(self):
        ''' Return the individual data '''
        return self.ind

    def get_attribute(self, attribute, playform_index=None):
        ''' Get specific attribute for a goalie '''
        if playform_index is None:
            playform_index = 'es'
        if attribute in self.bio.keys():
            return self.bio[attribute]
        elif attribute in self.ind.keys():
            # Return summarized value
            if playform_index == -1:
                tmp_ = 0
                for playform in PLAYFORMS:
                    tmp_ += self.ind[attribute][playform]
                return tmp_
            return self.ind[attribute][playform_index]
        else:
            raise ValueError('Unknown attribute ' + attribute)

    def get_toi(self, playform_index=None):
        ''' Get time on ice for a goalie '''
        if playform_index is None:
            playform_index = 'es'
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
    ''' Class for holding information about Teams
        Parsing from CSV-files is done in the corresponding "Database" class (i.e. "TeamDatabase"). This is also where the Team-objects are created.
    '''

    def __init__(self, team_id):
        ''' Team constructor '''
        self.name = team_id
        self.team_id = team_id
        self.set_division()

    def add_additional_data(self):
        ''' Create specific metrics not stored in CSV-files '''
        if self.team_toi_es == 0 or self.gp == 0:
            raise ValueError('Team ' + self.name + ' has not played any games!')

        self.team_toi_es_per_gp = self.team_toi_es / self.gp
        if self.gf + self.ga == 0:
            self.gf_pcg = 0
        else:
            self.gf_pcg = self.gf/(self.gf+self.ga)

        self.gf_per_60 = 3600*self.gf/self.team_toi_es
        self.ga_per_60 = 3600*self.ga/self.team_toi_es
        self.gf_diff_per_60 = self.gf_per_60 - self.ga_per_60
        self.sf_per_sec = self.sf/self.team_toi_es
        self.sa_per_sec = self.sa/self.team_toi_es
        self.sf_per_60 = 3600*self.sf_per_sec
        self.sa_per_60 = 3600*self.sa_per_sec
        self.cf_per_sec = self.cf/self.team_toi_es
        self.ca_per_sec = self.ca/self.team_toi_es
        self.cf_per_60 = 3600*self.cf_per_sec
        self.ca_per_60 = 3600*self.ca_per_sec
        self.ff_per_sec = self.ff/self.team_toi_es
        self.fa_per_sec = self.fa/self.team_toi_es
        self.ff_per_60 = 3600*self.ff_per_sec
        self.fa_per_60 = 3600*self.fa_per_sec
        self.blocked_against = self.cf-self.ff
        self.xgf_per_sec = self.xgf/self.team_toi_es
        self.xga_per_sec = self.xga/self.team_toi_es
        self.xgf_per_60 = 3600*self.xgf_per_sec
        self.xga_per_60 = 3600*self.xga_per_sec
        self.scf_per_sec = self.scf/self.team_toi_es
        self.sca_per_sec = self.sca/self.team_toi_es
        self.scf_per_60 = 3600 * self.scf_per_sec
        self.sca_per_60 = 3600 * self.sca_per_sec
        self.hdcf_per_sec = self.hdcf/self.team_toi_es
        self.hdca_per_sec = self.hdca/self.team_toi_es
        self.hdcf_per_60 = 3600*self.hdcf_per_sec
        self.hdca_per_60 = 3600*self.hdca_per_sec

        self.simulated_wins = 0
        self.simulated_po_div_final = 0
        self.simulated_po_conf_final = 0
        self.simulated_po_conf_champ = 0
        self.simulated_po_sc_champ = 0
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

    def _print(self):
        ''' Print team information '''
        print('Team ' + self.team_id + ':')
        print('   CF%: {0}. FF%: {1}. SCF%: {2}. HDCF%: {3}. xGF%: {4}. '.format(self.cf_pcg, self.ff_pcg, self.scf_pcg, self.hdcf_pcg, self.xgf_pcg))
        print('   ADD RANKING INFORMATION')

    def set_division(self):
        ''' Set conference and division for a team '''
        atlantic, metro, central, pacific = set(), set(), set(), set()
        atlantic.update(['BOS'], ['BUF'], ['DET'], ['FLA'], ['MTL'], ['OTT'], ['TBL'], ['TOR'])
        metro.update(['CAR'], ['CBJ'], ['NJD'], ['NYI'], ['NYR'], ['PHI'], ['PIT'], ['WSH'])
        central.update(['ARI'], ['CHI'], ['COL'], ['DAL'], ['MIN'], ['NSH'], ['STL'], ['WPG'])
        pacific.update(['ANA'], ['CGY'], ['EDM'], ['LAK'], ['SEA'], ['SJS'], ['VAN'], ['VGK'])

        if self.team_id in atlantic:
            self.conference = 'E'
            self.division = 'A'
        elif self.team_id in metro:
            self.conference = 'E'
            self.division = 'M'
        elif self.team_id in central:
            self.conference = 'W'
            self.division = 'C'
        elif self.team_id in pacific:
            self.conference = 'W'
            self.division = 'P'

    def get_division(self):
        ''' Return conference and division for a team '''
        return [self.conference, self.division]

    def update_score(self, key):
        ''' Update point totals for a team after a simulation '''
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
