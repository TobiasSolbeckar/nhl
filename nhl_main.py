from nhl_database import *
from nhl_simulation import *
from nhl_defines import * 
from nhl_helpers import *
from nhl_classes import *

def setup_csv_path(simulation_param):
	data_dir = simulation_param['data_dir']
	simulation_param['csvfiles'] = {}
	simulation_param['csvfiles']['schedule'] = os.path.join(data_dir,'2019_2020_NHL_Schedule.csv')
	simulation_param['csvfiles']['team_es'] = os.path.join(data_dir,'Team_ES_201920.csv')
	simulation_param['csvfiles']['team_pp'] = os.path.join(data_dir,'Team_PP_201920.csv')
	simulation_param['csvfiles']['team_pk'] = os.path.join(data_dir,'Team_PK_201920.csv')
	simulation_param['csvfiles']['team_home'] = os.path.join(data_dir,'Team_Home_201819_201920.csv')
	simulation_param['csvfiles']['team_away'] = os.path.join(data_dir,'Team_Away_201819_201920.csv')
	simulation_param['csvfiles']['goalie_bio'] = os.path.join(data_dir,'Goalie_ES_201920.csv')
	simulation_param['csvfiles']['skater_relative'] = os.path.join(data_dir,'Skater_Relative_201819_201920.csv')
	simulation_param['csvfiles']['skater_old_bio'] = os.path.join(data_dir,'Skater_Bio_201819.csv')
	simulation_param['csvfiles']['skater_bio'] = os.path.join(data_dir,'Skater_Bio_201920.csv')

	simulation_param['csvfiles']['skater_es'] = []
	simulation_param['csvfiles']['skater_pp'] = []
	simulation_param['csvfiles']['skater_pk'] = []
	simulation_param['csvfiles']['skater_on_ice'] = []
	simulation_param['csvfiles']['goalie_es'] = []
	simulation_param['csvfiles']['goalie_pp'] = []
	simulation_param['csvfiles']['goalie_pk'] = []
	for season in simulation_param['seasons']:
		simulation_param['csvfiles']['skater_es'].append(os.path.join(data_dir,'Skater_Individual_ES_' + season + '.csv'))
		simulation_param['csvfiles']['skater_pp'].append(os.path.join(data_dir,'Skater_Individual_PP_' + season + '.csv'))
		simulation_param['csvfiles']['skater_pk'].append(os.path.join(data_dir,'Skater_Individual_PK_' + season + '.csv'))
		simulation_param['csvfiles']['skater_on_ice'].append(os.path.join(data_dir,'Skater_OnIce_' + season + '.csv'))	
		simulation_param['csvfiles']['goalie_es'].append(os.path.join(data_dir,'Goalie_ES_' + season + '.csv'))
		simulation_param['csvfiles']['goalie_pp'].append(os.path.join(data_dir,'Goalie_PP_' + season + '.csv'))
		simulation_param['csvfiles']['goalie_pk'].append(os.path.join(data_dir,'Goalie_PK_' + season + '.csv'))

	# Make sure all CSV-files are availble
	for key in simulation_param['csvfiles']:
		filepath = simulation_param['csvfiles'][key]
		if isinstance(filepath,list) == True:
			for sub_path in filepath:
				if os.path.exists(sub_path) == False:
					print(os.path.basename(sub_path).split('.')[0])
					raise ValueError('CSV file ' + sub_path + ' does not exist.')
		else:
			if os.path.exists(filepath) == False:
				raise ValueError('CSV file ' + filepath + ' does not exist.')

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
	sp['days_rested'] = [[-1,-1]]
	sp['do_exp'] = False
	sp['do_player_cards'] = False
	sp['simulation_date'] = None
	sp['down_sample'] = False
	sp['initial_time'] = 0 										# Initial time in seconds
	sp['initial_ht_goals'] = 0
	sp['initial_at_goals'] = 0
	sp['do_plots'] = True
	sp['exp_team'] = None
	sp['add_average_goalies'] = None
	sp['exp_temp_attributes'] = None
	sp['exp_playform'] = STAT_ES
	sp['exp_position'] = ['F','D']
	sp['exp_additional_players'] = []
	sp['data_dir'] = 'Data'
	sp['backup_dir'] = 'Data_backup'
	sp['url_skater_bio_201819'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20182019&thruseason=20182019&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	sp['url_skater_bio'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	sp['url_skater_ind_es'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
	sp['url_skater_ind_pp'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v4&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
	sp['url_skater_ind_pk'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=4v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
	sp['url_skater_on_ice'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=oi&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
	sp['url_skater_relative'] = "http://naturalstattrick.com/playerteams.php?fromseason=20182019&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=oi&rate=r&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	sp['url_goalie_201819_201920'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20182019&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	sp['url_goalie_es_201920'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	sp['url_goalie_pp_201920'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v4&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	sp['url_goalie_pk_201920'] = "https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=4v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	sp['url_team_es'] = "https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
	sp['url_team_pp'] = "https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v4&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
	sp['url_team_pk'] = "https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=4v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="
	sp['url_team_home'] = "http://naturalstattrick.com/teamtable.php?fromseason=20182019&thruseason=20192020&stype=2&sit=5v5&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td="
	sp['url_team_away'] = "http://naturalstattrick.com/teamtable.php?fromseason=20182019&thruseason=20192020&stype=2&sit=5v5&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td="
	# Create paths to data files.
	sp = setup_csv_path(sp)
	
	return sp

################################################################################################################################################
################################################################################################################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Improvements:
# @TODO: Collect all TODOs in Trello.
# @TODO: use gameplay_state-specific data in put_players_on_ice()
# @TODO: It should be possible to easy update particular attributes, e.g. g_db = modify_attribute(g_db,'MARTIN_JONES','sv_pcg',0.915)
# @TODO: Create an "smoothed" SH% value for each team? E.g. removing all values outside of league average + 1 sigma?
# @TODO: Implement "what-if" (for season)
# @TODO: Simulate per day, rather than per team? How would that work when there is no games at a particular date?
# @TODO: Output from team_db_row_value looks ugly (too long)

# Investigations:
# @TODO: What happens if using all-situation (instead of 5v5) for sv_pcg during simulation?
# @TODO: Review game_status/data_param/simulation_param parameters. Are all necessary?
# @TODO: Something is weird with the penalty generating (and drawing of).
# @TODO: Use OnIce-data for SF% (or something)?
# @TODO: Use PP/PK specific data for sa for teams?

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
today = datetime.datetime.today().strftime('%Y-%m-%d')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
simulation_param = {}
simulation_param['seasons'] = ['201920']	#download_old_season_data(['201718'])
simulation_param['write_to_gsheet'] = False
simulation_param['generate_fresh_databases'] = False

simulation_param = create_simulation_parameters(simulation_param)
simulation_param['offseason'] = False
simulation_param['include_offseason_moves'] = False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#simulation_param['simulate_ind_games'] = True								# Default value = False
#simulation_param['simulate_playoff_series'] = True
#simulation_param['simulate_season'] = True									# Default value = False
simulation_param['do_exp'] = True 											# Default value = False
#simulation_param['do_player_cards'] = True
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Simulation/iteration parameters
#simulation_param['simulation_mode'] = SIMULATION_LIGHT 						# SIMULATION_LIGHT or SIMULATION_EXT
simulation_param['N'] = [50000,2500]											# Number of simulations for each game/season. Default = [50000,2500]
simulation_param['debug_team'] = None
simulation_param['debug_player'] = ['ERIK_KARLSSON']

# Create databases.
#simulation_param['add_average_goalies'] = ['CAR']
simulation_param = create_databases(simulation_param)

# Set starting goaltenders.
simulation_param = set_starting_goalie(simulation_param,'ANA','JOHN_GIBSON') #RYAN_MILLER
simulation_param = set_starting_goalie(simulation_param,'ARI','DARCY_KUEMPER') #ANTTI_RAANTA
simulation_param = set_starting_goalie(simulation_param,'BOS','JAROSLAV_HALAK') #TUUKKA_RASK
simulation_param = set_starting_goalie(simulation_param,'BUF','JONAS_JOHANSSON') #CARTER_HUTTON
simulation_param = set_starting_goalie(simulation_param,'CAR','ALEX_NEDELJKOVIC') #PETR_MRAZEK ; ANTON_FORSBERG
simulation_param = set_starting_goalie(simulation_param,'CBJ','JOONAS_KORPISALO') #ELVIS_MERZLIKINS
simulation_param = set_starting_goalie(simulation_param,'CGY','CAM_TALBOT') #DAVID_RITTICH
#simulation_param = set_starting_goalie(simulation_param,'CHI','COREY_CRAWFORD') #MALCOLM_SUBBAN
#simulation_param = set_starting_goalie(simulation_param,'COL','PAVEL_FRANCOUZ') #
simulation_param = set_starting_goalie(simulation_param,'DAL','ANTON_KHUDOBIN') #BEN_BISHOP
#simulation_param = set_starting_goalie(simulation_param,'DET','JONATHAN_BERNIER') #JIMMY_HOWARD
simulation_param = set_starting_goalie(simulation_param,'EDM','MIKE_SMITH') #MIKKO_KOSKINEN
#simulation_param = set_starting_goalie(simulation_param,'FLA','SERGEI_BOBROVSKY') #
#simulation_param = set_starting_goalie(simulation_param,'LAK','') #
simulation_param = set_starting_goalie(simulation_param,'MIN','ALEX_STALOCK') # DEVAN_DUBNYK
simulation_param = set_starting_goalie(simulation_param,'MTL','CAREY_PRICE') #
simulation_param = set_starting_goalie(simulation_param,'NJD','CORY_SCHNEIDER') # MACKENZIE_BLACKWOOD
simulation_param = set_starting_goalie(simulation_param,'NYI','SEMYON_VARLAMOV') # THOMAS_GREISS
simulation_param = set_starting_goalie(simulation_param,'NYR','ALEXANDAR_GEORGIEV') #IGOR_SHESTERKIN
simulation_param = set_starting_goalie(simulation_param,'NSH','JUUSE_SAROS') #
simulation_param = set_starting_goalie(simulation_param,'OTT','CRAIG_ANDERSON') #MARCUS_HOGBERG
simulation_param = set_starting_goalie(simulation_param,'PHI','CARTER_HART') #BRIAN_ELLIOTT
simulation_param = set_starting_goalie(simulation_param,'PIT','MATT_MURRAY') #TRISTAN_JARRY
simulation_param = set_starting_goalie(simulation_param,'SJS','MARTIN_JONES') #AARON_DELL
simulation_param = set_starting_goalie(simulation_param,'STL','JORDAN_BINNINGTON') #
simulation_param = set_starting_goalie(simulation_param,'TBL','ANDREI_VASILEVSKIY') #CURTIS_MCELHINNEY
simulation_param = set_starting_goalie(simulation_param,'TOR','JACK_CAMPBELL') #FREDERIK_ANDERSEN
#simulation_param = set_starting_goalie(simulation_param,'VAN','THATCHER_DEMKO') #JACOB_MARKSTROM
simulation_param = set_starting_goalie(simulation_param,'VGK','MARC-ANDRE_FLEURY') #ROBIN_LEHNER
simulation_param = set_starting_goalie(simulation_param,'WPG','CONNOR_HELLEBUYCK') #LAURENT_BROSSOIT
simulation_param = set_starting_goalie(simulation_param,'WSH','ILYA_SAMSONOV') #BRADEN_HOLTBY

# Gameplay parameters 
simulation_param['simulation_date'] = today
simulation_param['games_to_simulate'] = simulation_param['databases']['season_schedule'][simulation_param['simulation_date']]
#simulation_param['games_to_simulate'] = [['SJS','PIT']]
#simulation_param['days_rested'] = [[1,0]]
#simulation_param['initial_wins'] = [[0,0]]
#simulation_param['down_sample'] = False
#simulation_param['initial_time'] = 60*(20+20+16) # Initial time in seconds
#simulation_param['initial_ht_goals'] = 5
#simulation_param['initial_at_goals'] = 0

# Analytics parameters
simulation_param['team_plots'] = False
simulation_param['exp_min_toi'] = 100
simulation_param['exp_list_length'] = 15
#simulation_param['exp_team'] = None
simulation_param['exp_position'] = ['D','F']
simulation_param['exp_weighted_scale'] = WS_FWD
#simulation_param['exp_playform'] = STAT_PK
#simulation_param['exp_temp_attributes'] = ['primary_points_per_60']
#simulation_param['exp_additional_players'] = simulation_param['databases']['team_rosters']['SJS_F']
#simulation_param['exp_additional_players'] = ['ARTEMI_PANARIN']
simulation_param['exp_show_player_ranking'] = False

# Output/print parameters
simulation_param['print_times'] = False
simulation_param['verbose'] = False
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''
attributes = ['sf_pcg','gf_pcg','cf_pcg','ff_pcg','xgf_pcg','scf_pcg']
true_attribute = 'gf_pcg'
for attribute in attributes:
	x_array = []
	y_array = []	
	for team_id in ACTIVE_TEAMS:
		team = simulation_param['databases']['team_db'][team_id]
		x_array.append(team.rank[attribute])
		y_array.append(team.rank[true_attribute])
	print(attribute + ': ' + str(get_k_factor(x_array,y_array,True)))
'''

# For now, matplotlib cannot be loaded for Windows machines.
if platform.system() == 'Windows':
	print('Cannot do plots on Windows-platform')
	simulation_param['do_plots'] = False
	print('Cannot write to Google on Windows-platform')
	simulation_param['write_to_gsheet'] = False

if simulation_param['simulate_ind_games']:
	if simulation_param['simulation_mode'] == None:
		simulation_param['simulation_mode'] = SIMULATION_EXT

	N_sim = simulation_param['N'][simulation_param['simulation_mode']]
	for i,game in enumerate(simulation_param['games_to_simulate']):
		t0 = 1000*time.time()
		simulation_param['ht_id'] = game[0]
		simulation_param['at_id'] = game[1]
		in_game_data = create_game_specific_db(simulation_param)
		print('\n\nSimulating outcome of ' + simulation_param['ht_id'] + ' (HOME) vs. ' + simulation_param['at_id'] + ' (AWAY). Number of simulations = ' + str(N_sim) + '. Simulation model = ' + str(simulation_param['simulation_mode']))
		print('GOALIE ({0}): {1} (SV: {2:.1f}%, GAA: {3:.2f})'.format(simulation_param['ht_id'],in_game_data['ht_goalie'],100*simulation_param['databases']['goalie_db'][in_game_data['ht_goalie']].ind['sv_pcg'][STAT_ES],simulation_param['databases']['goalie_db'][in_game_data['ht_goalie']].ind['gaa'][STAT_ES]))
		print('GOALIE ({0}): {1} (SV: {2:.1f}%, GAA: {3:.2f})'.format(simulation_param['at_id'],in_game_data['at_goalie'],100*simulation_param['databases']['goalie_db'][in_game_data['at_goalie']].ind['sv_pcg'][STAT_ES],simulation_param['databases']['goalie_db'][in_game_data['at_goalie']].ind['gaa'][STAT_ES]))
		if simulation_param['verbose']:
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
		if simulation_param['simulation_date'] == None:
			ht_fatigue_factor = 1
			at_fatigue_factor = 1
		else:
			ht_team = simulation_param['databases']['team_db'][simulation_param['ht_id']]
			at_team = simulation_param['databases']['team_db'][simulation_param['at_id']]
			ht_days_rested = get_days_rested(simulation_param['ht_id'],simulation_param)
			at_days_rested = get_days_rested(simulation_param['at_id'],simulation_param)
			if ht_days_rested > 2:
				ht_days_rested = 2
			if at_days_rested > 2:
				at_days_rested = 2
			ht_fatigue_factor = ht_team.fatigue['per_days_rested'][ht_days_rested]['p_pcg_rel']
			at_fatigue_factor = at_team.fatigue['per_days_rested'][at_days_rested]['p_pcg_rel']

		ht_g_prob = ht_g/(ht_g+at_g)
		at_g_prob = at_g/(ht_g+at_g)
		print('\nProbability (goals):  {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*ht_g_prob,100*at_g_prob,simulation_param['at_id']))
		ht_g_venue = ht_g * get_home_team_advantage(simulation_param['databases']['team_db'],simulation_param['ht_id'],simulation_param['at_id'])
		at_g_venue = at_g
		ht_g_prob_venue = ht_g_venue/(ht_g_venue+at_g_venue)
		at_g_prob_venue = at_g_venue/(ht_g_venue+at_g_venue)
		print('Probability (goals, venue adjusted):  {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*ht_g_prob_venue,100*at_g_prob_venue,simulation_param['at_id']))
		ht_g_venue_and_fatigue = ht_g_venue * ht_fatigue_factor
		at_g_venue_and_fatigue = at_g_venue * at_fatigue_factor
		ht_g_prob_venue_and_fatigue = ht_g_venue_and_fatigue/(ht_g_venue_and_fatigue+at_g_venue_and_fatigue)
		at_g_prob_venue_and_fatigue = at_g_venue_and_fatigue/(ht_g_venue_and_fatigue+at_g_venue_and_fatigue)
		print('Probability (goals, venue and fatigue adjusted):  {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*ht_g_prob_venue_and_fatigue,100*at_g_prob_venue_and_fatigue,simulation_param['at_id']))
		print('   Average score: {0} {1:.2f} - {2:.2f} {3}'.format(simulation_param['ht_id'],ht_g/N_sim,at_g/N_sim,simulation_param['at_id']))
		if simulation_param['simulation_mode'] == SIMULATION_EXT:
			#print('   Average shots: {0} {1:.0f} - {2:.0f} {3}'.format(simulation_param['ht_id'],ht_s/N_sim,at_s/N_sim,simulation_param['at_id']))
			print('   Average shots EXP: {0} {1:.0f} - {2:.0f} {3}'.format(simulation_param['ht_id'],ht_exp_s/N_sim,at_exp_s/N_sim,simulation_param['at_id']))
		
		ht_rating = simulation_param['databases']['team_db'][simulation_param['ht_id']].exp_data['in_season_rating']
		at_rating = simulation_param['databases']['team_db'][simulation_param['at_id']].exp_data['in_season_rating']
		ht_rating_prob = ht_rating/(ht_rating+at_rating)
		at_rating_prob = at_rating/(ht_rating+at_rating)
		print('Probability (rating): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*ht_rating_prob,100*at_rating_prob,simulation_param['at_id']))
		ht_rating_venue = ht_rating * get_home_team_advantage(simulation_param['databases']['team_db'],simulation_param['ht_id'],simulation_param['at_id'])
		at_rating_venue = at_rating
		ht_rating_prob_venue = ht_rating_venue/(ht_rating_venue+at_rating_venue)
		at_rating_prob_venue = at_rating_venue/(ht_rating_venue+at_rating_venue)
		print('Probability (rating, venue adjusted): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*ht_rating_prob_venue,100*at_rating_prob_venue,simulation_param['at_id']))
		ht_rating_venue_and_fatigue = ht_rating_venue * ht_fatigue_factor
		at_rating_venue_and_fatigue = at_rating_venue * at_fatigue_factor
		ht_rating_prob_venue_and_fatigue = ht_rating_venue_and_fatigue/(ht_rating_venue_and_fatigue+at_rating_venue_and_fatigue)
		at_rating_prob_venue_and_fatigue = at_rating_venue_and_fatigue/(ht_rating_venue_and_fatigue+at_rating_venue_and_fatigue)
		print('Probability (rating, venue and fatigue adjusted): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*ht_rating_prob_venue_and_fatigue,100*at_rating_prob_venue_and_fatigue,simulation_param['at_id']))

		if (simulation_param['initial_time'] > 0) or ((simulation_param['initial_ht_goals'] + simulation_param['initial_at_goals']) > 0):
			print('Probability (wins): {0} {1:.1f}% - {2:.1f}% {3}'.format(simulation_param['ht_id'],100*get_probability([ht_w,at_w]),100*get_probability([at_w,ht_w]),simulation_param['at_id']))

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
	g_db = simulation_param['databases']['goalie_db']
	t_db = simulation_param['databases']['team_db']
	f_add = lambda a,b : a+b
	f_sub = lambda a,b : a-b
	f_mult = lambda a,b : a*b
	f_div = lambda a,b : a/b
	
	'''
	# Print data for SJS-lines
	
	#lines = [['MARC-EDOUARD_VLASIC','ERIK_KARLSSON'],['MARIO_FERRARO','TIM_HEED'],['RADIM_SIMEK','BRENT_BURNS'],['JACOB_MIDDLETON'],['EVANDER_KANE','TOMAS_HERTL','KEVIN_LABANC'],['PATRICK_MARLEAU','LOGAN_COUTURE','JONNY_BRODZINSKI'],['TIMO_MEIER','JOE_THORNTON','BARCLAY_GOODROW'],['ANTTI_SUOMELA','JOEL_KELLMAN','MELKER_KARLSSON'],['MARCUS_SORENSEN','STEFAN_NOESEN','JOACHIM_BLICHFELD']]
	#lines = [['EVANDER_KANE','TOMAS_HERTL','TIMO_MEIER'],['BARCLAY_GOODROW','JOE_THORNTON','KEVIN_LABANC'],['MARCUS_SORENSEN','DYLAN_GAMBRELL','PATRICK_MARLEAU'],['STEFAN_NOESEN','JOEL_KELLMAN','MELKER_KARLSSON']]
	#now_lines = [['EVANDER_KANE','BARCLAY_GOODROW','TIMO_MEIER'],['PATRICK_MARLEAU','JOE_THORNTON','KEVIN_LABANC'],['MARCUS_SORENSEN','ANTTI_SUOMELA','DYLAN_GAMBRELL'],['STEFAN_NOESEN','JOEL_KELLMAN','MELKER_KARLSSON']]
	old_lines = [['TIMO_MEIER','LOGAN_COUTURE','JOE_PAVELSKI'],['EVANDER_KANE','TOMAS_HERTL','JOONAS_DONSKOI'],['MARCUS_SORENSEN','JOE_THORNTON','KEVIN_LABANC'],['MELKER_KARLSSON','CHRIS_TIERNEY','BARCLAY_GOODROW']]
	best_now_lines = [['EVANDER_KANE','LOGAN_COUTURE','TIMO_MEIER'],['PATRICK_MARLEAU','TOMAS_HERTL','KEVIN_LABANC'],['MARCUS_SORENSEN','JOE_THORNTON','BARCLAY_GOODROW'],['STEFAN_NOESEN','JOEL_KELLMAN','ANTTI_SUOMELA']]
	
	now_lines = [['EVANDER_KANE','LOGAN_COUTURE','NOAH_GREGOR'],['TIMO_MEIER','JOE_THORNTON','KEVIN_LABANC'],['STEFAN_NOESEN','JOEL_KELLMAN','MELKER_KARLSSON'],['MARCUS_SORENSEN','ANTTI_SUOMELA','DYLAN_GAMBRELL']]
	
	all_lines = [old_lines,best_now_lines,now_lines]
	all_lines = now_lines
	
	for line in now_lines:
		tmp_vals = evaluate_combination(simulation_param['databases']['skater_db'],line,attributes=['estimated_off_per_60','estimated_def_per_60'])
		print(100*tmp_vals[0]/(tmp_vals[0]+tmp_vals[1]))
	
	for p_id in s_db.keys():
		ca_per_60 = t_db[simulation_param['debug_team']].ca_per_60
		sa_per_60 = t_db[simulation_param['debug_team']].sa_per_60
		ga_per_60 = t_db[simulation_param['debug_team']].ga_per_60
		xga_per_60 = t_db[simulation_param['debug_team']].xga_per_60
		sca_per_60 = t_db[simulation_param['debug_team']].sca_per_60
		hdca_per_60 = t_db[simulation_param['debug_team']].hdca_per_60
		player = get_skater(s_db,p_id)
		if player.get_attribute('team_id') == simulation_param['debug_team']:
			if player.get_toi() > 100*60:
				print('{0}: CA/60: {1:.2f}%. SA/60: {2:.2f}%. GA/60: {3:.2f}%. xGA/60: {4:.2f}%. SCA/60: {5:.2f}%. HDCA: {6:.2f}%.'.format(p_id,100*player.get_attribute('ca_per_60')/ca_per_60,100*player.get_attribute('sa_per_60')/sa_per_60,100*player.get_attribute('ga_per_60')/ga_per_60,100*player.get_attribute('xga_per_60')/xga_per_60,100*player.get_attribute('sca_per_60')/sca_per_60,100*player.get_attribute('hdca_per_60')/hdca_per_60))
			else:
				print(p_id + ' has only played ' + str(player.get_toi()/60) + ' minutes.')
	'''

	tmp_list = []
	tmp_list_data = []
	for team_id in ACTIVE_TEAMS:
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

	for p_id in simulation_param['exp_additional_players']:
		player = s_db[p_id]
		player.print_player()

	# Evaluate different ranking models
	mse = defaultdict(float)
	mse['errors'] = defaultdict(list)
	true_label = 'p_pcg'
	for team_id in ACTIVE_TEAMS:
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
	if simulation_param['team_plots'] == True:
		# Set up color/markers
		markers = []
		colors = ['c','m','g','r','b'] # black and yellow are protected colors.
		forms = ['o','v','s','*','x','p','d']
		for form in forms:
			for color in colors:
				markers.append(str(form + color))
		figure_index = 1
		
		# Figure 1
		plt.figure(figure_index)
		# Subplot 1.1
		ax = plt.subplot(2,1,1)
		marker_idx = 0
		x_attribute = 'scf_pcg'
		y_attribute = 'estimated_off_pcg'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].exp_data[x_attribute]
			y = t_db[team_id].exp_data[y_attribute]
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		plt.xlabel(x_attribute)
		#ax.invert_yaxis() 
		plt.ylabel(y_attribute)
		font_size = np.min([200/len(ACTIVE_TEAMS),9])
		ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)
		plt.grid(True)
		# Subplot 1.2
		ax = plt.subplot(2,1,2)
		marker_idx = 0
		x_attribute = 'scf_per_60'
		y_attribute = 'sca_per_60'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].exp_data[x_attribute]
			y = t_db[team_id].exp_data[y_attribute]
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		ax.invert_yaxis() 
		# Plot stuff
		start = float(np.min([np.min(gen_x),np.min(gen_y)]))
		stop = float(np.max([np.max(gen_x),np.max(gen_y)]))
		plt.plot([0.95*start,1.05*stop],[0.95*start,1.05*stop],'k--',label='50% threshold')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.grid(True)
		figure_index += 1
		
		########################################################################################################################
		# Figure 2
		plt.figure(figure_index)
		# Subplot 2.1
		ax = plt.subplot(2,1,1)
		marker_idx = 0
		x_attribute = 'sh_pcg'
		y_attribute = 'sv_pcg'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].exp_data[x_attribute]*100
			y = t_db[team_id].exp_data[y_attribute]*100
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.grid(True)
		font_size = np.min([200/len(ACTIVE_TEAMS),9])
		ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)
		# Subplot 2.2
		ax = plt.subplot(2,1,2)
		marker_idx = 0
		x_attribute = 'estimated_off'
		y_attribute = 'estimated_def'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].exp_data[x_attribute]
			y = t_db[team_id].exp_data[y_attribute]
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
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
		ax = plt.subplot(3,1,1)
		marker_idx = 0
		x_attribute = 'cf_pcg'
		y_attribute = 'scf_pcg'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].cf_pcg
			y = t_db[team_id].scf_pcg
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		start = float(np.min([np.min(gen_x),np.min(gen_y)]))
		stop = float(np.max([np.max(gen_x),np.max(gen_y)]))
		plt.plot([0.95*start,1.05*stop],[0.95*start,1.05*stop],'k--',label='50% threshold')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		font_size = np.min([200/len(ACTIVE_TEAMS),9])
		ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)
		plt.grid(True)
		
		# Subplot 1.2
		ax = plt.subplot(3,1,2)
		marker_idx = 0
		x_attribute = 'scf_pcg'
		y_attribute = 'xgf_pcg'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].scf_pcg
			y = t_db[team_id].xgf_pcg
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		start = float(np.min([np.min(gen_x),np.min(gen_y)]))
		stop = float(np.max([np.max(gen_x),np.max(gen_y)]))
		plt.plot([0.95*start,1.05*stop],[0.95*start,1.05*stop],'k--',label='50% threshold')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.subplots_adjust(left=0.05,bottom=0.07,top=0.95,right=0.82,hspace=0.3)
		plt.grid(True)

		# Subplot 1.3
		ax = plt.subplot(3,1,3)
		marker_idx = 0
		x_attribute = 'This axis has no meaning'
		y_attribute = 'SCF - PPG [ranking]'
		gen_x, gen_y, labels = [],[],[]
		for team_id in ACTIVE_TEAMS:
			x = marker_idx
			y = t_db[team_id].rank['p_pcg'] - t_db[team_id].rank['scf_pcg']
			gen_x.append(x)
			gen_y.append(y)
			labels.append(team_id)
			current_marker = markers[marker_idx]
			#plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.stem(gen_x,gen_y)
		#plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.grid(True)
		figure_index += 1
		
		########################################################################################################################
		# Figure 4
		plt.figure(figure_index)
		# Subplot 1.1
		ax = plt.subplot(2,2,1)
		marker_idx = 0
		x_attribute = 'sf_pcg'
		y_attribute = 'p_pcg'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].rank[x_attribute]
			y = t_db[team_id].rank[y_attribute]
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		start = int(np.min([np.min(ax.get_xlim()),np.min(ax.get_ylim())]))
		stop = int(np.max([np.max(ax.get_xlim()),np.max(ax.get_ylim())]))
		plt.plot(range(start,stop),range(start,stop),'k--',label='50% threshold')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.grid(True)
		# Subplot 1.2
		ax = plt.subplot(2,2,2)
		marker_idx = 0
		x_attribute = 'ff_pcg'
		y_attribute = 'p_pcg'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].rank[x_attribute]
			y = t_db[team_id].rank[y_attribute]
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		start = int(np.min([np.min(ax.get_xlim()),np.min(ax.get_ylim())]))
		stop = int(np.max([np.max(ax.get_xlim()),np.max(ax.get_ylim())]))
		plt.plot(range(start,stop),range(start,stop),'k--',label='50% threshold')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		font_size = np.min([200/len(ACTIVE_TEAMS),9])
		ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)		
		plt.grid(True)
		# Subplot 1.3
		ax = plt.subplot(2,2,3)
		marker_idx = 0
		x_attribute = 'scf_pcg'
		y_attribute = 'p_pcg'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].rank[x_attribute]
			y = t_db[team_id].rank[y_attribute]
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		start = float(np.min([np.min(gen_x),np.min(gen_y)]))
		stop = float(np.max([np.max(gen_x),np.max(gen_y)]))
		plt.plot([0.95*start,1.05*stop],[0.95*start,1.05*stop],'k--',label='50% threshold')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.grid(True)
		# Subplot 1.4
		ax = plt.subplot(2,2,4)
		marker_idx = 0
		x_attribute = 'xgf_pcg'
		y_attribute = 'p_pcg'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].rank[x_attribute]
			y = t_db[team_id].rank[y_attribute]
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		start = int(np.min([np.min(ax.get_xlim()),np.min(ax.get_ylim())]))
		stop = int(np.max([np.max(ax.get_xlim()),np.max(ax.get_ylim())]))
		plt.plot(range(start,stop),range(start,stop),'k--',label='50% threshold')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.grid(True)
		figure_index += 1
		########################################################################################################################
		# Figure 5
		plt.figure(figure_index)
		# Subplot 1.1
		ax = plt.subplot(3,1,1)
		marker_idx = 0
		x_attribute = 'blocked_against'
		y_attribute = 'cf'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].blocked_against
			y = t_db[team_id].cf
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		# Fit linear model to (scatter) data.
		fit = np.polyfit(gen_x, gen_y, 1)
		fit_fn = np.poly1d(fit)
		k = round(fit[0],4)
		x_val = range(int(np.min(ax.get_xlim())),int(np.max(ax.get_xlim())))
		plt.plot(x_val,fit_fn(x_val),'y--',label='Data fit (k=' + str(k) + ')')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		font_size = np.min([200/len(ACTIVE_TEAMS),9])
		ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)
		plt.grid(True)
		# Subplot 1.2
		ax = plt.subplot(3,1,2)
		marker_idx = 0
		x_attribute = 'blocked_against'
		y_attribute = 'cf'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].blocked_against
			y = t_db[team_id].ff
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		# Fit linear model to (scatter) data.
		fit = np.polyfit(gen_x, gen_y, 1)
		fit_fn = np.poly1d(fit)
		k = round(fit[0],4)
		x_val = range(int(np.min(ax.get_xlim())),int(np.max(ax.get_xlim())))
		plt.plot(x_val,fit_fn(x_val),'y--',label='Data fit (k=' + str(k) + ')')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.subplots_adjust(left=0.05,bottom=0.07,top=0.95,right=0.82,hspace=0.3)
		plt.grid(True)
		# Subplot 1.3
		ax = plt.subplot(3,1,3)
		marker_idx = 0
		x_attribute = 'blocked_against'
		y_attribute = 'sf'
		gen_x, gen_y = [],[]
		for team_id in ACTIVE_TEAMS:
			x = t_db[team_id].blocked_against
			y = t_db[team_id].sf
			gen_x.append(x)
			gen_y.append(y)
			current_marker = markers[marker_idx]
			plt.scatter(x,y,c=current_marker[1],marker=current_marker[0],label=team_id)
			marker_idx += 1
		plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
		# Plot stuff
		# Fit linear model to (scatter) data.
		fit = np.polyfit(gen_x, gen_y, 1)
		fit_fn = np.poly1d(fit)
		k = round(fit[0],4)
		x_val = range(int(np.min(ax.get_xlim())),int(np.max(ax.get_xlim())))
		plt.plot(x_val,fit_fn(x_val),'y--',label='Data fit (k=' + str(k) + ')')
		plt.xlabel(x_attribute)
		plt.ylabel(y_attribute)
		plt.subplots_adjust(left=0.05,bottom=0.07,top=0.95,right=0.82,hspace=0.3)
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
	

	if simulation_param['exp_temp_attributes'] != None:
		for attribute in simulation_param['exp_temp_attributes']:
			print('\nBest ' + str(list_length) + ' ' + attribute +'. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
			op = print_sorted_list(s_db,[attribute],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
	else:
		print('\nBest ' + str(list_length) + ' goal scorers. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['goal_scoring_rating'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 

		print('\nBest ' + str(list_length) + ' relative goal impact player. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['rel_gf_diff_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
		print('\nWorst ' + str(list_length) + ' relative goal impact player. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['rel_gf_diff_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 	
		print('\nBest (most) ' + str(list_length) + ' offensive impact player. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_diff'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
		print('\nWorst (least) ' + str(list_length) + ' offensive impact player. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_diff'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 
		
		_filter['position'] = ['F']
		print('\nBest ' + str(list_length) + ' offensive forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
		print('\nWorst ' + str(list_length) + ' offensive forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 
		print('\nBest ' + str(list_length) + ' defensive forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_def_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 
		print('\nWorst ' + str(list_length) + ' defensive forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_def_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
		print('\nBest ' + str(list_length) + ' combined forwards (w. points). Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_pcg','primary_points_per_60'],operation=f_mult,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True) 
		print('\nBest ' + str(list_length) + ' point scoring forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['primary_points_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True)
		print('\nBest ' + str(list_length) + ' combined forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_pcg'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True)
		print('\nWorst ' + str(list_length) + ' combined forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_pcg'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=False,do_print=True) 
		print('\nBest ' + str(list_length) + ' ranked forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['ranking','total'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
		print('\nWorst ' + str(list_length) + ' ranked forwards. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['ranking','total'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 	
		
		_filter['position'] = ['D']
		_filter['toi'] *= (4/3) # D-men plays more than forwards.
		print('\nBest ' + str(list_length) + ' offensive defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
		print('\nWorst ' + str(list_length) + ' offensive defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 
		print('\nBest ' + str(list_length) + ' defensive defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_def_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 
		print('\nWorst ' + str(list_length) + ' defensive defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_def_per_60'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
		print('\nBest ' + str(list_length) + ' combined defenders (w. points). Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_pcg','primary_points_per_60'],operation=f_mult,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True,normalize=True) 
		print('\nBest ' + str(list_length) + ' combined defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_pcg'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True) 
		print('\nWorst ' + str(list_length) + ' combined defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['estimated_off_pcg'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=False,do_print=True) 				 				
		print('\nBest ' + str(list_length) + ' ranked defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['ranking','total'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True) 
		print('\nWorst ' + str(list_length) + ' ranked defenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list(s_db,['ranking','total'],operation=None,_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True) 	
		_filter['toi'] /= (4/3)# Revert back to original TOI requirement.

		_filter['toi'] *= 6 # Goalies play more than skaters.
		print('\nBest ' + str(list_length) + ' goaltenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list_goalie(g_db,'sv_pcg',_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=True,do_print=True)
		print('\nWorst ' + str(list_length) + ' goaltenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list_goalie(g_db,'sv_pcg',_filter=_filter,print_list_length=list_length,scale_factor=100,high_to_low=False,do_print=True)
		print('\nBest ' + str(list_length) + ' goaltenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list_goalie(g_db,'ga_above_xga',_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True)
		print('\nWorst ' + str(list_length) + ' goaltenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list_goalie(g_db,'ga_above_xga',_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True)
		print('\nBest ' + str(list_length) + ' goaltenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list_goalie(g_db,'ga_above_xga_per_60',_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=False,do_print=True)
		print('\nWorst ' + str(list_length) + ' goaltenders. Based on seasons(s) ' + str(simulation_param['seasons']) + ' (min. ' + str(_filter['toi']) + ' minutes played):')
		op = print_sorted_list_goalie(g_db,'ga_above_xga_per_60',_filter=_filter,print_list_length=list_length,scale_factor=1,high_to_low=True,do_print=True)

		_filter['toi'] /= 6 # Revert back to original TOI requirement.
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
				if player.get_toi() > _filter['toi']*60:
					num_of_rows += 1
					for attribute in attributes:
						if attribute == 'toi':
							data_list.append(player.get_toi()/60)
						else:
							data_list.append(player.get_attribute(attribute))
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
	if _filter['team'] == None:
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
	##############################################################################################################################
	if player_ids[0] in s_db.keys():
		do_skater_plots = True
	else:
		do_skater_plots = False

	if do_skater_plots == True:
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
		#print(op)
		print('Play driving w. zone deployment. Number of players = ' + str(len(op['pair_list'])))
		#print(op)
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
		print('Primary points per 60 w. zone deployment. Number of players = ' + str(len(op['pair_list'])))
		for pair in op['pair_list']:
			# Normalize data
			norm_value = pair[0]
			norm_value -= np.min(op['data_list'])
			norm_value /= (np.max(op['data_list']) - np.min(op['data_list']))
			if (ll <= _filter['list_length']) or (pair[1] in pl_high):
				print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(pair[0])) # print the original data, not the normalized.
			ll += 1
			s_db[pair[1]].rating.append(norm_value)
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
		print('Goals scored above expected. Number of players = ' + str(len(op['pair_list'])))
		for pair in op['pair_list']:
			# Normalize data
			norm_value = pair[0]
			norm_value -= np.min(op['data_list'])
			norm_value /= (np.max(op['data_list']) - np.min(op['data_list']))
			if (ll <= _filter['list_length']) or (pair[1] in pl_high):
				print('   ' + str(ll) + ' - ' + pair[1] + ' (' + s_db[pair[1]].bio['team_id'] + '): ' + str(pair[0])) # print the original data, not the normalized.
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': GF vs xGF')
		sub_plot_index += 1
		figure_index += 1
		##############################################################################################################################
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
		[plt,ax,__] = plot_player_cards(plt.subplot(n_rows,n_cols,sub_plot_index),axes_info,s_db,player_ids,_filter)
		plt.title(str(figure_index) + '.' + str(sub_plot_index) + ': Shot efficency')
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
