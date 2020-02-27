from nhl_helpers import *
from nhl_defines import *
from nhl_classes import *
from nhl_web_scrape import *

def create_databases(simulation_param):
	global ACTIVE_PLAYERS
	'''
	@TODO: The timeout functionality should be handled in the 'write_xxx_csv'-functions, with different degrees on the error functions.
	For instance, it's OK if the unavailable players timeout (set a warning), but an error should be set if the (e.g.) bio cannot be read
	'''
	global DATABASE_BIT_REGISTER
	print('   Creating databases based on season(s) ' + str(simulation_param['seasons']))
	simulation_param['databases'] = {}
	# Create schedule database
	[team_schedules,season_schedule] = generate_schedule(simulation_param['csvfiles'])
	simulation_param['databases']['team_schedules'] = team_schedules
	simulation_param['databases']['season_schedule'] = season_schedule

	# Download new csv-files if current files are too old.
	data_dir = simulation_param['data_dir']
	mod_time_db = os.stat(simulation_param['csvfiles']['skater_bio']).st_mtime
	mod_time_db = datetime.datetime.fromtimestamp(mod_time_db)
	if mod_time_db.strftime("%y%m%d") != datetime.datetime.now().strftime("%y%m%d") or simulation_param['generate_fresh_databases']:
		print('Saving data backup to ' + simulation_param['backup_dir'])
		backup_data_dir(simulation_param['data_dir'],simulation_param['backup_dir'])
		print('Downloading new csv-files from www.naturalstattrick.com')
		print('   Downloading bio-data')
		DATABASE_BIT_REGISTER[SKATER_BIO_BIT] = write_skater_bio_csv(simulation_param['url_skater_bio'],os.path.join(data_dir,'Skater_Bio_201920.csv'))
		print('   Downloading individual ES data')
		DATABASE_BIT_REGISTER[SKATER_ES_BIT] = write_skater_ind_csv(simulation_param['url_skater_ind_es'],os.path.join(data_dir,'Skater_Individual_ES_201920.csv'))
		print('   Downloading individual PP data')
		DATABASE_BIT_REGISTER[SKATER_PP_BIT] = write_skater_ind_csv(simulation_param['url_skater_ind_pp'],os.path.join(data_dir,'Skater_Individual_PP_201920.csv'))
		print('   Downloading individual PK data')
		DATABASE_BIT_REGISTER[SKATER_PK_BIT] = write_skater_ind_csv(simulation_param['url_skater_ind_pk'],os.path.join(data_dir,'Skater_Individual_PK_201920.csv'))
		print('   Downloading on-ice data')
		DATABASE_BIT_REGISTER[SKATER_ON_ICE_BIT] = write_skater_on_ice_csv(simulation_param['url_skater_on_ice'],os.path.join(data_dir,'Skater_OnIce_201920.csv'))
		print('   Downloading relative data')
		DATABASE_BIT_REGISTER[SKATER_RELATIVE_BIT] = write_skater_relative_csv(simulation_param['url_skater_relative'],os.path.join(data_dir,'Skater_Relative_201819_201920.csv'))
		print('   Downloading goalie ES data')
		write_goalie_csv(simulation_param['url_goalie_201819_201920'],os.path.join(data_dir,'Goalie_201819_201920.csv'))
		DATABASE_BIT_REGISTER[GOALIE_ES_BIT] = write_goalie_csv(simulation_param['url_goalie_es_201920'],os.path.join(data_dir,'Goalie_ES_201920.csv'))
		print('   Downloading goalie PP data')
		DATABASE_BIT_REGISTER[GOALIE_PP_BIT] = write_goalie_csv(simulation_param['url_goalie_pp_201920'],os.path.join(data_dir,'Goalie_PP_201920.csv'))
		print('   Downloading goalie PK data')
		DATABASE_BIT_REGISTER[GOALIE_PK_BIT] = write_goalie_csv(simulation_param['url_goalie_pk_201920'],os.path.join(data_dir,'Goalie_PK_201920.csv'))
		print('   Downloading ES team data')
		DATABASE_BIT_REGISTER[TEAM_ES_BIT] = write_team_csv(simulation_param['url_team_es'],os.path.join(data_dir,'Team_ES_201920.csv'))
		print('   Downloading PP team data')
		DATABASE_BIT_REGISTER[TEAM_PP_BIT] = write_team_csv(simulation_param['url_team_pp'],os.path.join(data_dir,'Team_PP_201920.csv'))
		print('   Downloading PK team data')
		DATABASE_BIT_REGISTER[TEAM_PK_BIT] = write_team_csv(simulation_param['url_team_pk'],os.path.join(data_dir,'Team_PK_201920.csv'))
		print('   Downloading team data, home venue')
		DATABASE_BIT_REGISTER[TEAM_HOME_BIT] = write_team_csv(simulation_param['url_team_home'],os.path.join(data_dir,'Team_Home_201819_1920.csv'))
		print('   Downloading team data, away venue')
		DATABASE_BIT_REGISTER[TEAM_AWAY_BIT] = write_team_csv(simulation_param['url_team_away'],os.path.join(data_dir,'Team_Away_201819_1920.csv'))
		print('   Downloading unavailalbe players')
		DATABASE_BIT_REGISTER[UNAVAILABLE_PLAYERS_BIT] = write_unavailable_players_csv(os.path.join(data_dir,'Unavailable_Players.csv'))
	else:
		print('Using local csv-files.')

	if (DATABASE_BIT_REGISTER[SKATER_BIO_BIT] == False) or (DATABASE_BIT_REGISTER[SKATER_ES_BIT] == False) or (DATABASE_BIT_REGISTER[SKATER_PP_BIT] == False) or (DATABASE_BIT_REGISTER[SKATER_PK_BIT] == False) or (DATABASE_BIT_REGISTER[SKATER_ON_ICE_BIT] == False):
		raise ValueError('Cannot read skater information. Aborting.')

	if (DATABASE_BIT_REGISTER[GOALIE_ES_BIT] == False) or (DATABASE_BIT_REGISTER[GOALIE_PP_BIT] == False) or (DATABASE_BIT_REGISTER[GOALIE_PK_BIT] == False):
		raise ValueError('Cannot read goalie information. Aborting.')

	if (DATABASE_BIT_REGISTER[TEAM_ES_BIT] == False) or (DATABASE_BIT_REGISTER[TEAM_PP_BIT] == False) or (DATABASE_BIT_REGISTER[TEAM_PK_BIT] == False):
		raise ValueError('Cannot read team information. Aborting.')

	if (DATABASE_BIT_REGISTER[TEAM_HOME_BIT] == False) or (DATABASE_BIT_REGISTER[TEAM_AWAY_BIT] == False):
		print('Cannot read team venue information. No venue adjustment used.')

	if DATABASE_BIT_REGISTER[UNAVAILABLE_PLAYERS_BIT] == False:
		print('Cannot read information about unavailable players.')


	# Create team and skater database.
	print('   Creating Team-DB')
	simulation_param['databases']['team_db'] = create_team_db(simulation_param)

	print('   Creating Skater-DB')
	simulation_param['databases']['skater_db'] = create_skater_db(simulation_param)
	print('   Creating Goalie-DB')
	simulation_param['databases']['goalie_db'] = create_goalie_db(simulation_param)
	ACTIVE_PLAYERS = ACTIVE_SKATERS.union(ACTIVE_GOALIES)
	old_rating, new_rating, diff_rating = {},{},{}

	# Find out who is available.
	if DATABASE_BIT_REGISTER[UNAVAILABLE_PLAYERS_BIT] == True:
		players_to_remove = []
		simulation_param['databases']['unavailable_players'] = get_unavailable_players()
		for player_id in simulation_param['databases']['unavailable_players']:
			if (player_id not in simulation_param['databases']['skater_db']) and (player_id not in simulation_param['databases']['goalie_db']):
				#print('Unavailable player ' + player_id + ' not in skaterDB.')
				players_to_remove.append(player_id)
		for player_id in players_to_remove:
			simulation_param['databases']['unavailable_players'].remove(player_id)
	else:
		simulation_param['databases']['unavailable_players'] = set()

	print('   Modifying databases manually')
	simulation_param = modify_player_db(simulation_param)
	
	# Add experimental data - needs to be done after creation of SkaterDB (and GoalieDB).
	print('   Adding experimental data')
	simulation_param = add_experimental_data(simulation_param)

	for team_id in ACTIVE_TEAMS:
		team = simulation_param['databases']['team_db'][team_id]
		old_rating[team_id] = team.get_ratings()[1]

	if simulation_param['include_offseason_moves'] == True:
		for team_id in ACTIVE_TEAMS:
			team = simulation_param['databases']['team_db'][team_id]
			new_rating[team_id] = team.get_ratings()[1]
			diff_rating[team_id] = new_rating[team_id] - old_rating[team_id]
			#print('{0}: Difference in rating after off-seasons: {1:.1f}%'.format(team_id,100*diff_rating[team_id]/old_rating[team_id]))

	simulation_param['databases']['starting_goalies'] = generate_starting_goalies()
	simulation_param['databases']['team_specific_db'] = create_team_specific_db(simulation_param)	
	
	# Create roster lists split up on team and position.
	roster_output,flt = {},{}
	postions = ['D','F']
	for team_id in ACTIVE_TEAMS:
		flt['team_id'] = team_id
		flt['position'] = 'D'
		roster_output[str(team_id + '_D')] = create_player_list(simulation_param['databases']['skater_db'],flt)
		flt['position'] = 'F'
		roster_output[str(team_id + '_F')] = create_player_list(simulation_param['databases']['skater_db'],flt)
	simulation_param['databases']['team_rosters'] = roster_output
	return simulation_param

def download_old_season_data(seasons=None,data_dir='Data_download'):
	if seasons == None:
		raise ValueError('No seasons specified for download')
	print('Downloading new csv-files from www.naturalstattrick.com')
	for season in seasons:
		orig_season_name = season
		# Transformation to fit the url-format at Natural Stat Trick.
		season = str(season[:-2]) + '20' + str(season[-2:])
		url_skater_ind_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
		url_skater_ind_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v4&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
		url_skater_ind_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=4v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
		url_skater_on_ice = "http://naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=oi&rate=r&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
		url_skater_relative = "http://naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=oi&rate=r&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
		url_goalie_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season +"&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
		url_goalie_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v4&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
		url_goalie_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season +"&stype=2&sit=4v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
		# Individual data
		print('   Downloading individual ES data for season ' + season)
		write_skater_ind_csv(url_skater_ind_es,os.path.join(data_dir,'Skater_Individual_ES_' + orig_season_name + '.csv'))
		print('   Downloading individual PP data for season ' + season)
		write_skater_ind_csv(url_skater_ind_pp,os.path.join(data_dir,'Skater_Individual_PP_' + orig_season_name + '.csv'))
		print('   Downloading individual PK data for season ' + season)
		write_skater_ind_csv(url_skater_ind_pk,os.path.join(data_dir,'Skater_Individual_PK_' + orig_season_name + '.csv'))
		# On ice data
		print('   Downloading on-ice data for season ' + season)
		write_skater_on_ice_csv(url_skater_on_ice,os.path.join(data_dir,'Skater_OnIce_' + orig_season_name + '.csv'))
		# Relative data
		print('   Downloading relative data for season ' + season)
		write_skater_relative_csv(url_skater_relative,os.path.join(data_dir,'Skater_Relative_' + orig_season_name + '.csv'))
		# Goalie data
		print('   Downloading goalie ES data for season ' + season)
		write_goalie_csv(url_goalie_es,os.path.join(data_dir,'Goalie_ES_' + orig_season_name + '.csv'))
		print('   Downloading goalie PP data for season ' + season)
		write_goalie_csv(url_goalie_pp,os.path.join(data_dir,'Goalie_PP_' + orig_season_name + '.csv'))
		print('   Downloading goalie PK data for season ' + season)
		write_goalie_csv(url_goalie_pk,os.path.join(data_dir,'Goalie_PK_' + orig_season_name + '.csv'))


def create_skater_db(simulation_param):
	output = {}
	player_data = add_bio_data(simulation_param)
	player_data = add_es_data(simulation_param,player_data)
	player_data = add_pp_data(simulation_param,player_data)
	player_data = add_pk_data(simulation_param,player_data)
	player_data = add_on_ice_data(simulation_param,player_data)
	player_data = add_relative_data(simulation_param,player_data)

	for player_id in player_data.keys():
		if player_data[player_id]['ind'] == None or player_data[player_id]['on_ice'] == None:
			warnings.warn('\nSkipping player ' + player_id)
		else:
			output[player_id] = Skater(player_data[player_id]['bio'],player_data[player_id]['ind'],player_data[player_id]['on_ice'])

	return output

def add_bio_data(simulation_param):
	global ACTIVE_SKATERS
	player_data = {}
	old_data = get_old_data(simulation_param)
	with open(simulation_param['csvfiles']['skater_bio'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'player_name':
				# NAME
				# Create and store player-ID.
				player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
				if player_id == 'SEBASTIAN_AHO':
					if get_team_id_for_player('SEBASTIAN_AHO',str(row[SKATER_DB_BIO_TEAM_ID])) != 'CAR':
						print('Player ' + player_id +' is not playing for CAR')
					else:
						print('Player ' + player_id +' is playing for CAR')
				if (player_id == 'SEBASTIAN_AHO') and (get_team_id_for_player('SEBASTIAN_AHO',str(row[SKATER_DB_BIO_TEAM_ID])) != 'CAR'):
					print('Updating player_id from ' +  player_id + ' to SEBASTIAN_AHO2.')
					player_id = 'SEBASTIAN_AHO2'
				
				ACTIVE_SKATERS.add(player_id)
				# Initialize structs.
				player_data[player_id] = {}
				# Bio
				player_data[player_id]['bio'] = {}

				# Individual_SKATER
				player_data[player_id]['ind'] = {}
				player_data[player_id]['ind']['toi'] = [0,0,0]
				player_data[player_id]['ind']['gf'] = [0,0,0]
				player_data[player_id]['ind']['assist'] = [0,0,0]
				player_data[player_id]['ind']['f_assist'] = [0,0,0]
				player_data[player_id]['ind']['s_assist'] = [0,0,0]
				player_data[player_id]['ind']['isf'] = [0,0,0]
				player_data[player_id]['ind']['icf'] = [0,0,0]
				player_data[player_id]['ind']['iff'] = [0,0,0]
				player_data[player_id]['ind']['iscf'] = [0,0,0]
				player_data[player_id]['ind']['pt'] = [0,0,0]
				player_data[player_id]['ind']['pd'] = [0,0,0]
				player_data[player_id]['ind']['hits'] = [0,0,0]
				player_data[player_id]['ind']['hits_taken'] = [0,0,0]
				player_data[player_id]['ind']['ish_pcg'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['ixgf'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['ixgf'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['ixgf'] = [0.0,0.0,0.0]

				# On-ice data_SKATER
				player_data[player_id]['on_ice'] = {}
				player_data[player_id]['on_ice']['rel_scf_per_60'] = 1.0
				player_data[player_id]['on_ice']['rel_sca_per_60'] = 1.0
				player_data[player_id]['on_ice']['rel_scf_pcg'] = 1.0
				player_data[player_id]['on_ice']['gp'] = 0						
				player_data[player_id]['on_ice']['cf'] = 0						
				player_data[player_id]['on_ice']['ca'] = 0
				player_data[player_id]['on_ice']['cf_pcg'] = 0.0						
				player_data[player_id]['on_ice']['sf'] = 0						
				player_data[player_id]['on_ice']['sa'] = 0						
				player_data[player_id]['on_ice']['sf_pcg'] = 0.0
				player_data[player_id]['on_ice']['gf'] = 0						
				player_data[player_id]['on_ice']['ga'] = 0						
				player_data[player_id]['on_ice']['gf_pcg'] = 0.0
				player_data[player_id]['on_ice']['xgf'] = 0						
				player_data[player_id]['on_ice']['xga'] = 0						
				player_data[player_id]['on_ice']['xgf_pcg'] = 0.0						
				player_data[player_id]['on_ice']['scf'] = 0						
				player_data[player_id]['on_ice']['sca'] = 0						
				player_data[player_id]['on_ice']['scf_pcg'] = 0.0						
				player_data[player_id]['on_ice']['hdcf'] = 0						
				player_data[player_id]['on_ice']['hdca'] = 0						
				player_data[player_id]['on_ice']['hdcf_pcg'] = 0.0
				player_data[player_id]['on_ice']['ozs'] = 0
				player_data[player_id]['on_ice']['nzs'] = 0
				player_data[player_id]['on_ice']['dzs'] = 0						
				player_data[player_id]['on_ice']['ozfo'] = 0
				player_data[player_id]['on_ice']['nzfo'] = 0
				player_data[player_id]['on_ice']['dzfo'] = 0

				if player_id in old_data:
					player_data[player_id]['bio']['rookie'] = False
				else:
					player_data[player_id]['bio']['rookie'] = True
							
				player_data[player_id]['bio']['salary'] = 700000

				# Read player data.
				if str(row[SKATER_DB_BIO_NAME]) == '-':
					raise ValueError('Incorrect Player-ID')
				else:
					if player_id == 'SEBASTIAN_AHO2':
						player_data[player_id]['bio']['name'] = 'SEBSTIAN_AHO2'
					else:	
						name = generate_player_id(row[SKATER_DB_BIO_NAME])
						player_data[player_id]['bio']['name'] = name
				# TEAM
				if str(row[SKATER_DB_BIO_TEAM_ID]) == '-':
					raise ValueError('Incorrect Team-ID')
				else:
					player_data[player_id]['bio']['team_id'] = get_team_id_for_player(name,str(row[SKATER_DB_BIO_TEAM_ID]))
				# POSITION
				if str(row[SKATER_DB_BIO_POSITION]) == '-':
					raise ValueError('Incorrect Player position')					
				else:
					position = str(row[SKATER_DB_BIO_POSITION])
					player_data[player_id]['bio']['position'] = position
					if ('C' in position) or ('L' in position) or ('R' in position):
						player_data[player_id]['bio']['position'] = 'F'
				if str(row[SKATER_DB_BIO_AGE]) == '-':
					player_data[player_id]['bio']['age'] = 0						
				else:
					player_data[player_id]['bio']['age'] = int(row[SKATER_DB_BIO_AGE])
				if str(row[SKATER_DB_BIO_HEIGHT]) == '-':
					player_data[player_id]['bio']['height'] = 0						
				else:
					player_data[player_id]['bio']['height'] = int(row[SKATER_DB_BIO_HEIGHT])*2.54 # Convert to centimeters.
				if str(row[SKATER_DB_BIO_WEIGHT]) == '-':
					player_data[player_id]['bio']['weight'] = 0						
				else:
					player_data[player_id]['bio']['weight'] = int(row[SKATER_DB_BIO_WEIGHT])*0.453592 # Convert to kilograms.
				# DRAFT
				if str(row[SKATER_DB_BIO_DRAFT_YEAR]) == '-':
					player_data[player_id]['bio']['draft_year'] = 0						
				else:
					player_data[player_id]['bio']['draft_year'] = int(row[SKATER_DB_BIO_DRAFT_YEAR])
				if str(row[SKATER_DB_BIO_DRAFT_TEAM]) == '-':
					player_data[player_id]['bio']['draft_team'] = 'N/A'
				else:
					player_data[player_id]['bio']['draft_team'] = str(row[SKATER_DB_BIO_DRAFT_TEAM])
				if str(row[SKATER_DB_BIO_DRAFT_ROUND]) == '-':
					player_data[player_id]['bio']['draft_round'] = 7 # Default to last round			
				else:
					player_data[player_id]['bio']['draft_round'] = int(row[SKATER_DB_BIO_DRAFT_ROUND])
				if str(row[SKATER_DB_BIO_ROUND_PICK]) == '-':
					player_data[player_id]['bio']['round_pick'] = 32	# Default to last pick			
				else:
					player_data[player_id]['bio']['round_pick'] = int(row[SKATER_DB_BIO_ROUND_PICK])
				if str(row[SKATER_DB_BIO_TOTAL_DRAFT_POS]) == '-':
					player_data[player_id]['bio']['total_draft_pos'] = 225	# Default to one pick after last pick in the last round					
				else:
					player_data[player_id]['bio']['total_draft_pos'] = int(row[SKATER_DB_BIO_TOTAL_DRAFT_POS])

	return player_data


def add_bio_data_goalie(simulation_param):
	global ACTIVE_GOALIES
	player_data = {}
	with open(simulation_param['csvfiles']['goalie_bio'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'player_name':
				# NAME
				# Create and store player-ID.
				player_id = generate_player_id(row[GOALIE_DB_NAME])
				ACTIVE_GOALIES.add(player_id)
				# Initialize structs.
				player_data[player_id] = {}
				# Bio
				player_data[player_id]['bio'] = {}
				player_data[player_id]['bio']['position'] = 'G'

				# Individual_GOALIE
				player_data[player_id]['ind'] = {}
				player_data[player_id]['ind']['toi'] = [0,0,0]
				player_data[player_id]['ind']['toi_pcg'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['sa'] = [0,0,0]
				player_data[player_id]['ind']['sa_per_sec'] = [0,0,0]
				player_data[player_id]['ind']['sv'] = [0,0,0]
				player_data[player_id]['ind']['sv_pcg'] = [0,0,0]
				player_data[player_id]['ind']['ga'] = [0,0,0]
				player_data[player_id]['ind']['gaa'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['gsaa'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['gsaa_per_60'] = [0,0,0]
				player_data[player_id]['ind']['xga'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['ga_above_xga'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['ga_above_xga_per_60'] = [0.0,0.0,0.0]
				player_data[player_id]['ind']['avg_shot_dist'] = [0,0,0]
				player_data[player_id]['ind']['avg_goal_dist'] = [0,0,0]
			
				# Read player data.
				if str(row[SKATER_DB_BIO_NAME]) == '-':
					raise ValueError('Incorrect Player-ID')
				else:
					name = generate_player_id(row[GOALIE_DB_NAME])
					player_data[player_id]['bio']['name'] = name
				# TEAM
				if str(row[GOALIE_DB_TEAM_ID]) == '-':
					raise ValueError('Incorrect Team-ID')
				else:
					player_data[player_id]['bio']['team_id'] = get_team_id_for_player(name,str(row[GOALIE_DB_TEAM_ID]))

	return player_data



def get_old_data(simulation_param):
	previous_skaters = set()
	with open(simulation_param['csvfiles']['skater_old_bio'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'player_name':
				player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
				previous_skaters.add(player_id)
	return previous_skaters

def add_es_data(simulation_param,player_data):
	for season_data in simulation_param['csvfiles']['skater_es']:
		with open(season_data,'rt') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				if row[1] != 'player_name':
					# Only add players that are playing today.
					player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
					if player_id in ACTIVE_SKATERS:
						team_id = player_data[player_id]['bio']['team_id']
						#print(player_id + ' (' + team_id + ')')
						if (player_id == 'SEBASTIAN_AHO') and (str(row[SKATER_DB_IND_TEAM_ID]) != 'CAR'):
							print('Changing player-id to SEBASTIAN_AHO2')
							player_id = 'SEBASTIAN_AHO2'
							#raise ValueError('Wrong Sebastian Aho')
						#print(player_id + ' (' + team_id + ')')
						if str(row[SKATER_DB_IND_TEAM_ID]) == '-':
							raise ValueError('Incorrect team_id ' + str(row[SKATER_DB_IND_TEAM_ID]))
						else:
							player_data[player_id]['ind']['multiple_teams'] = False
							if len(str(row[SKATER_DB_IND_TEAM_ID]).split(',')) > 1:
								player_data[player_id]['ind']['multiple_teams'] = True
						
						if str(row[SKATER_DB_IND_TOI]) == '-':
							player_data[player_id]['ind']['toi'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['toi'][STAT_ES] += int(60*float(row[SKATER_DB_IND_TOI]))

						if str(row[SKATER_DB_IND_GOALS]) == '-':
							player_data[player_id]['ind']['gf'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['gf'][STAT_ES] += int(row[SKATER_DB_IND_GOALS])
						
						if str(row[SKATER_DB_IND_ASSIST]) == '-':
							player_data[player_id]['ind']['assist'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['assist'][STAT_ES] += int(row[SKATER_DB_IND_ASSIST])

						if str(row[SKATER_DB_IND_FIRST_ASSIST]) == '-':
							player_data[player_id]['ind']['f_assist'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['f_assist'][STAT_ES] += int(row[SKATER_DB_IND_FIRST_ASSIST])

						if str(row[SKATER_DB_IND_SECOND_ASSIST]) == '-':
							player_data[player_id]['ind']['s_assist'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['s_assist'][STAT_ES] += int(row[SKATER_DB_IND_SECOND_ASSIST])

						if str(row[SKATER_DB_IND_SF]) == '-':
							player_data[player_id]['ind']['isf'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['isf'][STAT_ES] += int(row[SKATER_DB_IND_SF])

						if str(row[SKATER_DB_IND_ICF]) == '-':
							player_data[player_id]['ind']['icf'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['icf'][STAT_ES] += int(row[SKATER_DB_IND_ICF])

						if str(row[SKATER_DB_IND_ICF]) == '-':
							player_data[player_id]['ind']['iff'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['iff'][STAT_ES] += int(row[SKATER_DB_IND_IFF])

						if str(row[SKATER_DB_IND_ICF]) == '-':
							player_data[player_id]['ind']['iscf'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['iscf'][STAT_ES] += int(row[SKATER_DB_IND_ISCF])

						if str(row[SKATER_DB_IND_TOTAL_PENALTIES]) == '-':
							player_data[player_id]['ind']['pt'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['pt'][STAT_ES] += int(row[SKATER_DB_IND_TOTAL_PENALTIES])

						if str(row[SKATER_DB_IND_PENALTIES_DRAWN]) == '-':
							player_data[player_id]['ind']['pd'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['pd'][STAT_ES] += int(row[SKATER_DB_IND_PENALTIES_DRAWN])

						if str(row[SKATER_DB_IND_HITS]) == '-':
							player_data[player_id]['ind']['hits'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['hits'][STAT_ES] += int(row[SKATER_DB_IND_HITS])

						if str(row[SKATER_DB_IND_HITS_TAKEN]) == '-':
							player_data[player_id]['ind']['hits_taken'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['hits_taken'][STAT_ES] += int(row[SKATER_DB_IND_HITS_TAKEN])						

						if str(row[SKATER_DB_IND_IXG]) == '-':
							player_data[player_id]['ind']['ixgf'][STAT_ES] += 0.0
						else:
							player_data[player_id]['ind']['ixgf'][STAT_ES] += float(row[SKATER_DB_IND_IXG])
	return player_data



def add_es_data_goalie(simulation_param,player_data):
	for season_data in simulation_param['csvfiles']['goalie_es']:
		with open(season_data,'rt') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				if row[1] != 'player_name':
					# Only add players that are playing today.
					player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
					if player_id in ACTIVE_GOALIES:
						if str(row[GOALIE_DB_TOI]) == '-':
							player_data[player_id]['ind']['toi'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['toi'][STAT_ES] += int(60*float(row[GOALIE_DB_TOI]))

						if str(row[GOALIE_DB_SA]) == '-':
							player_data[player_id]['ind']['sa'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['sa'][STAT_ES] += int(row[GOALIE_DB_SA])
						
						if str(row[GOALIE_DB_SV]) == '-':
							player_data[player_id]['ind']['sv'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['sv'][STAT_ES] += int(row[GOALIE_DB_SV])

						if str(row[GOALIE_DB_GA]) == '-':
							player_data[player_id]['ind']['ga'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['ga'][STAT_ES] += int(row[GOALIE_DB_GA])

						if str(row[GOALIE_DB_GSAA]) == '-':
							player_data[player_id]['ind']['gsaa'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['gsaa'][STAT_ES] += float(row[GOALIE_DB_GSAA])

						if str(row[GOALIE_DB_XGA]) == '-':
							player_data[player_id]['ind']['xga'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['xga'][STAT_ES] += float(row[GOALIE_DB_XGA])

						if str(row[GOALIE_DB_AVG_SHOT_DIST]) == '-':
							player_data[player_id]['ind']['avg_shot_dist'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['avg_shot_dist'][STAT_ES] += int(row[GOALIE_DB_AVG_SHOT_DIST])

						if str(row[GOALIE_DB_AVG_GOAL_DIST]) == '-':
							player_data[player_id]['ind']['avg_goal_dist'][STAT_ES] += 0
						else:
							player_data[player_id]['ind']['avg_goal_dist'][STAT_ES] += int(row[GOALIE_DB_AVG_GOAL_DIST])
	return player_data

def add_pp_data(simulation_param,player_data):
	for season_data in simulation_param['csvfiles']['skater_pp']:
		with open(season_data,'rt') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				if row[1] != 'player_name':
					# Only add players that are playing today.
					player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
					if player_id in ACTIVE_SKATERS:
						team_id = player_data[player_id]['bio']['team_id']
						if (player_id == 'SEBASTIAN_AHO') and (str(row[SKATER_DB_IND_TEAM_ID]) != 'CAR'):
							#player_id = 'SEBASTIAN_AHO2'
							raise ValueError('Wrong Sebastian Aho')

						if str(row[SKATER_DB_IND_TOI]) == '-':
							player_data[player_id]['ind']['toi'][STAT_PP] += 0						
						else:
							player_data[player_id]['ind']['toi'][STAT_PP] += int(60*float(row[SKATER_DB_IND_TOI]))
						
						if str(row[SKATER_DB_IND_GOALS]) == '-':
							player_data[player_id]['ind']['gf'][STAT_PP] += 0						
						else:
							player_data[player_id]['ind']['gf'][STAT_PP] += int(row[SKATER_DB_IND_GOALS])
						
						if str(row[SKATER_DB_IND_ASSIST]) == '-':
							player_data[player_id]['ind']['assist'][STAT_PP] += 0						
						else:
							player_data[player_id]['ind']['assist'][STAT_PP] += int(row[SKATER_DB_IND_ASSIST])

						if str(row[SKATER_DB_IND_FIRST_ASSIST]) == '-':
							player_data[player_id]['ind']['f_assist'][STAT_PP] += 0						
						else:
							player_data[player_id]['ind']['f_assist'][STAT_PP] += int(row[SKATER_DB_IND_FIRST_ASSIST])

						if str(row[SKATER_DB_IND_SECOND_ASSIST]) == '-':
							player_data[player_id]['ind']['s_assist'][STAT_PP] += 0						
						else:
							player_data[player_id]['ind']['s_assist'][STAT_PP] += int(row[SKATER_DB_IND_SECOND_ASSIST])

						if str(row[SKATER_DB_IND_SF]) == '-':
							player_data[player_id]['ind']['isf'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['isf'][STAT_PP] += int(row[SKATER_DB_IND_SF])

						if str(row[SKATER_DB_IND_TOTAL_PENALTIES]) == '-':
							player_data[player_id]['ind']['pt'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['pt'][STAT_PP] += int(row[SKATER_DB_IND_TOTAL_PENALTIES])

						if str(row[SKATER_DB_IND_PENALTIES_DRAWN]) == '-':
							player_data[player_id]['ind']['pd'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['pd'][STAT_PP] += int(row[SKATER_DB_IND_PENALTIES_DRAWN])

						if str(row[SKATER_DB_IND_HITS]) == '-':
							player_data[player_id]['ind']['hits'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['hits'][STAT_PP] += int(row[SKATER_DB_IND_HITS])

						if str(row[SKATER_DB_IND_HITS_TAKEN]) == '-':
							player_data[player_id]['ind']['hits_taken'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['hits_taken'][STAT_PP] += int(row[SKATER_DB_IND_HITS_TAKEN])	
	return player_data

def add_pp_data_goalie(simulation_param,player_data):
	for season_data in simulation_param['csvfiles']['goalie_pp']:
		with open(season_data,'rt') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				if row[1] != 'player_name':
					# Only add players that are playing today.
					player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
					if player_id in ACTIVE_GOALIES:
						if str(row[GOALIE_DB_TOI]) == '-':
							player_data[player_id]['ind']['toi'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['toi'][STAT_PP] += int(60*float(row[GOALIE_DB_TOI]))

						if str(row[GOALIE_DB_SA]) == '-':
							player_data[player_id]['ind']['sa'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['sa'][STAT_PP] += int(row[GOALIE_DB_SA])
						
						if str(row[GOALIE_DB_SV]) == '-':
							player_data[player_id]['ind']['sv'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['sv'][STAT_PP] += int(row[GOALIE_DB_SV])

						if str(row[GOALIE_DB_GA]) == '-':
							player_data[player_id]['ind']['ga'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['ga'][STAT_PP] += int(row[GOALIE_DB_GA])

						if str(row[GOALIE_DB_SV_PCG]) == '-':
							player_data[player_id]['ind']['sv_pcg'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['sv_pcg'][STAT_PP] += float(row[GOALIE_DB_SV_PCG])

						if str(row[GOALIE_DB_GAA]) == '-':
							player_data[player_id]['ind']['gaa'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['gaa'][STAT_PP] += float(row[GOALIE_DB_GAA])

						if str(row[GOALIE_DB_GSAA]) == '-':
							player_data[player_id]['ind']['gsaa'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['gsaa'][STAT_PP] += float(row[GOALIE_DB_GSAA])

						if str(row[GOALIE_DB_XGA]) == '-':
							player_data[player_id]['ind']['xga'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['xga'][STAT_PP] += float(row[GOALIE_DB_XGA])

						if str(row[GOALIE_DB_AVG_SHOT_DIST]) == '-':
							player_data[player_id]['ind']['avg_shot_dist'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['avg_shot_dist'][STAT_PP] += int(row[GOALIE_DB_AVG_SHOT_DIST])

						if str(row[GOALIE_DB_AVG_GOAL_DIST]) == '-':
							player_data[player_id]['ind']['avg_goal_dist'][STAT_PP] += 0
						else:
							player_data[player_id]['ind']['avg_goal_dist'][STAT_PP] += int(row[GOALIE_DB_AVG_GOAL_DIST])
	return player_data

def add_pk_data(simulation_param,player_data):
	for season_data in simulation_param['csvfiles']['skater_pk']:
		with open(season_data,'rt') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				if row[1] != 'player_name':
					# Only add players that are playing today.
					player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
					if player_id in ACTIVE_SKATERS:
						team_id = player_data[player_id]['bio']['team_id']
						if (player_id == 'SEBASTIAN_AHO') and (str(row[SKATER_DB_IND_TEAM_ID]) != 'CAR'):
							#player_id = 'SEBASTIAN_AHO2'
							raise ValueError('Wrong Sebastian Aho')

						if str(row[SKATER_DB_IND_TOI]) == '-':
							player_data[player_id]['ind']['toi'][STAT_PK] += 0	
						else:
							player_data[player_id]['ind']['toi'][STAT_PK] += int(60*float(row[SKATER_DB_IND_TOI]))
						
						if str(row[SKATER_DB_IND_GOALS]) == '-':
							player_data[player_id]['ind']['gf'][STAT_PK] += 0						
						else:
							player_data[player_id]['ind']['gf'][STAT_PK] += int(row[SKATER_DB_IND_GOALS])
						
						if str(row[SKATER_DB_IND_ASSIST]) == '-':
							player_data[player_id]['ind']['assist'][STAT_PK] += 0						
						else:
							player_data[player_id]['ind']['assist'][STAT_PK] += int(row[SKATER_DB_IND_ASSIST])

						if str(row[SKATER_DB_IND_FIRST_ASSIST]) == '-':
							player_data[player_id]['ind']['f_assist'][STAT_PK] += 0						
						else:
							player_data[player_id]['ind']['f_assist'][STAT_PK] += int(row[SKATER_DB_IND_FIRST_ASSIST])

						if str(row[SKATER_DB_IND_SECOND_ASSIST]) == '-':
							player_data[player_id]['ind']['s_assist'][STAT_PK] += 0						
						else:
							player_data[player_id]['ind']['s_assist'][STAT_PK] += int(row[SKATER_DB_IND_SECOND_ASSIST])

						if str(row[SKATER_DB_IND_SF]) == '-':
							player_data[player_id]['ind']['isf'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['isf'][STAT_PK] += int(row[SKATER_DB_IND_SF])

						if str(row[SKATER_DB_IND_TOTAL_PENALTIES]) == '-':
							player_data[player_id]['ind']['pt'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['pt'][STAT_PK] += int(row[SKATER_DB_IND_TOTAL_PENALTIES])

						if str(row[SKATER_DB_IND_PENALTIES_DRAWN]) == '-':
							player_data[player_id]['ind']['pd'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['pd'][STAT_PK] += int(row[SKATER_DB_IND_PENALTIES_DRAWN])

						if str(row[SKATER_DB_IND_HITS]) == '-':
							player_data[player_id]['ind']['hits'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['hits'][STAT_PK] += int(row[SKATER_DB_IND_HITS])

						if str(row[SKATER_DB_IND_HITS_TAKEN]) == '-':
							player_data[player_id]['ind']['hits_taken'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['hits_taken'][STAT_PK] += int(row[SKATER_DB_IND_HITS_TAKEN])	
	return player_data

def add_pk_data_goalie(simulation_param,player_data):
	for season_data in simulation_param['csvfiles']['goalie_pk']:
		with open(season_data,'rt') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				if row[1] != 'player_name':
					# Only add players that are playing today.
					player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
					if player_id in ACTIVE_GOALIES:
						if str(row[GOALIE_DB_TOI]) == '-':
							player_data[player_id]['ind']['toi'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['toi'][STAT_PK] += int(60*float(row[GOALIE_DB_TOI]))

						if str(row[GOALIE_DB_SA]) == '-':
							player_data[player_id]['ind']['sa'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['sa'][STAT_PK] += int(row[GOALIE_DB_SA])
						
						if str(row[GOALIE_DB_SV]) == '-':
							player_data[player_id]['ind']['sv'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['sv'][STAT_PK] += int(row[GOALIE_DB_SV])

						if str(row[GOALIE_DB_GA]) == '-':
							player_data[player_id]['ind']['ga'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['ga'][STAT_PK] += int(row[GOALIE_DB_GA])

						if str(row[GOALIE_DB_SV_PCG]) == '-':
							player_data[player_id]['ind']['sv_pcg'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['sv_pcg'][STAT_PK] += float(row[GOALIE_DB_SV_PCG])

						if str(row[GOALIE_DB_GAA]) == '-':
							player_data[player_id]['ind']['gaa'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['gaa'][STAT_PK] += float(row[GOALIE_DB_GAA])

						if str(row[GOALIE_DB_GSAA]) == '-':
							player_data[player_id]['ind']['gsaa'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['gsaa'][STAT_PK] += float(row[GOALIE_DB_GSAA])

						if str(row[GOALIE_DB_XGA]) == '-':
							player_data[player_id]['ind']['xga'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['xga'][STAT_PK] += float(row[GOALIE_DB_XGA])

						if str(row[GOALIE_DB_AVG_SHOT_DIST]) == '-':
							player_data[player_id]['ind']['avg_shot_dist'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['avg_shot_dist'][STAT_PK] += int(row[GOALIE_DB_AVG_SHOT_DIST])

						if str(row[GOALIE_DB_AVG_GOAL_DIST]) == '-':
							player_data[player_id]['ind']['avg_goal_dist'][STAT_PK] += 0
						else:
							player_data[player_id]['ind']['avg_goal_dist'][STAT_PK] += int(row[GOALIE_DB_AVG_GOAL_DIST])
	return player_data

def add_on_ice_data(simulation_param,player_data):
	for season_data in simulation_param['csvfiles']['skater_on_ice']:
		with open(season_data,'rt') as f:
			reader = csv.reader(f, delimiter=',')
			for row in reader:
				if row[1] != 'player_name':

					# Only add players that are playing today.
					player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
					if player_id in ACTIVE_SKATERS: 
						team_id = player_data[player_id]['bio']['team_id']
						if (player_id == 'SEBASTIAN_AHO') and (str(row[SKATER_DB_IND_TEAM_ID]) != 'CAR'):
							#player_id = 'SEBASTIAN_AHO2'
							raise ValueError('Wrong Sebastian Aho')

						if str(row[SKATER_DB_ON_ICE_GP]) == '-':
							player_data[player_id]['on_ice']['gp'] += 0						
						else:
							player_data[player_id]['on_ice']['gp'] += int(row[SKATER_DB_ON_ICE_GP])

						if str(row[SKATER_DB_ON_ICE_CF]) == '-':
							player_data[player_id]['on_ice']['cf'] += 0						
						else:
							player_data[player_id]['on_ice']['cf'] += int(row[SKATER_DB_ON_ICE_CF])

						if str(row[SKATER_DB_ON_ICE_CA]) == '-':
							player_data[player_id]['on_ice']['ca'] += 0
						else:
							player_data[player_id]['on_ice']['ca'] += int(row[SKATER_DB_ON_ICE_CA])

						if str(row[SKATER_DB_ON_ICE_GF]) == '-':
							player_data[player_id]['on_ice']['gf'] += 0						
						else:
							player_data[player_id]['on_ice']['gf'] += int(row[SKATER_DB_ON_ICE_GF])

						if str(row[SKATER_DB_ON_ICE_GA]) == '-':
							player_data[player_id]['on_ice']['ga'] += 0						
						else:
							player_data[player_id]['on_ice']['ga'] += int(row[SKATER_DB_ON_ICE_GA])

						if str(row[SKATER_DB_ON_ICE_SF]) == '-':
							player_data[player_id]['on_ice']['sf'] += 0						
						else:
							player_data[player_id]['on_ice']['sf'] += int(row[SKATER_DB_ON_ICE_SF])

						if str(row[SKATER_DB_ON_ICE_SA]) == '-':
							player_data[player_id]['on_ice']['sa'] += 0						
						else:
							player_data[player_id]['on_ice']['sa'] += int(row[SKATER_DB_ON_ICE_SA])

						if str(row[SKATER_DB_ON_ICE_xGF]) == '-':
							player_data[player_id]['on_ice']['xgf'] += 0						
						else:
							player_data[player_id]['on_ice']['xgf'] += float(row[SKATER_DB_ON_ICE_xGF])

						if str(row[SKATER_DB_ON_ICE_xGA]) == '-':
							player_data[player_id]['on_ice']['xga'] += 0						
						else:
							player_data[player_id]['on_ice']['xga'] += float(row[SKATER_DB_ON_ICE_xGA])

						if str(row[SKATER_DB_ON_ICE_SCF]) == '-':
							player_data[player_id]['on_ice']['scf'] += 0						
						else:
							player_data[player_id]['on_ice']['scf'] += int(row[SKATER_DB_ON_ICE_SCF])

						if str(row[SKATER_DB_ON_ICE_SCA]) == '-':
							player_data[player_id]['on_ice']['sca'] += 0						
						else:
							player_data[player_id]['on_ice']['sca'] += int(row[SKATER_DB_ON_ICE_SCA])

						if str(row[SKATER_DB_ON_ICE_HDCF]) == '-':
							player_data[player_id]['on_ice']['hdcf'] += 0						
						else:
							player_data[player_id]['on_ice']['hdcf'] += int(row[SKATER_DB_ON_ICE_HDCF])

						if str(row[SKATER_DB_ON_ICE_HDCA]) == '-':
							player_data[player_id]['on_ice']['hdca'] += 0						
						else:
							player_data[player_id]['on_ice']['hdca'] += int(row[SKATER_DB_ON_ICE_HDCA])

						if str(row[SKATER_DB_ON_ICE_OZS]) == '-':
							player_data[player_id]['on_ice']['ozs'] += 0
						else:
							player_data[player_id]['on_ice']['ozs'] += int(row[SKATER_DB_ON_ICE_OZS])

						if str(row[SKATER_DB_ON_ICE_NZS]) == '-':
							player_data[player_id]['on_ice']['nzs'] += 0
						else:
							player_data[player_id]['on_ice']['nzs'] += int(row[SKATER_DB_ON_ICE_NZS])

						if str(row[SKATER_DB_ON_ICE_DZS]) == '-':
							player_data[player_id]['on_ice']['dzs'] += 0						
						else:
							player_data[player_id]['on_ice']['dzs'] += int(row[SKATER_DB_ON_ICE_DZS])	

						if str(row[SKATER_DB_ON_ICE_OZFO]) == '-':
							player_data[player_id]['on_ice']['ozfo'] += 0
						else:
							player_data[player_id]['on_ice']['ozfo'] += int(row[SKATER_DB_ON_ICE_OZFO])

						if str(row[SKATER_DB_ON_ICE_NZFO]) == '-':
							player_data[player_id]['on_ice']['nzfo'] += 0
						else:
							player_data[player_id]['on_ice']['nzfo'] += int(row[SKATER_DB_ON_ICE_NZFO])

						if str(row[SKATER_DB_ON_ICE_DZFO]) == '-':
							player_data[player_id]['on_ice']['dzfo'] += 0
						else:
							player_data[player_id]['on_ice']['dzfo'] += int(row[SKATER_DB_ON_ICE_DZFO])
	return player_data

def add_relative_data(simulation_param,player_data):
	with open(simulation_param['csvfiles']['skater_relative'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'Player':
				player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
				if player_id in ACTIVE_SKATERS:
					if str(row[SKATER_DB_RELATIVE_CF_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_cf_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_cf_per_60'] = float(row[SKATER_DB_RELATIVE_CF_PER_60])

					if str(row[SKATER_DB_RELATIVE_CA_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_ca_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_ca_per_60'] = float(row[SKATER_DB_RELATIVE_CA_PER_60])
					
					if str(row[SKATER_DB_RELATIVE_CF_PCG]) == '-':
						player_data[player_id]['on_ice']['rel_cf_pcg'] = 0		
						player_data[player_id]['on_ice']['rel_cf_factor'] = 0		
						player_data[player_id]['on_ice']['rel_ca_factor'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_cf_pcg'] = float(row[SKATER_DB_RELATIVE_CF_PCG])
						player_data[player_id]['on_ice']['rel_cf_factor'] = (player_data[player_id]['on_ice']['rel_cf_pcg']/200 + 1.0) # Higher is better
						player_data[player_id]['on_ice']['rel_ca_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_cf_pcg']/200)# Lower is better

					if str(row[SKATER_DB_RELATIVE_FF_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_ff_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_ff_per_60'] = float(row[SKATER_DB_RELATIVE_FF_PER_60])

					if str(row[SKATER_DB_RELATIVE_FA_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_fa_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_fa_per_60'] = float(row[SKATER_DB_RELATIVE_FA_PER_60])
					
					if str(row[SKATER_DB_RELATIVE_FF_PCG]) == '-':
						player_data[player_id]['on_ice']['rel_ff_pcg'] = 0		
						player_data[player_id]['on_ice']['rel_ff_factor'] = 0		
						player_data[player_id]['on_ice']['rel_fa_factor'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_ff_pcg'] = float(row[SKATER_DB_RELATIVE_FF_PCG])
						player_data[player_id]['on_ice']['rel_ff_factor'] = (player_data[player_id]['on_ice']['rel_ff_pcg']/200 + 1.0) # Higher is better
						player_data[player_id]['on_ice']['rel_fa_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_ff_pcg']/200)# Lower is better

					if str(row[SKATER_DB_RELATIVE_SF_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_sf_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_sf_per_60'] = float(row[SKATER_DB_RELATIVE_SF_PER_60])

					if str(row[SKATER_DB_RELATIVE_SA_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_sa_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_sa_per_60'] = float(row[SKATER_DB_RELATIVE_SA_PER_60])
					
					if str(row[SKATER_DB_RELATIVE_SF_PCG]) == '-':
						player_data[player_id]['on_ice']['rel_sf_pcg'] = 0		
						player_data[player_id]['on_ice']['rel_sf_factor'] = 0		
						player_data[player_id]['on_ice']['rel_sa_factor'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_sf_pcg'] = float(row[SKATER_DB_RELATIVE_SF_PCG])
						player_data[player_id]['on_ice']['rel_sf_factor'] = (player_data[player_id]['on_ice']['rel_sf_pcg']/200 + 1.0) # Higher is better
						player_data[player_id]['on_ice']['rel_sa_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_sf_pcg']/200)# Lower is better

					if str(row[SKATER_DB_RELATIVE_GF_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_gf_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_gf_per_60'] = float(row[SKATER_DB_RELATIVE_GF_PER_60])

					if str(row[SKATER_DB_RELATIVE_GA_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_ga_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_ga_per_60'] = float(row[SKATER_DB_RELATIVE_GA_PER_60])
					
					if str(row[SKATER_DB_RELATIVE_GF_PCG]) == '-':
						player_data[player_id]['on_ice']['rel_gf_pcg'] = 0		
						player_data[player_id]['on_ice']['rel_gf_factor'] = 0		
						player_data[player_id]['on_ice']['rel_ga_factor'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_gf_pcg'] = float(row[SKATER_DB_RELATIVE_GF_PCG])
						player_data[player_id]['on_ice']['rel_gf_factor'] = (player_data[player_id]['on_ice']['rel_gf_pcg']/200 + 1.0) # Higher is better
						player_data[player_id]['on_ice']['rel_ga_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_gf_pcg']/200)# Lower is better

					if str(row[SKATER_DB_RELATIVE_xGF_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_xgf_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_xgf_per_60'] = float(row[SKATER_DB_RELATIVE_xGF_PER_60])

					if str(row[SKATER_DB_RELATIVE_XGA_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_xga_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_xga_per_60'] = float(row[SKATER_DB_RELATIVE_XGA_PER_60])
					
					if str(row[SKATER_DB_RELATIVE_xGF_PCG]) == '-':
						player_data[player_id]['on_ice']['rel_xgf_pcg'] = 0		
						player_data[player_id]['on_ice']['rel_xgf_factor'] = 0		
						player_data[player_id]['on_ice']['rel_xga_factor'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_xgf_pcg'] = float(row[SKATER_DB_RELATIVE_xGF_PCG])
						player_data[player_id]['on_ice']['rel_xgf_factor'] = (player_data[player_id]['on_ice']['rel_xgf_pcg']/200 + 1.0) # Higher is better
						player_data[player_id]['on_ice']['rel_xga_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_xgf_pcg']/200)# Lower is better

					if str(row[SKATER_DB_RELATIVE_SCF_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_scf_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_scf_per_60'] = float(row[SKATER_DB_RELATIVE_SCF_PER_60])

					if str(row[SKATER_DB_RELATIVE_SCA_PER_60]) == '-':
						player_data[player_id]['on_ice']['rel_sca_per_60'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_sca_per_60'] = float(row[SKATER_DB_RELATIVE_SCA_PER_60])
					
					if str(row[SKATER_DB_RELATIVE_SCF_PCG]) == '-':
						player_data[player_id]['on_ice']['rel_scf_pcg'] = 0		
						player_data[player_id]['on_ice']['rel_scf_factor'] = 0		
						player_data[player_id]['on_ice']['rel_sca_factor'] = 0		
					else:
						player_data[player_id]['on_ice']['rel_scf_pcg'] = float(row[SKATER_DB_RELATIVE_SCF_PCG])
						player_data[player_id]['on_ice']['rel_scf_factor'] = (player_data[player_id]['on_ice']['rel_scf_pcg']/200 + 1.0) # Higher is better
						player_data[player_id]['on_ice']['rel_sca_factor'] = (1.0 - player_data[player_id]['on_ice']['rel_scf_pcg']/200)# Lower is better
					'''
					# DEBUG:
					if player_data[player_id]['bio']['team_id'] == simulation_param['debug_team']:
						print(player_id)
						print('   Rel CF factor:  ' + str(player_data[player_id]['on_ice']['rel_cf_factor']))
						print('   Rel CA factor:  ' + str(player_data[player_id]['on_ice']['rel_ca_factor']))
						print('   Rel FF factor:  ' + str(player_data[player_id]['on_ice']['rel_ff_factor']))
						print('   Rel FA factor:  ' + str(player_data[player_id]['on_ice']['rel_fa_factor']))
						print('   Rel SF factor:  ' + str(player_data[player_id]['on_ice']['rel_sf_factor']))
						print('   Rel SA factor:  ' + str(player_data[player_id]['on_ice']['rel_sa_factor']))
						print('   Rel GF factor:  ' + str(player_data[player_id]['on_ice']['rel_gf_factor']))
						print('   Rel GA factor:  ' + str(player_data[player_id]['on_ice']['rel_ga_factor']))
						print('   Rel xGF factor: ' + str(player_data[player_id]['on_ice']['rel_xgf_factor']))
						print('   Rel xGA factor: ' + str(player_data[player_id]['on_ice']['rel_xga_factor']))
						print('   Rel SCF factor: ' + str(player_data[player_id]['on_ice']['rel_scf_factor']))
						print('   Rel SCA factor: ' + str(player_data[player_id]['on_ice']['rel_sca_factor']))
					'''
	return player_data
	
def create_goalie_db(simulation_param):
	global ACTIVE_GOALIES
	output = {}
	goalie_data = add_bio_data_goalie(simulation_param)
	goalie_data = add_es_data_goalie(simulation_param,goalie_data)
	goalie_data = add_pp_data_goalie(simulation_param,goalie_data)
	goalie_data = add_pk_data_goalie(simulation_param,goalie_data)	
	for goalie_id in goalie_data.keys():
		output[goalie_id] = Goalie(goalie_data[goalie_id]['bio'],goalie_data[goalie_id]['ind'])

	# This guy is needed
	if simulation_param['add_average_goalies'] != None:
		for i,team_id in enumerate(simulation_param['add_average_goalies']):
			AVERAGE_GOALIE_BIO = {}
			AVERAGE_GOALIE_BIO['name'] = str('AVERAGE_GOALIE_' + team_id + '_' + str(i))
			AVERAGE_GOALIE_BIO['position'] = 'G'
			AVERAGE_GOALIE_BIO['team_id'] = team_id
			AVERAGE_GOALIE_IND = goalie_data['MARCUS_HOGBERG']['ind'] # This is very randomly selected.
			print('   Adding special (average) goalkeeper ' + AVERAGE_GOALIE_BIO['name'] + ' to ' + team_id)
			ACTIVE_GOALIES.add(AVERAGE_GOALIE_BIO['name'])
			output[AVERAGE_GOALIE_BIO['name']] = Goalie(AVERAGE_GOALIE_BIO,AVERAGE_GOALIE_IND)
	

	return output

def create_team_db(simulation_param):
	global TOTAL_GOALS_PER_GAME
	global TOTAL_POINTS_PER_GAME
	global PROBABILITY_FOR_OT
	output = {}

	fatigue_factors = generate_fatigue_factors()
	with open(simulation_param['csvfiles']['team_es'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		names,reg_arrays,adv_arrays = [],[],[]
		total_gp,total_otl,total_gf = 0,0,0
		for row in reader:
			if row[1] != 'team_name':
				# Get data from row.
				[name,gp,team_toi_es,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xga,xgf,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)

				reg_array = [gp,team_toi_es,w,l,otl,p,gf,ga,p_pcg]
				adv_array = [sf,sa,sf_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdcf,hdca,hdcf_pcg,sv_pcg,pdo]
				fatigue_info = get_fatigue_factor(fatigue_factors,name)
				total_gp += gp
				total_otl += otl
				total_gf += gf
				output[name] = Team(name,reg_array,adv_array,simulation_param['databases']['team_schedules'][name],fatigue_info)

	if DATABASE_BIT_REGISTER[TEAM_HOME_BIT] == True:
		with open(simulation_param['csvfiles']['team_home'],'rt') as f:
			reader = csv.reader(f,delimiter=',')		
			for row in reader:
				if row[1] != 'team_name':
					[name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
					output[name].home_p_pcg = p_pcg
	else:
		for team_id in ACTIVE_TEAMS:
			output[name].home_p_pcg = 1.0

	if DATABASE_BIT_REGISTER[TEAM_AWAY_BIT] == True:
		with open(simulation_param['csvfiles']['team_away'],'rt') as f:
			reader = csv.reader(f,delimiter=',')		
			for row in reader:
				if row[1] != 'team_name':
					[name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
					output[name].away_p_pcg = p_pcg
	else:
		for team_id in ACTIVE_TEAMS:
			output[name].away_p_pcg = 1.0	
	
	with open(simulation_param['csvfiles']['team_pp'],'rt') as f:
		reader = csv.reader(f,delimiter=',')		
		for row in reader:
			if row[1] != 'team_name':
				[name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
				total_gf += gf
				output[name].team_toi_pp = team_toi
				output[name].team_gf_per_pp = 120*gf/team_toi 			# This means how many goals per two minutes (120 seconds) of PP the team gets.
				output[name].team_toi_pp_per_gp = team_toi/gp

	with open(simulation_param['csvfiles']['team_pk'],'rt') as f:
		reader = csv.reader(f,delimiter=',')
		for row in reader:
			if row[1] != 'team_name':
				[name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
				total_gf += gf
				output[name].team_toi_pk = team_toi
				output[name].team_ga_per_pp = 120*ga/team_toi 			# This means how many goals per two minutes of PK the team gives up.
				if output[name].team_ga_per_pp == 0:
					output[name].special_teams_rating = 0
				else:	
					output[name].special_teams_rating = output[name].team_gf_per_pp/output[name].team_ga_per_pp
				output[name].team_toi_pk_per_gp = team_toi/gp

	return output

def add_experimental_data(simulation_param): #add_experimental_data(team_db,skater_db,goalie_db,unavailable_players=None):
	# For readability
	team_db = simulation_param['databases']['team_db']
	skater_db = simulation_param['databases']['skater_db']
	goalie_db = simulation_param['databases']['goalie_db']
	unavailable_players = simulation_param['databases']['unavailable_players']

	sf_dict,gf_dict,cf_dict,ca_dict,scf_dict,sca_dict,hits_dict,hits_taken_dict = defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list)
	estimated_off_dict, estimated_def_dict = defaultdict(list),defaultdict(list)
	shots_against_dict,shots_saved_dict = defaultdict(list),defaultdict(list)
	gp_array = []
	
	# Update Skater data
	for skater_id in skater_db.keys():
		skater = get_skater(skater_db,skater_id)
		skater.ind['toi_pcg'] = [0,0,0]
		skater.ind['toi_pcg'][STAT_ES] = skater.ind['toi_per_gp'][STAT_ES] / team_db[skater.bio['team_id']].team_toi_es_per_gp
		skater.ind['toi_pcg'][STAT_PP] = skater.ind['toi_per_gp'][STAT_PP] / team_db[skater.bio['team_id']].team_toi_pp_per_gp
		skater.ind['toi_pcg'][STAT_PK] = skater.ind['toi_per_gp'][STAT_PK] / team_db[skater.bio['team_id']].team_toi_pk_per_gp

		skater.on_ice['rel_gf_diff_per_60'] = skater.on_ice['gf_diff_per_60'] - team_db[skater.bio['team_id']].gf_diff_per_60

		# Estimate offensive and defensive capabilities. Different depending on the skater has played for multiple teams or not.
		estimated_off_metric = 'sc'
		estimated_off = skater.on_ice[estimated_off_metric + 'f'] * skater.on_ice['rel_' + estimated_off_metric + 'f_factor']
		estimated_def = skater.on_ice[estimated_off_metric + 'a'] * skater.on_ice['rel_' + estimated_off_metric + 'a_factor']
				
		# Not really sure if this code should be included...
		# If included, it is assumed that the player will perform in line with his new team (however, still taking the relative factor into account).
		# If excluded, the player might be "dragged down" by his previous club.
		'''
		if skater.bio['multiple_teams'] == True:
			estimated_off = team_db[skater.bio['team_id']].exp_data[estimated_off_metric + 'f_per_sec'] * skater.ind['toi'][STAT_ES] * skater.on_ice['rel_' + estimated_off_metric + 'f_factor']
			estimated_def = team_db[skater.bio['team_id']].exp_data[estimated_off_metric + 'a_per_sec'] * skater.ind['toi'][STAT_ES] * skater.on_ice['rel_' + estimated_off_metric + 'a_factor']
		'''
		skater.on_ice['estimated_off'] = estimated_off
		skater.on_ice['estimated_def'] = estimated_def
		skater.on_ice['estimated_off_diff'] = estimated_off - estimated_def
		skater.on_ice['estimated_off_per_sec'] = estimated_off / skater.ind['toi'][STAT_ES]
		skater.on_ice['estimated_def_per_sec'] = estimated_def / skater.ind['toi'][STAT_ES]
		skater.on_ice['estimated_off_per_60'] = skater.on_ice['estimated_off_per_sec']*3600
		skater.on_ice['estimated_def_per_60'] = skater.on_ice['estimated_def_per_sec']*3600
		skater.on_ice['estimated_off_per_60_diff'] = skater.on_ice['estimated_off_per_60'] - skater.on_ice['estimated_def_per_60']
		skater.on_ice['estimated_fun_factor'] = skater.on_ice['estimated_off_per_60'] + skater.on_ice['estimated_def_per_60']
		# Only use available players for the ranking data
		# Store estimated offensive and defensive capabilities per team.
		if skater_id not in unavailable_players:
			sf_dict[skater.bio['team_id']].append(skater.ind['isf'][STAT_ES])
			gf_dict[skater.bio['team_id']].append(skater.ind['gf'][STAT_ES])
			hits_dict[skater.bio['team_id']].append(skater.ind['hits'][STAT_ES])
			hits_taken_dict[skater.bio['team_id']].append(skater.ind['hits_taken'][STAT_ES])
			scf_dict[skater.bio['team_id']].append(skater.on_ice['scf'])
			sca_dict[skater.bio['team_id']].append(skater.on_ice['sca'])
			# Store estimated offensive and defensive capabilities per team.
			estimated_off_dict[skater.bio['team_id']].append(estimated_off)
			estimated_def_dict[skater.bio['team_id']].append(estimated_def)
		# Error/warning handling for weird input
		if (skater.on_ice['estimated_off_per_sec']+skater.on_ice['estimated_def_per_sec']) == 0:
			warnings.warn('Bad input for player ' + skater.bio['name'] + '. Setting value ESTIMATED_OFF_PCG to 0.')
			skater.on_ice['estimated_off_pcg'] = 0
		else:
			skater.on_ice['estimated_off_pcg'] = skater.on_ice['estimated_off_per_sec'] / (skater.on_ice['estimated_off_per_sec']+skater.on_ice['estimated_def_per_sec'])
		if skater.get_attribute('team_id') == 'SJS':
			print(skater_id)
			print('   5v5-TOI: {0:.1f} min. 5v5-TOI/GP: {1:.1f} min. 5v5-TOI%: {2:.1f}%'.format(skater.get_toi()/60,skater.get_attribute('toi_per_gp',STAT_ES)/60,100*skater.get_attribute('toi_pcg',STAT_ES)))
			print('   PP-TOI: {0:.1f} s. PP-TOI/GP: {1:.1f}. PP-TOI%: {2:.1f}%'.format(skater.get_toi(STAT_PP)/60,skater.get_attribute('toi_per_gp',STAT_PP)/60,100*skater.get_attribute('toi_pcg',STAT_PP)))
			print('   PK-TOI: {0:.1f} s. PK-TOI/GP: {1:.1f}. PK-TOI%: {2:.1f}%'.format(skater.get_toi(STAT_PK)/60,skater.get_attribute('toi_per_gp',STAT_PK)/60,100*skater.get_attribute('toi_pcg',STAT_PK)))
			print('   Off/60: {0:.1f}. Def/60: {1:.1f}. Off%: {2:.1f}%'.format(skater.get_attribute('estimated_off_per_60'),skater.get_attribute('estimated_def_per_60'),100*skater.get_attribute('estimated_off_pcg')))
			print('   PT/60: {0:.2f}. PD/60: {1:.2f}. PD diff/60: {2:.2f}'.format(skater.get_attribute('pt_per_60'),skater.get_attribute('pd_per_60'),skater.get_attribute('pd_diff_per_60')))	
	# Add ranking data. 
	values_dict = get_skater_values(skater_db)
	for skater_id in ACTIVE_SKATERS:
		skater_db[skater_id].rank['estimated_off_pcg'] = get_rank(skater_db[skater_id].on_ice['estimated_off_pcg'],values_dict['estimated_off_pcg'])
		skater_db[skater_id].rank['primary_points_per_60'] = get_rank(skater_db[skater_id].ind['primary_points_per_60'][0],values_dict['primary_points_per_60'])
		skater_db[skater_id].rank['goal_scoring_rating'] = get_rank(skater_db[skater_id].ind['goal_scoring_rating'][0],values_dict['goal_scoring_rating'])
		if skater_db[skater_id].bio['position'] == 'F':
			WS = WS_FWD
		else:
			WS = WS_DEF
		skater_db[skater_id].rank['total'] = WS[0]*skater_db[skater_id].rank['estimated_off_pcg'] + WS[1]*skater_db[skater_id].rank['primary_points_per_60'] + WS[2]*skater_db[skater_id].rank['goal_scoring_rating']
	

	# Update goalie data
	toi_dict = defaultdict(list)
	for g_id in goalie_db.keys():
		goalie = goalie_db[g_id]
		# Calculate total sa/ss per team, only if player is available
		if g_id not in unavailable_players:
			goalie = get_goalie(goalie_db,g_id)
			shots_against_dict[goalie.bio['team_id']].append(sum(goalie.ind['sa']))			# Using sum to get sa/sv for all strengths (EV/PP/PK)
			shots_saved_dict[goalie.bio['team_id']].append(sum(goalie.ind['sv']))
			toi_dict[goalie.bio['team_id']].append(goalie.ind['toi'][STAT_ES])

	for g_id in goalie_db.keys():
		goalie = goalie_db[g_id]
		goalie.ind['toi_pcg'][STAT_ES] = goalie.ind['toi'][STAT_ES] / sum(toi_dict[goalie.bio['team_id']])

	# Update team data
	for team_id in team_db.keys():
		gp_array.append(team_db[team_id].gp)
	avg_gp = np.mean(gp_array)
	if avg_gp > 20:
		avg_gp = 20

	print('\nTeam metrics (5v5):')
	tmp_list = []
	for team_id in ACTIVE_TEAMS:
		team_sh_pcg = sum(gf_dict[team_id])/sum(sf_dict[team_id])
		team_sv_pcg = sum(shots_saved_dict[team_id])/sum(shots_against_dict[team_id])
		team_estimated_off = sum(estimated_off_dict[team_id])								# How much offense the team generates, based on the individual players.
		team_estimated_def = sum(estimated_def_dict[team_id])								# How much offense the team gives up, based on the individual players.
		team_scf = sum(scf_dict[team_id])
		team_sca = sum(sca_dict[team_id])
		team_db[team_id].exp_data['hits'] = sum(hits_dict[team_id])
		team_db[team_id].exp_data['hits_taken'] = sum(hits_taken_dict[team_id])
		team_db[team_id].exp_data['hits_diff'] = team_db[team_id].exp_data['hits'] - team_db[team_id].exp_data['hits_taken']
		team_db[team_id].exp_data['sh_pcg'] = team_sh_pcg
		team_db[team_id].exp_data['sv_pcg'] = team_sv_pcg
		team_db[team_id].exp_data['estimated_off'] = team_estimated_off*team_db[team_id].exp_data['sh_pcg']
		team_db[team_id].exp_data['estimated_def'] = team_estimated_def*(1-team_db[team_id].exp_data['sv_pcg'])
		team_db[team_id].exp_data['estimated_off_pcg'] = team_db[team_id].exp_data['estimated_off']/(team_db[team_id].exp_data['estimated_off']+team_db[team_id].exp_data['estimated_def'])

		team_db[team_id].exp_data['pdo'] = team_db[team_id].exp_data['sh_pcg']+team_db[team_id].exp_data['sv_pcg']
		team_db[team_id].exp_data['scf_per_60'] = (3600*team_scf/team_db[team_id].team_toi_es)/5  	# Division by five to compare with ind. skater stat.
		team_db[team_id].exp_data['sca_per_60'] = (3600*team_sca/team_db[team_id].team_toi_es)/5	# Division by five to compare with ind. skater stat.
		team_db[team_id].exp_data['scf_pcg'] = (team_scf/(team_scf+team_sca))
		
		# Assign ratings. Different for pre_season or non_pre_season.
		team_db[team_id].exp_data['pre_season_rating'] = team_db[team_id].exp_data['estimated_off_pcg']
		team_db[team_id].exp_data['in_season_rating'] = (team_db[team_id].p_pcg*P_PCG_FACTOR*avg_gp/20) + team_db[team_id].exp_data['estimated_off_pcg']

		print('   {0}: Rating: {1:.3f}. "Goodness": {2:.3f}. Play-control: {3:.1f}%. PDO: {4:.3f}. Shooting: {5:.1f}%. Saving: {6:.1f}%'.format(team_id,team_db[team_id].exp_data['in_season_rating'],team_db[team_id].exp_data['estimated_off_pcg'],100*team_db[team_id].exp_data['scf_pcg'],team_db[team_id].exp_data['pdo'],100*team_db[team_id].exp_data['sh_pcg'],100*team_db[team_id].exp_data['sv_pcg']))

	# Add ranking data. This needs to be done in a separate for-loop because of 'estimated_off_pcg'
	# Get values for ranking
	values_dict = get_team_values(team_db)
	
	# Assign ranking(s)
	for team_id in ACTIVE_TEAMS:
		team_db[team_id].rank['p_pcg'] = get_rank(team_db[team_id].p_pcg,values_dict['p_pcg'])
		team_db[team_id].rank['gf_pcg'] = get_rank(team_db[team_id].gf_pcg,values_dict['gf_pcg'])
		team_db[team_id].rank['sf_pcg'] = get_rank(team_db[team_id].sf_pcg,values_dict['sf_pcg'])
		team_db[team_id].rank['cf_pcg'] = get_rank(team_db[team_id].cf_pcg,values_dict['cf_pcg'])
		team_db[team_id].rank['ff_pcg'] = get_rank(team_db[team_id].ff_pcg,values_dict['ff_pcg'])
		team_db[team_id].rank['xgf_pcg'] = get_rank(team_db[team_id].xgf_pcg,values_dict['xgf_pcg'])
		team_db[team_id].rank['scf_pcg'] = get_rank(team_db[team_id].scf_pcg,values_dict['scf_pcg'])
		team_db[team_id].rank['hdcf_pcg'] = get_rank(team_db[team_id].hdcf_pcg,values_dict['hdcf_pcg'])
		team_db[team_id].rank['sv_pcg'] = get_rank(team_db[team_id].sv_pcg,values_dict['sv_pcg'])
		team_db[team_id].rank['pdo'] = get_rank(team_db[team_id].pdo,values_dict['pdo'])
		team_db[team_id].rank['hits'] = get_rank(team_db[team_id].exp_data['hits'],values_dict['hits'])
		team_db[team_id].rank['hits_taken'] = get_rank(team_db[team_id].exp_data['hits_taken'],values_dict['hits_taken'])
		team_db[team_id].rank['hits_diff'] = get_rank(team_db[team_id].exp_data['hits_diff'],values_dict['hits_diff'])
		team_db[team_id].rank['estimated_off_pcg'] = get_rank(team_db[team_id].exp_data['estimated_off_pcg'],values_dict['estimated_off_pcg'])
		team_db[team_id].rank['in_season_rating'] = get_rank(team_db[team_id].exp_data['in_season_rating'],values_dict['in_season_rating'])

	# Store values for the return
	simulation_param['databases']['team_db'] = team_db
	simulation_param['databases']['skater_db'] = skater_db
	simulation_param['databases']['goalie_db'] = goalie_db
	simulation_param['databases']['unavailable_players'] = unavailable_players
	return simulation_param 	#return [team_db,skater_db,goalie_db]

def generate_schedule(csvfiles):
	schedule_per_team = defaultdict(list)
	schedule_per_date = defaultdict(list)
	with open(csvfiles['schedule'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			date = str(row[0])
			home_team_id = get_team_id(row[3])
			away_team_id = get_team_id(row[2])
			schedule_per_team[home_team_id].append(away_team_id)
			schedule_per_team[away_team_id].append(home_team_id)
			schedule_per_date[date].append([home_team_id,away_team_id])
	return [schedule_per_team, schedule_per_date]

def create_team_specific_db(simulation_param):
	output = defaultdict(dict)
	for skater_id in simulation_param['databases']['skater_db'].keys():
		skater = get_skater(simulation_param['databases']['skater_db'],skater_id)
		if (skater_id not in simulation_param['databases']['unavailable_players']):
			output[skater.bio['team_id']][skater.bio['name']] = skater
	return output

def get_row_values_for_goalie_db(row):
	if str(row[GOALIE_DB_NAME]) == '-':
		raise ValueError('Incorrect Player-ID')
	else:
		name = generate_player_id(row[GOALIE_DB_NAME])
	
	if str(row[GOALIE_DB_TOI]) == '-':
		toi = 0.0						
	else:
		toi = int(60*float(row[GOALIE_DB_TOI]))
	
	if str(row[GOALIE_DB_SA]) == '-':
		sa = 0
	else:
		sa = int(row[GOALIE_DB_SA])

	if str(row[GOALIE_DB_SV]) == '-':
		sv = 0
	else:
		sv = int(row[GOALIE_DB_SV])

	if str(row[GOALIE_DB_GA]) == '-':
		ga = 0
	else:
		ga = int(row[GOALIE_DB_GA])	
	
	if str(row[GOALIE_DB_SV_PCG]) == '-':
		sv_pcg = 0.0						
	else:
		sv_pcg = float(row[GOALIE_DB_SV_PCG])

	if str(row[GOALIE_DB_GAA]) == '-':
		gaa = 0.0						
	else:
		gaa = float(row[GOALIE_DB_GAA])
	
	if str(row[GOALIE_DB_GSAA]) == '-':
		gsaa = 0
	else:
		gsaa = float(row[GOALIE_DB_GSAA])

	if str(row[GOALIE_DB_XGA]) == '-':
		xga = 0
	else:
		xga = float(row[GOALIE_DB_XGA])
	
	if str(row[GOALIE_DB_AVG_SHOT_DIST]) == '-':
		avg_shot_dist = 0.0						
	else:
		avg_shot_dist = float(row[GOALIE_DB_AVG_SHOT_DIST])

	if str(row[GOALIE_DB_AVG_GOAL_DIST]) == '-':
		avg_goal_dist = 0.0						
	else:
		avg_goal_dist = float(row[GOALIE_DB_AVG_GOAL_DIST])


	return [name,toi,sa,sv,ga,sv_pcg,gaa,gsaa,xga,avg_shot_dist,avg_goal_dist]

def get_row_values_for_team_db(row):
	# Strings
	if str(row[TEAM_DB_NAME_COL]) == '-':
		raise ValueError('Incorrect Team-ID')
	elif str(row[TEAM_DB_NAME_COL]) == 'St Louis Blues': # Special case to fix descrepencies in worksheets
		name = 'STL'
	else:
		name = get_team_id(str(row[TEAM_DB_NAME_COL]))
	
	# Integers
	if str(row[TEAM_DB_GP_COL]) == '-':
		gp = 0	
	else:
		gp = int(row[TEAM_DB_GP_COL])
	
	if str(row[TEAM_DB_TOI_COL]) == '-':
		team_toi = 0
	else:
		team_toi = int(60*float(row[TEAM_DB_TOI_COL]))

	if str(row[TEAM_DB_W_COL]) == '-':
		w = 0	
	else:
		w = int(row[TEAM_DB_W_COL])

	if str(row[TEAM_DB_L_COL]) == '-':
		l = 0	
	else:
		l = int(row[TEAM_DB_L_COL])

	if str(row[TEAM_DB_OTL_COL]) == '-':
		otl = 0	
	else:
		otl = int(row[TEAM_DB_OTL_COL])

	if str(row[TEAM_DB_P_COL]) == '-':
		p = 0	
	else:
		p = int(row[TEAM_DB_P_COL])

	if str(row[TEAM_DB_CF_COL]) == '-':
		cf = 0	
	else:
		cf = int(row[TEAM_DB_CF_COL])
	
	if str(row[TEAM_DB_CA_COL]) == '-':
		ca = 0	
	else:
		ca = int(row[TEAM_DB_CA_COL])

	if str(row[TEAM_DB_FF_COL]) == '-':
		ff = 0	
	else:
		ff = int(row[TEAM_DB_FF_COL])
	
	if str(row[TEAM_DB_FA_COL]) == '-':
		fa = 0	
	else:
		fa = int(row[TEAM_DB_FA_COL])
	
	if str(row[TEAM_DB_SF_COL]) == '-':
		sf = 0	
	else:
		sf = int(row[TEAM_DB_SF_COL])
	
	if str(row[TEAM_DB_SA_COL]) == '-':
		sa = 0	
	else:
		sa = int(row[TEAM_DB_SA_COL])

	if str(row[TEAM_DB_GF_COL]) == '-':
		gf = 0	
	else:
		gf = int(row[TEAM_DB_GF_COL])
	
	if str(row[TEAM_DB_GA_COL]) == '-':
		ga = 0	
	else:
		ga = int(row[TEAM_DB_GA_COL])

	if str(row[TEAM_DB_SCF_COL]) == '-':
		scf = 0	
	else:
		scf = int(row[TEAM_DB_SCF_COL])
	
	if str(row[TEAM_DB_SCA_COL]) == '-':
		sca = 0	
	else:
		sca = int(row[TEAM_DB_SCA_COL])

	if str(row[TEAM_DB_HDCF_COL]) == '-':
		hdcf = 0	
	else:
		hdcf = int(row[TEAM_DB_HDCF_COL])
	
	if str(row[TEAM_DB_HDCA_COL]) == '-':
		hdca = 0	
	else:
		hdca = int(row[TEAM_DB_HDCA_COL])

	# Floats
	if str(row[TEAM_DB_P_PCG_COL]) == '-':
		p_pcg = 0.0
	else:
		p_pcg = float(row[TEAM_DB_P_PCG_COL])
	
	if str(row[TEAM_DB_SF_PCG_COL]) == '-':
		sf_pcg = 0.0
	else:
		sf_pcg = float(row[TEAM_DB_SF_PCG_COL])/100

	if str(row[TEAM_DB_CF_PCG_COL]) == '-':
		cf_pcg = 0.0
	else:
		cf_pcg = float(row[TEAM_DB_CF_PCG_COL])/100

	if str(row[TEAM_DB_FF_PCG_COL]) == '-':
		ff_pcg = 0.0
	else:
		ff_pcg = float(row[TEAM_DB_FF_PCG_COL])/100

	if str(row[TEAM_DB_SCF_PCG_COL]) == '-':
		scf_pcg = 0.0
	else:
		scf_pcg = float(row[TEAM_DB_SCF_PCG_COL])/100

	if str(row[TEAM_DB_xGF_COL]) == '-':
		xgf = 0
	else:
		xgf = float(row[TEAM_DB_xGF_COL])

	if str(row[TEAM_DB_xGA_COL]) == '-':
		xga = 0
	else:
		xga = float(row[TEAM_DB_xGA_COL])

	if str(row[TEAM_DB_xGF_PCG_COL]) == '-':
		xgf_pcg = 0.0
	else:
		xgf_pcg = float(row[TEAM_DB_xGF_PCG_COL])/100

	if str(row[TEAM_DB_HDCF_PCG_COL]) == '-':
		hdcf_pcg = 0.0
	else:
		hdcf_pcg = float(row[TEAM_DB_HDCF_PCG_COL])/100

	if str(row[TEAM_DB_SV_PCG_COL]) == '-':
		sv_pcg = 0.0
	else:
		sv_pcg = float(row[TEAM_DB_SV_PCG_COL])/100
	
	if str(row[TEAM_DB_PDO_COL]) == '-':
		pdo = 0.0
	else:
		pdo = float(row[TEAM_DB_PDO_COL])
	
	return [name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,xgf,xga,xgf_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo]


def modify_player_db(simulation_param):
	'''
	Manually update databases if needed.
	Ex:
		simulation_param['databases'][skater_db] = ...
		simulation_param['databases'][goalie_db] = ...
	'''

	# ADD MODIFICATIONS TO DATABASE HERE
	
	
	return simulation_param

def update_new_team(db,player,new_team):
	global ACTIVE_PLAYERS
	if (player not in ACTIVE_PLAYERS):
		raise ValueError('Unknown player ' + player + '.')

	if new_team == None:
		#print('Removing player ' + player + ' from database')
		del db[player] 						# db is a dict()
		ACTIVE_PLAYERS.remove(player) 		# ACTIVE_PLAYERS is a set()
	else:
		if new_team == db[player].bio['team_id']:
			warnings.warn('Player ' + player + ' already playing for team ' + db[player].bio['team_id'])
		else:
			#print('Moving player ' + player + ' to ' + get_long_name(new_team))
			db[player].bio['team_id'] = new_team
			db[player].bio['multiple_teams'] = True
	return db


def add_unavailable_player(simulation_param,player_id):
	simulation_param['databases']['unavailable_players'].add(player_id)
	# Make sure to remove player from the team specific database.
	player = get_player(simulation_param,player_id)
	team_id = player.get_attribute('team_id')
	del simulation_param['databases']['team_specific_db'][team_id][player_id]
	return simulation_param

def get_unavailable_players():
	unavailable_players = defaultdict(list)
	dict_output = generic_csv_reader('Data/Unavailable_Players.csv',dict_key_attribute='team_id')
	for team_id in ACTIVE_TEAMS:
		if dict_output[team_id]['unavailable_players'] == '[]':
			unavailable_players[team_id] = []
		else:
			str_array = dict_output[team_id]['unavailable_players'][1:-1]
			str_array = str_array.replace("'","")
			str_array = str_array.replace(' ','')
			names = str_array.split(',')
			for name in names:
				unavailable_players[team_id].append(name) 			# This output is not used at the moment.

	all_unavailable_players = set()
	for team_id in unavailable_players.keys():
		for player_id in unavailable_players[team_id]:
			if player_id == 'DAN_DEKEYSER':
				player_id = 'DANNY_DEKEYSER'
			
			all_unavailable_players.add(player_id)
	return all_unavailable_players

def get_team_id_for_player(name,team_id):
	manually_checked_players = set()
	manually_checked_players.add('MARCO_SCANDELLA')
	manually_checked_players.add('ILYA_KOVALCHUK')
	manually_checked_players.add('VLADISLAV_NAMESTNIKOV')
	new_team = {}
	#new_team['VLADISLAV_NAMESTNIKOV'] = 'OTT'
	new_team['ERIK_GUDBRANSON'] = 'ANA'
	new_team['ANDREAS_MARTINSEN'] = 'PTI'
	new_team['BRENDAN_PERLINI'] = 'DET'
	new_team['JACOB_DE_LA_ROSE'] = 'STL'
	new_team['ROBBY_FABBRI'] = 'DET'
	new_team['CHANDLER_STEPHENSON'] = 'VGK'
	new_team['NICK_SHORE'] = 'WPG'
	new_team['TAYLOR_HALL'] = 'ARI'
	new_team['STEFAN_NOESEN'] = 'SJS'
	new_team['MARCO_SCANDELLA'] = 'STL'
	new_team['MIKE_REILLY'] = 'OTT'
	#new_team['ILYA_KOVALCHUK'] = 'MTL'
	new_team['MICHAEL_FROLIK'] = 'BUF'
	new_team['JACK_CAMPBELL'] = 'TOR'
	new_team['KYLE_CLIFFORD'] = 'TOR'
	new_team['TREVOR_MOORE'] = 'LAK'
	new_team['NICK_SEELER'] = 'CHI'
	new_team['JASON_ZUCKER'] = 'PIT'
	new_team['ALEX_GALCHENYUK'] = 'MIN'
	new_team['ANDY_GREENE'] = 'NYI'
	new_team['BRENDEN_DILLON'] = 'WSH'
	new_team['TYLER_TOFFOLI'] = 'VAN'
	new_team['JULIEN_GAUTHIER'] = 'NYR'
	new_team['BLAKE_COLEMAN'] = 'TBL'
	new_team['ALEC_MARTINEZ'] = 'VGK'
	new_team['DYLAN_DEMELO'] = 'WPG'
	new_team['TIM_SCHALLER'] = 'LAK'
	new_team['JAYCE_HAWRYLUK'] = 'OTT'
	new_team['DENIS_MALGIN'] = 'TOR'
	new_team['CODY_EAKIN'] = 'WPG'
	new_team['DANTON_HEINEN'] = 'ANA'
	new_team['NICK_RITCHIE'] = 'BOS'
	new_team['DEREK_GRANT'] = 'PHI'
	new_team['PATRICK_MARLEAU'] = 'PIT'
	new_team['WAYNE_SIMMONDS'] = 'BUF'
	new_team['NATE_THOMPSON'] = 'PHI'
	new_team['VINCENT_TROCHECK'] = 'CAR'
	new_team['ERIK_HAULA'] = 'FLA'
	new_team['LUCAS_WALLMARK'] = 'FLA'
	new_team['JEAN-GABRIEL_PAGEAU'] = 'NYI'
	new_team['VLADISLAV_NAMESTNIKOV'] = 'COL'
	new_team['ILYA_KOVALCHUK'] = 'WSH'
	new_team['ANDREAS_ATHANASIOU'] = 'EDM'
	new_team['SAM_GAGNER'] = 'DET'
	new_team['TYLER_ENNIS'] = 'EDM'
	new_team['EVAN_RODRIGUES'] = 'PIT'
	new_team['CONOR_SHEARY'] = 'PIT'
	new_team['DOMINIK_KAHUN'] = 'BUF'
	new_team['SONNY_MILANO'] = 'ANA'
	new_team['DEVIN_SHORE'] = 'CBJ'
	new_team['BARCLAY_GOODROW'] = 'TBL'
	new_team['DANIEL_SPRONG'] = 'WSH'
	new_team['MIKE_GREEN'] = 'EDM'
	new_team['CHRISTIAN_DJOOS'] = 'ANA'
	new_team['NICK_COUSINS'] = 'VGK'
	new_team['MATTHEW_PECA'] = 'OTT'
	new_team['ZACH_BOGOSIAN'] = 'TBL'
	new_team['CODY_GOLOUBEF'] = 'DET'
	new_team['ANDREW_AGOZZINO'] = 'ANA'
	new_team['MATT_IRWIN'] = 'ANA'
	new_team['DEREK_FORBORT'] = 'LAK'
	new_team['BRADY_SKJEI'] = 'CAR'
	new_team['ERIK_GUSTAFSSON'] = 'CGY'
	new_team['ROBIN_LEHNER'] ='VGK'

	# Make sure players have been added to their new clubs. If not, set an error.
	team_id_arr = (team_id.replace(' ','').split(','))
	if len(team_id_arr) > 1:
		if name not in new_team.keys():
			raise ValueError('Player ' + name + ' has more than one team(s). Team-ID: ' + team_id)
		if len(team_id_arr) > 2:
			if name not in manually_checked_players:
				raise ValueError('Player ' + name + ' changed club more than once. Please add to "manually_checked_players" to continue.')

	if team_id == 'L.A':
		team_id = 'LAK'
	elif team_id == 'N.J':
		team_id = 'NJD'
	elif team_id == 'S.J':
		team_id = 'SJS'
	elif team_id == 'T.B':
		team_id = 'TBL'		

	if name in set(new_team.keys()):
		return new_team[name]
	else:
		return team_id
