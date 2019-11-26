from nhl_database import *
from nhl_simulation import *
from nhl_defines import * 
from nhl_helpers import *
from nhl_classes import *

def setup_csv_path(simulation_param):
	simulation_param['csvfiles'] = {}
	simulation_param['csvfiles']['schedule'] = 'Data/2019_2020_NHL_Schedule.csv'
	simulation_param['csvfiles']['goalies'] = 'Data/Goalies_201819_201920.csv'
	simulation_param['csvfiles']['goalies_bio'] = 'Data/Goalies_201920.csv'
	simulation_param['csvfiles']['skaters_es'] = 'Data/Skater_Individual_ES_201819_201920.csv'
	simulation_param['csvfiles']['skaters_pp'] = 'Data/Skater_Individual_PP_201819_201920.csv'
	simulation_param['csvfiles']['skaters_pk'] = 'Data/Skater_Individual_PK_201819_201920.csv'
	simulation_param['csvfiles']['skaters_on_ice'] = 'Data/Skater_OnIce_201819_201920.csv'
	simulation_param['csvfiles']['skaters_relative'] = 'Data/Skater_Relative_201819_201920.csv'
	simulation_param['csvfiles']['skaters_bio'] = 'Data/Skater_Bio_201920.csv'	
	simulation_param['csvfiles']['teams_es'] = 'Data/Team_ES_201920.csv'
	simulation_param['csvfiles']['teams_pp'] = 'Data/Team_PP_201920.csv'
	simulation_param['csvfiles']['teams_pk'] = 'Data/Team_PK_201920.csv'

	# If only current season shall be examined
	if simulation_param['only_this_season'] == True:
		simulation_param['csvfiles']['goalies'] = 'Data/Goalies_201920.csv'
		simulation_param['csvfiles']['skaters_es'] = 'Data/Skater_Individual_ES_201920.csv'
		simulation_param['csvfiles']['skaters_pp'] = 'Data/Skater_Individual_PP_201920.csv'
		simulation_param['csvfiles']['skaters_pk'] = 'Data/Skater_Individual_PK_201920.csv'
		simulation_param['csvfiles']['skaters_on_ice'] = 'Data/Skater_OnIce_201920.csv'
		simulation_param['csvfiles']['skaters_relative'] = 'Data/Skater_Relative_201920.csv'
	return simulation_param

def create_simulation_parameters(sp):
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
	sp['do_plots'] = True

	if sp['only_this_season']:
		sp['seasons_included'] = ['2019/2020']
	else:
		sp['seasons_included'] = ['2018/2019','2019/2020']
	
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
# @TODO: Something is weird with the penalty generating (and drawing of).
# @TODO: Use OnIce-data for SF% (or something)?
# @TODO: Should players_in_pbox be a set() instead of a list?
# @TODO: Use PP/PK specific data for sa for teams?
# @TODO: Use PP/PK specific data for goalies?
# @TODO: Investigate size of playoff_N?

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
today = datetime.datetime.today().strftime('%Y-%m-%d')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
simulation_param = {}
simulation_param['only_this_season'] = False
simulation_param['write_to_gsheet'] = True
simulation_param = create_simulation_parameters(simulation_param)
simulation_param['offseason'] = False
simulation_param['include_offseason_moves'] = False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#simulation_param['simulate_ind_games'] = True 								# Default value = False
#simulation_param['simulate_playoff_series'] = True
simulation_param['simulate_season'] = True									# Default value = False
#simulation_param['print_ul_stats'] = True 									# Default value = False
#simulation_param['do_exp'] = True 											# Default value = False
#simulation_param['do_player_cards'] = True
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Simulation/iteration parameters
#simulation_param['simulation_mode'] = SIMULATION_LIGHT 						# SIMULATION_LIGHT or SIMULATION_EXT
simulation_param['N'] = [50000,2500]											# Number of simulations for each game/season. Default = [50000,2500]
simulation_param['debug_team'] = 'SJS'
simulation_param['debug_player'] = ['ERIK_KARLSSON']

# Create databases.
simulation_param = create_databases(simulation_param)

# Gameplay parameters								
#simulation_param['games_to_simulate'] = simulation_param['databases']['season_schedule']['2019-11-16']
#simulation_param['games_to_simulate'] = simulation_param['databases']['season_schedule'][today]
simulation_param['games_to_simulate'] = [['SJS','DET']]
#simulation_param['initial_wins'] = [[0,0]]
simulation_param['down_sample'] = False
simulation_param['initial_time'] = 0
simulation_param['initial_ht_goals'] = 0
simulation_param['initial_at_goals'] = 0

# Analytics parameters
simulation_param['exp_min_toi'] = 200
simulation_param['exp_list_length'] = 3
simulation_param['exp_team'] = None
#simulation_param['exp_position'] = ['F','D']
#simulation_param['exp_additional_players'] = simulation_param['databases']['team_rosters']['SJS_F']
simulation_param['exp_additional_players'] = ['DYLAN_DEMELO','JUSTIN_BRAUN','JOAKIM_RYAN','RADIM_SIMEK','ERIK_KARLSSON','TIM_HEED','MARIO_FERRARO']
simulation_param['exp_show_player_ranking'] = False
simulation_param['exp_weighted_scale'] = WS_FWD

# Output/print parameters
simulation_param['print_times'] = False
simulation_param['verbose'] = False
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# For now, matplotlib cannot be loaded for Windows machines.
if platform.system() == 'Windows':
	simulation_param['do_plots'] = False

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
		for ct in CURRENT_TEAM:
			# Print roster information
			print('\n' + simulation_param[ct + '_id'] + ' roster:')
			_fwd,_def,_unav = [],[],[]
			for p_id in in_game_data[ct + '_skaters'].keys():
				if simulation_param['databases']['skater_db'][p_id].bio['position'] == 'D':
					_def.append(p_id)
				else:
					_fwd.append(p_id)
			for p_id in simulation_param['databases']['unavailable_players']:
				if simulation_param['databases']['skater_db'][p_id].bio['team_id'] == simulation_param[ct + '_id']:
					_unav.append(p_id)
			print('GOALIE: ' + in_game_data[ct + '_goalie'] + ' (SV: ' + str(100*simulation_param['databases']['goalie_db'][in_game_data[ct + '_goalie']].sv_pcg) + '%, GAA: ' + str(simulation_param['databases']['goalie_db'][in_game_data[ct + '_goalie']].gaa) + ')')
			print('DEF:    ' + str(_def))
			print('FWD:    ' + str(_fwd))
			print('UNAVAILABLE:    ' + str(_unav))

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
		
		#print(simulation_param['debug_player'] + ' TOI: ' + str(simulation_param['databases']['skater_db'][simulation_param['debug_player']].in_game_stats['toi']/N_sim))
		
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
	po_dict = defaultdict(int)
	po_dict_points = defaultdict(int)
	print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
	print('Simulating regular season, per ' + str(datetime.datetime.today().strftime('%Y-%m-%d')) + '. N = ' + str(N_sim))
	t0_tmp = time.time()

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
					team.simulate_game_in_season(opponent,simulation_param,in_game_data)
		
		# For all teams, see if the team made the playoff or not
		[poc_east, poc_west] = get_playoff_cut(team_db)
		for team_id in ACTIVE_TEAMS:
			team = get_team(team_db,team_id)
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
		teams = teams[1:1+len(ACTIVE_TEAMS)]
		pcg_value = len(ACTIVE_TEAMS) * [0]

	for team_id in ACTIVE_TEAMS:
		team = get_team(simulation_param['databases']['team_db'],team_id)
		team.exp_data['mean_made_playoffs'] = team.exp_data['total_made_playoffs']/N_sim
		team.exp_data['mean_simulated_points'] = team.exp_data['total_simulated_points']/N_sim
		print('{0} - {1:.1f}%. Projected points: {2:.1f}.'.format(team_id,100*team.exp_data['mean_made_playoffs'],team.exp_data['mean_simulated_points']))
		if simulation_param['write_to_gsheet']:
			pcg_value[output_sheet.find(get_long_name(team_id)).row-2] = 100*team.exp_data['mean_made_playoffs']

	[poc_east, poc_west] = get_playoff_cut(simulation_param['databases']['team_db'],use_simulated_points=True)

	if simulation_param['write_to_gsheet']:
		output_sheet.update_acell(str(correct_col + '1'), str(today))
		data_range = str(correct_col + '2:' + correct_col + '32')
		cell_list = output_sheet.range(data_range)
		for i,cell in enumerate(cell_list):
			cell.value = pcg_value[i]
		# Update in batch
		output_sheet.update_cells(cell_list)

	print('Projected points:')
	tl_a = create_tables(simulation_param['databases']['team_db'],'atlantic',print_to_cmd=True,store=True,use_simulated_points=True)
	tl_m = create_tables(simulation_param['databases']['team_db'],'metro',print_to_cmd=True,store=True,use_simulated_points=True)
	tl_c = create_tables(simulation_param['databases']['team_db'],'central',print_to_cmd=True,store=True,use_simulated_points=True)
	tl_p = create_tables(simulation_param['databases']['team_db'],'pacific',print_to_cmd=True,store=True,use_simulated_points=True)
	
	print('Playoff cutoffs [east, west]: [{0:.1f}, {1:.1f}]'.format(poc_east,poc_west))


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

if simulation_param['do_exp']:
	s_db = simulation_param['databases']['skater_db']
	t_db = simulation_param['databases']['team_db']
	f_add = lambda a,b : a+b
	f_sub = lambda a,b : a-b
	f_mult = lambda a,b : a*b
	f_div = lambda a,b : a/b
	
	if simulation_param['do_plots'] == True:
		# Set up color/markers
		gen_x, gen_y,markers = [],[],[]
		colors = ['c','m','g','r','b'] # black and yellow are protected colors.
		forms = ['o','v','s','*','x','p','d']
		for form in forms:
			for color in colors:
				markers.append(str(form + color))
		ax = plt.subplot(2,1,1)
		marker_idx = 0
		for team_id in ACTIVE_TEAMS:
			#x = t_db[team_id].exp_data['estimated_off_pcg']
			x = t_db[team_id].exp_data['scf_pcg']
			#y = t_db[team_id].p_pcg
			y = t_db[team_id].exp_data['estimated_off_pcg']
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		#plt.xlabel('Estimated Offensive%')
		plt.xlabel('scf_pcg')
		#ax.invert_yaxis() 
		#plt.ylabel('Point%')
		plt.ylabel('estimated_off_pcg')
		font_size = np.min([200/len(ACTIVE_TEAMS),9])
		ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)
		plt.grid(True)

		ax = plt.subplot(2,1,2)
		gen_x, gen_y = [],[]
		marker_idx = 0
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].exp_data['scf_per_60']
			y = t_db[team_id].exp_data['sca_per_60']
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		plt.xlabel('SCF per 60')
		plt.axis([20,32,20,32])
		ax.invert_yaxis() 
		plt.ylabel('SCA per 60')
		#font_size = np.min([200/len(ACTIVE_TEAMS),9])
		#ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)
		#plt.subplots_adjust(left=0.05,bottom=0.07,top=0.95,right=0.82,hspace=0.3)
		plt.grid(True)
		plt.show()

	
	# Write to console.

	list_length = simulation_param['exp_list_length']

	_filter = {}
	_filter['toi'] = simulation_param['exp_min_toi']
	_filter['position'] = ['F','D']
	_filter['team'] = simulation_param['exp_team']
	_filter['additional_players'] = simulation_param['exp_additional_players']
	

	print('\nBest ' + str(list_length) + ' "penalty-difference-players". Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['pd_diff_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
	print('\nWorst ' + str(list_length) + ' "penalty-difference-players". Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['pd_diff_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 

	_filter['position'] = ['F']
	print('\nBest ' + str(list_length) + ' offensive forwards. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_per_sec'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=3600,high_to_low=True,do_print=True) 
	print('\nWorst ' + str(list_length) + ' offensive forwards. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_per_sec'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=3600,high_to_low=False,do_print=True) 
	print('\nBest ' + str(list_length) + ' defensive forwards. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_def_per_sec'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=3600,high_to_low=False,do_print=True) 
	print('\nWorst ' + str(list_length) + ' defensive forwards. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_def_per_sec'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=3600,high_to_low=True,do_print=True) 
	print('\nBest ' + str(list_length) + ' combined forwards (w. points). Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_pcg','primary_points_per_60'],operation=f_mult,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True) 
	print('\nBest ' + str(list_length) + ' combined forwards. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_pcg'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True) 
	print('\nBest ' + str(list_length) + ' primary points per 60. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['primary_points_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
	print('\nWorst ' + str(list_length) + ' combined forwards. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_pcg'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=False,do_print=True)

	_filter['position'] = ['D']
	print('\nBest ' + str(list_length) + ' offensive defenders. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_per_sec'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True) 
	print('\nWorst ' + str(list_length) + ' offensive defenders. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_per_sec'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=3600,high_to_low=False,do_print=True) 
	print('\nBest ' + str(list_length) + ' defensive defenders. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_def_per_sec'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=False,do_print=True) 
	print('\nWorst ' + str(list_length) + ' defensive defenders. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_def_per_sec'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=3600,high_to_low=True,do_print=True) 
	print('\nBest ' + str(list_length) + ' combined defenders (w. points). Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_pcg','primary_points_per_60'],operation=f_mult,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True) 
	print('\nBest ' + str(list_length) + ' combined defenders. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_pcg'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True) 
	print('\nWorst ' + str(list_length) + ' combined defenders. Based on seasons(s) ' + str(simulation_param['seasons_included']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
	op = print_sorted_list(s_db,['estimated_off_pcg'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=False,do_print=True) 				 				

	if simulation_param['write_to_gsheet'] == True:
		g_wb = acces_gsheet('SharksData_Public',credential_path='creds.json')		
		output_sheet = g_wb.worksheet("SkaterData")
		start_cell = output_sheet.find('name')
		attributes = output_sheet.row_values(start_cell.row)
		end_col = get_alpha(len(attributes))
		num_of_rows = 0
		data_list = []
		for player_id in s_db.keys():
			player = s_db[player_id]
			if get_attribute_value(player,'toi') > _filter['toi']*60:
				num_of_rows += 1
				for attribute in attributes:
					if attribute == 'toi':
						data_list.append(int(get_attribute_value(player,attribute))/60)
					else:
						data_list.append(get_attribute_value(player,attribute))

		data_range = str('A2:' + end_col + str(1+num_of_rows))
		cell_list = output_sheet.range(data_range)
		for i,cell in enumerate(cell_list):
			cell.value = data_list[i]

		# Update in batch
		output_sheet.update_cells(cell_list)

if (simulation_param['do_player_cards'] == True) and (simulation_param['do_plots'] == True):
	s_db = simulation_param['databases']['skater_db']
	g_db = simulation_param['databases']['goalie_db']
	
	# Decide which players should be on the report cards.
	pl_high = []
	_filter = {}
	_filter['list_length'] = simulation_param['exp_list_length']
	_filter['toi'] = simulation_param['exp_min_toi']
	_filter['team'] = simulation_param['exp_team']
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
		ll = 1
		print('Play driving w. zone deployment:')
		#print(op)
		for pair in op['pair_list']:
			# Normalize data
			value = pair[0]
			value -= np.min(op['data_list'])
			value /= (np.max(op['data_list']) - np.min(op['data_list']))
			if (ll <= _filter['list_length']) or (pair[1] in pl_high):
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Primary points w. zone deployment')
		ll = 1
		print('Primary points per 60 w. zone deployment:')
		for pair in op['pair_list']:
			# Normalize data
			value = pair[0]
			value -= np.min(op['data_list'])
			value /= (np.max(op['data_list']) - np.min(op['data_list']))
			if (ll <= _filter['list_length']) or (pair[1] in pl_high):
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
		axes_info['x']['attribute'] = 'ixgf'
		axes_info['x']['label'] = 'Individual expected goals'
		axes_info['x']['scale'] = 1
		axes_info['x']['invert'] = False
		axes_info['y']['attribute'] = 'gf'
		axes_info['y']['label'] = 'Goals scored'
		axes_info['y']['scale'] = 1
		axes_info['y']['invert'] = False
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Goals vs. xG')
		ll = 1
		print('Goals scored above expected:')
		for pair in op['pair_list']:
			# Normalize data
			value = pair[0]
			value -= np.min(op['data_list'])
			value /= (np.max(op['data_list']) - np.min(op['data_list']))
			if (ll <= _filter['list_length']) or (pair[1] in pl_high):
				print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(value))
			ll += 1
			s_db[pair[1]].rating.append(value)
		sub_plot_index += 1
		# Goals above/below average
		axes_info['fit_data'] = True
		axes_info['add_threshold'] = False
		axes_info['x']['attribute'] = None
		axes_info['y']['attribute'] = 'gf_above_xgf'
		axes_info['y']['label'] = 'Goals above expected'
		axes_info['y']['scale'] = 1
		axes_info['y']['invert'] = False
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,g_db,player_ids,_filter)
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
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,g_db,player_ids,_filter)
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,g_db,player_ids,_filter)
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
		[plt,ax,op] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,g_db,player_ids,_filter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': GAA vs GSAA_60')
		sub_plot_index += 1
		figure_index += 1
	# Show figure
	plt.show()

	# Print total rating.
	values = []
	print('TOTAL RATING:')
	counter = 1
	op_l = []
	for player_id in player_ids:
		if s_db[player_id].ind['toi'][STAT_ES] > _filter['toi']*60 and s_db[player_id].bio['position'] in _filter['position']:
			total_value = weighted_sum(s_db[player_id].rating,_filter['ws'])
			op_l.append((total_value,player_id))
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
