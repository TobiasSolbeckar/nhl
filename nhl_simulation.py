from nhl_defines import *
from nhl_helpers import *
from nhl_classes import *

def	simulate_ind_game(simulation_param,data_param):
	'''
	Simulating one game between 'ht_id' and 'at_id', based on content in 'simulation_param'
	'''
	if simulation_param['verbose']:
		print('Simulating game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
		print('Starting goalies. {0}: {1}, {2}: {3}'.format(simulation_param['ht_id'],data_param['ht_goalie'],simulation_param['at_id'],data_param['at_goalie']))

	# Set up games status parameters
	game_status = {}
	game_status['time_step'] = 1
	game_status['ht_id'] = simulation_param['ht_id']
	game_status['at_id'] = simulation_param['at_id']
	game_status['ht_goalie'] = data_param['ht_goalie']
	game_status['at_goalie'] = data_param['at_goalie']
	game_status['ht_goals'] = simulation_param['initial_ht_goals']
	game_status['at_goals'] = simulation_param['initial_at_goals']
	game_status['ht_points'], game_status['at_points'],game_status['ht_shots'],game_status['at_shots'] = 0,0,0,0
	game_status['game_active'] = False
	game_status['goal_scored'] = [False, False]
	game_status['ht_penalty'], game_status['at_penalty'] = defaultdict(int), defaultdict(int)
	game_status['active_penalties'] = [0,0]
	game_status['current_period'] = 0

	# Debug/test
	game_status['ht_number_of_skaters'], game_status['at_number_of_skaters'] = [], [] # [def, fwd]
	game_status['ht_on_ice_db'],game_status['at_on_ice_db'] = {},{}
	game_status['players_in_pbox'] = []  
	game_status['previous_gameplay_state'] = GAMEPLAY_ES
	game_status['gameplay_changed'] = False
	game_status['gameplay_state'] = GAMEPLAY_ES
	game_status['ht_goalie_in_net'], game_status['at_goalie_in_net'] = True, True
	game_status['ht_goalscorers'],game_status['at_goalscorers'] = [],[]
	game_status['ht_pp'],game_status['ht_pk'],game_status['at_pp'],game_status['at_pk'] = False, False, False, False
	if simulation_param['down_sample'] == True:
		game_status['time_step'] = 10

	if simulation_param['verbose']:
		print('- - - - - - - - START OF GAME - - - - - - - -')
	game_status['game_active'] = True
	simulation_param['period_length'] = 1200
	[game_status,data_param] = simulate_regulation_time(simulation_param,data_param,game_status)

	# Check the score after three periods of play. If equal, move on to OT.
	if game_status['ht_goals'] == game_status['at_goals']:
		# Game moves on to OT
		if simulation_param['verbose']:
			print('- - - - - - - - START OF OT - - - - - - - -')
		simulation_param['period_length'] = 300
		[game_status, data_param] = simulate_ot(simulation_param,data_param,game_status)
		if game_status['game_active'] == True:
			if simulation_param['verbose']:
				print('- - - - - - - - START OF PENALTY SO - - - - - - - -')
			if random.uniform(0,1) < 0.5:
				game_status['ht_goals'] += 1
				if simulation_param['verbose']:
					print('- - - - - - - - ' + game_status['ht_id'] + ' WINS ON PENALTY SO - - - - - - - -')
				game_status['ht_points'] = 2
				game_status['at_points'] = 1
			else:
				game_status['at_goals'] += 1
				if simulation_param['verbose']:
					print('- - - - - - - - ' + game_status['at_id'] + ' WINS ON PENALTY SO - - - - - - - -')
				game_status['ht_points'] = 1
				game_status['at_points'] = 2
			game_status['game_active'] = False
		else:
			# Game is over. Who won?
			if game_status['ht_goals'] > game_status['at_goals']:
				if simulation_param['verbose']:
					print('- - - - - - - - END OF GAME - - - - - - - -')
					print('- - - - - - - - ' + game_status['ht_id'] + ' WINS IN OT - - - - - - - -')
				game_status['ht_points'] = 2
				game_status['at_points'] = 1
			else:
				if simulation_param['verbose']:
					print('- - - - - - - - END OF GAME - - - - - - - -')
					print('- - - - - - - - ' + game_status['at_id'] + ' WINS IN OT - - - - - - - -')
				game_status['ht_points'] = 1
				game_status['at_points'] = 2
	elif game_status['ht_goals'] > game_status['at_goals']: # Game is over. Who won?
		if simulation_param['verbose']:
			print('- - - - - - - - END OF GAME - - - - - - - -')
			print('- - - - - - - - ' + game_status['ht_id'] + ' WINS IN REGULATION - - - - - - - -')
		game_status['ht_points'] = 2
		game_status['at_points'] = 0
		game_status['game_active'] = False
	else:
		if simulation_param['verbose']:
			print('- - - - - - - - END OF GAME - - - - - - - -')
			print('- - - - - - - - ' + game_status['at_id'] + ' WINS IN REGULATION - - - - - - - -')
		game_status['ht_points'] = 0
		game_status['at_points'] = 2
		game_status['game_active'] = False

	# Print post-game stats.
	if simulation_param['verbose']:
		if game_status['game_active'] == False:
			print('- - - - - - - - GAME STATS - - - - - - - -')
			print('Score:')
			print(game_status['ht_id'] + ' ' + str(game_status['ht_goals']) + ' - ' + str(game_status['at_goals']) + ' ' + game_status['at_id'])
			ht_gscr_str = []
			for skater_id in game_status['ht_goalscorers']:
				print_str = skater_id + ' (' + str(game_status['ht_goalscorers'].count(skater_id)) + ')'
				if print_str not in ht_gscr_str:
					ht_gscr_str.append(print_str)			
			at_gscr_str = []
			for skater_id in game_status['at_goalscorers']:
				print_str = skater_id + ' (' + str(game_status['at_goalscorers'].count(skater_id)) + ')'
				if print_str not in at_gscr_str:
					at_gscr_str.append(print_str)

			print('   Goals ' + game_status['ht_id'] + ': ' + str(ht_gscr_str))
			print('   Goals ' + game_status['at_id'] + ': ' + str(at_gscr_str))
			print('Shots:')
			print(game_status['ht_id'] + ' ' + str(game_status['ht_shots']) + ' - ' + str(game_status['at_shots']) + ' ' + game_status['at_id'])

			ht_sv_pcg = (game_status['at_shots']-game_status['at_goals'])/game_status['at_shots']
			at_sv_pcg = (game_status['ht_shots']-game_status['ht_goals'])/game_status['ht_shots']
			print('Saving percentage: {0}: {1:.1f} - {2}: {3:.1f}'.format(data_param['ht_goalie'],100*ht_sv_pcg,data_param['at_goalie'],100*at_sv_pcg))
			if False:
				print('- - - - - - - - INDIVIDUAL STATS - - - - - - - -')
				print('NAME   TOI   GOALS   SHOTS')
				print(game_status['ht_id'])
				for player_id in data_param['ht_players'].keys():
					player = get_player(data_param['ht_players'],player_id)
					print('   ' + player_id + '   ' + str(get_time_str_from_sec(player.in_game_stats['toi'])) + '   ' + str(player.in_game_stats['goals']) + '    ' + str(player.in_game_stats['shots']))

				print(game_status['at_id'])
				for player_id in data_param['at_players'].keys():
					player = get_player(data_param['at_players'],player_id)
					print('   ' + player_id + '   ' + str(get_time_str_from_sec(player.in_game_stats['toi'])) + '   ' + str(player.in_game_stats['goals']) + '    ' + str(player.in_game_stats['shots']))

			if False:
				print('Time - simulating ice-time:  ' + str(times[0]))
				print('Time - simulating ht performance:  ' + str(times[1]))
				print('Time - simulating at performance:  ' + str(times[2]))

	return game_status

def simulate_regulation_time(simulation_param,data_param,game_status):
	'''
	Simulate regulation time.
	INPUTS:
	simulation_param 	= data concerning the simulation engine
	data_param 			= data concerning team/player statistics
	game_status 		= data concerning the current in-game status
	
	OUTPUTS:
	game_status
	data_param
	'''
	verbose = simulation_param['verbose']

	ht_id = game_status['ht_id'] 		# For readability
	at_id = game_status['at_id'] 		# For readability
	game_status['time'] = simulation_param['initial_time']
	game_status = get_time_str(game_status)
	while (game_status['time'] < simulation_param['period_length']*simulation_param['number_of_periods']):

		if (game_status['time']%simulation_param['period_length']) == 0:
			game_status['current_period'] += 1
			if verbose:
				print('- - - - - - - - START OF PERIOD ' + str(game_status['current_period']) + ' - - - - - - - -')

		t0 = time.time()
		
		# 1: Update the state machine
		game_status = update_state_machine(game_status)

		# 2: Put new players on the ice, if the old shift is done
		if ((game_status['time']%simulation_param['shift_length']) == 0) or (game_status['gameplay_changed'] == True):
			game_status = put_players_on_ice(game_status,data_param,verbose)

		# 3: Update game clock before simulating the gameplay.
		game_status['time'] += game_status['time_step']

		# 4: Get the print-version of time, for print-outs only.
		game_status = get_time_str(game_status)
		
		# 5: Simulate gameplay for one second
		[game_status, data_param] = simulate_gameplay(game_status,data_param,verbose)

		# 6: Update penalties after gameplay simulation, if there are someone in the penalty box.
		if game_status['players_in_pbox'] != []:
			game_status = update_penalties(game_status)

		if ( (game_status['time']%simulation_param['period_length']) == (simulation_param['period_length']-1) ) and (verbose == True):
			print('- - - - - - - - END OF PERIOD ' + str(game_status['current_period']) + ' - - - - - - - -')
	'''
	sum_time = 0
	for tmp_i in range(len(debug_time_vector)):
		sum_time += debug_time_vector[tmp_i]
	for tmp_i in range(len(debug_time_vector)):
		debug_time_vector[tmp_i] = (100*debug_time_vector[tmp_i])/sum_time

	print('State machine: ' + str(debug_time_vector[0]))
	print('New placers on ice: ' + str(debug_time_vector[1]))
	print('Update game clock: ' + str(debug_time_vector[2]))
	print('Get print version of time: ' + str(debug_time_vector[3]))
	print('Simulate gameplay: ' + str(debug_time_vector[4]))
	print('Update penalties: ' + str(debug_time_vector[5]))
	'''

	return [game_status, data_param]

def simulate_ot(simulation_param,data_param,game_status):
	'''
	Simulate over-time.
	INPUTS:
	simulation_param 	= data concerning the simulation engine
	data_param 			= data concerning team/player statistics
	game_status 		= data concerning the current in-game status
	
	OUTPUTS:
	game_status
	data_param
	'''

	verbose = simulation_param['verbose']
	ht_id = game_status['ht_id'] 		# For readability
	at_id = game_status['at_id'] 		# For readability
	game_status['time'] = 3600
	game_status = get_time_str(game_status)
	while (game_status['time'] < 3600+simulation_param['period_length']) and (game_status['game_active'] == True):
		if (game_status['time']%simulation_param['period_length']) == 0:
			game_status['current_period'] += 1
			if verbose:
				print('- - - - - - - - START OF PERIOD ' + str(game_status['current_period']) + ' - - - - - - - -')

		t0 = time.time()
		
		# 1: Update the state machine
		game_status = update_state_machine(game_status)

		# 2: Put new players on the ice, if the old shift is done
		if (game_status['time']%simulation_param['shift_length']) == 0:
			game_status = put_players_on_ice(game_status,data_param,verbose)

		# 3: Update game clock before simulating the gameplay.
		game_status['time'] += game_status['time_step']

		# 4: Get the print-version of time, for print-outs only.
		game_status = get_time_str(game_status)
		
		# 5: Simulate gameplay for one second
		[game_status, data_param] = simulate_gameplay(game_status,data_param,verbose)

		# 6: Update penalties after gameplay simulation, if there are someone in the penalty box.
		if game_status['players_in_pbox'] != []:
			game_status = update_penalties(game_status)

		if ( (game_status['time']%simulation_param['period_length']) == (simulation_param['period_length']-1) ) and (verbose == True):
			print('- - - - - - - - END OF PERIOD ' + str(game_status['current_period']) + ' - - - - - - - -')

	return [game_status, data_param]

def simulate_gameplay(game_status,data_param,verbose=False):
	game_status['goal_scored'] = [False, False]
	
	for i,ct in enumerate(CURRENT_TEAM):
		ot = OPPONENT_TEAM[i]
		opponent_goalie = get_player(data_param[ot + '_players'],data_param[ot + '_goalie'])
		opponent_team_sa_per_time = game_status['time_step']*data_param[ot].sa_per_sec 

		for skater_id in game_status[ct + '_on_ice_db'].keys():
			skater = get_player(data_param[ct + '_skaters'],skater_id)
			sf_per_time = game_status[ct + '_on_ice_db'][skater_id][0]
			sh_pcg = game_status[ct + '_on_ice_db'][skater_id][1]
			pt_per_time = game_status[ct + '_on_ice_db'][skater_id][2]
			pd_per_time = game_status[ct + '_on_ice_db'][skater_id][3]
			off_per_time = game_status[ct + '_on_ice_db'][skater_id][4]
			def_per_time = game_status[ct + '_on_ice_db'][skater_id][5]
			
			# Update toi for the current skater.
			skater.in_game_stats['toi'] += game_status['time_step']

			# Calculate the probability that the current skater takes a penalty.
			penalty_prob = pt_per_time
			#penalty_prob = (pt_per_time + at_on_ice_pd)/2
			#penalty_prob = (pt_per_time + at_on_ice_pd/5)/2
			if random.uniform(0,1) < penalty_prob:
				if verbose:
					print(game_status['time_str'] + ':    Penalty for ' + game_status[ct + '_id'] + ' (' + skater_id + ')')
				game_status[ct + '_penalty'][skater_id] = 120
				game_status['players_in_pbox'].append(skater_id)
			else:
				# Player can only shot when not getting a penalty.
				# Calculate the probability that the current skater will take a shot.
				shot_prob = (sf_per_time + opponent_team_sa_per_time/5)/2
				if random.uniform(0,1) < shot_prob:
					if verbose:
						print(game_status['time_str'] + ': Shot (' + game_status[ct + '_penalty_status'] + ') for ' + game_status[ct + '_id'] + ' (' + skater_id + ')')
					
					# Update in-game stats.
					game_status[ct + '_shots'] += 1
					skater.in_game_stats['shots'] += 1

					# Calculate the probability that the shot taken is a goal.	
					goal_prob = (sh_pcg + (1-opponent_goalie.sv_pcg))/2
					if random.uniform(0,1) < goal_prob:
						if verbose:
							print(game_status['time_str'] + ':    Goal (' + game_status[ct + '_penalty_status'] + ') for ' + game_status[ct + '_id'] + ' (' + skater_id + ')')
											
						# Update in-game stats.
						game_status['goal_scored'][i] = True						
						skater.in_game_stats['goals'] += 1
						game_status[ct + '_goals'] += 1
						game_status[ct + '_goalscorers'].append(skater_id)

						# Sudden death if OT
						if game_status['current_period'] >= 4: 
							game_status['game_active'] = False

			data_param[ct + '_skaters'][skater_id] = skater
	
	return [game_status,data_param]

def update_state_machine(game_status):
	
	# Store old game_status
	game_status['previous_gameplay_state'] = game_status['gameplay_state']
	game_status['ht_pp'],game_status['ht_pk'],game_status['at_pp'],game_status['at_pk'] = False,False,False,False
	game_status['ht_goalie_in_net'], game_status['at_goalie_in_net'] = True, True
	
	# Update game state machine
	if game_status['active_penalties'][0] > game_status['active_penalties'][1]:
		game_status['gameplay_state'] = GAMEPLAY_PP_AT
		game_status['ht_pk'] = True
		game_status['at_pp'] = True
		game_status['ht_penalty_status'] = 'SH'
		game_status['at_penalty_status'] = 'PP'
		if game_status['current_period'] <= 3:
			game_status['ht_number_of_skaters'] = [2,2] # [def, fwd]
			game_status['at_number_of_skaters'] = [1,4] # [def, fwd]
		else:
			game_status['ht_number_of_skaters'] = [2,1] # [def, fwd]
			game_status['at_number_of_skaters'] = [1,3] # [def, fwd]
		
	elif game_status['active_penalties'][0] < game_status['active_penalties'][1]:
		game_status['gameplay_state'] = GAMEPLAY_PP_HT
		game_status['ht_pp'] = True
		game_status['at_pk'] = True
		game_status['ht_penalty_status'] = 'PP'
		game_status['at_penalty_status'] = 'SH'
		if game_status['current_period'] <= 3:
			game_status['ht_number_of_skaters'] = [1,4] # [def, fwd]
			game_status['at_number_of_skaters'] = [2,2] # [def, fwd]
		else:
			game_status['ht_number_of_skaters'] = [1,3] # [def, fwd]
			game_status['at_number_of_skaters'] = [2,1] # [def, fwd]	
	else:
		game_status['gameplay_state'] = GAMEPLAY_ES
		game_status['ht_penalty_status'] = 'ES'
		game_status['at_penalty_status'] = 'ES'
		if game_status['current_period'] <= 3:
			game_status['ht_number_of_skaters'] = [2,3] # [def, fwd]
			game_status['at_number_of_skaters'] = [2,3] # [def, fwd]
		else:
			game_status['ht_number_of_skaters'] = [1,2] # [def, fwd]
			game_status['at_number_of_skaters'] = [1,2] # [def, fwd]

	#__TSA_DEBUG:
	if int(game_status['time_str'].split(":")[0]) >= 58:
		if (game_status['ht_goals'] - game_status['at_goals'] == 1) or (game_status['ht_goals'] - game_status['at_goals'] == 2):
			game_status['at_goalie_in_net'] = False
			game_status['at_number_of_skaters'][1] += 1 # Away team pulling goalie
		elif (game_status['at_goals'] - game_status['ht_goals'] == 1) or (game_status['at_goals'] - game_status['ht_goals'] == 2):
			game_status['ht_goalie_in_net'] = False
			game_status['ht_number_of_skaters'][1] += 1 # Home team pulling goalie
	# __TSA_END_DEBUG

	# Check if the gameplay_status has changed.
	if (game_status['previous_gameplay_state'] != game_status['gameplay_state']) or (sum(game_status['goal_scored']) > 0):
		game_status['gameplay_changed'] = True
		#game_status['goal_scored'] = False
	else:
		game_status['gameplay_changed'] = False

	return game_status	

def update_penalties(game_status):

	for skater_id in game_status['ht_penalty'].copy().keys():
		game_status['ht_penalty'][skater_id] = game_status['ht_penalty'][skater_id] - game_status['time_step']
		if (game_status['ht_penalty'][skater_id] <= 0) or (game_status['goal_scored'][1] == True):
			del game_status['ht_penalty'][skater_id]
			game_status['players_in_pbox'].remove(skater_id)

	for skater_id in game_status['at_penalty'].copy().keys():
		game_status['at_penalty'][skater_id] = game_status['at_penalty'][skater_id] - game_status['time_step']
		if (game_status['at_penalty'][skater_id] <= 0) or (game_status['goal_scored'][0] == True):
			del game_status['at_penalty'][skater_id]
			game_status['players_in_pbox'].remove(skater_id)

	game_status['active_penalties'][0] = len(game_status['ht_penalty'])
	game_status['active_penalties'][1] = len(game_status['at_penalty'])

	return game_status

def get_in_game_players(db,key,th):
	names = []
	print('key = ' + str(key) + '. th = ' + str(th))
	for pl_id in db.keys():
		print('checking player ' + pl_id)
		pl = get_player(db,pl_id)
		print(pl_id + '.in_game_stats[' + str(key) + '] = ' + str(pl.in_game_stats[key]))
		if pl.in_game_stats[key] >= th:
			pl_id_str = pl_id
			if pl.in_game_stats[key] > th:
				pl_id_str = str(pl_id + ' (' + str(pl.in_game_stats[key]) + ')')
			names.append(pl_id_str)
	return names

def put_players_on_ice(game_status,data_param,verbose=False):
	lines_on_ice = [None,None]
	for i,ct in enumerate(CURRENT_TEAM):
		line_values = {}
		line_values['off_per_time'] = 0
		line_values['def_per_time'] = 0
		ot = OPPONENT_TEAM[i]
		ct_on_ice_db = {}
		players_on_ice = set()
		added_skaters = [0,0]
		add_more_f = True
		add_more_d = True
		while added_skaters[0] < game_status[ct + '_number_of_skaters'][0] or added_skaters[1] < game_status[ct + '_number_of_skaters'][1]: 
			for skater_id in set(data_param[ct + '_skaters']):  # using a set for randomizing purposes
				skater = get_player(data_param[ct + '_skaters'],skater_id)
				if game_status['gameplay_state'] == GAMEPLAY_ES:
					toi_pcg = skater.es['toi_pcg']
					sf = skater.es['sf']
					gf = skater.es['gf']
					sf_per_time = game_status['time_step']*skater.es['sf_per_sec']
					#sh_pcg = skater.es['sh_pcg']
					pt_per_time = game_status['time_step']*skater.es['pt_per_sec']
					pd_per_time = game_status['time_step']*skater.es['pd_per_sec']
					off_per_time = game_status['time_step']*skater.es['estimated_off_per_sec']
					def_per_time = game_status['time_step']*skater.es['estimated_def_per_sec']
				elif game_status[ct + '_pp'] == True:
					toi_pcg = skater.pp['toi_pcg']
					sf = skater.pp['sf']
					gf = skater.pp['gf']
					sf_per_time = game_status['time_step']*skater.pp['sf_per_sec']
					sh_pcg = skater.pp['sh_pcg']
					pt_per_time = 0 # No penalties during PP/PK are allowed for now.
					pd_per_time = 0 # No penalties during PP/PK are allowed for now.
					off_per_time = game_status['time_step']*skater.es['estimated_off_per_sec']
					def_per_time = game_status['time_step']*skater.es['estimated_def_per_sec']
				elif game_status[ct + '_pk'] == True:
					toi_pcg = skater.pk['toi_pcg']
					sf = skater.pk['sf']
					gf = skater.pk['gf']
					sf_per_time = game_status['time_step']*skater.pk['sf_per_sec']
					sh_pcg = skater.pk['sh_pcg']
					pt_per_time = 0 # 5-on-3 situations allowed for now.
					pd_per_time = 0 # No penalties during PP/PK are allowed for now.
					off_per_time = game_status['time_step']*skater.es['estimated_off_per_sec']
					def_per_time = game_status['time_step']*skater.es['estimated_def_per_sec']
				else:
					raise ValueError('Incorrect game_status')
				if game_status[ot + '_goalie_in_net'] == False:
					sf_per_time *= 3 # Estimation of how much more often a shot is taken when the goalie is pulled
					sh_pcg = 1.7 # Ugly hack to get the total goal-prob to be about 90% when the goalie is pulled

				if (random.uniform(0,1) < toi_pcg) and (skater.bio['name'] not in players_on_ice) and (skater.bio['name'] not in game_status['players_in_pbox']):
					if (skater.bio['position'] == 'D') and (add_more_d == True):
						players_on_ice.add(skater.bio['name'])
						ct_on_ice_db[skater_id] = [sf_per_time,sh_pcg,pt_per_time,pd_per_time,off_per_time,def_per_time]
						added_skaters[0] += 1
						line_values['off_per_time'] += off_per_time
						line_values['def_per_time'] += def_per_time
					if (skater.bio['position'] == 'F') and (add_more_f == True):
						players_on_ice.add(skater.bio['name'])
						ct_on_ice_db[skater_id] = [sf_per_time,sh_pcg,pt_per_time,pd_per_time,off_per_time,def_per_time]
						added_skaters[1] += 1
						line_values['off_per_time'] += off_per_time
						line_values['def_per_time'] += def_per_time
					if added_skaters[0] == game_status[ct + '_number_of_skaters'][0]:
						add_more_d = False
					if added_skaters[1] == game_status[ct + '_number_of_skaters'][1]:
						add_more_f = False
					if (add_more_d == False) and (add_more_f == False):
						break
					#print('Adding player: ' + skater.name)
					#print('Added skaters: ' + str(added_skaters))
					#print('ht_number_of_skaters: ' + str(game_status['ht_number_of_skaters']))
					#if (added_skaters[0] == game_status['ht_number_of_skaters'][0]) and (added_skaters[1] == game_status['ht_number_of_skaters'][1]):
						#break
		game_status[ct + '_on_ice_db'] = ct_on_ice_db
		lines_on_ice[i] = line_values
	if verbose:
		print(game_status['time_str'] + ': Players on the ice for ' + game_status['ht_id'] + ': ' + str(game_status['ht_on_ice_db'].keys()))
		print(game_status['time_str'] + ': Players on the ice for ' + game_status['at_id'] + ': ' + str(game_status['at_on_ice_db'].keys()))
	return game_status

def get_starting_goalie(goalie_db,team_id):
	found_goalie = False
	while found_goalie == False:
		for goalie_id in set(goalie_db.keys()):
			goalie = get_player(goalie_db, goalie_id)
			if (goalie.bio['team_id'] == team_id) and (random.uniform(0,1) < goalie.toi_pcg) and (goalie_id not in get_unavailable_players()[goalie.bio['team_id']]):		
				found_goalie = True
				return goalie_id

def get_time_str(game_status):
	m = game_status['time']//60
	s = game_status['time']%60
	if m < 10:
		m = str('0'+str(m))
	else:
		m = str(m)

	if s < 10:
		s = str('0'+str(s))
	else:
		s = str(s)

	game_status['time_str'] = str(m + ':' + s)
	
	return game_status

def get_playoff_cut(team_db):
	# Returns the lowest point value needed to make the playoffs in each division

	[tmp,div_a,div_b] = create_tables(team_db,'eastern',False,True)
	wild_card_east = [div_a[3],div_a[4],div_b[3],div_b[4]]
	wild_card_east.sort(reverse=True)

	[tmp,div_a,div_b] = create_tables(team_db,'western',False,True)
	wild_card_west = [div_a[3],div_a[4],div_b[3],div_b[4]]
	wild_card_west.sort(reverse=True)

	return [wild_card_east[1][0], wild_card_west[1][0]]

def get_playoff_teams(t1,t2):
	wc = [t1[3],t1[4],t2[3],t2[4]] 					# wc = wild card
	top = [t1[0],t2[0]]
	wc.sort(reverse=True)
	top.sort(reverse=True)
	[c7, c8] = [wc[0], wc[1]]
	[c1, c2] = [top[0], top[1]]

	return [(c1[1],c8[1]),(c2[1],c7[1]),(t1[1][1],t1[2][1]),(t2[1][1],t2[2][1])]

def create_playoff_tree(playoff_teams,simulation_param,verbose=True):
	''' Returns the conference champion, conference finalists and division finalists '''

	division_finals = [None, None, None, None]
	conference_finals = [None, None]
	conference_champ = None

	# Round 1, game 1
	simulation_param['ht_id'] = playoff_teams[0][0]
	simulation_param['at_id'] = playoff_teams[0][1]
	if verbose:
		print('Simulating first round playoff game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
	in_game_data = create_game_specific_db(simulation_param)
	in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
	if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
		division_finals[0] = simulation_param['ht_id']
		if verbose:
			print(simulation_param['ht_id'] + ' wins')
	else:
		division_finals[0] = simulation_param['at_id']
		if verbose:
			print(simulation_param['at_id'] + ' wins')

	# Round 1, game 3
	simulation_param['ht_id'] = playoff_teams[1][0]
	simulation_param['at_id'] = playoff_teams[1][1]
	if verbose:
		print('Simulating first round playoff game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
	in_game_data = create_game_specific_db(simulation_param)
	in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
	if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
		division_finals[2] = simulation_param['ht_id']
		if verbose:
			print(simulation_param['ht_id'] + ' wins')
	else:
		division_finals[2] = simulation_param['at_id']
		if verbose:
			print(simulation_param['at_id'] + ' wins')
	
	if (get_team(simulation_param['databases']['team_db'],playoff_teams[0][0]).division == 'C') or (get_team(simulation_param['databases']['team_db'],playoff_teams[0][0]).division == 'A'):
		# Different match-up depending on the result in the regular seasson.
		# Round 1, game 2
		simulation_param['ht_id'] = playoff_teams[2][0]
		simulation_param['at_id'] = playoff_teams[2][1]
		if verbose:
			print('Simulating first round playoff game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
		in_game_data = create_game_specific_db(simulation_param)
		in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
		if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
			division_finals[1] = simulation_param['ht_id']
			if verbose:
				print(simulation_param['ht_id'] + ' wins')
		else:
			division_finals[1] = simulation_param['at_id']
			if verbose:
				print(simulation_param['at_id'] + ' wins')

		# Round 1, game 4
		simulation_param['ht_id'] = playoff_teams[3][0]
		simulation_param['at_id'] = playoff_teams[3][1]
		if verbose:
			print('Simulating first round playoff game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
		in_game_data = create_game_specific_db(simulation_param)
		in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
		if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
			division_finals[3] = simulation_param['ht_id']
			if verbose:
				print(simulation_param['ht_id'] + ' wins')
		else:
			division_finals[3] = simulation_param['at_id']
			if verbose:
				print(simulation_param['at_id'] + ' wins')
	else:
		# Round 1, game 2
		simulation_param['ht_id'] = playoff_teams[3][0]
		simulation_param['at_id'] = playoff_teams[3][1]
		if verbose:
			print('Simulating first round playoff game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
		in_game_data = create_game_specific_db(simulation_param)
		in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
		if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
			division_finals[1] = simulation_param['ht_id']
			if verbose:
				print(simulation_param['ht_id'] + ' wins')
		else:
			division_finals[1] = simulation_param['at_id']
			if verbose:
				print(simulation_param['at_id'] + ' wins')
		# Round 1, game 4
		simulation_param['ht_id'] = playoff_teams[2][0]
		simulation_param['at_id'] = playoff_teams[2][1]
		if verbose:
			print('Simulating first round playoff game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
		in_game_data = create_game_specific_db(simulation_param)
		in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
		if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
			division_finals[3] = simulation_param['ht_id']
			if verbose:
				print(simulation_param['ht_id'] + ' wins')
		else:
			division_finals[3] = simulation_param['at_id']
			if verbose:
				print(simulation_param['at_id'] + ' wins')
	if verbose:
		print('Division finals: ' + str(division_finals))

	# Simulating division finals
	simulation_param['ht_id'] = division_finals[0]
	simulation_param['at_id'] = division_finals[1]
	if verbose:
		print('Simulating division final game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
	in_game_data = create_game_specific_db(simulation_param)
	in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
	if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
		conference_finals[0] = simulation_param['ht_id']
		if verbose:
			print(simulation_param['ht_id'] + ' wins')
	else:
		conference_finals[0] = simulation_param['at_id']
		if verbose:
			print(simulation_param['at_id'] + ' wins')
	
	simulation_param['ht_id'] = division_finals[2]
	simulation_param['at_id'] = division_finals[3]
	if verbose:
		print('Simulating division final game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
	in_game_data = create_game_specific_db(simulation_param)
	in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
	if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
		conference_finals[1] = simulation_param['ht_id']
		if verbose:
			print(simulation_param['ht_id'] + ' wins')
	else:
		conference_finals[1] = simulation_param['at_id']
		if verbose:
			print(simulation_param['at_id'] + ' wins')
	if verbose:
		print('Conference finals: ' + str(conference_finals))

	simulation_param['ht_id'] = conference_finals[0]
	simulation_param['at_id'] = conference_finals[1]
	if verbose:
		print('Simulating conference final game between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'])
	in_game_data = create_game_specific_db(simulation_param)
	in_game_data['ht'].simulate_game(in_game_data['at'],simulation_param,in_game_data)
	if in_game_data['ht'].gf_in_simulated_game > in_game_data['at'].gf_in_simulated_game:
		conference_champ = simulation_param['ht_id']
		if verbose:
			print(simulation_param['ht_id'] + ' wins')
	else:
		conference_champ = simulation_param['at_id']
		if verbose:
			print(simulation_param['at_id'] + ' wins')
	if verbose:
		print('Conference champion: ' + str(conference_champ))

	return [conference_champ, conference_finals, division_finals]

def create_tables(team_db,key,print_to_cmd=True,store=False):
	tl_league,tl_eastern,tl_western,tl_atlantic,tl_metro,tl_central,tl_pacific = [],[],[],[],[],[],[]
	
	for team_id in team_db.keys():
		team = get_team(team_db,team_id)
		tl_league.append((team.p,team_id))
		if team.division == 'A':
			tl_eastern.append((team.p,team_id))
			tl_atlantic.append((team.p,team_id))
		elif team.division == 'M':
			tl_eastern.append((team.p,team_id))
			tl_metro.append((team.p,team_id))
		elif team.division == 'C':
			tl_western.append((team.p,team_id))
			tl_central.append((team.p,team_id))
		else:
			tl_western.append((team.p,team_id))
			tl_pacific.append((team.p,team_id))		
	
	show_all_stats = True
	if team.gp == 82:
		show_al_stats = True

	tl_league.sort(reverse=True)
	tl_eastern.sort(reverse=True)
	tl_western.sort(reverse=True)
	tl_atlantic.sort(reverse=True)
	tl_metro.sort(reverse=True)
	tl_central.sort(reverse=True)
	tl_pacific.sort(reverse=True)	
	
	if key == 'league':
		if print_to_cmd:
			print('Projected standings for League')
			for i,pair in enumerate(tl_league):
				if show_all_stats:
					team = get_team(team_db,pair[1])
					print('{0}: {1} - {2:.1f} [GP: {3}, W: {4}, L: {5}, OTL: {6}]'.format(str(i+1),pair[1],pair[0],team.gp,team.w,team.l,team.otl))
				else:
					print('{0}: {1} - {2:.1f}'.format(str(i+1),pair[1],pair[0]))
		if store:
			return tl_league
	elif key == 'eastern':
		if print_to_cmd:
			print('Projected standings for Eastern Conference')
			for i,pair in enumerate(tl_eastern):
				if show_all_stats:
					team = get_team(team_db,pair[1])
					print('{0}: {1} - {2:.1f} [GP: {3}, W: {4}, L: {5}, OTL: {6}]'.format(str(i+1),pair[1],pair[0],team.gp,team.w,team.l,team.otl))
				else:
					print('{0}: {1} - {2:.1f}'.format(str(i+1),pair[1],pair[0]))
		if store:
			return [tl_eastern,tl_atlantic,tl_metro]
	elif key == 'western':
		if print_to_cmd:
			print('Projected standings for Western Conference')
			for i,pair in enumerate(tl_western):
				if show_all_stats:
					team = get_team(team_db,pair[1])
					print('{0}: {1} - {2:.1f} [GP: {3}, W: {4}, L: {5}, OTL: {6}]'.format(str(i+1),pair[1],pair[0],team.gp,team.w,team.l,team.otl))
				else:
					print('{0}: {1} - {2:.1f}'.format(str(i+1),pair[1],pair[0]))	
		if store:
			return [tl_western,tl_central,tl_pacific]
	elif key == 'atlantic':
		if print_to_cmd:
			print('Projected standings for Atlantic Division')
			for i,pair in enumerate(tl_atlantic):				
				if show_all_stats:
					team = get_team(team_db,pair[1])
					print('{0}: {1} - {2:.1f} [GP: {3}, W: {4}, L: {5}, OTL: {6}]'.format(str(i+1),pair[1],pair[0],team.gp,team.w,team.l,team.otl))
				else:
					print('{0}: {1} - {2:.1f}'.format(str(i+1),pair[1],pair[0]))
		if store:
			return tl_atlantic
	elif key == 'metro':
		if print_to_cmd:
			print('Projected standings for Metropolitan Division')
			for i,pair in enumerate(tl_metro):
				if show_all_stats:
					team = get_team(team_db,pair[1])
					print('{0}: {1} - {2:.1f} [GP: {3}, W: {4}, L: {5}, OTL: {6}]'.format(str(i+1),pair[1],pair[0],team.gp,team.w,team.l,team.otl))
				else:
					print('{0}: {1} - {2:.1f}'.format(str(i+1),pair[1],pair[0]))
		if store:
			return tl_metro
	elif key == 'central':
		if print_to_cmd:
			print('Projected standings for Central Division')
			for i,pair in enumerate(tl_central):
				if show_all_stats:
					team = get_team(team_db,pair[1])
					print('{0}: {1} - {2:.1f} [GP: {3}, W: {4}, L: {5}, OTL: {6}]'.format(str(i+1),pair[1],pair[0],team.gp,team.w,team.l,team.otl))
				else:
					print('{0}: {1} - {2:.1f}'.format(str(i+1),pair[1],pair[0]))
		if store:
			return tl_central
	elif key == 'pacific':
		if print_to_cmd:
			print('Projected standings for Pacific Division')
			for i,pair in enumerate(tl_pacific):
				if show_all_stats:
					team = get_team(team_db,pair[1])
					print('{0}: {1} - {2:.1f} [GP: {3}, W: {4}, L: {5}, OTL: {6}]'.format(str(i+1),pair[1],pair[0],team.gp,team.w,team.l,team.otl))
				else:
					print('{0}: {1} - {2:.1f}'.format(str(i+1),pair[1],pair[0]))
		if store:
			return tl_pacific
	else:
		raise ValueError('wrong key')

def create_game_specific_db(simulation_param):

	# Create 'sub-versions' of the player_db, containing only the players in the current game.
	ht_skater_db, at_skater_db = {},{}
	ht_skater_db = simulation_param['databases']['team_specific_db'][simulation_param['ht_id']]
	at_skater_db = simulation_param['databases']['team_specific_db'][simulation_param['at_id']]

	# Set up data_param, containing information about the players in the game.
	data_param = {}
	data_param['ht_skaters'] = ht_skater_db								# Separate 'skaters' and 'goalies'. 'players' = union('skaters','goalies')
	data_param['at_skaters'] = at_skater_db								# Separate 'skaters' and 'goalies'. 'players' = union('skaters','goalies')
	data_param['ht_players'] = copy.deepcopy(ht_skater_db)
	data_param['at_players'] = copy.deepcopy(at_skater_db)
	data_param['teams'] = simulation_param['databases']['team_db']
	data_param['ht'] = get_team(simulation_param['databases']['team_db'],simulation_param['ht_id'])
	data_param['at'] = get_team(simulation_param['databases']['team_db'],simulation_param['at_id'])
	
	# Add the starting goalie to the ht/at-player_db.
	if simulation_param['databases']['starting_goalies'][simulation_param['ht_id']] != None:
		data_param['ht_goalie'] = simulation_param['databases']['starting_goalies'][simulation_param['ht_id']]
		print('Starting goalie for ' + simulation_param['ht_id'] + ': ' + data_param['ht_goalie'])
	else:
		data_param['ht_goalie'] = get_starting_goalie(simulation_param['databases']['goalie_db'],simulation_param['ht_id'])
	data_param['ht_players'][data_param['ht_goalie']] = get_player(simulation_param['databases']['goalie_db'],data_param['ht_goalie'])

	if simulation_param['databases']['starting_goalies'][simulation_param['at_id']] != None:
		data_param['at_goalie'] = simulation_param['databases']['starting_goalies'][simulation_param['at_id']]
		print('Starting goalie for ' + simulation_param['at_id'] + ': ' + data_param['at_goalie'])
	else:
		data_param['at_goalie'] = get_starting_goalie(simulation_param['databases']['goalie_db'],simulation_param['at_id'])
	data_param['at_players'][data_param['at_goalie']] = get_player(simulation_param['databases']['goalie_db'],data_param['at_goalie'])
	
	return data_param

def simulate_po_series(simulation_param,teams,initial_wins):
	simulation_param['ht_id'] = teams[0]
	simulation_param['at_id'] = teams[1]
	N_sim = simulation_param['N'][simulation_param['simulation_mode']]
	in_game_data = create_game_specific_db(simulation_param)
	print('\nSimulating playoff series between ' + simulation_param['ht_id'] + ' and ' + simulation_param['at_id'] + '. Number of simulations = ' + str(N_sim) + '.')
	series_distribution = [0,0,0,0,0,0,0,0]
	t0_tmp = time.time()
	for i in range(N_sim):
		print_progress(i,N_sim,t0_tmp,step=20)
		series_done = False
		wins_in_series = list(initial_wins)
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
	return series_distribution
