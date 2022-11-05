import datetime
import time
import os
import platform
import csv
import random
import warnings
import json
from collections import defaultdict
from shutil import copyfile

import numpy as np
import gspread
# from oauth2client.client import SignedJwtAssertionCredentials

from src.nhl_defines import *

if platform.system() == 'Darwin':
    import matplotlib.pyplot as plt


def generate_long_name():
    ''' Get complete name for each team '''
    long_name = {}
    long_name['ANA'] = 'Anaheim Ducks'
    long_name['ARI'] = 'Arizona Coyotes'
    long_name['BOS'] = 'Boston Bruins'
    long_name['BUF'] = 'Buffalo Sabres'
    long_name['CAR'] = 'Carolina Hurricanes'
    long_name['CBJ'] = 'Columbus Blue Jackets'
    long_name['CGY'] = 'Calgary Flames'
    long_name['CHI'] = 'Chicago Blackhawks'
    long_name['COL'] = 'Colorado Avalanche'
    long_name['DAL'] = 'Dallas Stars'
    long_name['DET'] = 'Detroit Red Wings'
    long_name['EDM'] = 'Edmonton Oilers'
    long_name['FLA'] = 'Florida Panthers'
    long_name['LAK'] = 'Los Angeles Kings'
    long_name['MIN'] = 'Minnesota Wild'
    long_name['MTL'] = 'Montreal Canadiens'
    long_name['NJD'] = 'New Jersey Devils'
    long_name['NSH'] = 'Nashville Predators'
    long_name['NYI'] = 'New York Islanders'
    long_name['NYR'] = 'New York Rangers'
    long_name['OTT'] = 'Ottawa Senators'
    long_name['PHI'] = 'Philadelphia Flyers'
    long_name['PIT'] = 'Pittsburgh Penguins'
    long_name['SEA'] = 'Seattle Kraken'
    long_name['SJS'] = 'San Jose Sharks'
    long_name['STL'] = 'St. Louis Blues'
    long_name['TBL'] = 'Tampa Bay Lightning'
    long_name['TOR'] = 'Toronto Maple Leafs'
    long_name['VAN'] = 'Vancouver Canucks'
    long_name['VGK'] = 'Vegas Golden Knights'
    long_name['WPG'] = 'Winnipeg Jets'
    long_name['WSH'] = 'Washington Capitals'
    return long_name


def generate_all_teams_dict(return_type):
    ''' Create dictionary with specified return type for each team.
    The return type will be the same for all teams.
    '''
    output = {}
    output['ANA'] = return_type
    output['ARI'] = return_type
    output['BOS'] = return_type
    output['BUF'] = return_type
    output['CAR'] = return_type
    output['CBJ'] = return_type
    output['CGY'] = return_type
    output['CHI'] = return_type
    output['COL'] = return_type
    output['DAL'] = return_type
    output['DET'] = return_type
    output['EDM'] = return_type
    output['FLA'] = return_type
    output['LAK'] = return_type
    output['MIN'] = return_type
    output['MTL'] = return_type
    output['NJD'] = return_type
    output['NSH'] = return_type
    output['NYI'] = return_type
    output['NYR'] = return_type
    output['OTT'] = return_type
    output['PHI'] = return_type
    output['PIT'] = return_type
    output['SEA'] = return_type
    output['SJS'] = return_type
    output['STL'] = return_type
    output['TBL'] = return_type
    output['TOR'] = return_type
    output['VAN'] = return_type
    output['VGK'] = return_type
    output['WPG'] = return_type
    output['WSH'] = return_type
    return output


def get_daily_fo_url(team_id):
    ''' Return the line combinations for each team, based on data from www.dailyfaceoff.com '''
    daily_fo_url_dict = {}
    daily_fo_url_dict['ANA'] = "https://www.dailyfaceoff.com/teams/anaheim-ducks/line-combinations/"
    daily_fo_url_dict['ARI'] = "https://www.dailyfaceoff.com/teams/arizona-coyotes/line-combinations/"
    daily_fo_url_dict['BOS'] = "https://www.dailyfaceoff.com/teams/boston-bruins/line-combinations/"
    daily_fo_url_dict['BUF'] = "https://www.dailyfaceoff.com/teams/buffalo-sabres/line-combinations/"
    daily_fo_url_dict['CAR'] = "https://www.dailyfaceoff.com/teams/carolina-hurricanes/line-combinations/"
    daily_fo_url_dict['CBJ'] = "https://www.dailyfaceoff.com/teams/columbus-blue-jackets/line-combinations/"
    daily_fo_url_dict['CGY'] = "https://www.dailyfaceoff.com/teams/calgary-flames/line-combinations/"
    daily_fo_url_dict['CHI'] = "https://www.dailyfaceoff.com/teams/chigaco-blackhawks/line-combinations/"
    daily_fo_url_dict['COL'] = "https://www.dailyfaceoff.com/teams/colorado-avalanche/line-combinations/"
    daily_fo_url_dict['DAL'] = "https://www.dailyfaceoff.com/teams/dallas-stars/line-combinations/"
    daily_fo_url_dict['DET'] = "https://www.dailyfaceoff.com/teams/detroit-red-wings/line-combinations/"
    daily_fo_url_dict['EDM'] = "https://www.dailyfaceoff.com/teams/edmonton-oilers/line-combinations/"
    daily_fo_url_dict['FLA'] = "https://www.dailyfaceoff.com/teams/florida-panthers/line-combinations/"
    daily_fo_url_dict['LAK'] = "https://www.dailyfaceoff.com/teams/los-angeles-kings/line-combinations/"
    daily_fo_url_dict['MIN'] = "https://www.dailyfaceoff.com/teams/minnesota-wild/line-combinations/"
    daily_fo_url_dict['MTL'] = "https://www.dailyfaceoff.com/teams/montreal-canadiens/line-combinations/"
    daily_fo_url_dict['NJD'] = "https://www.dailyfaceoff.com/teams/new-jersey-devils/line-combinations/"
    daily_fo_url_dict['NSH'] = "https://www.dailyfaceoff.com/teams/nashville-predators/line-combinations/"
    daily_fo_url_dict['NYI'] = "https://www.dailyfaceoff.com/teams/new-york-islanders/line-combinations/"
    daily_fo_url_dict['NYR'] = "https://www.dailyfaceoff.com/teams/new-york-rangers/line-combinations/"
    daily_fo_url_dict['OTT'] = "https://www.dailyfaceoff.com/teams/ottawa-senators/line-combinations/"
    daily_fo_url_dict['PHI'] = "https://www.dailyfaceoff.com/teams/philadelphia-flyers/line-combinations/"
    daily_fo_url_dict['PIT'] = "https://www.dailyfaceoff.com/teams/pittsburgh-penguins/line-combinations/"
    daily_fo_url_dict['SJS'] = "https://www.dailyfaceoff.com/teams/san-jose-sharks/line-combinations/"
    daily_fo_url_dict['STL'] = "https://www.dailyfaceoff.com/teams/st-louis-blues/line-combinations/"
    daily_fo_url_dict['TBL'] = "https://www.dailyfaceoff.com/teams/tampa-bay-lightning/line-combinations/"
    daily_fo_url_dict['TOR'] = "https://www.dailyfaceoff.com/teams/toronto-maple-leafs/line-combinations/"
    daily_fo_url_dict['VAN'] = "https://www.dailyfaceoff.com/teams/vancouver-canucks/line-combinations/"
    daily_fo_url_dict['VGK'] = "https://www.dailyfaceoff.com/teams/vegas-golden-knights/line-combinations/"
    daily_fo_url_dict['WPG'] = "https://www.dailyfaceoff.com/teams/winnipeg-jets/line-combinations/"
    daily_fo_url_dict['WSH'] = "https://www.dailyfaceoff.com/teams/washington-capitals/line-combinations/"
    return daily_fo_url_dict[team_id]


def get_home_team_advantage(t_db, ht_id, at_id=None):
    ''' Calculate advantage for home team '''
    ht = t_db[ht_id]
    ht_rel_pcg = ht.home_p_pcg/(ht.home_p_pcg+ht.away_p_pcg)

    if at_id is None:
        ret_val = ht_rel_pcg
    else:
        at = t_db[at_id]
        at_rel_pcg = at.home_p_pcg/(at.home_p_pcg+at.away_p_pcg)
        ret_val = ht_rel_pcg/(1-at_rel_pcg)
    return ret_val


def get_days_rested(team_id, simulation_param):
    ''' Get amount of days each team has rested for '''
    # For now, only takes the most recent rest into account.
    maximum_rest = 3  # number of days after the team is fully healthy/rested.
    i = 0
    found = False
    days_rested = maximum_rest
    while i < maximum_rest and found is False:
        games_on_date = simulation_param['databases']['season_schedule'][get_previous_day(simulation_param['simulation_date'], i+1)]  # i+1 since there is not need to check the same day as the game.
        for game in games_on_date:
            if team_id in game:
                days_rested = i
                found = True
        i += 1
    return days_rested


def is_skipp_year(year):
    return ((year % 4)) == 0 or ((year % 400) == 0)


def get_previous_day(start_date, number_of_days):
    # This is very ugly and should be done by using datetime.dateime libraray instead.
    # Date needs to be in str-format: 'YYYY-MM-DD'

    if number_of_days == 0:
        datestr = start_date
    else:
        datestr = start_date
        i = 0
        while i < number_of_days:
            [year, month, day] = datestr.split('-')
            if int(day) > 1:
                day = int(day)-1
            else:
                if int(month) in [2, 4, 6, 8, 9, 11]:
                    month = int(month)-1
                    day = 31
                elif int(month) in [5, 7, 10, 12]:
                    month = int(month)-1
                    day = 30
                elif int(month) == 3:
                    month = int(month)-1
                    if is_skipp_year(year):
                        day = 29
                    else:
                        day = 28
                else:
                    year = int(year)-1
                    month = 12
                    day = 31
            datestr = str(str(year) + '-' + str(month) + '-' + str(day))
            i += 1
    return datestr


def get_delta_days(date0, date1):
    ''' Returns difference in days between two dates '''
    # Assumes 'YYYY-MM-DD'
    [year0, month0, day0] = date0.split('-')
    [year1, month1, day1] = date1.split('-')

    delta = datetime.date(int(year1), int(month1), int(day1)) - datetime.date(int(year0), int(month0), int(day0))
    return delta.days


def get_long_name(team_id):
    ''' Get full/complete name of team from team-ID '''
    tmp = generate_long_name()
    return tmp[team_id]


def get_team_id(long_name):
    ''' Get team-ID from full/complete name '''
    tmp = generate_long_name()
    for team_id in tmp:
        if tmp[team_id] == long_name:
            return team_id


def print_progress(i, N, t0, step=10):
    time_unit = ['min', 'min']
    printed = False
    if ((i % (N/(100/step))) == 0) and (i > 0):
        t_elp = (time.time() - t0)/60
        t_left = t_elp*((N/i) - 1)
        if t_elp < 1.0:
            t_elp *= 60
            time_unit[0] = 'sec'
        if t_left < 1.0:
            t_left *= 60
            time_unit[1] = 'sec'
        n = datetime.datetime.now()
        print_n = str(datetime.time(n.hour, n.minute, n.second))
        if time_unit[1] == 'sec':
            eta = n+datetime.timedelta(seconds=t_left)
        else:
            eta = n+datetime.timedelta(minutes=t_left)
        print_eta = str(datetime.time(eta.hour, eta.minute, eta.second))
        print('{0}: {1:.0f} % completed. Time elapsed: {2:.0f} {3}. Estimated time left: {4:.0f} {5} (ETA: {6}).'.format(print_n, 100*i/N, t_elp, time_unit[0], t_left, time_unit[1], print_eta))
        printed = True
    return printed


def val_in_list(val, lst):
    ''' Returns the number of times the value val appears in the list lst. '''
    o = 0
    for vl in lst:
        if vl == val:
            o += 1
    return o


def get_list_pcg(lst):
    new_lst = []
    for entry in lst:
        new_lst.append(100*entry/sum(lst))
    return new_lst


def get_time_str_from_sec(seconds):
    m = seconds//60
    s = seconds % 60
    if m < 10:
        m = str('0'+str(m))
    else:
        m = str(m)

    if s < 10:
        s = str('0'+str(s))
    else:
        s = str(s)

    return str(m + ':' + s)


def get_position_for_player(position):
    if (position == 'L') or (position == 'C') or (position == 'R'):
        position = 'F'
    return position


def generate_player_id(raw_str):
    # Format: Firstname Lastname
    names_array = raw_str.split(" ")
    first_name = names_array[0].upper()
    last_name = ""
    for name in names_array[1:]:
        last_name = last_name + name.upper()
    player_id = first_name + "_" + last_name
    player_id = player_id.replace('.', '_')
    player_id = player_id.replace("'", '')

    # Handle special cases
    if player_id == 'ALEXANDER_NYLANDER':
        player_id = 'ALEX_NYLANDER'

    return player_id


def is_this_aho(raw_player_str, raw_team_str):
    player_id = str(raw_player_str).upper().replace(' ', '_')
    player_id = player_id.replace('.', '_')
    player_id = player_id.replace("'", '')
    if player_id == 'SEBASTIAN_AHO':
        bool_a = True
        if raw_team_str == 'CAR':
            player_id = 'SEBASTIAN_AHO'
        else:
            player_id = 'SEBASTIAN_AHO2'
    else:
        bool_a = False
        player_id = 'N/A'
    return [bool_a, player_id]


def generate_player_and_team_id(raw_player_str, raw_team_str=None):
    # player_id = str(raw_player_str).upper().replace(' ', '_')
    # player_id = player_id.replace('.', '_')
    # player_id = player_id.replace("'", '')

    if (player_id == 'SEBASTIAN_AHO') and (raw_team_str != 'CAR'):
        player_id = 'SEBASTIAN_AHO2'
        return [player_id, 'NYI']

    # Handle special cases
    if player_id == 'ALEXANDER_NYLANDER':
        player_id = 'ALEX_NYLANDER'

    if raw_team_str is None:
        team_id = 'MAKE_BELIEVES'
    else:
        # Get team-id
        # Add players that have played for more than two clubs the current season to "manually_checked_players"
        manually_checked_players = set()
        # manually_checked_players.add('EXAMPLE_PLAYER')
        manually_checked_players.add('GREG_PATERYN')
        # Add players that have played for two teams the current season to "new_team"-dict:
        new_team = {}
        new_team['IAN_COLE'] = 'MIN'
        new_team['GREG_PATERYN'] = 'SJS'
        new_team['JARRED_TINORDI'] = 'BOS'
        new_team['RYAN_DZINGEL'] = 'OTT'
        new_team['CEDRIC_PAQUETTE'] = 'CAR'
        new_team['MARK_FRIEDMAN'] = 'PIT'
        new_team['PATRIK_LAINE'] = 'CBJ'
        new_team['PIERRE-LUC_DUBOIS'] = 'WPG'
        new_team['ERIC_STAAL'] = 'MTL'
        new_team['TRAVIS_ZAJAC'] = 'NYI'
        new_team['KYLE_PALMIERI'] = 'NYI'
        new_team['ALEX_GALCHENYUK'] = 'TOR'
        new_team['JIMMY_VESEY'] = 'VAN'
        new_team['VINNIE_HINOSTROZA'] = 'CHI'
        new_team['BRENDAN_LEMIEUX'] = 'LAK'
        new_team['MICHAEL_AMADIO'] = 'OTT'
        new_team['CHRISTIAN_WOLANIN'] = 'LAK'
        new_team['ALEXANDER_VOLKOV'] = 'ANA'
        new_team['MIKKO_LEHTONEN'] = 'CBJ'
        new_team['JONAS_JOHANSSON'] = 'COL'
        new_team['JEFF_CARTER'] = 'PIT'
        new_team['CARL_SODERBERG'] = 'COL'
        new_team['RICHARD_PANIK'] = 'DET'
        new_team['SAMI_VATANEN'] = 'DAL'
        new_team['DAVID_SAVARD'] = 'TBL'
        new_team['ERIK_GUDBRANSON'] = 'NSH'
        new_team['TAYLOR_HALL'] = 'BOS'
        new_team['BRETT_CONNOLLY'] = 'CHI'
        new_team['JANI_HAKANPAA'] = 'CAR'
        new_team['MIKE_REILLY'] = 'BOS'
        new_team['NIKITA_GUSEV'] = 'FLA'
        new_team['MATTIAS_JANMARK'] = 'VGK'
        new_team['CURTIS_LAZAR'] = 'BOS'
        new_team['ANTHONY_MANTHA'] = 'WSH'
        new_team['SAM_BENNETT'] = 'FLA'
        new_team['HAYDN_FLEURY'] = 'ANA'
        new_team['JAKUB_VRANA'] = 'DET'
        new_team['BRANDON_MONTOUR'] = 'FLA'
        new_team['LUCAS_WALLMARK'] = 'CHI'
        new_team['ANDERS_BJORK'] = 'BUF'
        new_team['JONAS_SIEGENTHALER'] = 'NJD'
        new_team['VICTOR_METE'] = 'OTT'
        new_team['RILEY_STILLMAN'] = 'CHI'
        new_team['DEVAN_DUBNYK'] = 'COL'
        new_team['DAVID_RITTICH'] = 'TOR'
        new_team['BRAYDON_COBURN'] = 'NYI'
        new_team['NICK_FOLIGNO'] = 'TOR'
        new_team['JORDIE_BENN'] = 'WPG'
        new_team['DMITRY_KULIKOV'] = 'EDM'
        new_team['PATRIK_NEMETH'] = 'COL'
        new_team['JON_MERRILL'] = 'MTL'
        new_team['TRAVIS_BOYD'] = 'VAN'
        new_team['ERIK_GUSTAFSSON'] = 'MTL'
        new_team['MICHAEL_RAFFL'] = 'WSH'
        new_team['MATTHEW_HIGHMORE'] = 'VAN'
        new_team['ADAM_GAUDETTE'] = 'CHI'
        new_team['DRAKE_CAGGIULA'] = 'BUF'
        new_team['ALEXANDER_BARABANOV'] = 'SJS'

        team_id = raw_team_str
        # Make sure players have been added to their new clubs. If not, set an error.
        team_id_arr = (team_id.replace(' ', '').split(','))
        if len(team_id_arr) > 1:
            if player_id not in new_team.keys():
                # raise ValueError('Player ' + player_id + ' has more than one team(s). Team-ID: ' + team_id)
                print('Player ' + player_id + ' has more than one team(s). Team-ID: ' + team_id + '. Using team ' + team_id_arr[0] + ' for analysis.')
                team_id = team_id_arr[0]
            if len(team_id_arr) > 2:
                if player_id not in manually_checked_players:
                    # raise ValueError('Player ' + player_id + ' (' + str(raw_team_str) + ') changed club more than once. Please add to "manually_checked_players" to continue.')
                    print('Player ' + player_id + ' has more than two team(s). Team-ID: ' + team_id + '. Using team ' + team_id_arr[0] + ' for analysis.')
                    team_id = team_id_arr[0]

        if team_id == 'L.A':
            team_id = 'LAK'
        elif team_id == 'N.J':
            team_id = 'NJD'
        elif team_id == 'S.J':
            team_id = 'SJS'
        elif team_id == 'T.B':
            team_id = 'TBL'
        elif team_id == 'PHX':
            team_id = 'ARI'

        if player_id in set(new_team.keys()):
            team_id = new_team[player_id]

        # Weird special case due to misspelled team_id at NST-data.
        if team_id == 'PTI':
            team_id = 'PIT'

        if team_id not in ACTIVE_TEAMS:
            raise ValueError('Team-ID for player ' + player_id + ' is incorrect ("' + team_id + '")')

    return [player_id, team_id]


def sort_and_print(unsorted_list, reversed=False, value_idx=0, decs=1):
    ''' Sorts and prints a list of tuples. Assuming the first position in each tuple is the key to be sorted on '''
    if value_idx != 0:
        desc_idx = 0
    else:
        desc_idx = 1

    i = 0
    for tup in sorted(unsorted_list, reverse=reversed):
        i += 1
        desc = tup[desc_idx]
        value = tup[value_idx]
        if decs == 0:
            print(f'{i:3}: {desc}: {value:.0f}')
        elif decs == 1:
            print(f'{i:3}: {desc}: {value:.1f}')
        elif decs == 2:
            print(f'{i:3}: {desc}: {value:.2f}')
        elif decs == 3:
            print(f'{i:3}: {desc}: {value:.3f}')
        elif decs == 4:
            print(f'{i:3}: {desc}: {value:.4f}')
        elif decs == 5:
            print(f'{i:3}: {desc}: {value:.5f}')
        elif decs == 6:
            print(f'{i:3}: {desc}: {value:.6f}')
        elif decs == 7:
            print(f'{i:3}: {desc}: {value:.7f}')


def print_sorted_list_skaters(db,
                              attributes,
                              _filter={},
                              print_list_length=50,
                              scale_factor=1,
                              high_to_low=True,
                              normalize=False):
    ''' Prints a list sorted on a specified attribute '''
    # Validate filter settings
    if 'toi' not in _filter or _filter == {}:
        _filter['toi'] = 100
    if 'position' not in _filter or _filter == {}:
        _filter['position'] = ['F', 'D']
    if 'additional_players' not in _filter or _filter == {}:
        _filter['additional_players'] = []
    if 'playform' not in _filter or _filter == {}:
        _filter['playform'] = 'es'
    print('Filter settings: ' + str(_filter))
    # Initialize local parameters
    output = {}
    added_players = set()
    sorted_list, data_list, all_data = [], [], []
    for skater_id in db.id_set:
        # Loop through all skaters
        skater = db.get_player(skater_id)
        # Check if skater fits the filter settings
        if (skater.ind['toi'][_filter['playform']] >= 60*_filter['toi'] and skater.bio['position'] in _filter['position']) or (skater_id in _filter['additional_players']):
            if len(attributes) > 1:
                if attributes[0] == 'ranking':
                    val = skater.get_attribute(attributes[1], playform_index='ranking')
                else:
                    raise ValueError('Got ' + str(len(attributes)) + ' attributes, expected 1')
            else:
                val = skater.get_attribute(attributes[0], _filter['playform'])
            val *= scale_factor
            all_data.append(val)
            # Go over experimental attributes
            if _filter['generic'] == []:
                sorted_list.append((val, skater_id))
                data_list.append(val)
                added_players.add(skater_id)
            else:
                add_player = True
                for attribute_to_check in _filter['generic']:
                    if skater.get_attribute(attribute_to_check[0]) != attribute_to_check[1]:
                        if skater.get_attribute(attribute_to_check[0]) is True:
                            print("Removing player " + skater_id + " due to " + attribute_to_check[0])
                        add_player = False
                if add_player is True:
                    sorted_list.append((val, skater_id))
                    data_list.append(val)
                    added_players.add(skater_id)
            if (skater_id in _filter['additional_players']) and (skater_id not in added_players):
                sorted_list.append((val, skater_id))
                data_list.append(val)

    sorted_list.sort(reverse=high_to_low)
    data_list.sort(reverse=high_to_low)
    all_data.sort(reverse=high_to_low)

    output['mu'] = np.mean(all_data)
    output['sigma'] = np.std(all_data)
    output['list'] = sorted_list
    output['data'] = data_list
    output['all_data'] = all_data

    if normalize is True:
        norm_factor = 1/np.max(data_list)
    else:
        norm_factor = 1

    print('{0}. Scale factor={1:.0f}. Min.TOI={2:.0f}. Total players={3:.0f}. Average value={4:.2f}. Stdev={5:.2f}.'
            .format(attributes,
                    scale_factor,
                    _filter['toi'],
                    len(all_data),
                    output['mu'],
                    output['sigma']))
    ranking = 0
    for pair in sorted_list:
        ranking += 1
        skater_id = pair[1]
        skater = db.get_player(skater_id)
        if ranking <= print_list_length or skater_id in _filter['additional_players']:
            if attributes[0] == 'ranking':
                val = norm_factor*pair[0]
                print('({0}) {1}: {2} (AGE: {3:.0f}; TEAM: {4}) - {5:.2f} ({6:.2f} sigma. TOI: {7:.1f} min/gp)'
                        .format(ranking,
                                all_data.index(pair[0]) + 1,  # Add one to make print out look nice
                                skater.bio['name'],
                                skater.bio['age'],
                                skater.bio['team_id'],
                                val,
                                (val-output['mu'])/output['sigma'],
                                (skater.get_attribute('toi')/60)/skater.get_attribute('gp')))
            else:
                val = norm_factor*pair[0]
                print('{0} ({1}): {2} ({3}) - {4:.2f} ({5:.2f} sigma)'
                        .format(ranking,
                                all_data.index(pair[0]) + 1,  # Add one to make print out look nice
                                skater.bio['name'],
                                skater.bio['team_id'],
                                val,
                                (val-output['mu'])/output['sigma']))
                print('   TOI: {0:.1f} minutes'.format(skater.get_toi(_filter['playform'])/60))
    return output


def print_sorted_list_goalie(db,
                             attribute,
                             _filter,
                             print_list_length=10,
                             scale_factor=1,
                             high_to_low=True,
                             do_print=True,
                             normalize=False):
    # Validate filter settings
    if 'toi' not in _filter or _filter == {}:
        _filter['toi'] = 500
    if 'additional_players' not in _filter or _filter == {}:
        _filter['additional_players'] = []
    if 'team' not in _filter or _filter == {}:
        _filter['team'] = None
    print('Filter settings: ' + str(_filter))
    output = {}
    added_players = set()
    sorted_list, data_list, all_data = [], [], []
    for goalie_id in db.id_set:
        goalie = db.get_player(goalie_id)
        if goalie.get_attribute('toi') >= 60*_filter['toi'] or goalie_id in _filter['additional_players']:
            val = goalie.get_attribute(attribute[0]) * scale_factor
            all_data.append(val)
            if _filter['team'] is None:
                sorted_list.append((val, goalie_id))
                data_list.append(val)
                added_players.add(goalie_id)
            else:
                if goalie.get_attribute('team_id') in _filter['team']:
                    sorted_list.append((val, goalie_id))
                    data_list.append(val)
                    added_players.add(goalie_id)
            if (goalie_id in _filter['additional_players']) and (goalie_id not in added_players):
                sorted_list.append((val, goalie_id))
                data_list.append(val)

    # This is not very nice.
    sorted_list.sort(reverse=high_to_low)
    data_list.sort(reverse=high_to_low)
    all_data.sort(reverse=high_to_low)
    output['mu'] = np.mean(all_data)
    output['sigma'] = np.std(all_data)
    output['list'] = sorted_list
    output['data'] = data_list
    if normalize is True:
        norm_factor = 1/np.max(data_list)
    else:
        norm_factor = 1
    if do_print is True:
        print('{0}. Scale factor={1:.0f}. Min.TOI={2:.0f}. Total players={3:.0f}. Average value={4:.2f}.'
              .format(attribute,
                      scale_factor,
                      _filter['toi'],
                      len(all_data),
                      output['mu']))
        ranking = 0
        for pair in sorted_list:
            ranking += 1
            goalie_id = pair[1]
            goalie = db.data[goalie_id]
            if ranking <= print_list_length or goalie_id in _filter['additional_players']:
                val = norm_factor*pair[0]
                print('{0}: {1} ({2}) - {3:.2f} ({4:.2f} sigma)'
                      .format(all_data.index(val) + 1,
                              goalie.get_attribute('name'),
                              goalie.get_attribute('team_id'),
                              val,
                              (val-output['mu'])/output['sigma']))
    return output


def get_pair_index(pair_list, key):
    for idx, pair in enumerate(pair_list):
        val = pair[0]
        name = pair[1]
        if name == key:
            return [idx, val]
    raise ValueError('No key ' + key + ' found in list')


def get_sigma_difference(db, player_id, attribute, playform=None):
    if playform is None:
        playform = 'es'

    _filter = {}
    _filter['toi'] = 200
    _filter['position'] = ['F', 'D']
    _filter['team'] = None
    _filter['playform'] = playform

    op = print_sorted_list(db,
                           [attribute],
                           operation=None,
                           _filter=_filter,
                           print_list_length=50,
                           scale_factor=1,
                           high_to_low=True,
                           do_print=False,
                           normalize=False)
    player = db.get_player(player_id)
    player_val = player.get_attribute(attribute, playform)
    return (player_val-op['mu'])/op['sigma']


def get_k_value(x_val, y_val):
    ''' Return k-value between two value vectors '''
    fit = np.polyfit(x_val, y_val, 1)
    fit_fn = np.poly1d(fit)
    k = round(fit[0], 4)
    return fit


def plot_player_cards(ax, axes_info, p_db, player_ids, _filter):
    # Init
    gen_x, gen_y, markers = [], [], []
    output = {}
    output['pair_list'], output['data_list'] = [], []
    ydata_only = False
    tmp_index = 0

    # Set up additional axes information
    if axes_info['x']['attribute'] is None:
        axes_info['fit_data'] = False
        ydata_only = True
        axes_info['x']['label'] = 'Player no.'
        axes_info['x']['invert'] = False

    # Set up color/markers
    colors = ['c', 'm', 'g', 'r', 'b']  # black and yellow are protected colors.
    forms = ['o', 'v', 's', '*', 'x', 'p', 'd']
    for form in forms:
        for color in colors:
            markers.append(str(form + color))

    # Error check
    if len(player_ids) > len(markers):
        warnings.warn('Too many players to plot, text output only')
        do_plots = False
    else:
        do_plots = True
    # Plot all data for league
    for tmp_id in p_db:
        tmp_player = p_db[tmp_id]
        if (tmp_player.get_toi() > _filter['toi']*60) and (tmp_player.get_attribute('position') in _filter['position']):
            if ydata_only is True:
                gen_x.append(tmp_index)
                tmp_index += 1
            else:
                gen_x.append(axes_info['x']['scale']*tmp_player.get_attribute(axes_info['x']['attribute']))
            gen_y.append(axes_info['y']['scale']*tmp_player.get_attribute(axes_info['y']['attribute']))
    plt.scatter(gen_x, gen_y, c='k', marker='.')

    # Add mean value.
    plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')

    # Fit linear model to (scatter) data.
    if axes_info['fit_data'] is True:
        fit = np.polyfit(gen_x, gen_y, 1)
        fit_fn = np.poly1d(fit)
        k = round(fit[0], 4)
        output['fit'] = fit
        output['fit_fn'] = fit_fn
        x_val = range(int(np.min(ax.get_xlim())), int(np.max(ax.get_xlim())))
        plt.plot(x_val, fit_fn(x_val), 'y--',label='Data fit (k=' + str(k) + ')')

    # Add 50% threshold.
    if axes_info['add_threshold'] is True:
        start = int(np.min([np.min(ax.get_xlim()), np.min(ax.get_ylim())]))
        stop = int(np.max([np.max(ax.get_xlim()), np.max(ax.get_ylim())]))
        plt.plot(range(start, stop), range(start, stop), 'k--', label='50% threshold')

    # Plot data for the specified players.
    marker_idx = 0
    for i, player_id in enumerate(player_ids):
        player = p_db[player_id]
        if player.get_toi() < _filter['toi']*60:
            warnings.warn('Player ' + player_id + ' has played less than ' + str(_filter['toi']) + ' minutes even strength (' + str(int(player.get_toi()/60)) + '). Data not included in plot(s).')
        else:
            if player.get_attribute('position') in _filter['position']:
                if do_plots is True:
                    current_marker = markers[marker_idx]
                if (ydata_only is True) and (do_plots is True):
                    plt.scatter(i,
                                axes_info['y']['scale']*player.get_attribute(axes_info['y']['attribute']),
                                c=current_marker[1],
                                marker=current_marker[0],
                                label=player_id)
                else:
                    if axes_info['fit_data'] is True:
                        x_val = axes_info['x']['scale']*player.get_attribute(axes_info['x']['attribute'])
                        y_val = axes_info['y']['scale']*player.get_attribute(axes_info['y']['attribute'])
                        y_est = fit_fn(x_val)
                        y_diff = y_val - y_est
                        output['pair_list'].append((y_diff, player_id))
                        output['data_list'].append(y_diff)
                        if y_diff > 0:
                            sign = '+'
                        else:
                            sign = ''
                        lbl_val_str = ' (' + sign + str(int(100*y_diff/y_est)) + '%)'
                    else:
                        lbl_val_str = ''
                    if do_plots is True:
                        plt.scatter(axes_info['x']['scale']*player.get_attribute(axes_info['x']['attribute']),
                                    axes_info['y']['scale']*player.get_attribute(axes_info['y']['attribute']),
                                    c=current_marker[1],
                                    marker=current_marker[0],
                                    label=player_id+lbl_val_str)
                marker_idx += 1

    # Invert axis for readability.
    if axes_info['x']['invert'] is True:
        ax.invert_xaxis()
    if axes_info['y']['invert'] is True:
        ax.invert_yaxis()

    # Plot stuff
    plt.xlabel(axes_info['x']['label'])
    plt.ylabel(axes_info['y']['label'])
    font_size = np.min([140/len(player_ids), 9])
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)
    plt.subplots_adjust(left=0.05, bottom=0.07, top=0.95, right=0.82, hspace=0.3)
    plt.grid(True)

    output['pair_list'].sort(reverse=True)
    return [plt, ax, output]


def weighted_sum(lst, w_lst):
    op = 0
    if len(lst) != len(w_lst):
        raise ValueError('Incompatible lengths')
    for i, entry in enumerate(lst):
        op += w_lst[i]*entry

    return op


def get_from_distribution(val_dict, attribute, normalize=False):
    sum_value = 1.0
    if attribute == 'isf_per_time':
        index = 0
    elif attribute == 'sh_pcg':
        index = 1
    elif attribute == 'pt_per_time':
        index = 2
    elif attribute == 'pd_per_time':
        index = 3
    elif attribute == 'off_per_time':
        index = 4
    elif attribute == 'def_per_time':
        index = 5
    else:
        raise ValueError('Unknown attribute ' + attribute)
    if normalize is True:
        vals = []
        for p_id in val_dict.keys():
            player_values = val_dict[p_id]
            vals.append(player_values[index])
        sum_value = np.sum(vals)
    while True:
        for p_id in set(val_dict.keys()):  # set for randomizing purposes
            player_values = val_dict[p_id]
            if sum_value == 0:  # special case
                return p_id
            if random.uniform(0, 1) <= (player_values[index]/sum_value):
                return p_id


def acces_gsheet(name_of_ws, credential_path='creds.json'):
    # Open/access g-Sheet
    #name_of_ws = "SharksData_Public"
    credential_path = 'creds.json'          # Old version
    print('Authentication Google Sheet "' + name_of_ws + '"...')
    json_key = json.load(open(credential_path))  # json credentials you downloaded earlier
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)  # get email and key from creds
    g_file = gspread.authorize(credentials) # authenticate with Google
    print('Authentication done')
    print('Opening worksheet...')
    g_wb = g_file.open(name_of_ws)  # Open Google WorkBook
    return g_wb


def get_time_str(time):
    m = time//60
    s = time % 60
    if m < 10:
        m = str('0'+str(m))
    else:
        m = str(m)

    if s < 10:
        s = str('0'+str(s))
    else:
        s = str(s)

    return str(m + ':' + s)


def get_alpha(pos=None):
    # translates column index (1,2,3) to column name ('A','B','C').
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','Z']
    combined_alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','Z']
    for f_letter in alpha:
        for s_letter in alpha:
            combined_alpha.append(f_letter + s_letter)

    if pos is None:
        return combined_alpha
    else:
        return combined_alpha[pos-1]


def get_sorted_db(simulation_param, value_key, cut_off=None, toi_filter=0, position_filter=None, best_first=True):
    """
    Return the cut_off best players in a certain category. Can filter out players based on time-on-ice [minutes]
    """
    lst = []
    split_key = value_key.split('_')
    split_val_key = ''
    for val in split_key[1:]:
        split_val_key += val + '_'
    split_val_key = split_val_key[:-1]
    if position_filter is None:
        position_filter = ['G', 'D', 'F']
    for skater_id in simulation_param['databases']['skater_db'].keys():
        skater = get_skater(simulation_param['databases']['skater_db'], skater_id)
        if (skater.es['toi']/60 >= toi_filter) and (skater.bio['position'] in position_filter):
            if split_key[0] == 'es':
                lst.append((skater.es[split_val_key], skater_id))
            elif split_key[0] == 'on_ice':
                lst.append((skater.on_ice[split_val_key], skater_id))
            else:
                raise ValueError('Unknown split-key "' + value_key.split('_')[0] + '"')
    lst.sort(reverse=best_first)
    if cut_off is None:
        return lst
    else:
        return lst[0:cut_off]


def create_player_list(s_db, _filter):
    list_of_players = []
    for skater_id in s_db.id_set:
        skater = s_db.get_skater(skater_id)
        player_ok = True
        for attribute in _filter:
            if isinstance(_filter[attribute], str) is True:
                if skater.get_attribute(attribute) != _filter[attribute]:
                    player_ok &= False
            elif _filter[attribute] > 0:
                if skater.get_attribute(attribute) < _filter[attribute]:
                    player_ok &= False
            elif _filter[attribute] < 0:
                if skater.get_attribute(attribute) > -1*_filter[attribute]:
                    player_ok &= False

        if player_ok:
            list_of_players.append(skater_id)
    return list_of_players


def get_probability(values, idx=0):
    if isinstance(values, list) is False:
        raise ValueError('Uncompatible types. Input must be a list.')
    else:
        val = values[idx]
        return val/sum(values)


def get_skater_values(skater_db):
    values_dict = defaultdict(list)
    for skater_id in skater_db.id_set:
        skater = skater_db.data[skater_id]
        values_dict['estimated_off_per_60'].append(skater.on_ice['estimated_off_per_60'])
        values_dict['estimated_def_per_60'].append(skater.on_ice['estimated_def_per_60'])
        values_dict['estimated_off_pcg'].append(skater.on_ice['estimated_off_pcg'])
        values_dict['estimated_off_diff'].append(skater.on_ice['estimated_off_diff'])
        values_dict['primary_points_per_60'].append(skater.ind['primary_points_per_60']['es'])
        values_dict['goal_scoring_rating'].append(skater.ind['goal_scoring_rating']['es'])
    return values_dict


def get_team_values(team_db):
    values_dict = defaultdict(list)
    for team_id in ACTIVE_TEAMS:
        team = team_db.data[team_id]
        values_dict['p_pcg'].append(team.p_pcg)
        values_dict['gf_pcg'].append(team.gf_pcg)
        values_dict['sf_pcg'].append(team.sf_pcg)
        values_dict['cf_pcg'].append(team.cf_pcg)
        values_dict['ff_pcg'].append(team.ff_pcg)
        values_dict['xgf_pcg'].append(team.xgf_pcg)
        values_dict['scf_pcg'].append(team.scf_pcg)
        values_dict['hdcf_pcg'].append(team.hdcf_pcg)
        values_dict['sv_pcg'].append(team.sv_pcg)
        values_dict['pdo'].append(team.pdo)
        for key in team.exp_data:
            values_dict[key].append(team.exp_data[key])

        # values_dict['hits'].append(team.exp_data['hits'])
        # values_dict['hits_taken'].append(team.exp_data['hits_taken'])
        # values_dict['hits_diff'].append(team.exp_data['hits_diff'])
        # values_dict['estimated_off_pcg'].append(team.exp_data['estimated_off_pcg'])
        # values_dict['in_season_rating'].append(team.exp_data['in_season_rating'])
    return values_dict


def get_rank(value, lst):
    '''
    Returns the rank of the value in the list
    '''
    lst.sort(reverse=False)
    rank = 1
    for lst_val in lst:
        if lst_val == value:
            return rank
        rank += 1
    if rank > len(lst):
        raise ValueError('Could not find value ' + str(value) + ' in the list.')


def generate_fatigue_factors(csv_path='Data/nhl_result_from_2018.csv'):
    fatigue_factors = {}
    for team_id in ACTIVE_TEAMS:
        team = get_long_name(team_id)
        fatigue_factors[team_id] = {}
        op_days = {}
        op_days[0], op_days[1], op_days[2] = defaultdict(int), defaultdict(int), defaultdict(int)
        op_all = defaultdict(int)
        all_gf, all_ga, all_p, all_p_total = 0, 0, 0, 0
        ht_gf_idx = 2
        at_gf_idx = 4
        ot_idx = 5
        prev_date = -1
        with open(csv_path, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[1] != 'Date':
                    ht = row[1]
                    at = row[3]
                    if (ht == team) or (at == team):
                        if team == ht:
                            gf = int(row[ht_gf_idx])
                            ga = int(row[at_gf_idx])
                        else:
                            gf = int(row[at_gf_idx])
                            ga = int(row[ht_gf_idx])
                        this_date = row[0]
                        if prev_date != -1:
                            days_since_last_game = get_delta_days(prev_date, this_date) - 1
                            if days_since_last_game >= 2:
                                days_since_last_game = 2
                            if gf > ga:
                                p = 2
                            elif row[ot_idx] != '':
                                p = 1
                            else:
                                p = 0
                            op_days[days_since_last_game]['games_played'] += 1
                            op_days[days_since_last_game]['goals'] += gf
                            op_days[days_since_last_game]['ga'] += ga
                            op_days[days_since_last_game]['p'] += p
                            op_days[days_since_last_game]['p_total'] += 2
                            op_all['goals'] += gf
                            op_all['ga'] += ga
                            op_all['p'] += p
                            op_all['p_total'] += 2
                        prev_date = this_date

        total_gf_pcg = get_probability([op_all['goals'], op_all['ga']])
        total_p_pcg = op_all['p']/op_all['p_total']
        for i in range(3):
            days_gf_pcg = get_probability([op_days[i]['goals'], op_days[i]['ga']])
            days_p_pcg = op_days[i]['p']/op_days[i]['p_total']
            op_days[i]['gf_pcg'] = days_gf_pcg
            op_days[i]['gf_pcg_rel'] = days_gf_pcg/total_gf_pcg
            op_days[i]['p_pcg'] = days_p_pcg
            op_days[i]['p_pcg_rel'] = days_p_pcg/total_p_pcg
        fatigue_factors[team_id]['per_days_rested'] = op_days
        fatigue_factors[team_id]['total'] = op_all
    return fatigue_factors


def get_fatigue_factor(fatigue_factors, team_id, days_rested=-1):
    if days_rested == -1:
        return fatigue_factors[team_id]
    else:
        if days_rested > 2:
            warnings.warn('2 days of rest is maximum. Returning fatigue factor for 2 rest days (' + str(days_rested) + ' selected).')
            days_rested = 2
        return fatigue_factors[team_id]['per_days_rested'][days_rested]['p_pcg_rel']


def generate_starting_goalies():
    starting_goalies_dict = generate_all_teams_dict(return_type=None)
    return starting_goalies_dict


def handler(signum, frame):
    raise Exception("Connection timed out")

def get_k_factor(x_array, y_array, do_plot=False):
    fit = np.polyfit(x_array, y_array, 1)
    fit_fn = np.poly1d(fit)
    k = round(fit[0], 4)
    if do_plot is True:
        plt.figure(1)
        x_val = np.linspace(1, 31, 31)
        plt.scatter(x_array, y_array, c='k', marker='.')
        plt.plot(x_val, fit_fn(x_val), 'y--', label='Data fit (k=' + str(k) + ')')
        plt.show()
    return k


def backup_data_dir(src, dst):
    '''
    Backup all csv-files from the source folder to the destination folder
    '''
    list_of_all = os.listdir(src)
    for filename in list_of_all:
        filepath = os.path.join(src, filename)
        if os.path.splitext(filepath)[1] == '.csv':
            copyfile(filepath, os.path.join(dst, filename))


def generic_csv_reader(csv_file_path, dict_key_attribute='name', output_attributes=False):
    '''
    Assuming first line is the headers.
    Returns an dict with accoridng to input dict_key;
        output[dict_key] = {}
        output[dict_key][header_1] = value_1
        output[dict_key][header_2] = value_2
        ...
        output[dict_key][header_n] = value_n
    '''
    output = {}
    attributes = []
    with open(csv_file_path, 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        first_row = True
        for row in reader:
            if first_row is True:
                first_row = False
                # Extract headers
                '''
                for value in row:
                    attributes.append(str(value).lower())
                '''
                attributes = row
                if output_attributes is True:
                    output['attributes'] = attributes
                if dict_key_attribute not in attributes:
                    raise ValueError('Could not find dictionary key "' + dict_key_attribute + '" in attributes: ' + str(attributes))
                dict_key_index = attributes.index(dict_key_attribute)
            else:
                # Add data to dict
                dict_key = row[dict_key_index]
                output[dict_key] = {}
                for i, value in enumerate(row):
                    attribute = attributes[i]
                    output[dict_key][attribute] = value
    return output


def clean_string(input_string):
    ''' Clean up string, to use as attribute name '''
    input_string = input_string.replace(' ','_')
    input_string = input_string.replace('%','percent')
    input_string = input_string.strip('.-')
    return input_string.lower()
