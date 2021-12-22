import copy
import datetime
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import platform
from scipy import stats
import time

from nhl_database import *
#from nhl_simulation import set_starting_goalie, create_game_specific_db, simulate_po_series, get_playoff_cut, create_tables
from nhl_helpers import *
from nhl_entities import Skater, Goalie, Team
from nhl_settings import Settings
from nhl_defines import *
from nhl_web_scrape import *
from nhl_simulation import Simulation, GameSimulatuion, SeasonSimulation


def simulate_individual_games(simulation_param):
    if simulation_param['simulation_mode'] is None:
        simulation_param['simulation_mode'] = DEFINES['SIMULATION_EXT']

    N_sim = simulation_param['N'][simulation_param['simulation_mode']]
    for i, game in enumerate(simulation_param['games_to_simulate']):
        t0 = 1000*time.time()
        simulation_param['ht_id'] = game[0]
        simulation_param['at_id'] = game[1]
        in_game_data = create_game_specific_db(simulation_param)
        print('\n\nSimulating outcome of ' + simulation_param['ht_id'] +
              ' (HOME) vs. ' + simulation_param['at_id'] +
              ' (AWAY). Number of simulations = ' +
              str(N_sim) + '. Simulation model = ' + str(simulation_param['simulation_mode']))
        print('GOALIE ({0}): {1} (SV: {2:.1f}%, GAA: {3:.2f})'.format(
            simulation_param['ht_id'],
            in_game_data['ht_goalie'],
            100*simulation_param['databases']['goalie_db'][in_game_data['ht_goalie']].ind['sv_pcg']['es'],
            simulation_param['databases']['goalie_db'][in_game_data['ht_goalie']].ind['gaa']['es']))
        print('GOALIE ({0}): {1} (SV: {2:.1f}%, GAA: {3:.2f})'.format(
            simulation_param['at_id'],
            in_game_data['at_goalie'],
            100*simulation_param['databases']['goalie_db'][in_game_data['at_goalie']].ind['sv_pcg']['es'],
            simulation_param['databases']['goalie_db'][in_game_data['at_goalie']].ind['gaa']['es']))
        if simulation_param['verbose']:
            for ct in DEFINES['CURRENT_TEAM']:
                # Print roster information
                print('\n' + simulation_param[ct + '_id'] + ' roster:')
                _fwd, _def, _unav = [], [], []
                for p_id in in_game_data[ct + '_skaters'].keys():
                    if simulation_param['databases']['skater_db'][p_id].bio['position'] == 'D':
                        _def.append(p_id)
                    else:
                        _fwd.append(p_id)
                for p_id in simulation_param['databases']['unavailable_players']:
                    if p_id in simulation_param['databases']['skater_db'].keys():
                        if simulation_param['databases']['skater_db'][p_id].bio['team_id'] == simulation_param[ct + '_id']:
                            _unav.append(p_id)
                    elif p_id in simulation_param['databases']['goalie_db'].keys():
                        if simulation_param['databases']['goalie_db'][p_id].bio['team_id'] == simulation_param[ct + '_id']:
                            _unav.append(p_id)
                    else:
                        raise ValueError('Player ' + p_id + ' neither Skater nor Goalie.')
                print('DEF:    ' + str(_def))
                print('FWD:    ' + str(_fwd))
                print('UNAVAILABLE:    ' + str(_unav))

        # Set up simulation output parameters
        ht_g, at_g, ht_s, at_s, ht_g_prev_batch, at_g_prev_batch = 0, 0, 0, 0, 0, 0
        ht_exp_s, at_exp_s = 0, 0
        ht_w_t0, at_w_t0 = simulation_param['databases']['team_db'][simulation_param['ht_id']].wins, simulation_param['databases']['team_db'][simulation_param['at_id']].wins
        ht_w_prev_batch, at_w_prev_batch = 0, 0
        batch_g_prob = []
        batch_w_prob = []
        t0_tmp = time.time()
        step_size = 10
        for k in range(N_sim):
            if print_progress(k, N_sim, t0_tmp, step_size):
                ht_g_batch = ht_g - ht_g_prev_batch
                at_g_batch = at_g - at_g_prev_batch
                ht_w_batch = ht_w - ht_w_prev_batch
                at_w_batch = at_w - at_w_prev_batch
                ht_g_batch_prob = (ht_g_batch/(ht_g_batch+at_g_batch))
                ht_w_batch_prob = (ht_w_batch/(ht_w_batch+at_w_batch))
                batch_g_prob.append(ht_g_batch_prob)
                batch_w_prob.append(ht_w_batch_prob)
                if simulation_param['verbose']:
                    print('  Probability (batch - goals): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],
                          100*ht_g_batch_prob, 100*(1 - ht_g_batch_prob), simulation_param['at_id']))
                    print('  Probability (total - goals): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],
                          100*(ht_g/(ht_g+at_g)), 100*(1 - (ht_g/(ht_g+at_g))), simulation_param['at_id']))
                    print('  Probability (batch - wins): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],
                          100*ht_w_batch_prob, 100*(1 - ht_w_batch_prob), simulation_param['at_id']))
                    print('  Probability (total - wins): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],
                          100*(ht_w/(ht_w+at_w)), 100*(1 - (ht_w/(ht_w+at_w))), simulation_param['at_id']))
                ht_g_prev_batch = ht_g
                at_g_prev_batch = at_g
                ht_w_prev_batch = ht_w
                at_w_prev_batch = at_w
            # Simulate the game
            in_game_data['ht'].simulate_game(in_game_data['at'], simulation_param, in_game_data)

            # Store output, for summary reasons.
            ht_g += in_game_data['ht'].gf_in_simulated_game
            at_g += in_game_data['at'].gf_in_simulated_game
            ht_s += in_game_data['ht'].sf_in_simulated_game
            at_s += in_game_data['at'].sf_in_simulated_game

            ht_exp_s += in_game_data['ht'].exp_data['team_sf_in_simulated_game']
            at_exp_s += in_game_data['at'].exp_data['team_sf_in_simulated_game']

            ht_w = simulation_param['databases']['team_db'][simulation_param['ht_id']].wins - ht_w_t0
            at_w = simulation_param['databases']['team_db'][simulation_param['at_id']].wins - at_w_t0

        if simulation_param['verbose']:
            mu_g = np.mean(batch_g_prob)
            sig_g = np.std(batch_g_prob)
            print('\nMean value and standard deviation (ht goals) for batch-size ' +
                  str(N_sim/step_size) + ': ' + str(mu_g) + ', ' + str(sig_g))
            print('   Upper threshold ht goals (3-sigma): ' + str(mu_g+3*sig_g))
            print('   Lower threshold ht goals (3-sigma): ' + str(mu_g-3*sig_g))
            mu_w = np.mean(batch_w_prob)
            sig_w = np.std(batch_w_prob)
            print('Mean value and standard deviation (ht wins) for batch-size ' +
                  str(N_sim/step_size) + ': ' + str(mu_w) + ', ' + str(sig_w))
            print('   Upper threshold ht win (3-sigma): ' + str(mu_w+3*sig_w))
            print('   Lower threshold ht win (3-sigma): ' + str(mu_w-3*sig_w))

        # Print simulation output
        if simulation_param['simulation_date'] is None:
            ht_fatigue_factor = 1
            at_fatigue_factor = 1
        else:
            ht_team = simulation_param['databases']['team_db'][simulation_param['ht_id']]
            at_team = simulation_param['databases']['team_db'][simulation_param['at_id']]
            ht_days_rested = get_days_rested(simulation_param['ht_id'], simulation_param)
            at_days_rested = get_days_rested(simulation_param['at_id'], simulation_param)
            if ht_days_rested > 2:
                ht_days_rested = 2
            if at_days_rested > 2:
                at_days_rested = 2
            ht_fatigue_factor = ht_team.fatigue['per_days_rested'][ht_days_rested]['p_pcg_rel']
            at_fatigue_factor = at_team.fatigue['per_days_rested'][at_days_rested]['p_pcg_rel']

        ht_g_prob = ht_g/(ht_g+at_g)
        at_g_prob = at_g/(ht_g+at_g)
        print('\nProbability (goals):  {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'], 100*ht_g_prob, 100*at_g_prob, simulation_param['at_id']))
        ht_g_venue = ht_g * get_home_team_advantage(simulation_param['databases']['team_db'], simulation_param['ht_id'], simulation_param['at_id'])
        at_g_venue = at_g
        ht_g_prob_venue = ht_g_venue/(ht_g_venue+at_g_venue)
        at_g_prob_venue = at_g_venue/(ht_g_venue+at_g_venue)
        print('Probability (goals, venue adjusted):  {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'], 100*ht_g_prob_venue, 100*at_g_prob_venue, simulation_param['at_id']))
        ht_g_venue_and_fatigue = ht_g_venue * ht_fatigue_factor
        at_g_venue_and_fatigue = at_g_venue * at_fatigue_factor
        ht_g_prob_venue_and_fatigue = ht_g_venue_and_fatigue/(ht_g_venue_and_fatigue+at_g_venue_and_fatigue)
        at_g_prob_venue_and_fatigue = at_g_venue_and_fatigue/(ht_g_venue_and_fatigue+at_g_venue_and_fatigue)
        print('Probability (goals, venue and fatigue adjusted):  {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'], 100*ht_g_prob_venue_and_fatigue, 100*at_g_prob_venue_and_fatigue, simulation_param['at_id']))
        print('   Average score: {0} {1:.2f} - {2:.2f} {3}'.format(simulation_param['ht_id'], ht_g/N_sim, at_g/N_sim, simulation_param['at_id']))
        if simulation_param['simulation_mode'] == DEFINES['SIMULATION_EXT']:
            #print('   Average shots: {0} {1:.0f} - {2:.0f} {3}'.format(simulation_param['ht_id'],ht_s/N_sim,at_s/N_sim,simulation_param['at_id']))
            print('   Average shots EXP: {0} {1:.0f} - {2:.0f} {3}'.format(simulation_param['ht_id'], ht_exp_s/N_sim, at_exp_s/N_sim, simulation_param['at_id']))

        ht_rating = simulation_param['databases']['team_db'][simulation_param['ht_id']].exp_data['in_season_rating']
        at_rating = simulation_param['databases']['team_db'][simulation_param['at_id']].exp_data['in_season_rating']
        ht_rating_prob = ht_rating/(ht_rating+at_rating)
        at_rating_prob = at_rating/(ht_rating+at_rating)
        print('Probability (rating): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'], 100*ht_rating_prob, 100*at_rating_prob, simulation_param['at_id']))
        ht_rating_venue = ht_rating * get_home_team_advantage(simulation_param['databases']['team_db'], simulation_param['ht_id'], simulation_param['at_id'])
        at_rating_venue = at_rating
        ht_rating_prob_venue = ht_rating_venue/(ht_rating_venue+at_rating_venue)
        at_rating_prob_venue = at_rating_venue/(ht_rating_venue+at_rating_venue)
        print('Probability (rating, venue adjusted): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'], 100*ht_rating_prob_venue, 100*at_rating_prob_venue, simulation_param['at_id']))
        ht_rating_venue_and_fatigue = ht_rating_venue * ht_fatigue_factor
        at_rating_venue_and_fatigue = at_rating_venue * at_fatigue_factor
        ht_rating_prob_venue_and_fatigue = ht_rating_venue_and_fatigue /\
            (ht_rating_venue_and_fatigue+at_rating_venue_and_fatigue)
        at_rating_prob_venue_and_fatigue = at_rating_venue_and_fatigue /\
            (ht_rating_venue_and_fatigue+at_rating_venue_and_fatigue)
        print('Probability (rating, venue and fatigue adjusted): {0} {1:.1f}% - {2:.1f}% {3}'
              .format(simulation_param['ht_id'],
                      100*ht_rating_prob_venue_and_fatigue,
                      100*at_rating_prob_venue_and_fatigue,
                      simulation_param['at_id']))

        if (simulation_param['initial_time'] > 0) or ((simulation_param['initial_ht_goals'] + simulation_param['initial_at_goals']) > 0):
            print('Probability (wins): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'], 100*get_probability([ht_w,at_w]),100*get_probability([at_w,ht_w]),simulation_param['at_id']))

        # Timing
        t_end = 1000*time.time()
        t_tot = t_end-t0
        if simulation_param['print_times']:
            print('Total time: ' + str(t_tot) + ' ms.')
            print('Average time per game simulation: ' + str(t_tot/N_sim) + ' ms.')
            print('Total time (N = 1000): ' + str((1000/N_sim)*(t_tot)*(1/1000)) + ' s.')
            print('Total time (N = 5000): ' + str((5000/N_sim)*(t_tot)*(1/1000)) + ' s.')
            print('Total time (N = 10000): ' + str((10000/N_sim)*(t_tot)*(1/1000)) + ' s.')
            print('Total time, one round (N = 10000): ' + str(15.5*(10000/N_sim)*(t_tot)*(1/(1000*60))) + ' min.')
            print('Total time, one season (N = 1): ' + str(82*15.5*(1/N_sim)*(t_tot)*(1/(1000*60))) + ' min.')
            print('Total time, one season (N = 10000): ' + str(82*15.5*(10000/N_sim)*(t_tot)*(1/(1000*3600))) + ' h.')


def simulate_season(simulation_param):
    if simulation_param['simulation_mode'] is None:
        simulation_param['simulation_mode'] = DEFINES['SIMULATION_LIGHT']

    N_sim = simulation_param['N'][simulation_param['simulation_mode']]
    # Update simulation parameters to fit "season simulation"
    simulation_param['initial_time'] = 0
    simulation_param['initial_ht_goals'] = 0
    simulation_param['initial_at_goals'] = 0
    simulation_param['print_times'] = False
    simulation_param['verbose'] = False

    t_0 = 1000*time.time()
    po_dict = defaultdict(int)
    po_dict_points = defaultdict(int)
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
    print('Simulating regular season, per ' + str(datetime.datetime.today().strftime('%Y-%m-%d')) + '. N = ' + str(N_sim))
    t0_tmp = time.time()

    for i in range(N_sim):
        print_progress(i, N_sim, t0_tmp, step=5)

        team_db = copy.deepcopy(simulation_param['databases']['team_db'])

        # Setup schedule.
        if simulation_param['offseason'] is True:
            for team_id in DEFINES['ACTIVE_TEAMS']:
                team = get_team(team_db, team_id)
                team.reset_schedule(simulation_param)

        # Simulate rest of the season.
        for team_id in DEFINES['ACTIVE_TEAMS']:
            team = get_team(team_db, team_id)
            if simulation_param['simulation_mode'] == DEFINES['SIMULATION_LIGHT']:
                for opponent_id in team.remaining_schedule:
                    opponent = get_team(team_db, opponent_id)
                    team.simulate_game_in_season(opponent, simulation_param)
            else:
                for opponent_id in team.remaining_schedule:
                    opponent = get_team(team_db, opponent_id)
                    simulation_param['ht_id'] = team_id
                    simulation_param['at_id'] = opponent_id
                    in_game_data = create_game_specific_db(simulation_param)
                    team.simulate_game_in_season(opponent, simulation_param, in_game_data)

        # For all teams, see if the team made the playoff or not
        [poc_east, poc_west] = get_playoff_cut(team_db)
        for team_id in DEFINES['ACTIVE_TEAMS']:
            team = get_team(team_db, team_id)
            if team.conference == 'W':
                poc = poc_west
            else:
                poc = poc_east
            if team.p >= poc:
                simulation_param['databases']['team_db'][team_id].exp_data['total_made_playoffs'] += 1
            simulation_param['databases']['team_db'][team_id].exp_data['total_simulated_points'] += team.p

    # Print results from simulation
    print('\nRegular season summary:')
    # Writing to Google documents
    if simulation_param['write_to_gsheet']:
        g_wb = acces_gsheet('SharksData_Public',credential_path='creds.json')
        output_sheet = g_wb.worksheet("TEST_TEAM")
        start_row = (output_sheet.find("INDEX").row)+1
        teams_col = output_sheet.find("NAME").col
        headers_list = output_sheet.row_values(output_sheet.find("INDEX").row)
        correct_col = get_alpha(len(headers_list))
        teams = output_sheet.col_values(teams_col)
        teams = teams[1:1+len(DEFINES['ACTIVE_TEAMS'])]
        pcg_value = len(DEFINES['ACTIVE_TEAMS']) * [0]

    for team_id in DEFINES['ACTIVE_TEAMS']:
        team = get_team(simulation_param['databases']['team_db'], team_id)
        team.exp_data['mean_made_playoffs'] = team.exp_data['total_made_playoffs']/N_sim
        team.exp_data['mean_simulated_points'] = team.exp_data['total_simulated_points']/N_sim
        print('{0} - {1:.1f}%. Projected points: {2:.1f}.'
              .format(team_id, 100*team.exp_data['mean_made_playoffs'], team.exp_data['mean_simulated_points']))
        if simulation_param['write_to_gsheet']:
            pcg_value[output_sheet.find(get_long_name(team_id)).row-2] = 100*team.exp_data['mean_made_playoffs']

    [poc_east, poc_west] = get_playoff_cut(simulation_param['databases']['team_db'], use_simulated_points=True)

    if simulation_param['write_to_gsheet']:
        output_sheet.update_acell(str(correct_col + '1'), str(today))
        data_range = str(correct_col + '2:' + correct_col + '32')
        cell_list = output_sheet.range(data_range)
        for i, cell in enumerate(cell_list):
            cell.value = pcg_value[i]
        # Update in batch
        output_sheet.update_cells(cell_list)

    print('Projected points:')
    tl_a = create_tables(simulation_param['databases']['team_db'], 'atlantic',
                         print_to_cmd=True,
                         store=True,
                         use_simulated_points=True)
    tl_m = create_tables(simulation_param['databases']['team_db'], 'metro',
                         print_to_cmd=True,
                         store=True,
                         use_simulated_points=True)
    tl_c = create_tables(simulation_param['databases']['team_db'], 'central',
                         print_to_cmd=True,
                         store=True,
                         use_simulated_points=True)
    tl_p = create_tables(simulation_param['databases']['team_db'], 'pacific',
                         print_to_cmd=True,
                         store=True,
                         use_simulated_points=True)

    print('Playoff cutoffs [east, west]: [{0:.1f}, {1:.1f}]'.format(poc_east, poc_west))
    t_tot = 1000*time.time()-t_0
    if simulation_param['print_times']:
        print('Total time: ' + str(t_tot/1000) + ' s.')
        print('Total time per computation: ' + str((1/N_sim)*(t_tot/1000)) + ' s.')
        print('Total time for computation (N=100): ' + str((100/N_sim)*(t_tot/(3600*1000))) + ' h.')
        print('Total time for computation (N=500): ' + str((500/N_sim)*(t_tot/(3600*1000))) + ' h.')
        print('Total time for computation (N=1000): ' + str((1000/N_sim)*(t_tot/(3600*1000))) + ' h.')
        print('Total time for computation (N=5000): ' + str((5000/N_sim)*(t_tot/(3600*1000))) + ' h.')
        print('Total time for computation (N=10000): ' + str((10000/N_sim)*(t_tot/(3600*1000))) + ' h.')


def do_player_cards(simulation_param):
    s_db = simulation_param['databases']['skater_db']
    g_db = simulation_param['databases']['goalie_db']

    # Decide which players should be on the report cards.
    pl_high = []
    _filter = {}
    _filter['list_length'] = simulation_param['exp_list_length']
    _filter['toi'] = simulation_param['exp_min_toi']
    _filter['team'] = simulation_param['exp_team']
    if _filter['team'] is None:
        _filter['team'] = []
    _filter['position'] = simulation_param['exp_position']
    player_ids = []
    for sid in s_db.keys():
        if s_db[sid].bio['team_id'] in _filter['team'] and s_db[sid].bio['position'] in _filter['position']:
            player_ids.append(sid)

    for player_id in simulation_param['exp_additional_players']:
        player_ids.append(player_id)

    if simulation_param['exp_show_player_ranking']:
        pl_high = player_ids
        player_ids = list(s_db.keys())

    _filter['ws'] = simulation_param['exp_weighted_scale']

    figure_index = 1
    axes_info = {}
    axes_info['x'] = {}
    axes_info['y'] = {}

    if player_ids[0] in s_db.keys():
        do_skater_plots = True
    else:
        do_skater_plots = False

    if do_skater_plots is True:
        print('\nPlotting data according to: ')
        print('   Team: ' + str(simulation_param['exp_team']))
        print('   Position: ' + str(simulation_param['exp_position']))
        print('   Players: ' + str(simulation_param['exp_additional_players']))
        print('   Weighted scale: ' + str(simulation_param['exp_weighted_scale']) + '\n')

        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 2
        n_cols = 1
        # Play driving abilities.
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = True
        axes_info['x']['attribute'] = 'estimated_off_per_sec'
        axes_info['x']['label'] = 'Offensive threat per 60'
        axes_info['x']['scale'] = 3600
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'estimated_def_per_sec'
        axes_info['y']['label'] = 'Defensive threat per 60'
        axes_info['y']['scale'] = 3600
        axes_info['y']['invert'] = True
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index), axes_info, s_db, player_ids, _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Play driving')
        sub_plot_index += 1
        # Play driving abilities, based on zone deployment.
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = False
        axes_info['y']['attribute'] = 'estimated_off_pcg'
        axes_info['y']['label'] = '"Play control" [%]'
        axes_info['y']['scale'] = 100
        axes_info['y']['invert'] = False
        axes_info['x']['attribute'] = 'dz_pcg'
        axes_info['x']['label'] = 'Defensive zone deployment [%]'  # off-k = 0.2348
        axes_info['x']['scale'] = 100
        axes_info['x']['invert'] = True
        [plt, ax, op] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index), axes_info, s_db, player_ids, _filter)
        ll = 1
        print('Play driving w. zone deployment. Number of players = ' + str(len(op['pair_list'])))
        for pair in op['pair_list']:
            # Normalize data
            norm_value = pair[0]
            norm_value -= np.min(op['data_list'])
            norm_value /= (np.max(op['data_list']) - np.min(op['data_list']))
            if (ll <= _filter['list_length']) or (pair[1] in pl_high):
                print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(norm_value))
            ll += 1
            s_db[pair[1]].rating.append(norm_value)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Play driving w. zone deployment')
        sub_plot_index += 1
        figure_index += 1
        ###############################################################################################################
        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 2
        n_cols = 1
        # Points, based on zone deployment
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = False
        axes_info['y']['attribute'] = 'points_per_60'
        axes_info['y']['label'] = 'Points per 60'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        axes_info['x']['attribute'] = 'oz_pcg'
        axes_info['x']['label'] = 'Offensive zone deployment [%]'
        axes_info['x']['scale'] = 100
        axes_info['x']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': All points w. zone deployment')
        sub_plot_index += 1
        # Points, based on zone deployment
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = False
        axes_info['y']['attribute'] = 'primary_points_per_60'
        axes_info['y']['label'] = 'Primary points per 60'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        axes_info['x']['attribute'] = 'oz_pcg'
        axes_info['x']['label'] = 'Offensive zone deployment [%]'
        axes_info['x']['scale'] = 100
        axes_info['x']['invert'] = False
        [plt, ax, op] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Primary points w. zone deployment')
        ll = 1
        print('Primary points per 60 w. zone deployment. Number of players = ' + str(len(op['pair_list'])))
        for pair in op['pair_list']:
            # Normalize data
            norm_value = pair[0]
            norm_value -= np.min(op['data_list'])
            norm_value /= (np.max(op['data_list']) - np.min(op['data_list']))
            if (ll <= _filter['list_length']) or (pair[1] in pl_high):
                print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(pair[0]))
            ll += 1
            s_db[pair[1]].rating.append(norm_value)
        sub_plot_index += 1
        figure_index += 1
        ###############################################################################################################
        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 2
        n_cols = 1
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = True
        axes_info['x']['attribute'] = 'ixgf'
        axes_info['x']['label'] = 'Individual expected goals'
        axes_info['x']['scale'] = 1
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'goals'
        axes_info['y']['label'] = 'Goals scored'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, op] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Goals vs. xG')
        ll = 1
        print('Goals scored above expected. Number of players = ' + str(len(op['pair_list'])))
        for pair in op['pair_list']:
            # Normalize data
            norm_value = pair[0]
            norm_value -= np.min(op['data_list'])
            norm_value /= (np.max(op['data_list']) - np.min(op['data_list']))
            if (ll <= _filter['list_length']) or (pair[1] in pl_high):
                print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(pair[0]))
            ll += 1
            s_db[pair[1]].rating.append(norm_value)
        sub_plot_index += 1
        # Goals above/below average
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = None
        axes_info['y']['attribute'] = 'gf_above_xgf'
        axes_info['y']['label'] = 'Goals above expected'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': GF vs xGF')
        sub_plot_index += 1
        figure_index += 1
        ################################################################################################################
        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 3
        n_cols = 1
        # Shot quality
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'isf_per_sec'
        axes_info['x']['label'] = 'Shoots taken per 60'
        axes_info['x']['scale'] = 3600
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'ish_pcg'
        axes_info['y']['label'] = 'Shooting success [%]'
        axes_info['y']['scale'] = 100
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)

        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Shot quality')
        sub_plot_index += 1
        # Corsi quality
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'icf_per_60'
        axes_info['x']['label'] = 'Indivicual CF per 60'
        axes_info['x']['scale'] = 1
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'icf_pcg'
        axes_info['y']['label'] = 'Corsi-shooting success [%]'
        axes_info['y']['scale'] = 100
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Corsi quality')
        sub_plot_index += 1
        # Corsi vs. shot
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'icf_per_60'
        axes_info['x']['label'] = 'Indivicual CF per 60'
        axes_info['x']['scale'] = 1
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'isf_per_60'
        axes_info['y']['label'] = 'Individual SF per 60'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Shot efficency')
        sub_plot_index += 1
        figure_index += 1
        ###############################################################################################################
        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 2
        n_cols = 1
        # Zone deployment, 1
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = True
        axes_info['x']['attribute'] = 'oz_pcg'
        axes_info['x']['label'] = 'Offensive zone deployment [%]'
        axes_info['x']['scale'] = 100
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'dz_pcg'
        axes_info['y']['label'] = 'Defensive zone deployment [%]'
        axes_info['y']['scale'] = 100
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Zone deployment')
        sub_plot_index += 1
        # Zone deployment, 2
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = None
        axes_info['y']['attribute'] = 'avg_zone_start'
        axes_info['y']['label'] = 'Average zone start (-1=DZ, 0=NZ, +1=OZ)'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Average zone start position')
        sub_plot_index += 1
        figure_index += 1
        ###############################################################################################################
        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 2
        n_cols = 1
        # ?
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'estimated_off_pcg'
        axes_info['x']['label'] = '"Play control" [%]'
        axes_info['x']['scale'] = 100
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'primary_points_per_60'
        axes_info['y']['label'] = 'Primary points per 60'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': ?')
        sub_plot_index += 1
        # Points quality
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'points'
        axes_info['x']['label'] = 'Total points'
        axes_info['x']['scale'] = 1
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'part_primary'
        axes_info['y']['label'] = 'Primary points quota [%]'
        axes_info['y']['scale'] = 100
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Part of points being primary')
        sub_plot_index += 1
        figure_index += 1
        ###############################################################################################################
        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 2
        n_cols = 1
        # ?
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'total_draft_pos'
        axes_info['x']['label'] = '"Draft position'
        axes_info['x']['scale'] = 1
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'primary_points_per_60'
        axes_info['y']['label'] = 'Primary points per 60'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Points vs. total draft position')
        sub_plot_index += 1
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = True
        axes_info['x']['attribute'] = 'pd_per_60'
        axes_info['x']['label'] = 'Penalties drawn per 60'
        axes_info['x']['scale'] = 1
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'pt_per_60'
        axes_info['y']['label'] = 'Penalties taken per 60'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = True
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Points vs. draft round')
        sub_plot_index += 1
        figure_index += 1
        ###############################################################################################################
    else:
        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 2
        n_cols = 1
        # GSAA
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'sa_per_sec'
        axes_info['x']['label'] = 'Shoots against per 60'
        axes_info['x']['scale'] = 3600
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'gsaa_per_60'
        axes_info['y']['label'] = 'Goals saved above average per 60'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Test 1')
        sub_plot_index += 1
        # Play driving abilities, based on zone deployment.
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'sa_per_sec'
        axes_info['x']['label'] = 'Shoots against per 60'
        axes_info['x']['scale'] = 3600
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'gaa'
        axes_info['y']['label'] = 'Goals against average'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = True
        [plt, ax, op] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Test 2')
        sub_plot_index += 1
        figure_index += 1
        ###############################################################################################################
        plt.figure(figure_index)
        sub_plot_index = 1
        n_rows = 2
        n_cols = 1
        # Play driving abilities.
        axes_info['fit_data'] = True
        axes_info['add_threshold'] = True
        axes_info['x']['attribute'] = 'xga'
        axes_info['x']['label'] = 'xGA'
        axes_info['x']['scale'] = 1
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'ga'
        axes_info['y']['label'] = 'Goals against'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, __] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Goals against vs. xGA')
        sub_plot_index += 1
        # Play driving abilities, based on zone deployment.
        axes_info['fit_data'] = False
        axes_info['add_threshold'] = False
        axes_info['x']['attribute'] = 'gaa'
        axes_info['x']['label'] = 'Goals aginst average'
        axes_info['x']['scale'] = 1
        axes_info['x']['invert'] = False
        axes_info['y']['attribute'] = 'gsaa_per_60'
        axes_info['y']['label'] = 'Goals saved against average per 60'
        axes_info['y']['scale'] = 1
        axes_info['y']['invert'] = False
        [plt, ax, op] = plot_player_cards(plt.subplot(n_rows, n_cols, sub_plot_index),
                                          axes_info,
                                          s_db,
                                          player_ids,
                                          _filter)
        plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': GAA vs GSAA_60')
        sub_plot_index += 1
        figure_index += 1
    # Show figure
    plt.show()

    # Print total rating.
    values, op_l = [], []
    print('TOTAL RATING:')
    counter = 1
    for player_id in player_ids:
        if s_db[player_id].ind['toi']['es'] > _filter['toi']*60 and s_db[player_id].bio['position'] in _filter['position']:
            total_value = weighted_sum(s_db[player_id].rating, _filter['ws'])
            op_l.append((total_value, player_id))
            counter += 1
    op_l.sort(reverse=True)
    ll = 1
    for pair in op_l:
        if (ll <= _filter['list_length']) or (pair[1] in pl_high):
            value = pair[0]/sum(_filter['ws'])
            print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(value))
            if pair[1] in pl_high:
                values.append(value)
        ll += 1
    print('Total number of players: ' + str(counter))
    print('Average value for player highlighted: ' + str(np.mean(values)))


def perform_player_analysis(player):
    s_db = simulation_param['databases']['skater_db']
    g_db = simulation_param['databases']['goalie_db']
    t_db = simulation_param['databases']['team_db']
    f_add = lambda a, b: a+b
    f_sub = lambda a, b: a-b
    f_mult = lambda a, b: a*b
    f_div = lambda a, b: a/b

    print('Analysis based on zone deployment')
    zone_deployment, performance = [], []
    deployment_metric = 'oz_pcg'
    performance_metric = 'xgf_pcg'
    for p_id in DEFINES['ACTIVE_SKATERS']:
        player = s_db[p_id]
        if player.get_attribute('toi') >= simulation_param['exp_min_toi']*60:
            zone_deployment.append(player.get_attribute(deployment_metric))
            performance.append(player.get_attribute(performance_metric))
            x = zone_deployment
            y = performance
    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)
    diff_sum = 0
    k = round(fit[0], 4)
    m = round(fit[1], 4)
    print('Data fit: ' + performance_metric + ' = ' + str(k) + '*' + deployment_metric + ' + ' + str(m))
    tmp_a = []
    for p_id in DEFINES['ACTIVE_SKATERS']:
        player = s_db[p_id]
        if player.get_attribute('toi') >= simulation_param['exp_min_toi']*60:
            diff = player.get_attribute(performance_metric) / (k*player.get_attribute(deployment_metric) + m)
            diff_sum += (diff*diff)
            tmp_a.append((diff, p_id))
    tmp_a.sort(reverse=True)
    print('Diff sum: ' + str(100/diff_sum))
    idx = 1
    for pair in tmp_a:
        player_id = pair[1]
        player = s_db[player_id]
        if player_id in simulation_param['exp_additional_players']:
            print('{0}: {1} ({2}): {3:.2f}, {4}: {5:.2f}, {6}: {7:.2f}, PP/60: {8:.2f}'.format(idx,player_id,player.get_attribute('team_id'),pair[0],deployment_metric,player.get_attribute(deployment_metric),performance_metric,player.get_attribute(performance_metric),player.get_attribute('points_per_60')))
        idx += 1

    #plt.plot(x,fit_fn(x),'y--',label='Data fit (k=' + str(k) + ')')
    #plt.show()
    '''
    # Print data based on player age and years played after draft year.
    ages = []
    d_ages = []
    ppa_list,ppda_list = [],[]
    ppa_list_sorted,ppda_list_sorted = [],[]
    ppa,ppda = defaultdict(list),defaultdict(list)
    for player_id in DEFINES['ACTIVE_SKATERS']:
        player = s_db[player_id]
        if player.get_attribute('position') == 'F':
            ppa[player.get_attribute('age')].append(player.get_attribute('points',DEFINES[''es''])+player.get_attribute('points','pp')+player.get_attribute('points','pk'))
            ppda[player.get_attribute('draft_age')].append(player.get_attribute('points',DEFINES[''es''])+player.get_attribute('points','pp')+player.get_attribute('points','pk'))
            sum_attribute = 'estimated_off_pcg'
            #ppa[player.get_attribute('age')].append(player.get_attribute(sum_attribute))
            #ppda[player.get_attribute('draft_age')].append(player.get_attribute(sum_attribute))
    for age in ppa.keys():
        if len(ppa[age]) > 10:
            ppa_list.append((age,np.mean(ppa[age])))
            ages.append(age)
        else:
            print('Too few players in age group ' + str(age) + ' (' + str(len(ppa[age])) + ')')
    for d_age in ppda.keys():
        if len(ppda[d_age]) > 10:
            ppda_list.append((d_age,np.mean(ppda[d_age])))
            d_ages.append(d_age)
        else:
            print('Too few players in draft age group ' + str(d_age) + ' (' + str(len(ppda[d_age])) + ')')
    # Sort the data
    ppa_list.sort()
    ppda_list.sort()
    ages.sort()
    d_ages.sort()

    print('Points average based on age: ')
    for pair in ppa_list:
        print(str(pair[0]) + ': ' + str(pair[1]))
        ppa_list_sorted.append(pair[1])
    print(ppa_list_sorted)
    mu,std = st.norm.fit(ppa_list_sorted)
    x = np.linspace(21, 35, 1)
    p = st.norm.pdf(x, mu, std)
    plt.plot(x,p)
    print('Points average based on years after draft year: ')
    for pair in ppda_list:
        print(str(pair[0]) + ': ' + str(pair[1]))
        ppda_list_sorted.append(pair[1])
    # Plots
    plt.figure(1)
    plt.bar(ages,ppa_list_sorted)
    plt.figure(2)
    plt.bar(d_ages,ppda_list_sorted)
    # Show plots
    plt.show()
    '''

    '''
    # Fit Gaussian distribtion to player age
    fitted_pdfs,label_strs = [],[]
    colors = ["red","blue","green","black","cyan","brown","magenta"]
    # Decide what to use as metric
    metric = 'points_per_60'
    category = 'draft_age'
    #ths = [0.5,0.75,0.9]
    start_val = 0
    delta = 1
    ths = np.linspace(start_val,start_val+(delta*6),7)
    x_min = 0
    x_max = 5
    x = np.linspace(x_min,x_max,200)
    for th in ths:


        ## This is not used right now. This part should be used if different attribute curves should be compared.
        #metrics_array = []
        ## Save metric data for all players (here, only fwds are used)
        #for s_id in DEFINES['ACTIVE_SKATERS']:
        #   skater = s_db[s_id]
        #   if skater.get_attribute('position') == 'F':
        #       metrics_array.append(skater.get_attribute(metric))
        #metrics_threshold = th*np.max(metrics_array)

        # Use this to get different age curves
        metrics_threshold = th
        data = []
        for s_id in DEFINES['ACTIVE_SKATERS']:
            skater = s_db[s_id]
            if skater.get_attribute('position') == 'F':
                #if skater.get_attribute(metric) > metrics_threshold:
                    #data.append(skater.get_attribute(category))
                #if skater.get_attribute(category) == metrics_threshold:
                if (skater.get_attribute(category) >= metrics_threshold) and (skater.get_attribute(category) < metrics_threshold+delta):
                    data.append(skater.get_attribute(metric))

        [mu,std] = st.norm.fit(data)
        fitted_pdf = st.norm.pdf(x,mu,std)
        label_str = str('{0}={1:.1f}, mu={2:.3f}, std={3:.3f}'.format(category,metrics_threshold,mu,std))
        fitted_pdfs.append(fitted_pdf)
        label_strs.append(label_str)

    for i in range(len(ths)):
        plt.plot(x,fitted_pdfs[i],colors[i],label=label_strs[i],linewidth=1)
        #plt.hist(data,normed=1,color="cyan",alpha=.3) #alpha, from 0 (transparent) to 1 (opaque)

    plt.title('Age distribution')
    plt.legend()
    plt.show()
    for s_id in DEFINES['ACTIVE_SKATERS']:
        skater = s_db[s_id]
        if skater.get_attribute('team_id') == 'SJS':
            print('{0} has draft age: {1:.0f} years'.format(s_id,skater.get_attribute('draft_age')))

    '''
    '''
    tmp_list = []
    tmp_list_data = []
    for team_id in DEFINES['ACTIVE_TEAMS']:
        team = t_db[team_id]
        value = (team.gf-team.ga)-(team.xgf-team.xga)
        tmp_list.append((value,team_id))
        tmp_list_data.append(value)
    mu = np.mean(tmp_list_data)
    sigma = np.std(tmp_list_data)
    tmp_list.sort(reverse=True)
    for i,pair in enumerate(tmp_list):
        team_id = pair[1]
        value = pair[0]
        print('{0:.0f}: {1} - {2:.2f} ({3:.2f} sigma).'.format(i+1,team_id,value,(value-mu)/sigma))
    print('Mean: ' + str(mu))
    print('Stdv: ' + str(sigma))
    '''

    for p_id in simulation_param['exp_additional_players']:
        player = s_db[p_id]
        player.print_player()

    # Evaluate different ranking models
    mse = defaultdict(float)
    mse['errors'] = defaultdict(list)
    true_label = 'p_pcg'
    for team_id in DEFINES['ACTIVE_TEAMS']:
        team = t_db[team_id]
        for attribute in team.rank.keys():
            if attribute != true_label:
                error = int(team.rank[true_label]-team.rank[attribute])
                mse[attribute] += float(np.sqrt(error * error))
                mse['errors'][attribute].append(error)
    for attribute in team.rank.keys():
        print(attribute)
        if mse[attribute] != 0.0:
            mse[attribute] = float(1/mse[attribute])
        print('   "Model ranking": ' + str(mse[attribute]))

    # Print team stats
    if simulation_param['team_plots'] is True:
        # Set up color/markers
        markers = []
        colors = ['c', 'm', 'g', 'r', 'b']  # black and yellow are protected colors.
        forms = ['o', 'v', 's', '*', 'x', 'p', 'd']
        for form in forms:
            for color in colors:
                markers.append(str(form + color))
        figure_index = 1

        # Figure 1
        plt.figure(figure_index)
        # Subplot 1.1
        ax = plt.subplot(2, 1, 1)
        marker_idx = 0
        x_attribute = 'scf_pcg'
        y_attribute = 'estimated_off_pcg'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].exp_data[x_attribute]
            y = t_db[team_id].exp_data[y_attribute]
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        plt.xlabel(x_attribute)
        #ax.invert_yaxis()
        plt.ylabel(y_attribute)
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=np.min([200/len(DEFINES['ACTIVE_TEAMS']), 9]))
        plt.grid(True)
        # Subplot 1.2
        ax = plt.subplot(2, 1, 2)
        marker_idx = 0
        x_attribute = 'scf_per_60'
        y_attribute = 'sca_per_60'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].exp_data[x_attribute]
            y = t_db[team_id].exp_data[y_attribute]
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        ax.invert_yaxis()
        # Plot stuff
        start = float(np.min([np.min(gen_x), np.min(gen_y)]))
        stop = float(np.max([np.max(gen_x), np.max(gen_y)]))
        plt.plot([0.95*start, 1.05*stop], [0.95*start, 1.05*stop], 'k--', label='50% threshold')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.grid(True)
        figure_index += 1

        ########################################################################################################################
        # Figure 2
        plt.figure(figure_index)
        # Subplot 2.1
        ax = plt.subplot(2, 1, 1)
        marker_idx = 0
        x_attribute = 'sh_pcg'
        y_attribute = 'sv_pcg'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].exp_data[x_attribute]*100
            y = t_db[team_id].exp_data[y_attribute]*100
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.grid(True)
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=np.min([200/len(DEFINES['ACTIVE_TEAMS']), 9]))
        # Subplot 2.2
        ax = plt.subplot(2, 1, 2)
        marker_idx = 0
        x_attribute = 'estimated_off'
        y_attribute = 'estimated_def'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].exp_data[x_attribute]
            y = t_db[team_id].exp_data[y_attribute]
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        ax.invert_yaxis()
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.grid(True)
        figure_index += 1

        ########################################################################################################################
        # Figure 3
        plt.figure(figure_index)
        # Subplot 1.1
        ax = plt.subplot(3, 1, 1)
        marker_idx = 0
        x_attribute = 'cf_pcg'
        y_attribute = 'scf_pcg'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].cf_pcg
            y = t_db[team_id].scf_pcg
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        start = float(np.min([np.min(gen_x), np.min(gen_y)]))
        stop = float(np.max([np.max(gen_x), np.max(gen_y)]))
        plt.plot([0.95*start, 1.05*stop], [0.95*start, 1.05*stop], 'k--', label='50% threshold')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=np.min([200/len(DEFINES['ACTIVE_TEAMS']), 9]))
        plt.grid(True)

        # Subplot 1.2
        ax = plt.subplot(3, 1, 2)
        marker_idx = 0
        x_attribute = 'scf_pcg'
        y_attribute = 'xgf_pcg'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].scf_pcg
            y = t_db[team_id].xgf_pcg
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        start = float(np.min([np.min(gen_x), np.min(gen_y)]))
        stop = float(np.max([np.max(gen_x), np.max(gen_y)]))
        plt.plot([0.95*start, 1.05*stop], [0.95*start, 1.05*stop], 'k--', label='50% threshold')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.subplots_adjust(left=0.05, bottom=0.07, top=0.95, right=0.82, hspace=0.3)
        plt.grid(True)

        # Subplot 1.3
        ax = plt.subplot(3, 1, 3)
        marker_idx = 0
        x_attribute = 'This axis has no meaning'
        y_attribute = 'SCF - PPG [ranking]'
        gen_x, gen_y, labels = [], [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = marker_idx
            y = t_db[team_id].rank['p_pcg'] - t_db[team_id].rank['scf_pcg']
            gen_x.append(x)
            gen_y.append(y)
            labels.append(team_id)
            current_marker = markers[marker_idx]
            marker_idx += 1
        plt.stem(gen_x, gen_y)
        # Plot stuff
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.grid(True)
        figure_index += 1

        ########################################################################################################################
        # Figure 4
        plt.figure(figure_index)
        # Subplot 1.1
        ax = plt.subplot(2, 2, 1)
        marker_idx = 0
        x_attribute = 'sf_pcg'
        y_attribute = 'p_pcg'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].rank[x_attribute]
            y = t_db[team_id].rank[y_attribute]
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        start = int(np.min([np.min(ax.get_xlim()), np.min(ax.get_ylim())]))
        stop = int(np.max([np.max(ax.get_xlim()), np.max(ax.get_ylim())]))
        plt.plot(range(start, stop), range(start, stop), 'k--', label='50% threshold')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.grid(True)
        # Subplot 1.2
        ax = plt.subplot(2, 2, 2)
        marker_idx = 0
        x_attribute = 'ff_pcg'
        y_attribute = 'p_pcg'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].rank[x_attribute]
            y = t_db[team_id].rank[y_attribute]
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        start = int(np.min([np.min(ax.get_xlim()), np.min(ax.get_ylim())]))
        stop = int(np.max([np.max(ax.get_xlim()), np.max(ax.get_ylim())]))
        plt.plot(range(start, stop), range(start, stop), 'k--', label='50% threshold')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=np.min([200/len(DEFINES['ACTIVE_TEAMS']), 9]))
        plt.grid(True)
        # Subplot 1.3
        ax = plt.subplot(2, 2, 3)
        marker_idx = 0
        x_attribute = 'scf_pcg'
        y_attribute = 'p_pcg'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].rank[x_attribute]
            y = t_db[team_id].rank[y_attribute]
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        start = float(np.min([np.min(gen_x),np.min(gen_y)]))
        stop = float(np.max([np.max(gen_x),np.max(gen_y)]))
        plt.plot([0.95*start, 1.05*stop], [0.95*start, 1.05*stop], 'k--', label='50% threshold')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.grid(True)
        # Subplot 1.4
        ax = plt.subplot(2, 2, 4)
        marker_idx = 0
        x_attribute = 'xgf_pcg'
        y_attribute = 'p_pcg'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].rank[x_attribute]
            y = t_db[team_id].rank[y_attribute]
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        start = int(np.min([np.min(ax.get_xlim()), np.min(ax.get_ylim())]))
        stop = int(np.max([np.max(ax.get_xlim()), np.max(ax.get_ylim())]))
        plt.plot(range(start, stop), range(start, stop), 'k--', label='50% threshold')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.grid(True)
        figure_index += 1
        ########################################################################################################################
        # Figure 5
        plt.figure(figure_index)
        # Subplot 1.1
        ax = plt.subplot(3, 1, 1)
        marker_idx = 0
        x_attribute = 'blocked_against'
        y_attribute = 'cf'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].blocked_against
            y = t_db[team_id].cf
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        # Fit linear model to (scatter) data.
        fit = np.polyfit(gen_x, gen_y, 1)
        fit_fn = np.poly1d(fit)
        k = round(fit[0], 4)
        x_val = range(int(np.min(ax.get_xlim())), int(np.max(ax.get_xlim())))
        plt.plot(x_val, fit_fn(x_val), 'y--', label='Data fit (k=' + str(k) + ')')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=np.min([200/len(DEFINES['ACTIVE_TEAMS']), 9]))
        plt.grid(True)
        # Subplot 1.2
        ax = plt.subplot(3, 1, 2)
        marker_idx = 0
        x_attribute = 'blocked_against'
        y_attribute = 'cf'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].blocked_against
            y = t_db[team_id].ff
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        # Fit linear model to (scatter) data.
        fit = np.polyfit(gen_x, gen_y, 1)
        fit_fn = np.poly1d(fit)
        k = round(fit[0], 4)
        x_val = range(int(np.min(ax.get_xlim())), int(np.max(ax.get_xlim())))
        plt.plot(x_val, fit_fn(x_val), 'y--', label='Data fit (k=' + str(k) + ')')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.subplots_adjust(left=0.05, bottom=0.07, top=0.95, right=0.82, hspace=0.3)
        plt.grid(True)
        # Subplot 1.3
        ax = plt.subplot(3, 1, 3)
        marker_idx = 0
        x_attribute = 'blocked_against'
        y_attribute = 'sf'
        gen_x, gen_y = [], []
        for team_id in DEFINES['ACTIVE_TEAMS']:
            x = t_db[team_id].blocked_against
            y = t_db[team_id].sf
            gen_x.append(x)
            gen_y.append(y)
            current_marker = markers[marker_idx]
            plt.scatter(x, y, c=current_marker[1], marker=current_marker[0], label=team_id)
            marker_idx += 1
        plt.scatter(np.mean(gen_x), np.mean(gen_y), c='y', marker='s', label='NHL mean')
        # Plot stuff
        # Fit linear model to (scatter) data.
        fit = np.polyfit(gen_x, gen_y, 1)
        fit_fn = np.poly1d(fit)
        k = round(fit[0], 4)
        x_val = range(int(np.min(ax.get_xlim())), int(np.max(ax.get_xlim())))
        plt.plot(x_val, fit_fn(x_val), 'y--', label='Data fit (k=' + str(k) + ')')
        plt.xlabel(x_attribute)
        plt.ylabel(y_attribute)
        plt.subplots_adjust(left=0.05, bottom=0.07, top=0.95, right=0.82, hspace=0.3)
        plt.grid(True)
        figure_index += 1
        plt.show()

    # Write to console.
    list_length = simulation_param['exp_list_length']
    _filter = {}
    _filter['toi'] = simulation_param['exp_min_toi']
    _filter['position'] = simulation_param['exp_position']
    _filter['team'] = simulation_param['exp_team']
    _filter['additional_players'] = simulation_param['exp_additional_players']
    _filter['playform'] = simulation_param['exp_playform']

    if simulation_param['exp_temp_attributes'] is not None:
        for attribute in simulation_param['exp_temp_attributes']:
            print('\nBest ' + str(list_length) + ' ' + attribute + '. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
            op = print_sorted_list(db=s_db,
                                   attributes=[attribute],
                                   operation=None,
                                   _filter=_filter,
                                   print_list_length=list_length,
                                   scale_factor=1,
                                   high_to_low=True,
                                   do_print=True)
    else:
        print('\nBest ' + str(list_length) + ' goal scorers. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['goal_scoring_rating'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' relative goal impact player. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['rel_gf_diff_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' relative goal impact player. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['rel_gf_diff_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=False,
                               do_print=True)
        print('\nBest (most) ' + str(list_length) + ' offensive impact player. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_diff'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nWorst (least) ' + str(list_length) + ' offensive impact player. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_diff'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=False,
                               do_print=True)

        # Forwards only.
        _filter['position'] = ['F']
        print('\nBest ' + str(list_length) + ' offensive forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' offensive forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=False,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' defensive forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_def_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=False,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' defensive forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_def_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' combined forwards (w. points). Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_pcg','primary_points_per_60'],
                               operation=f_mult,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=100,
                               high_to_low=True,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' point scoring forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['primary_points_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' combined forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_pcg'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=100,
                               high_to_low=True,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' combined forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_pcg'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=100,
                               high_to_low=False,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' ranked forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['ranking', 'total'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' ranked forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['ranking', 'total'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=False,
                               do_print=True)

        _filter['position'] = ['D']
        _filter['toi'] *= (4/3)  # D-men plays more than forwards.
        print('\nBest ' + str(list_length) + ' offensive defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' offensive defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=False,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' defensive defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_def_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=False,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' defensive defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_def_per_60'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' combined defenders (w. points). Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_pcg', 'primary_points_per_60'],
                               operation=f_mult,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=100,
                               high_to_low=True,
                               do_print=True,
                               normalize=True)

        print('\nBest ' + str(list_length) + ' combined defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_pcg'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=100,
                               high_to_low=True,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' combined defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['estimated_off_pcg'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=100,
                               high_to_low=False,
                               do_print=True)

        print('\nBest ' + str(list_length) + ' ranked defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['ranking', 'total'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=True,
                               do_print=True)

        print('\nWorst ' + str(list_length) + ' ranked defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list(db=s_db,
                               attributes=['ranking', 'total'],
                               operation=None,
                               _filter=_filter,
                               print_list_length=list_length,
                               scale_factor=1,
                               high_to_low=False,
                               do_print=True)
        # Revert back to original TOI requirement.
        _filter['toi'] /= (4/3)

        # Goalies play more than skaters.
        _filter['toi'] *= 6
        print('\nBest ' + str(list_length) + ' save percentage goaltenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list_goalie(db=g_db,
                                      attribute='sv_pcg',
                                      _filter=_filter,
                                      print_list_length=list_length,
                                      scale_factor=100,
                                      high_to_low=True,
                                      do_print=True)

        print('\nWorst ' + str(list_length) + ' save percentage goaltenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list_goalie(db=g_db,
                                      attribute='sv_pcg',
                                      _filter=_filter,
                                      print_list_length=list_length,
                                      scale_factor=100,
                                      high_to_low=False,
                                      do_print=True)

        print('\n ' + str(list_length) + ' goaltenders with most saved goals above expected. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list_goalie(db=g_db,
                                      attribute='gsax',
                                      _filter=_filter,
                                      print_list_length=list_length,
                                      scale_factor=1,
                                      high_to_low=True,
                                      do_print=True)

        print('\n ' + str(list_length) + ' goaltenders with least saved goals above expected. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list_goalie(db=g_db,
                                      attribute='gsax',
                                      _filter=_filter,
                                      print_list_length=list_length,
                                      scale_factor=1,
                                      high_to_low=False,
                                      do_print=True)

        print('\nBest ' + str(list_length) + ' goaltenders, goals saved above expected per 60 minutes. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list_goalie(db=g_db,
                                      attribute='gsax_per_60',
                                      _filter=_filter,
                                      print_list_length=list_length,
                                      scale_factor=1,
                                      high_to_low=True,
                                      do_print=True)

        print('\nWorst ' + str(list_length) + ' goaltenders, goals saved above expected per 60 minutes. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
        op = print_sorted_list_goalie(db=g_db,
                                      attribute='gsax_per_60',
                                      _filter=_filter,
                                      print_list_length=list_length,
                                      scale_factor=1,
                                      high_to_low=False,
                                      do_print=True)
        _filter['toi'] /= 6  # Revert back to original TOI requirement.

        if simulation_param['write_to_gsheet'] is True:
            g_wb = acces_gsheet('SharksData_Public', credential_path='creds.json')
            output_sheet = g_wb.worksheet("SkaterData")
            start_cell = output_sheet.find('name')
            attributes = output_sheet.row_values(start_cell.row)
            end_col = get_alpha(len(attributes))
            num_of_rows = 0
            data_list = []
            for player_id in s_db.keys():
                player = s_db[player_id]
                if player.get_toi() > _filter['toi']*60:
                    num_of_rows += 1
                    for attribute in attributes:
                        if attribute == 'toi':
                            data_list.append(player.get_toi()/60)
                        else:
                            data_list.append(player.get_attribute(attribute))
            data_range = str('A2:' + end_col + str(1+num_of_rows))
            cell_list = output_sheet.range(data_range)
            for i, cell in enumerate(cell_list):
                cell.value = data_list[i]

            # Update in batch
            output_sheet.update_cells(cell_list)


def download_season_data(year, data_dir='Data'):
    ''' Download all data from www.naturalstattrick.com for a specific year.
    This function will *not* check if the data is alreay available.
    '''
    y = str(year)
    y = y[0:4] + '20' + y[-2:]
    if len(y) != 8:
        raise ValueError('Unexpected data format. Expected YYYYYYYY, got "' + y + '"')
    url_skater_bio = f"https://www.naturalstattrick.com/playerteams.php?fromseason={y}&thruseason={y}&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
    url_goalie_bio = "http://www.naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=G&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"




    #url_skater_ind_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
    url_skater_ind_es = "http://naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
    url_skater_ind_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v4&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
    url_skater_ind_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=4v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
    url_skater_on_ice = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v5&score=all&stdoi=oi&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
    #url_skater_on_ice = f"https://naturalstattrick.com/playerteams.php?fromseason={y}&thruseason={y}&stype=2&sit=5v5&score=all&stdoi=oi&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"



    url_goalie_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
    url_goalie_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v4&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
    url_goalie_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=4v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
    url_team_es = "https://www.naturalstattrick.com/teamtable.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
    url_team_pp = "https://www.naturalstattrick.com/teamtable.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=5v4&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
    url_team_pk = "https://www.naturalstattrick.com/teamtable.php?fromseason=" + y + "&thruseason=" + y + "&stype=2&sit=4v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="

    # Is it necessary to download new season data?
    do_download = True
    filepath = os.path.join(data_dir, 'Skater_Individual_ES_' + str(year) + '.csv')
    if os.path.exists(filepath) is True:
        if datetime.datetime.now().year > int(y[-4:]):
            print(f"   No new data downloaded, data already exists for old season '{year}'")
            do_download = False
        tsm = time.time() - os.path.getmtime(filepath)
        if do_download is True and (tsm / (24*3600) < 3):
            print("   No new data downloaded, data already up-to-date")
            do_download = False

    if do_download is True:
        print('   Downloading bio-data')
        write_bio_csv(url_skater_bio, os.path.join(data_dir,'Skater_Bio_' + str(year) + '.csv'))
        write_bio_csv(url_goalie_bio, os.path.join(data_dir,'Goalie_Bio_' + str(year) + '.csv'))
        print('   Downloading individual ES data')
        write_skater_ind_csv(url_skater_ind_es,os.path.join(data_dir,'Skater_Individual_ES_' + str(year) + '.csv'))
        print('   Downloading individual PP data')
        write_skater_ind_csv(url_skater_ind_pp,os.path.join(data_dir,'Skater_Individual_PP_' + str(year) + '.csv'))
        print('   Downloading individual PK data')
        write_skater_ind_csv(url_skater_ind_pk,os.path.join(data_dir,'Skater_Individual_PK_' + str(year) + '.csv'))
        print('   Downloading on-ice data')
        write_skater_on_ice_csv(url_skater_on_ice,os.path.join(data_dir,'Skater_OnIce_' + str(year) + '.csv'))
        print('   Downloading goalie ES data')
        write_goalie_csv(url_goalie_es,os.path.join(data_dir,'Goalie_ES_' + str(year) + '.csv'))
        print('   Downloading goalie PP data')
        write_goalie_csv(url_goalie_pp,os.path.join(data_dir,'Goalie_PP_' + str(year) + '.csv'))
        print('   Downloading goalie PK data')
        write_goalie_csv(url_goalie_pk,os.path.join(data_dir,'Goalie_PK_' + str(year) + '.csv'))
        print('   Downloading ES team data')
        write_team_csv(url_team_es,os.path.join(data_dir,'Team_ES_' + str(year) + '.csv'))
        print('   Downloading PP team data')
        write_team_csv(url_team_pp,os.path.join(data_dir,'Team_PP_' + str(year) + '.csv'))
        print('   Downloading PK team data')
        write_team_csv(url_team_pk,os.path.join(data_dir,'Team_PK_' + str(year) + '.csv'))

    # Always download contract data
    print('   Downloading contract data')
    write_ufas(os.path.join(data_dir,'Contract_Expiry_Data.csv'))

    # Separate check to see if player/team data should be downloaded
    filepath = os.path.join(data_dir, "player_team_info.csv")
    try:
        tsm = time.time() - os.path.getmtime(filepath)
        if (tsm / (24*3600) > 30):
            do_download = True
        else:
            do_download = False
    except FileNotFoundError:
        do_download = True
    if do_download is True:
        print('   Downloading player/team information')
        write_player_team_info(filepath)

    # This is currently not working
    # print('   Downloading unavailalbe players')
    # write_unavailable_players_csv(os.path.join(data_dir,'Unavailable_Players.csv'))

    # @TODO: This is not yet implemented. Not sure if it's needed.
    # Should probably not look at home/away data from 2020/2021
    #write_team_csv(simulation_param['url_team_home'],os.path.join(data_dir,'Team_Home_201819_1920.csv'))
    #write_team_csv(simulation_param['url_team_away'],os.path.join(data_dir,'Team_Away_201819_1920.csv'))



def create_databases(settings):
    ''' Create and return databases for Skaters, Goalies and Teams '''
    dbs = {}
    # Create databases.
    team_db = TeamDatabase(settings)
    skater_db = SkaterDatabase(settings)
    goalie_db = GoalieDatabase(settings)
    # Create special metrics for teams, skaters and goalies.
    # This needs to be performed _after_ the "normal" databases have been created
    [team_db, skater_db, goalie_db] = create_metrics(team_db, skater_db, goalie_db)
    [team_db, skater_db, goalie_db] = create_rankings(team_db, skater_db, goalie_db)
    dbs['skater'] = skater_db
    dbs['goalie'] = goalie_db
    dbs['team'] = team_db
    return dbs

def calculate_r2(team_db, attribute, target_attribute='p_pcg', verbose=True):
    ''' R2-factor '''
    x, y = [], []
    for team_id in ACTIVE_TEAMS:
        team = team_db.get_team(team_id)
        x.append(team.__dict__[attribute])
        y.append(team.__dict__[target_attribute])
    res = stats.linregress(x, y)
    if verbose is True:
        print(f'Relation between "{attribute}" and "{target_attribute}". R-squared: {res.rvalue**2:.3f}')
    return (res.rvalue**2)

def calculate_special_r2(team_db):
    N = 50
    attributes = ["pdo", "xgf_pcg"]
    for i in range(N):
        a = i/N
        b = 1-a
        x, y = [], []
        ranks_x, ranks_y = [], []
        teams_for_analysis = {}
        for team_id in ACTIVE_TEAMS:
            team = team_db.get_team(team_id)
            x_val = (a*team.__dict__[attributes[0]] + b*team.__dict__[attributes[1]])
            # if team_id == "SJS":
            #     print(f'Appending value {x_val:.2f} ({a*team.__dict__[attributes[0]]:.2f} + {b*team.__dict__[attributes[1]]:.2}) for team {team_id}')
            teams_for_analysis[team_id] = {"xval": x_val, "yval": team.p_pcg}
            x.append(x_val)
            y.append(team.p_pcg)

        x.sort()
        y.sort()
        identical, good, ok, bad = [], [], [], []
        for team_id, team in teams_for_analysis.items():
            team_rank_x = x.index(team["xval"])
            team_rank_y = y.index(team["yval"])
            if abs(team_rank_x - team_rank_y) < 1:
                identical.append(team_id)
            elif abs(team_rank_x - team_rank_y) < 4:
                good.append(team_id)
            elif abs(team_rank_x - team_rank_y) < 7:
                ok.append(team_id)
            else:
                bad.append(team_id)
            ranks_x.append(team_rank_x)
            ranks_y.append(team_rank_y)
            #print(f'{team_id}: {team["xval"]} ({team_rank_x})')
            #print(f'{team_id}: {team["yval"]} ({team_rank_y})')

        # res = stats.linregress(x, y)
        # if False:
        #     print(f'Identical rankings: {len(identical)} ({identical})')
        #     print(f'Good rankings: {len(good)} ({good})')
        #     print(f'OK rankings: {len(ok)} ({ok})')
        #     print(f'Bad rankings: {len(bad)} ({bad})')
        # print(f'{res.rvalue**2:.4f}  [{attributes[0]}: {a:.3f}, {attributes[1]}: {b:.3f}]')

        res = stats.linregress(ranks_x, ranks_y)
        if False:
            print(f'Identical rankings: {len(identical)} ({identical})')
            print(f'Good rankings: {len(good)} ({good})')
            print(f'OK rankings: {len(ok)} ({ok})')
            print(f'Bad rankings: {len(bad)} ({bad})')
        val_1 = res.rvalue**2
        val_2 = (len(identical)*3 + len(good)*2 + len(ok)*1)/(32*3)
        # print(f'   {val_1:.4f}')
        # print(f'   {val_2:.4f}')
    raise ValueError("DJ")
    # y.append(team.p_pcg)
    # res = stats.linregress(x, y)
    # print(f"{team_id}: {x_val:.3f}")
    # print(f"xgf: {a:.2f}, cf:{b:.2f}. R-squared: {res.rvalue**2:.3f}")


def special_attributes_r2(team_db, target_attribute='p_pcg'):
    ''' R2-factor '''
    output_array = []
    for a1 in np.linspace(0,1,300):
        a2 = 1 - a1
        x, y = [], []
        for team_id in ACTIVE_TEAMS:
            team = team_db.get_team(team_id)
            x.append(a1*team.xgf_pcg + a2*team.scf_pcg)
            y.append(team.__dict__[target_attribute])
        res = stats.linregress(x, y)
        output_array.append((res.rvalue**2, (a1, a2)))
    sort_and_print(output_array, decs=5)

def team_analysis(team_db):
    output_array = []
    for team_id in ACTIVE_TEAMS:
        team = team_db.get_team(team_id)
        output_array.append((100*(team.p_pcg - team.xgf_pcg), team_id))
    sort_and_print(output_array)

def extrapolated_player_rating(settings, attributes=["ozfo_pcg", "xgf_pcg"], toi_limit=100, N=50):
    """ Generic method for printing extrapolated data"""
    x_attribute, y_attribute = attributes
    attribute_data = settings.databases['skater'].get_data_dict([x_attribute, y_attribute])
    x_val = attribute_data[x_attribute]
    y_val = attribute_data[y_attribute]
    k, m = get_k_value(x_val, y_val)

    sdb = settings.databases['skater']
    sorted_list = []
    for player_id in sdb.id_set:
        player = sdb.get_player(player_id)
        if player.get_attribute('toi') > toi_limit*60:
            y_hat = k*player.get_attribute(x_attribute) + m
            diff = player.get_attribute(y_attribute) / y_hat  # High value -> player is doing better than they "should"
            sorted_list.append((diff, player_id))
            sorted_list.sort(reverse=False)
    i = 0
    for value, player_id in sorted_list:
        player = sdb.get_player(player_id)
        if i < N:
            print(f"{player_id} ({player.get_attribute('team_id')}): {value:.2f}")
            i += 1

def print_team_rating(settings):
    team_db = settings.databases['team']
    sorted_list = []
    # @TODO: Should be possible to select other criterias than "pre_season_rating"
    for team_id in ACTIVE_TEAMS:
        sorted_list.append((team_db.data[team_id].exp_data["pre_season_rating"], team_id))
    sorted_list.sort(reverse=True)
    i = 1
    print('\n\n*** PRE-SEASON RATINGS ***')
    for value, team_id in sorted_list:
        team = team_db.data[team_id]
        dd = team.exp_data['team_off_pcg']
        off_rank = 33-team.rank["team_off"]
        def_rank = team.rank["team_def"]
        gsax_rank = 33 - team.rank["gsax_per_60"]
        off_value = team.exp_data["team_off"]
        def_value = team.exp_data["team_def"]
        gsax = team.exp_data["gsax_per_60"]
        print(f' {i:2} - {team_id}: {value:.3f} ({dd:.3f}) OffRank: {off_rank} DefRank: {def_rank:.0f} GSAX_rank: {gsax_rank}')
        i += 1

if __name__ == '__main__':
    _filter = {}
    _filter["generic"] = []
    # Construct argument parser
    ap = argparse.ArgumentParser()
    # Add arguments to parser
    ap.add_argument("-y", "--year", nargs="+", required=True, help="Season to analyze")
    ap.add_argument("-d", "--download", action='store_true', help="Set flag to download data for a season")
    ap.add_argument("-l", "--print_list", action='store_true', help="Set flag to print list of certain skill")
    ap.add_argument("-r", "--print_ranking", action='store_true', help="Set flag to print list of ranking")
    ap.add_argument("-p", "--player", help="Name of player to analyze")
    ap.add_argument("-a", "--attribute", help="Attribute to use when printing list")
    ap.add_argument("-u", "--ufas", action='store_true', help="Set flag to only consider Unrestricted Free Agents")
    ap.add_argument("-t", "--team", help="Name of team to analyze")

    args = vars(ap.parse_args())
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # First, check to see if new data should be downloaded
    if args['download'] is True:
        download_season_data(str(args["year"]))
    # Create settings and store databases, this should always be done.
    settings = Settings(args["year"]) # Use "download_old_season_data" to download older seasons data
    settings.update_setting('databases', create_databases(settings))

    # Parse CL-input
    if args['team'] is not None:
        _filter['generic'].append(("team_id", args['team']))
    if args['ufas'] is True:
        _filter['generic'].append(("ufa", True))

    # Print either the raw list or the ranking
    if args['print_list'] is True:
        _filter['toi'] = 100
        if args['attribute'] is None:
            attribute = "gf_above_xgf_per_60"
        else:
            attribute = args['attribute']
        _filter['position'] = ['D']
        sdb = settings.databases['skater']
        print_sorted_list_skaters(settings.databases['skater'], [attribute], _filter=_filter, scale_factor=1, high_to_low=True, print_list_length=30)
        _filter['position'] = ['F']
        print_sorted_list_skaters(settings.databases['skater'], [attribute], _filter=_filter, scale_factor=1, high_to_low=True, print_list_length=30)
        _filter['toi'] = 400
        print_sorted_list_goalie(settings.databases['goalie'], ['gsax_per_60'], _filter=_filter, high_to_low=True, print_list_length=30)
    elif args['print_ranking'] is True:
        _filter['toi'] = 100
        _filter['position'] = ['D']
        print('\nDefencemen ranking:')
        print_sorted_list_skaters(settings.databases['skater'], ['ranking', 'total'], _filter=_filter, scale_factor=1, high_to_low=True, print_list_length=30)
        _filter['position'] = ['F']
        print('\nForward ranking:')
        print_sorted_list_skaters(settings.databases['skater'], ['ranking', 'total'], _filter=_filter, scale_factor=1, high_to_low=True, print_list_length=30)
    else:
        pass
        # for at in ['p_pcg', 'gf_pcg', 'cf_pcg', 'ff_pcg', 'sf_pcg', 'scf_pcg', 'hdcf_pcg', 'xgf_pcg']:
        #     calculate_r2(settings.databases['team'], at, 'p_pcg', verbose=True)

        """
        #special_attributes_r2(settings.databases['team'])
        #team_analysis(settings.databases['team'])
        settings.add_setting('ht_id', 'SJS')
        settings.add_setting('at_id', 'ANA')
        settings.add_setting('ht_goalie', 'MARTIN_JONES')
        settings.add_setting('at_goalie', 'JOHNH_GIBSON')
        settings.add_setting('ht_initial_goals', 0)
        settings.add_setting('at_initial_goals', 0)
        settings.add_setting('game_db', {})

        #simulation = Simulation(settings)
        game = GameSimulatuion(settings)
        game.simulate_game()
        """
    '''
    # Create roster lists split up on team and position.
    roster_output, flt = {}, {}
    for team_id in DEFINES['ACTIVE_TEAMS']:
        flt['team_id'] = team_id
        flt['position'] = 'D'
        roster_output[str(team_id + '_D')] = create_player_list(simulation_param['databases']['skater_db'], flt)
        flt['position'] = 'F'
        roster_output[str(team_id + '_F')] = create_player_list(simulation_param['databases']['skater_db'], flt)
    simulation_param['databases']['team_rosters'] = roster_output
    '''
    '''
    # Simulation/iteration parameters
    settings.update_setting('simulation_mode', 'SIMULATION_LIGHT')
    settings.update_setting('number_of_simulations, [50000, 2500])
    settings.update_setting('games_to_simulate', [['DAL', 'CGY'], ['SJS', 'COL']]

    # Set starting goaltenders.
    settings.set_starting_goalie(settings, 'SJS', 'MARTIN_JONES') #AARON_DELL
    settings.set_starting_goalie(settings, 'WSH', 'ILYA_SAMSONOV') #HENRIK_LUNDQVIST
    '''
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # For now, matplotlib cannot be loaded for Windows machines.
    if platform.system() == 'Windows':
        print('Cannot do plots on Windows-platform')
        simulation_param['do_plots'] = False
        print('Cannot write to Google on Windows-platform')
        simulation_param['write_to_gsheet'] = False