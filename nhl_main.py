from nhl_database import *
from nhl_simulation import *
from nhl_defines import * 
from nhl_helpers import *
from nhl_classes import *

def get_sorted_db(simulation_param,value_key,cut_off=None,toi_filter=0,position_filter=None,best_first=True):
	"""
	Return the cut_off best players in a certain category. Can filter out players based on time-on-ice [minutes]
	"""
	lst = []
	split_key = value_key.split('_')
	split_val_key = ''
	for val in split_key[1:]:
		split_val_key += val + '_'
	split_val_key = split_val_key[:-1]
	if position_filter == None:
		position_filter = ['G','D','F']
	for skater_id in simulation_param['databases']['skater_db'].keys():
		skater = get_player(simulation_param['databases']['skater_db'],skater_id)
		if (skater.es['toi']/60 >= toi_filter) and (skater.bio['position'] in position_filter):
			if split_key[0] == 'es':
				lst.append((skater.es[split_val_key],skater_id))
			elif split_key[0] == 'on_ice':
				lst.append((skater.on_ice[split_val_key],skater_id))
			else:
				raise ValueError('Unknown split-key "' + value_key.split('_')[0] + '"')
	lst.sort(reverse=best_first)
	if cut_off == None:
		return lst
	else:
		return lst[0:cut_off]

def print_player_from_team(player_db,team_id,position=[]):
	if position == []:
		position = ['G','D','F']
	for player_id in player_db:
		player = get_player(player_db,player_id)
		if (player.bio['team_id'] == team_id) and (player.bio['position'] in position):
			print(player_id)

def setup_csv_path(simulation_param):
	simulation_param['csvfiles'] = {}
	simulation_param['csvfiles']['schedule'] = 'Data/2019_2020_NHL_Schedule.csv'
	simulation_param['csvfiles']['goalies'] = 'Data/Goalies_201819_201920.csv'
	simulation_param['csvfiles']['goalies_bio'] = 'Data/Goalies_RECENT.csv'
	simulation_param['csvfiles']['skaters_es'] = 'Data/Skater_Individual_ES_201819_201920.csv'
	simulation_param['csvfiles']['skaters_pp'] = 'Data/Skater_Individual_PP_201819_201920.csv'
	simulation_param['csvfiles']['skaters_pk'] = 'Data/Skater_Individual_PK_201819_201920.csv'
	simulation_param['csvfiles']['skaters_on_ice'] = 'Data/Skater_OnIce_201819_201920.csv'
	simulation_param['csvfiles']['skaters_corsica'] = 'Data/Skater_Corsica_201819_201920.csv'
	simulation_param['csvfiles']['skaters_bio'] = 'Data/Skater_Bio_201920.csv'	
	simulation_param['csvfiles']['teams_es'] = 'Data/Team_ES_201920.csv'
	simulation_param['csvfiles']['teams_pp'] = 'Data/Team_PP_201920.csv'
	simulation_param['csvfiles']['teams_pk'] = 'Data/Team_PK_201920.csv'
	return simulation_param

def create_simulation_parameters():
	sp = {}
	sp['simulation_mode'] = None
	sp['N'] = [50000,2500]										# Number of simulations for each game/season. [rating_based,simulation_based]
	sp['number_of_periods'] = 3									# Number of periods to be played.
	sp['period_length'] = 1200									# Length of one period, in seconds.
	sp['shift_length'] = 45 									# Length of one on-ice shift, in seconds.
	sp['simulate_season'] = False
	sp['simulate_ind_games'] = False
	sp['simulate_playoff_series'] = False
	sp['initial_wins'] = [[0,0]]
	sp['print_ul_stats'] = False
	sp['do_exp'] = False
	sp['do_player_cards'] = False

	
	# Create paths to data files.
	sp = setup_csv_path(sp)
	
	return sp

################################################################################################################################################
################################################################################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Bugs:
# @TODO: "UL-filters" should be part of the simulation_param dict.
# @TODO: Create simulation parameter to control which playoff calculation should be used.
# @TODO: Apply TOI-filter to UL-calculations.
# @TODO: Fix playoff-simulation functionality

# Improvements:
# @TODO: Currently only ES-data ('on_ice') is used also for PP/PK for SIMULATION_EXT.
# @TODO: Print the rosters and starting goalies for teams during SIMULATION_EXT.
# @TODO: It should be possible to easy update particular attributes, e.g. g_db = modify_attribute(g_db,'MARTIN_JONES','sv_pcg',0.915)
# @TODO: Create an "smoothed" SH% value for each team? E.g. removing all values outside of league average + 1 sigma?
# @TODO: Implement "what-if" (for season)
# @TODO: Simulate per day, rather than per team? How would that work when there is no games at a particular date?
# @TODO: Output from team_db_row_value looks ugly (too long)
# @TODO: Create a class that is Game()

# Investigations:
# @TODO: Review game_status/data_param/simulation_param parameters. Are all necessary?
# @TODO: Is "unavailable_players" working for season simulation?
# @TODO: Something is weird with the penalty generating (and drawing of).
# @TODO: Something is weird with shots faced.
# @TODO: Use OnIce-data for SF% (or something)?
# @TODO: Should players_in_pbox be a set() instead of a list?
# @TODO: Use PP/PK specific data for sa for teams?
# @TODO: Use PP/PK specific data for goalies?
# @TODO: Investigate size of playoff_N?

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
today = datetime.datetime.today().strftime('%Y-%m-%d')
simulation_param = create_simulation_parameters()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#simulation_param['simulate_season'] = True									# Default value = False
simulation_param['simulate_ind_games'] = True 								# Default value = False
#simulation_param['simulate_playoff_series'] = True
#simulation_param['print_ul_stats'] = True 									# Default value = False
#simulation_param['do_exp'] = True 											# Default value = False
#simulation_param['do_player_cards'] = True
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Set up simulation parameters
# Simulation/iteration parameters
simulation_param['offseason'] = False
simulation_param['include_offseason_moves'] = False
#simulation_param['simulation_mode'] = SIMULATION_LIGHT 						# SIMULATION_LIGHT or SIMULATION_EXT
simulation_param['simulation_mode'] = SIMULATION_EXT 							# SIMULATION_LIGHT or SIMULATION_EXT
simulation_param['N'] = [50000,1000]											# Number of simulations for each game/season. Default = [50000,2500]

# Create databases.
simulation_param['debug_team'] = 'SJS'
simulation_param['debug_player'] = 'ERIK_KARLSSON'
simulation_param = create_databases(simulation_param)

# Gameplay parameters								
#simulation_param['games_to_simulate'] = simulation_param['databases']['season_schedule']['2019-10-16']
simulation_param['games_to_simulate'] = simulation_param['databases']['season_schedule'][today]
#simulation_param['games_to_simulate'] = [['SJS','BUF']]
#simulation_param['initial_wins'] = [[0,0]]

simulation_param['down_sample'] = False
simulation_param['initial_time'] = 0
simulation_param['initial_ht_goals'] = 0
simulation_param['initial_at_goals'] = 0

# Output/print parameters
simulation_param['print_times'] = False
simulation_param['verbose'] = False						
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if simulation_param['simulate_ind_games']:
	if simulation_param['simulation_mode'] == None:
		simulation_param['simulation_mode'] = SIMULATION_EXT

	N_sim = simulation_param['N'][simulation_param['simulation_mode']]
	for i,game in enumerate(simulation_param['games_to_simulate']):
		t0 = 1000*time.time()
		simulation_param['ht_id'] = game[0]
		simulation_param['at_id'] = game[1]
		in_game_data = create_game_specific_db(simulation_param)
		print('\nSimulating outcome between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'] + '. Number of simulations = ' + str(N_sim) + '. Simulation model = ' + str(simulation_param['simulation_mode']))
		print('\n' + simulation_param['ht_id'] + ' roster:')
		_fwd = []
		_def = []
		for p_id in in_game_data['ht_skaters'].keys():
			if simulation_param['databases']['skater_db'][p_id].bio['position'] == 'D':
				_def.append(p_id)
			else:
				_fwd.append(p_id)
		print('GOALIE: ' + in_game_data['ht_goalie'] + ' (SV: ' + str(100*simulation_param['databases']['goalie_db'][in_game_data['ht_goalie']].sv_pcg) + '%, GAA: ' + str(simulation_param['databases']['goalie_db'][in_game_data['ht_goalie']].gaa) + ')')
		print('DEF:    ' + str(_def))
		print('FWD:    ' + str(_fwd))
		print('UNAVAILABLE: ' + str(simulation_param['databases']['unavailable_players'][simulation_param['ht_id']]))
		
		print('\n' + simulation_param['at_id'] + ' roster:')
		_fwd = []
		_def = []
		for p_id in in_game_data['at_skaters'].keys():
			if simulation_param['databases']['skater_db'][p_id].bio['position'] == 'D':
				_def.append(p_id)
			else:
				_fwd.append(p_id)
		print('GOALIE: ' + in_game_data['at_goalie'] + ' (SV: ' + str(100*simulation_param['databases']['goalie_db'][in_game_data['at_goalie']].sv_pcg) + '%, GAA: ' + str(simulation_param['databases']['goalie_db'][in_game_data['at_goalie']].gaa) + ')')
		print('DEF: ' + str(_def))
		print('FWD: ' + str(_fwd))
		print('UNAVAILABLE: ' + str(simulation_param['databases']['unavailable_players'][simulation_param['at_id']]))

		# Set up simulation output parameters
		ht_g, at_g, ht_s, at_s, ht_g_prev_batch, at_g_prev_batch = 0,0,0,0,0,0
		ht_exp_s,at_exp_s = 0,0
		ht_w_t0, at_w_t0 = simulation_param['databases']['team_db'][simulation_param['ht_id']].w, simulation_param['databases']['team_db'][simulation_param['at_id']].w
		ht_w_prev_batch, at_w_prev_batch = 0,0
		batch_g_prob = []
		batch_w_prob = []
		t0_tmp = time.time()
		step_size = 10
		for i in range(N_sim):
			if print_progress(i,N_sim,t0_tmp,step_size):
				ht_g_batch = ht_g - ht_g_prev_batch
				at_g_batch = at_g - at_g_prev_batch
				ht_w_batch = ht_w - ht_w_prev_batch
				at_w_batch = at_w - at_w_prev_batch
				ht_g_batch_prob = (ht_g_batch/(ht_g_batch+at_g_batch))
				ht_w_batch_prob = (ht_w_batch/(ht_w_batch+at_w_batch))
				batch_g_prob.append(ht_g_batch_prob)
				batch_w_prob.append(ht_w_batch_prob)
				if simulation_param['verbose']:
					print('   Probability (batch - goals): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*ht_g_batch_prob,100*(1 - ht_g_batch_prob),simulation_param['at_id']))
					print('   Probability (total - goals): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*(ht_g/(ht_g+at_g)),100*(1 - (ht_g/(ht_g+at_g))),simulation_param['at_id']))
					print('   Probability (batch - wins): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*ht_w_batch_prob,100*(1 - ht_w_batch_prob),simulation_param['at_id']))
					print('   Probability (total - wins): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*(ht_w/(ht_w+at_w)),100*(1 - (ht_w/(ht_w+at_w))),simulation_param['at_id']))
				ht_g_prev_batch = ht_g
				at_g_prev_batch = at_g
				ht_w_prev_batch = ht_w
				at_w_prev_batch = at_w
			# Simulate the game
			in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)

			# Store output, for summary reasons.
			ht_g += in_game_data['ht'].gf_in_simulated_game
			at_g += in_game_data['at'].gf_in_simulated_game
			ht_s += in_game_data['ht'].sf_in_simulated_game
			at_s += in_game_data['at'].sf_in_simulated_game

			ht_exp_s += in_game_data['ht'].exp_data['team_sf_in_simulated_game']
			at_exp_s += in_game_data['at'].exp_data['team_sf_in_simulated_game']

			ht_w = simulation_param['databases']['team_db'][simulation_param['ht_id']].w - ht_w_t0
			at_w = simulation_param['databases']['team_db'][simulation_param['at_id']].w - at_w_t0
		
		print(simulation_param['debug_player'] + ' TOI: ' + str(simulation_param['databases']['skater_db'][simulation_param['debug_player']].in_game_stats['toi']/N_sim))
		
		if simulation_param['verbose']:
			mu_g = np.mean(batch_g_prob)
			sig_g = np.std(batch_g_prob) 
			print('\nMean value and standard deviation (ht goals) for batch-size ' + str(N_sim/step_size) + ': ' + str(mu_g) + ', ' + str(sig_g))
			print('   Upper threshold ht goals (3-sigma): ' + str(mu_g+3*sig_g))
			print('   Lower threshold ht goals (3-sigma): ' + str(mu_g-3*sig_g))
			mu_w = np.mean(batch_w_prob)
			sig_w = np.std(batch_w_prob) 
			print('Mean value and standard deviation (ht wins) for batch-size ' + str(N_sim/step_size) + ': ' + str(mu_w) + ', ' + str(sig_w))
			print('   Upper threshold ht win (3-sigma): ' + str(mu_w+3*sig_w))
			print('   Lower threshold ht win (3-sigma): ' + str(mu_w-3*sig_w))

		# Print simulation output
		print('\nProbability (goals):  {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*(ht_g/(ht_g+at_g)),100*(1 - (ht_g/(ht_g+at_g))),simulation_param['at_id']))
		print('Average score: {0} {1:.2f} - {2:.2f} {3}'.format(simulation_param['ht_id'],ht_g/N_sim,at_g/N_sim,simulation_param['at_id']))
		if simulation_param['simulation_mode'] == SIMULATION_EXT:
			print('Average shots: {0} {1:.0f} - {2:.0f} {3}'.format(simulation_param['ht_id'],ht_s/N_sim,at_s/N_sim,simulation_param['at_id']))
			print('Average shots EXP: {0} {1:.0f} - {2:.0f} {3}'.format(simulation_param['ht_id'],ht_exp_s/N_sim,at_exp_s/N_sim,simulation_param['at_id']))
		print('Probability (wins):   {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*(ht_w/(ht_w+at_w)),100*(1 - (ht_w/(ht_w+at_w))),simulation_param['at_id']))
		
		
		# Timing
		t_end = 1000*time.time()
		t_tot = t_end-t0
		if simulation_param['print_times']:
			print('Total time: ' + str(t_tot) + ' ms.')
			print('Average time per game simulation: ' + str(t_tot/N_sim) + ' ms.' )
			print('Total time (N = 1000): ' + str((1000/N_sim)*(t_tot)*(1/1000)) + ' s.')
			print('Total time (N = 5000): ' + str((5000/N_sim)*(t_tot)*(1/1000)) + ' s.')
			print('Total time (N = 10000): ' + str((10000/N_sim)*(t_tot)*(1/1000)) + ' s.')
			print('Total time, one round (N = 10000): ' + str(15.5*(10000/N_sim)*(t_tot)*(1/(1000*60))) + ' min.')
			print('Total time, one season (N = 1): ' + str(82*15.5*(1/N_sim)*(t_tot)*(1/(1000*60))) + ' min.')
			print('Total time, one season (N = 10000): ' + str(82*15.5*(10000/N_sim)*(t_tot)*(1/(1000*3600))) + ' h.')

if simulation_param['simulate_playoff_series']:
	simulation_param['simulation_mode'] = SIMULATION_EXT
	for g_idx,game in enumerate(simulation_param['games_to_simulate']):
		t = get_list_pcg(simulate_po_series(simulation_param,game,simulation_param['initial_wins'][g_idx]))
		"""
		simulation_param['ht_id'] = game[0]
		simulation_param['at_id'] = game[1]
		in_game_data = create_game_specific_db(simulation_param)
		print('\nSimulating playoff series between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'] + '. Number of simulations = ' + str(simulation_param['N']) + '.')
		series_distribution = [0,0,0,0,0,0,0,0]
		t0_tmp = time.time()
		for i in range(simulation_param['N']):
			print_progress(i,simulation_param['N'],t0_tmp,step=20)
			series_done = False
			wins_in_series = list(simulation_param['initial_wins'][g_idx])
			game_number = sum(wins_in_series)
			while series_done == False:
				in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
				if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
					wins_in_series[0] += 1
				else:
					wins_in_series[1] += 1
				if wins_in_series[0] == 4:
					if wins_in_series[1] == 0:
						series_distribution[0] += 1
					elif wins_in_series[1] == 1:
						series_distribution[1] += 1
					elif wins_in_series[1] == 2:
						series_distribution[2] += 1
					else:
						series_distribution[3] += 1
					series_done = True
				if wins_in_series[1] == 4:
					if wins_in_series[0] == 0:
						series_distribution[4] += 1
					elif wins_in_series[0] == 1:
						series_distribution[5] += 1
					elif wins_in_series[0] == 2:
						series_distribution[6] += 1
					else:
						series_distribution[7] += 1
					series_done = True
				game_number += 1
				"""
		#t = get_list_pcg(series_distribution)
		print('{0} - {1:.1f}% [in 4: {2:.1f}%, in 5: {3:.1f}%, in 6: {4:.1f}%, in 7: {5:.1f}%]'.format(simulation_param['ht_id'],sum(t[0:4]),t[0],t[1],t[2],t[3]))
		print('{0} - {1:.1f}% [in 4: {2:.1f}%, in 5: {3:.1f}%, in 6: {4:.1f}%, in 7: {5:.1f}%]'.format(simulation_param['at_id'],sum(t[4:8]),t[4],t[5],t[6],t[7]))

if simulation_param['simulate_season']:
	if simulation_param['simulation_mode'] == None:
		simulation_param['simulation_mode'] = SIMULATION_LIGHT

	N_sim = simulation_param['N'][simulation_param['simulation_mode']]
	# Update simulation parameters to fit "season simulation"
	simulation_param['initial_time'] = 0
	simulation_param['initial_ht_goals'] = 0
	simulation_param['initial_at_goals'] = 0
	simulation_param['print_times'] = False
	simulation_param['verbose'] = False

	t_0 = 1000*time.time()
	sort_on_alpha = True
	poc_west_ar,poc_east_ar = [],[]
	po_dict = defaultdict(int)
	po_dict_points = defaultdict(int)
	print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
	print('Simulating regular season, per ' + str(datetime.datetime.today().strftime('%Y-%m-%d')) + '. N = ' + str(N_sim))
	t0_tmp = time.time()

	'''
	current_remaining_schedule = {}
	for team_id in ACTIVE_TEAMS:
		if simulation_param['offseason'] == True:
			simulation_param['databases']['team_db'][team_id].gp = 0
			simulation_param['databases']['team_db'][team_id].w = 0
			simulation_param['databases']['team_db'][team_id].l = 0
			simulation_param['databases']['team_db'][team_id].otl = 0
			simulation_param['databases']['team_db'][team_id].p = 0
			simulation_param['databases']['team_db'][team_id].gf = 0
			simulation_param['databases']['team_db'][team_id].ga = 0
			simulation_param['databases']['team_db'][team_id].p_pcg = 0
			simulation_param['databases']['team_db'][team_id].exp_data['in_season_rating'] = simulation_param['databases']['team_db'][team_id].exp_data['pre_season_rating']
			simulation_param['databases']['team_db'][team_id].remaining_schedule = simulation_param['databases']['team_schedules'][team_id]
			current_remaining_schedule[team_id] = simulation_param['databases']['team_schedules'][team_id]
		else:
			current_remaining_schedule[team_id] = simulation_param['databases']['team_db'][team_id].remaining_schedule
	'''

	for i in range(N_sim):
		print_progress(i,N_sim,t0_tmp,step=5)
		
		team_db = copy.deepcopy(simulation_param['databases']['team_db'])

		# Setup schedule.
		if simulation_param['offseason'] == True:
			for team_id in ACTIVE_TEAMS:
				team = get_team(team_db,team_id)
				team.reset_schedule(simulation_param)
		
		# Simulate rest of the season.
		for team_id in ACTIVE_TEAMS:
			team = get_team(team_db,team_id)
			if simulation_param['simulation_mode'] == SIMULATION_LIGHT:
				for opponent_id in team.remaining_schedule:
					opponent = get_team(team_db,opponent_id)
					team.simulate_game_in_season(opponent,simulation_param)
			else:
				for opponent_id in team.remaining_schedule:
					opponent = get_team(team_db,opponent_id)	
					simulation_param['ht_id'] = team_id
					simulation_param['at_id'] = opponent_id
					in_game_data = create_game_specific_db(simulation_param)
					#print('Simulating game: ' + team_id + ' - ' + opponent_id)
					team.simulate_game_in_season(opponent,simulation_param,in_game_data)
		
		# Create playoff cutoff.
		[poc_east, poc_west] = get_playoff_cut(team_db)
		poc_east_ar.append(poc_east)
		poc_west_ar.append(poc_west)
		
		# For all teams, see if the team made the playoff or not
		for team_id in ACTIVE_TEAMS:
			team = get_team(team_db,team_id)
			if team.conference == 'W':
				poc = poc_west
			else:
				poc = poc_east
			if team.p >= poc:
				po_dict[team_id] += 1
			else:
				po_dict[team_id] += 0 # to get it included in defaultdict
			po_dict_points[team_id] += team.p

	print_list = []
	print_list_points = []
	for team_id in po_dict.keys():
		average_points = po_dict_points[team_id]/N_sim
		get_team(team_db,team_id).p = average_points
		if sort_on_alpha:
			print_list.append((team_id,po_dict[team_id]/N_sim))
			print_list_points.append((team_id,average_points))
		else:
			print_list.append((po_dict[team_id]/N_sim,team_id))
			print_list_points.append((average_points,team_id))
	
	print('\nRegular season summary:')
	total_prob = 0
	if sort_on_alpha:
		print_list.sort()
		print_list_points.sort()
		for i,pair in enumerate(print_list):
			team = get_team(team_db,pair[0])
			projected_points = print_list_points[i][1]
			print('{0}: {1} - {2:.1f}%. Projected points: {3:.1f}.'.format(str(i+1),pair[0],100*pair[1],projected_points))
			total_prob += pair[1]
	else:
		print_list.sort(reverse=True)
		print_list_points.sort(reverse=True)
		for i,pair in enumerate(print_list):
			team = get_team(team_db,pair[0])
			projected_points = print_list_points[i][1]
			print('{0}: {1} - {2:.1f}%. Projected points: {3:.1f}.'.format(str(i+1),pair[0],100*pair[1],projected_points))
			total_prob += pair[0]
	print('Projected points:')
	tl_a = create_tables(team_db,'atlantic',True,True)
	tl_m = create_tables(team_db,'metro',True,True)
	tl_c = create_tables(team_db,'central',True,True)
	tl_p = create_tables(team_db,'pacific',True,True)
	points_arr = []
	for pair in tl_a:
		points_arr.append(pair[0])
	for pair in tl_m:
		points_arr.append(pair[0])
	for pair in tl_c:
		points_arr.append(pair[0])
	for pair in tl_p:
		points_arr.append(pair[0])
	print('__TSA_DEBUG: Mean league points: ' + str(np.mean(points_arr)))
	print('__TSA_DEBUG: Std league points:  ' + str(np.std(points_arr)))
	print('__TSA_DEBUG: Max league points:  ' + str(np.max(points_arr)))
	print('__TSA_DEBUG: Min league points:  ' + str(np.min(points_arr)))

	print('Playoff cutoffs [east, west]: [{0:.1f}, {1:.1f}]'.format(sum(poc_east_ar)/len(poc_east_ar),sum(poc_west_ar)/len(poc_west_ar)))

	''' @TODO: This isn't working
	N_sim_playoff = simulation_param['N'][simulation_param['simulation_mode']]
	if N_sim_playoff > 0:
		simulation_param['simulation_mode'] = SIMULATION_EXT
		print('\nSimulating playoff, based on projected points. N = ' + str(N_sim_playoff))
		ec_teams = get_playoff_teams(tl_a,tl_m) 
		wc_teams = get_playoff_teams(tl_c,tl_p)
		playoff_teams = []
		for team_pair in ec_teams:
			playoff_teams.append(team_pair[0])
			playoff_teams.append(team_pair[1])
		for team_pair in wc_teams:
			playoff_teams.append(team_pair[0])
			playoff_teams.append(team_pair[1])
		# Simulate up till SCF
		
		t0_tmp = time.time()
		team_conf_champs, team_conf_finals, team_div_finals = [],[],[]
		for i in range(N_sim_playoff):
			print_progress(i,N_sim_playoff,t0_tmp,step=5)
			[ec_champ, ec_finals, ec_division_finals] = create_playoff_tree(ec_teams,simulation_param,False)
			[wc_champ, wc_finals, wc_division_finals] = create_playoff_tree(wc_teams,simulation_param,False)
			for team_id in playoff_teams:
				if team_id in ec_champ or team_id in wc_champ:
					simulation_param['databases']['team_db'][team_id].simulated_po_conf_champ += 1
				if team_id in ec_finals or team_id in wc_finals:
					simulation_param['databases']['team_db'][team_id].simulated_po_conf_final += 1
				if team_id in ec_division_finals or team_id in wc_division_finals:
					simulation_param['databases']['team_db'][team_id].simulated_po_div_final += 1
			# Simulate the Cup-game
			simulation_param['ht_id'] = ec_champ
			simulation_param['at_id'] = wc_champ
			in_game_data = create_game_specific_db(simulation_param)
			in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
			if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
				sc_champ = simulation_param['ht_id']
				simulation_param['databases']['team_db'][simulation_param['ht_id']].simulated_po_sc_champ += 1
			else:
				sc_champ = simulation_param['at_id']
				simulation_param['databases']['team_db'][simulation_param['at_id']].simulated_po_sc_champ += 1
		team_db = simulation_param['databases']['team_db']

		print('\nPlay-off summary:')
		for team_id in playoff_teams:
			print('{0}: To division final: {1:.1f}%. To conference final: {2:.1f}%. To SC final: {3:.1f}%. SC win: {4:.1f}%'.format(team_id,100*team_db[team_id].simulated_po_div_final/N_sim_playoff,100*team_db[team_id].simulated_po_conf_final/N_sim_playoff,100*team_db[team_id].simulated_po_conf_champ/N_sim_playoff,100*team_db[team_id].simulated_po_sc_champ/N_sim_playoff))
	'''

	t_tot = 1000*time.time()-t_0
	if simulation_param['print_times']:
		print('Total time: ' + str(t_tot/1000) + ' s.')
		print('Total time per computation: ' + str((1/N_sim)*(t_tot/1000)) + ' s.')
		print('Total time for computation (N=100): ' + str((100/N_sim)*(t_tot/(3600*1000))) + ' h.')
		print('Total time for computation (N=500): ' + str((500/N_sim)*(t_tot/(3600*1000))) + ' h.')
		print('Total time for computation (N=1000): ' + str((1000/N_sim)*(t_tot/(3600*1000))) + ' h.')
		print('Total time for computation (N=5000): ' + str((5000/N_sim)*(t_tot/(3600*1000))) + ' h.')
		print('Total time for computation (N=10000): ' + str((10000/N_sim)*(t_tot/(3600*1000))) + ' h.')

if simulation_param['print_ul_stats']:
	gp_filter=10
	toi_filter=250
	cf_filter=[0.4, 1]
	ozfo_filter=[0.35, 0.65]
	nhl_output = []
	vals = []
	
	for skater_id in simulation_param['databases']['skater_db']:
		include_player = True
		skater = get_player(simulation_param['databases']['skater_db'],skater_id)
		if skater.on_ice['gp'] < gp_filter:
			include_player = False
		if skater.on_ice['cf_pcg'] < cf_filter[0]:
			include_player = False
		if skater.on_ice['cf_pcg'] > cf_filter[1]:
			include_player = False
		if skater.on_ice['ozfo_pcg'] < ozfo_filter[0]:
			include_player = False
		if skater.on_ice['ozfo_pcg'] > ozfo_filter[1]:
			include_player = False

		if include_player == True:
			modified_val = skater.on_ice['cf_pcg']*(1/skater.on_ice['ozfo_pcg'])
			#modified_val = skater.on_ice['cf_pcg']
			nhl_output.append((modified_val,skater_id))
			vals.append(modified_val)
		else:
			warnings.warn('print_ul_stats::Skipping player ' + skater_id)


	nhl_avg = sum(vals)/len(vals)
	
	# Print section
	output_to_print = nhl_output
	print_length = 50		# How many entries should be printed. 0 = no filter

	output_to_print.sort(reverse=False)
	if print_length != 0:
		output_to_print = output_to_print[-print_length:]

	print('Difference compared to overall league average value (avg = {0:.3f}):'.format(nhl_avg))

	for i,val in enumerate(output_to_print):
		diff = (val[0]-nhl_avg)
		skater = get_player(simulation_param['databases']['skater_db'],val[1])
		sign = ''
		if diff > 0:
			sign ='+'

		print('{0:.0f}: {1} ({2}): {3}{4:.3f}. [CF: {5:.1f}%, OZFO: {6:.1f}%]'.format((len(output_to_print)-i),skater.bio['name'],skater.bio['team_id'],sign,diff,100*skater.on_ice['cf_pcg'],100*skater.on_ice['ozfo_pcg']))
	vals = []
	for team_id in ACTIVE_TEAMS:
		team = get_team(simulation_param['databases']['team_db'],team_id)
		val = team.p_pcg
		vals.append((val,team_id))
	vals.sort(reverse=True)
	for i,val in enumerate(vals):
		team_id = val[1]
		team = get_team(simulation_param['databases']['team_db'],team_id)
		team.exp_data['position'] = (i+1)
		if (i+1) <= 16:
			team.exp_data['in_playoff'] = True
		else:
			team.exp_data['in_playoff'] = False
	#########################################################################################################
	print('"Effectivness-factor"/win% per cf%: ')
	vals = []
	sum_pos_diff = 0
	for team_id in ACTIVE_TEAMS:
		team = get_team(simulation_param['databases']['team_db'],team_id)
		val = team.p_pcg/team.cf_pcg
		vals.append((val,team_id))
	vals.sort(reverse=True)
	for i,val in enumerate(vals):
		team = get_team(simulation_param['databases']['team_db'],val[1])
		pos_diff = abs(i+1-team.exp_data['position'])
		sum_pos_diff += pos_diff
		print('{0}: {1}: {2:.3f}. (Diff: {3})'.format(i+1,val[1],val[0],pos_diff))
	print('Sum diff: ' + str(sum_pos_diff))
	#########################################################################################################
	print('')
	print('Most shot attemps on-goal [%] - (sf/cf): ')
	vals = []
	sum_pos_diff = 0
	for team_id in ACTIVE_TEAMS:
		team = get_team(simulation_param['databases']['team_db'],team_id)
		val = team.sf/team.cf
		vals.append((val,team_id))
	vals.sort(reverse=True)
	for i,val in enumerate(vals):
		team = get_team(simulation_param['databases']['team_db'],val[1])
		pos_diff = abs(i+1-team.exp_data['position'])
		sum_pos_diff += pos_diff
		print('{0}: {1}: {2:.3f}. (Diff: {3})'.format(i+1,val[1],val[0],pos_diff))
	print('Sum diff: ' + str(sum_pos_diff))
	#########################################################################################################
	print('')
	print('Most unblocked shots attemps on-goal [%] - (sf/ff): ')
	vals = []
	sum_pos_diff = 0
	for team_id in ACTIVE_TEAMS:
		team = get_team(simulation_param['databases']['team_db'],team_id)
		val = team.sf/team.ff
		vals.append((val,team_id))
	vals.sort(reverse=True)
	for i,val in enumerate(vals):
		team = get_team(simulation_param['databases']['team_db'],val[1])
		pos_diff = abs(i+1-team.exp_data['position'])
		sum_pos_diff += pos_diff
		print('{0}: {1}: {2:.3f}. (Diff: {3})'.format(i+1,val[1],val[0],pos_diff))
	print('Sum diff: ' + str(sum_pos_diff))
	#########################################################################################################
	print('')
	print('HDCA / CA [%] - (hdca/ca): ')
	vals = []
	sum_pos_diff = 0
	for team_id in ACTIVE_TEAMS:
		team = get_team(simulation_param['databases']['team_db'],team_id)
		val = team.hdca/team.ca
		vals.append((val,team_id))
	vals.sort(reverse=True)
	for i,val in enumerate(vals):
		team = get_team(simulation_param['databases']['team_db'],val[1])
		pos_diff = abs(i+1-team.exp_data['position'])
		sum_pos_diff += pos_diff
		print('{0}: {1}: {2:.3f}. (Diff: {3})'.format(i+1,val[1],val[0],pos_diff))
	print('Sum diff: ' + str(sum_pos_diff))
	#########################################################################################################
	print('')
	print('SCF% * PDO: ')
	vals = []
	sum_pos_diff = 0
	correct_po = 0
	for team_id in ACTIVE_TEAMS:
		team = get_team(simulation_param['databases']['team_db'],team_id)
		val = team.scf_pcg*team.pdo
		vals.append((val,team_id))
	vals.sort(reverse=True)
	for i,val in enumerate(vals):
		team = get_team(simulation_param['databases']['team_db'],val[1])
		pos_diff = abs(i+1-team.exp_data['position'])
		sum_pos_diff += pos_diff
		if ((i+1) <= 16) and (team.exp_data['in_playoff'] == True):
			correct_po += 1
		if ((i+1) > 16) and (team.exp_data['in_playoff'] == False):
			correct_po += 1
		print('{0}: {1}: {2:.3f}. (Pos: {3}, Diff: {4})'.format(i+1,val[1],val[0],team.exp_data['position'],pos_diff))
	print('Sum diff: ' + str(sum_pos_diff))
	print('Correct PO: ' + str(correct_po/31))

if simulation_param['do_exp']:
	s_db = simulation_param['databases']['skater_db']
	f_add = lambda a,b : a+b
	f_sub = lambda a,b : a-b
	f_prod = lambda a,b : a*b
	f_div = lambda a,b : a/b

	if False:
		pos_val = 'hdcf_pcg'
		depl_val = 'dz_pcg'
		s_th = 2
		gp_limit = 15
		val_array = []
		output_array = []
		rating_array = []
		for skater_id in simulation_param['databases']['skater_db'].keys():
			val_array.append(get_player(simulation_param['databases']['skater_db'],skater_id).on_ice[depl_val])
		mu = np.mean(val_array)
		s = np.std(val_array)
		upper = mu+s_th*s
		lower = mu-s_th*s
		print('Mean: ' + str(mu))
		print('Std: ' + str(s))
		for skater_id in simulation_param['databases']['skater_db'].keys():
			add_to_rating = True
			print_player = True
			skater = get_player(simulation_param['databases']['skater_db'],skater_id)
			if skater.on_ice[depl_val] > upper:
				#print('{0} ({1:.2f}) is above threshold ({2:.2f})'.format(skater.bio['name'],skater.on_ice[val],upper))
				add_to_rating = False
			if skater.on_ice[depl_val] < lower:
				#print('{0} ({1:.2f}) is below threshold ({2:.2f})'.format(skater.bio['name'],skater.on_ice[val],lower))
				add_to_rating = False
			if skater.bio['position'] != 'F':
				add_to_rating = False
			if skater.on_ice['gp'] < gp_limit:
				#print('{0} ({1:.0f}) has not played enough games ({2:.0f})'.format(skater.bio['name'],skater.on_ice['gp'],gp_limit))
				add_to_rating = False			
			
			if add_to_rating == True:
				rating = ((skater.on_ice['cf_pcg']+skater.on_ice['scf_pcg']+skater.on_ice['hdcf_pcg'])/3)*(skater.on_ice[depl_val])
				#rating = skater.on_ice['hdcf_pcg']+skater.on_ice[depl_val]
				rating_array.append(rating)

			print_player = add_to_rating
			
			
			if skater.bio['team_id'] != 'SJS':
				print_player = False
			

			if print_player == True:
				output_array.append((rating,skater.bio['name'] + ' (' + skater.bio['team_id'] + ')'))

		rating_mu = np.mean(rating_array)
		rating_s = np.std(rating_array)
		rating_max = np.max(rating_array)
		rating_min = np.min(rating_array)

		print('Norm-Mu: ' + str(rating_mu/rating_max))
		print('Std: ' + str(rating_s))
		output_array.sort()
		i = 0
		for val,print_name in output_array:
			skater_id = print_name[:-6]
			skater = get_player(simulation_param['databases']['skater_db'],skater_id)
			norm_val = val/rating_max
			diff = val-rating_mu
			pos_avg = ((skater.on_ice['cf_pcg']+skater.on_ice['scf_pcg']+skater.on_ice['hdcf_pcg'])/3)
			#pos_avg = skater.on_ice['hdcf_pcg']
			print('{0:.0f}: {1}: {2:.2f}. Sigma-diff: {3:.2f}. {4}: {5:.1f}% [OZS: {6:.1f}%, NZS: {7:.1f}%, DZS: {8:.1f}%]'.format(len(output_array)-i,print_name,norm_val,diff/rating_s,'POS_AVG',100*pos_avg,100*skater.on_ice['oz_pcg'],100*skater.on_ice['nz_pcg'],100*skater.on_ice['dz_pcg']))
			i += 1

	if False:
		tmp = []
		tdb = simulation_param['databases']['team_db']
		for team_id in ACTIVE_TEAMS:
			tmp.append((tdb[team_id].exp_data['pre_season_rating'],team_id))
		tmp.sort(reverse=True)
		print('Pre season rating:')
		ranking = 1
		norm_cf = tdb['SJS'].exp_data['pre_season_rating']/tdb['SJS'].exp_data['in_season_rating']
		for pair in tmp:
			#print(str(ranking) + ': ' + pair[1] + ' - New rating; ' + str(pair[0]) + '. Old (normalized) rating; ' + str(norm_cf*tdb[pair[1]].exp_data['rating']))
			print('{0}: {1} - New rating: {2:.4}. In-season rating (normalized): {3:.4}'.format(ranking,pair[1],pair[0],norm_cf*tdb[pair[1]].exp_data['in_season_rating']))
			ranking += 1
		tmp = []
		for skater_id in simulation_param['databases']['skater_db'].keys():
			skater = simulation_param['databases']['skater_db'][skater_id]
			val = 10000*skater.on_ice['estimated_off_per_sec'] * skater.es['ish_pcg']
			tmp.append((val,skater_id))
		tmp.sort(reverse=True)
		
		print('\nRankings rating, NHL:')
		ranking = 1
		for pair in tmp:
			skater = simulation_param['databases']['skater_db'][pair[1]]
			if ranking <= 100 and skater.es['toi'] > 12000:
				print('{0}: {1} ({2}) - Off/s: {3:.1f}. Off: {4:.2f}% Sh: {5:.2f}% TOI/GP: {6:.1f}min, TOI%: {7:.1f}%, DZFO% {8:.1f}%'.format(ranking,pair[1],skater.bio['team_id'],pair[0],100*skater.on_ice['estimated_off_pcg'],100*skater.es['ish_pcg'],(skater.es['toi']/60)/skater.on_ice['gp'],100*skater.es['toi_pcg'],100*skater.on_ice['dzfo_pcg']))
				ranking += 1

		ranking = 1
		print('\nRankings rating, SJS:')
		for pair in tmp:
			skater = simulation_param['databases']['skater_db'][pair[1]]
			if skater.es['toi'] > 12000 and skater.bio['team_id'] == 'SJS':
				print('{0}: {1} ({2}) - Off/s: {3:.1f}. Off: {4:.2f}% Sh: {5:.2f}% TOI/GP: {6:.1f}min, TOI%: {7:.1f}%, DZFO% {8:.1f}%'.format(ranking,pair[1],skater.bio['team_id'],pair[0],100*skater.on_ice['estimated_off_pcg'],100*skater.es['ish_pcg'],(skater.es['toi']/60)/skater.on_ice['gp'],100*skater.es['toi_pcg'],100*skater.on_ice['dzfo_pcg']))
				ranking += 1

	if False:
		func = f_prod		
		
		#def print_sorted_list(db,attributes,playform,operation=None,toi_filter=200,team=None,print_list_length=50,scale_factor=1,high_to_low=True,do_print=True):
		op_nhl = print_sorted_list(s_db,['estimated_off_pcg'],'es',operation=f_add,toi_filter=300,position_filter=['F','D'],team=None,print_list_length=50,scale_factor=100,high_to_low=True)
		print('Mean: ' + str(op_nhl['mu']))
		print('Sigma: ' + str(op_nhl['sigma']))
		for team_id in ACTIVE_TEAMS:
			if team_id == 'SJS':
				op_team = print_sorted_list(s_db,['primary_points_per_60'],'es',operation=f_prod,toi_filter=300,position_filter=['F','D'],team='SJS',print_list_length=100,scale_factor=1,high_to_low=True,do_print=True)
			else:
				op_team = print_sorted_list(s_db,['primary_points_per_60'],'es',operation=f_prod,toi_filter=300,position_filter=['F','D'],team=team_id,print_list_length=100,scale_factor=1,high_to_low=True,do_print=False)
			print(team_id + ': ')
			print('   Mean: ' + str(op_team['mu']))
			print('   Sigma: ' + str(op_team['sigma']))

	if False:
		op = print_sorted_list(s_db,['ish_pcg'],'es',operation=f_prod,toi_filter=300,position_filter=['F','D'],team=None,print_list_length=100,scale_factor=100,high_to_low=True,do_print=False)
		print('SH% Mean: ' + str(op['mu']))
		print('SH% Std: ' + str(op['sigma']))

		attr = 'estimated_off_pcg'
		pf = 'es'
		#player_id = 'ANDRE_BURAKOVSKY'
		#player_id = 'ONDREJ_KASE'
		#player_id = 'ANDREI_SVECHNIKOV'
		#player_id = 'RASMUS_DAHLIN'
		#player_id = 'SAMUEL_GIRARD'
		#player_id = 'KEVIN_FIALA'
		#player_id = 'RYAN_DONATO'
		#player_id = 'MATHIEU_JOSEPH'
		#player_id = 'MIKHAIL_SERGACHEV'
		#player_id = 'TRAVIS_DERMOTT'
		player_id = 'LUKAS_RADIL'
		#player_id = 'JUSTIN_BRAUN'
		#player_id =	'SEAN_COUTURIER'
		sf = 100

		s_db = simulation_param['databases']['skater_db']
		op = print_sorted_list(s_db,[attr,'dz_pcg'],pf,operation=f_add,toi_filter=300,position_filter=['F','D'],team=None,print_list_length=100,scale_factor=sf,high_to_low=True,do_print=True)
		
		skater = s_db[player_id]
		val = sf*(get_attribute_value(skater,attr,pf)+get_attribute_value(skater,'dz_pcg',pf))
		print('Mean: ' + str(op['mu']))
		print('Std: ' + str(op['sigma']))
		print('Good threshold: ' + str(op['mu']+2*op['sigma']))
		print('Bad threshold: ' + str(op['mu']-2*op['sigma']))

		[idx,__] = get_pair_index(op['list'],player_id)

		print(player_id + ': ' + str(val) + ' (' + str(idx+1) + '/' + str(len(op['data'])+1) + ')')
		skater.print_player(s_db)

		#def get_sigma_difference(db,player_id,attribute,playform='es')
		print('Combined sigma-diff: ' + str(get_sigma_difference(s_db,player_id,attr) + get_sigma_difference(s_db,player_id,'dz_pcg')))

	if True:
		op = print_sorted_list(s_db,['sf','scf'],'on_ice',operation=f_div,toi_filter=300,position_filter=['F','D'],team=None,print_list_length=100,scale_factor=1,high_to_low=True,do_print=True) 

if simulation_param['do_player_cards']:
	s_db = simulation_param['databases']['skater_db']
	g_db = simulation_param['databases']['goalie_db']
	#__ = print_sorted_list(s_db,['avg_zone_start'],'es',operation=f_add,toi_filter=200,position_filter=['F','D'],team=None,print_list_length=20,scale_factor=1,high_to_low=True,do_print=True)
	'''
	Decide which players should be on the report cards.
	'''
	pl_high = []
	ws_def = [1.5,0.5,0.1] # suggestion for defenders
	ws_cen = [1,1,0.5] # suggestion for centers
	ws_wng = [1,0.5,1] # suggestion for wingers
	ws_fwd = [1,0.75,0.75]
	flter = {}
	
	flter['ws'] = ws_cen
	flter['list_length'] = 20
	flter['team'] = ['SJS']
	#flter['team'] = ACTIVE_TEAMS
	flter['position'] = ['F']
	flter['toi'] = 200
	player_ids = []
	for sid in s_db.keys():
		if s_db[sid].bio['team_id'] in flter['team'] and s_db[sid].bio['position'] in flter['position']:
			player_ids.append(sid)

	#player_ids = ['NIKITA_KUCHEROV','BRAD_MARCHAND','PATRICK_KANE','ALEX_OVECHKIN','MITCHELL_MARNER','LEON_DRAISAITL','JOHNNY_GAUDREAU','ARTEMI_PANARIN','MIKKO_RANTANEN','DAVID_PASTRNAK','BLAKE_WHEELER','CLAUDE_GIROUX','MARK_STONE','VLADIMIR_TARASENKO','TAYLOR_HALL','JONATHAN_HUBERDEAU','MATTHEW_TKACHUK','GABRIEL_LANDESKOG','PATRIK_LAINE','PHIL_KESSEL']
	#player_ids = ['CONNOR_MCDAVID','SIDNEY_CROSBY','NATHAN_MACKINNON','ALEKSANDER_BARKOV','JOHN_TAVARES','AUSTON_MATTHEWS','PATRICE_BERGERON','STEVEN_STAMKOS','MARK_SCHEIFELE','BRAYDEN_POINT','TYLER_SEGUIN','RYAN_OREILLY','EVGENI_MALKIN','SEBASTIAN_AHO','JACK_EICHEL','EVGENY_KUZNETSOV','LOGAN_COUTURE','NICKLAS_BACKSTROM','SEAN_MONAHAN','ELIAS_PETTERSSON']
	#player_ids = ['ALEX_PIETRANGELO','BRENT_BURNS','CHARLIE_MCAVOY','COLTON_PARAYKO','DREW_DOUGHTY','DUSTIN_BYFUGLIEN','ERIK_KARLSSON','JACCOB_SLAVIN','JACOB_TROUBA','JOHN_CARLSON','JOHN_KLINGBERG','KRIS_LETANG','MARK_GIORDANO','MIRO_HEISKANEN','MORGAN_RIELLY','P_K__SUBBAN','RASMUS_DAHLIN','ROMAN_JOSI','RYAN_SUTER','SETH_JONES','THOMAS_CHABOT','TOREY_KRUG','TYSON_BARRIE','VICTOR_HEDMAN','ZACH_WERENSKI']
	#player_ids = ['JESSE_PULJUJARVI','MELKER_KARLSSON','JUSTIN_WILLIAMS','JONNY_BRODZINSKI','PATRICK_MARLEAU']
	#player_ids.append
	#player_ids = ['DANIL_YURTAYKIN','DYLAN_GAMBRELL','JONNY_BRODZINSKI','LEAN_BERGMANN','LUKAS_RADIL','MELKER_KARLSSON']
	#player_ids = ['VLADISLAV_NAMESTNIKOV']
	#player_ids = list(s_db.keys())
	
	
	#pl_high = ['ALEX_PIETRANGELO','BRENT_BURNS','CHARLIE_MCAVOY','COLTON_PARAYKO','DREW_DOUGHTY','DUSTIN_BYFUGLIEN','ERIK_KARLSSON','JACCOB_SLAVIN','JACOB_TROUBA','JOHN_CARLSON','JOHN_KLINGBERG','KRIS_LETANG','MARK_GIORDANO','MIRO_HEISKANEN','MORGAN_RIELLY','P_K__SUBBAN','RASMUS_DAHLIN','ROMAN_JOSI','RYAN_SUTER','SETH_JONES','THOMAS_CHABOT','TOREY_KRUG','TYSON_BARRIE','VICTOR_HEDMAN','ZACH_WERENSKI']
	#pl_high = ['NIKITA_KUCHEROV','BRAD_MARCHAND','PATRICK_KANE','ALEX_OVECHKIN','MITCHELL_MARNER','LEON_DRAISAITL','JOHNNY_GAUDREAU','ARTEMI_PANARIN','MIKKO_RANTANEN','DAVID_PASTRNAK','BLAKE_WHEELER','CLAUDE_GIROUX','MARK_STONE','VLADIMIR_TARASENKO','TAYLOR_HALL','JONATHAN_HUBERDEAU','MATTHEW_TKACHUK','GABRIEL_LANDESKOG','PATRIK_LAINE','PHIL_KESSEL']
	#pl_high = ['CONNOR_MCDAVID','SIDNEY_CROSBY','NATHAN_MACKINNON','ALEKSANDER_BARKOV','JOHN_TAVARES','AUSTON_MATTHEWS','PATRICE_BERGERON','STEVEN_STAMKOS','MARK_SCHEIFELE','BRAYDEN_POINT','TYLER_SEGUIN','RYAN_OREILLY','EVGENI_MALKIN','SEBASTIAN_AHO','JACK_EICHEL','EVGENY_KUZNETSOV','LOGAN_COUTURE','NICKLAS_BACKSTROM','SEAN_MONAHAN','ELIAS_PETTERSSON']
	
	pl_high = player_ids
	
	'''
	for sid in s_db.keys():
		if s_db[sid].bio['team_id'] in ['SJS'] and s_db[sid].bio['position'] in ['F']:
			pl_high.append(sid)
	pl_high.append('VALERI_NICHUSHKIN')
	pl_high.append('JESSE_PULJUJARVI')
	pl_high.append('TYLER_TOFFOLI')
	pl_high.append('PATRICK_MARLEAU')
	pl_high.append('RYAN_STROME')
	'''
	##############################################################################################################################
	if pl_high != []:
		player_ids = list(s_db.keys())
		if s_db[pl_high[0]].bio['position'] == 'F':
			flter['ws'] = ws_fwd
		else:
			flter['ws'] = ws_def

	figure_index = 1
	axes_info = {}
	axes_info['x'] = {}
	axes_info['y'] = {}
	##############################################################################################################################
	if player_ids[0] in s_db.keys():
		do_skater_plots = True
	else:
		do_skater_plots = False

	if do_skater_plots == True:
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
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
		axes_info['x']['label'] = 'Defensive zone deployment [%]' #off-k = 0.2348
		axes_info['x']['scale'] = 100
		axes_info['x']['invert'] = True
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		ll = 1
		print('Play driving w. zone deployment:')
		for pair in op['pair_list']:
			# Normalize data
			value = pair[0]
			value -= np.min(op['data_list'])
			value /= (np.max(op['data_list']) - np.min(op['data_list']))
			if (ll <= flter['list_length']) or (pair[1] in pl_high):
				print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(value))
			ll += 1
			s_db[pair[1]].rating.append(value)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Play driving w. zone deployment')
		sub_plot_index += 1
		figure_index += 1
		##############################################################################################################################
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
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
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Primary points w. zone deployment')
		ll = 1
		print('Primary points per 60 w. zone deployment:')
		for pair in op['pair_list']:
			# Normalize data
			value = pair[0]
			value -= np.min(op['data_list'])
			value /= (np.max(op['data_list']) - np.min(op['data_list']))
			if (ll <= flter['list_length']) or (pair[1] in pl_high):
				print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(value))
			ll += 1
			s_db[pair[1]].rating.append(value)
		sub_plot_index += 1
		figure_index += 1
		##############################################################################################################################
		plt.figure(figure_index)
		sub_plot_index = 1
		n_rows = 2
		n_cols = 1
		axes_info['fit_data'] = True
		axes_info['add_threshold'] = True
		axes_info['x']['attribute'] = 'ixg'
		axes_info['x']['label'] = 'Individual expected goals'
		axes_info['x']['scale'] = 1
		axes_info['x']['invert'] = False
		axes_info['y']['attribute'] = 'gf'
		axes_info['y']['label'] = 'Goals scored'
		axes_info['y']['scale'] = 1
		axes_info['y']['invert'] = False
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Goals vs. xG')
		ll = 1
		print('Goals scored above expected:')
		for pair in op['pair_list']:
			# Normalize data
			value = pair[0]
			value -= np.min(op['data_list'])
			value /= (np.max(op['data_list']) - np.min(op['data_list']))
			if (ll <= flter['list_length']) or (pair[1] in pl_high):
				print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(value))
			ll += 1
			s_db[pair[1]].rating.append(value)
		sub_plot_index += 1
		# Goals above/below average
		axes_info['fit_data'] = True
		axes_info['add_threshold'] = False
		axes_info['x']['attribute'] = None
		axes_info['y']['attribute'] = 'goals_above_x'
		axes_info['y']['label'] = 'Goals above expected'
		axes_info['y']['scale'] = 1
		axes_info['y']['invert'] = False
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': GF vs xGF')
		sub_plot_index += 1
		figure_index += 1
		##############################################################################################################################
		plt.figure(figure_index)
		sub_plot_index = 1
		n_rows = 2
		n_cols = 1
		# Shot quality
		axes_info['fit_data'] = False
		axes_info['add_threshold'] = False
		axes_info['x']['attribute'] = 'sf_per_sec'
		axes_info['x']['label'] = 'Shoots taken per 60'
		axes_info['x']['scale'] = 3600
		axes_info['x']['invert'] = False
		axes_info['y']['attribute'] = 'ish_pcg'
		axes_info['y']['label'] = 'Shooting success [%]'
		axes_info['y']['scale'] = 100
		axes_info['y']['invert'] = False
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Corsi quality')
		sub_plot_index += 1
		figure_index += 1
		##############################################################################################################################
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Average zone start position')
		sub_plot_index += 1
		figure_index += 1
		##############################################################################################################################
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Part of points being primary')
		sub_plot_index += 1
		figure_index += 1
		##############################################################################################################################
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Points vs. total draft position')
		sub_plot_index += 1	
		axes_info['fit_data'] = True
		axes_info['add_threshold'] = False
		axes_info['x']['attribute'] = 'draft_round'
		axes_info['x']['label'] = '"Draft round'
		axes_info['x']['scale'] = 1
		axes_info['x']['invert'] = False
		axes_info['y']['attribute'] = 'estimated_off_pcg'
		axes_info['y']['label'] = 'Play control [%]'
		axes_info['y']['scale'] = 100
		axes_info['y']['invert'] = False
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Points vs. draft round')
		sub_plot_index += 1	
		figure_index += 1
		##############################################################################################################################
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,g_db,player_ids,flter)
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
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,g_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Test 2')
		sub_plot_index += 1
		figure_index += 1
		##############################################################################################################################
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,g_db,player_ids,flter)
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
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,g_db,player_ids,flter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': GAA vs GSAA_60')
		sub_plot_index += 1
		figure_index += 1
	# Show figure
	plt.show()

	# Print total rating.
	values = []
	print('TOTAL RATING:')
	op_l = []
	for player_id in player_ids:
		if s_db[player_id].es['toi'] > flter['toi']*60:
			total_value = weighted_sum(s_db[player_id].rating,flter['ws'])
			op_l.append((total_value,player_id))
	op_l.sort(reverse=True)
	ll = 1
	for pair in op_l:
		if (ll <= flter['list_length']) or (pair[1] in pl_high):
			value = pair[0]/sum(flter['ws'])
			print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(value))
			if pair[1] in pl_high:
				values.append(value)
		ll += 1
	print('Average value for player highlighted: ' + str(np.mean(values)))

