from nhl_helpers import *
from nhl_defines import *
from nhl_classes import *

def create_databases(simulation_param):
	global ACTIVE_PLAYERS
	simulation_param['databases'] = {}
	# Create schedule database
	[team_schedules,season_schedule] = generate_schedule(simulation_param['csvfiles'])
	simulation_param['databases']['team_schedules'] = team_schedules
	simulation_param['databases']['season_schedule'] = season_schedule

	# Create team and skater database.
	print('   Creating Team-DB')
	simulation_param['databases']['team_db'] = create_team_db(simulation_param)
	print('   Creating Skater-DB')
	s_db = create_skater_db(simulation_param)
	print('   Creating Goalie-DB')
	g_db = create_goalie_db(simulation_param)
	ACTIVE_PLAYERS = ACTIVE_SKATERS.union(ACTIVE_GOALIES)
	old_rating, new_rating, diff_rating = {},{},{}

	# Find out who is available.
	simulation_param['databases']['unavailable_players'] = get_unavailable_players()
	for player_id in simulation_param['databases']['unavailable_players']:
		if (player_id not in s_db) and (player_id not in g_db):
			raise ValueError('Unavailable player ' + player_id + ' not in skaterDB.')
	
	# Add experimental data - needs to be done after creation of SkaterDB (and GoalieDB).
	print('   Adding experimental data')
	[simulation_param['databases']['team_db'],simulation_param['databases']['skater_db']] = add_experimental_data(simulation_param['databases']['team_db'],s_db,g_db,simulation_param['databases']['unavailable_players'],simulation_param['debug_team'])
	
	for team_id in ACTIVE_TEAMS:
		team = simulation_param['databases']['team_db'][team_id]
		old_rating[team_id] = team.get_ratings()[1]
	
	if simulation_param['include_offseason_moves'] == True:
		print('   Modifying databases for off-season moves')
		[s_db,g_db] = modify_player_db(s_db,g_db)
		
		# Update experimental data after modification of skater_db and goalie_db.
		[simulation_param['databases']['team_db'],simulation_param['databases']['skater_db']] = add_experimental_data(simulation_param['databases']['team_db'],s_db,g_db,simulation_param['databases']['unavailable_players'])
		# Update ratings after off-season moves
		for team_id in ACTIVE_TEAMS:
			team = simulation_param['databases']['team_db'][team_id]
			new_rating[team_id] = team.get_ratings()[1]
			diff_rating[team_id] = new_rating[team_id] - old_rating[team_id]
			#print('{0}: Difference in rating after off-seasons: {1:.1f}%'.format(team_id,100*diff_rating[team_id]/old_rating[team_id]))

	# Save the goalie database.
	simulation_param['databases']['goalie_db'] = g_db

	simulation_param['databases']['starting_goalies'] = generate_all_teams_dict(return_type=None)
	simulation_param['databases']['team_specific_db'] = create_team_specific_db(simulation_param)	

	return simulation_param

def create_skater_db(simulation_param):
	output = {}
	player_data = add_bio_data(simulation_param)
	player_data = add_es_data(simulation_param,player_data)
	player_data = add_pp_data(simulation_param,player_data)
	player_data = add_pk_data(simulation_param,player_data)
	player_data = add_on_ice_data(simulation_param,player_data)
	player_data = add_corsica_data(simulation_param,player_data)

	for player_id in player_data.keys():
		if player_data[player_id]['ind'] == None or player_data[player_id]['on_ice'] == None:
			warnings.warn('\nSkipping player ' + player_id)
		else:
			output[player_id] = Skater(player_data[player_id]['bio'],player_data[player_id]['ind'],player_data[player_id]['on_ice'])
	return output

def add_bio_data(simulation_param):
	global ACTIVE_SKATERS
	player_data = {}
	with open(simulation_param['csvfiles']['skaters_bio'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'Player':
				# NAME
				if str(row[SKATER_DB_BIO_NAME]) == '-':
					raise ValueError('Incorrect Player-ID')
				else:
					name = generate_player_id(row[SKATER_DB_BIO_NAME])
				# TEAM
				if str(row[SKATER_DB_BIO_TEAM_ID]) == '-':
					raise ValueError('Incorrect Team-ID')
				else:
					team_id = get_team_id_for_player(name,str(row[SKATER_DB_BIO_TEAM_ID]))
				# POSITION
				if str(row[SKATER_DB_BIO_POSITION]) == '-':
					raise ValueError('Incorrect Player position')					
				else:
					position = str(row[SKATER_DB_BIO_POSITION])
					if ('C' in position) or ('L' in position) or ('R' in position):
						position = 'F'

				if str(row[SKATER_DB_BIO_AGE]) == '-':
					age = 0						
				else:
					age = int(row[SKATER_DB_BIO_AGE])

				if str(row[SKATER_DB_BIO_HEIGHT]) == '-':
					height = 0						
				else:
					height = int(row[SKATER_DB_BIO_HEIGHT])*2.54 # Convert to centimeters.
				
				if str(row[SKATER_DB_BIO_WEIGHT]) == '-':
					weight = 0						
				else:
					weight = int(row[SKATER_DB_BIO_WEIGHT])*0.453592 # Convert to kilograms.

				# DRAFT
				if str(row[SKATER_DB_BIO_DRAFT_YEAR]) == '-':
					draft_year = 0						
				else:
					draft_year = int(row[SKATER_DB_BIO_DRAFT_YEAR])
				
				if str(row[SKATER_DB_BIO_DRAFT_TEAM]) == '-':
					draft_team = 'N/A'
				else:
					draft_team = str(row[SKATER_DB_BIO_DRAFT_TEAM])
				
				if str(row[SKATER_DB_BIO_DRAFT_ROUND]) == '-':
					draft_round = 7 # Default to last round			
				else:
					draft_round = int(row[SKATER_DB_BIO_DRAFT_ROUND])
				
				if str(row[SKATER_DB_BIO_ROUND_PICK]) == '-':
					round_pick = 32	# Default to last pick			
				else:
					round_pick = int(row[SKATER_DB_BIO_ROUND_PICK])
				
				if str(row[SKATER_DB_BIO_TOTAL_DRAFT_POS]) == '-':
					total_draft_pos = 225	# Default to one pick after last pick in the last round					
				else:
					total_draft_pos = int(row[SKATER_DB_BIO_TOTAL_DRAFT_POS])

				if name == 'SEBASTIAN_AHO' and team_id != 'CAR':
					name = 'SEBASTIAN_AHO2'
				ACTIVE_SKATERS.add(name)
				player_data[name] = {}
				player_data[name]['bio'] = [name,team_id,position,age,height,weight,draft_team,draft_year,draft_round,round_pick,total_draft_pos]
				# Setup empty structs.
				player_data[name]['ind'] = None
				player_data[name]['on_ice'] = None
	return player_data

def add_es_data(simulation_param,player_data):
	with open(simulation_param['csvfiles']['skaters_es'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'Player':
				# Only add players that are playing today.
				player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
				if player_id in ACTIVE_SKATERS:
					team_id = player_data[player_id]['bio'][1]
					if (player_id == 'SEBASTIAN_AHO') and (str(row[SKATER_DB_ES_TEAM_ID]) != 'CAR'):
						#player_id = 'SEBASTIAN_AHO2'
						raise ValueError('Wrong Sebastian Aho')
					
					player_data[player_id]['ind'] = {}

					if str(row[SKATER_DB_ES_TEAM_ID]) == '-':
						raise ValueError('Incorrect team_id ' + str(row[SKATER_DB_ES_TEAM_ID]))
					else:
						player_data[player_id]['ind']['multiple_teams'] = False
						if len(str(row[SKATER_DB_ES_TEAM_ID]).split(',')) > 1:
							player_data[player_id]['ind']['multiple_teams'] = True
					
					if str(row[SKATER_DB_ES_TOI]) == '-':
						player_data[player_id]['ind']['toi'] = [0,0,0]
						toi = 0
					else:
						toi = int(60*float(row[SKATER_DB_ES_TOI]))
						player_data[player_id]['ind']['toi'] = [toi,0,0]

					if str(row[SKATER_DB_ES_GOALS]) == '-':
						player_data[player_id]['ind']['gf'] = [0,0,0]
					else:
						player_data[player_id]['ind']['gf'] = [int(row[SKATER_DB_ES_GOALS]),0,0]
					
					if str(row[SKATER_DB_ES_ASSIST]) == '-':
						player_data[player_id]['ind']['assist'] = [0,0,0]
					else:
						player_data[player_id]['ind']['assist'] = [int(row[SKATER_DB_ES_ASSIST]),0,0]

					if str(row[SKATER_DB_ES_FIRST_ASSIST]) == '-':
						player_data[player_id]['ind']['f_assist'] = [0,0,0]					
					else:
						player_data[player_id]['ind']['f_assist'] = [int(row[SKATER_DB_ES_FIRST_ASSIST]),0,0]

					if str(row[SKATER_DB_ES_SECOND_ASSIST]) == '-':
						player_data[player_id]['ind']['s_assist'] = [0,0,0]				
					else:
						player_data[player_id]['ind']['s_assist'] = [int(row[SKATER_DB_ES_SECOND_ASSIST]),0,0]

					if str(row[SKATER_DB_ES_SF]) == '-':
						player_data[player_id]['ind']['isf'] = [0,0,0]
					else:
						sf = int(row[SKATER_DB_ES_SF])
						player_data[player_id]['ind']['isf'] = [sf,0,0]

					if str(row[SKATER_DB_ES_ICF]) == '-':
						player_data[player_id]['ind']['icf'] = [0,0,0]
					else:
						player_data[player_id]['ind']['icf'] = [int(row[SKATER_DB_ES_ICF]),0,0]
						
					if str(row[SKATER_DB_ES_TOTAL_PENALTIES]) == '-':
						player_data[player_id]['ind']['pt'] = [0,0,0]
					else:
						pt = int(row[SKATER_DB_ES_TOTAL_PENALTIES])
						player_data[player_id]['ind']['pt'] = [pt,0,0]

					if str(row[SKATER_DB_ES_PENALTIES_DRAWN]) == '-':
						player_data[player_id]['ind']['pd'] = [0,0,0]
					else:
						pd = int(row[SKATER_DB_ES_PENALTIES_DRAWN])
						player_data[player_id]['ind']['pd'] = [pd,0,0]

					# Float
					if str(row[SKATER_DB_ES_SH_PCG]) == '-':
						player_data[player_id]['ind']['ish_pcg'] = [0.0,0.0,0.0]						
					else:
						player_data[player_id]['ind']['ish_pcg'] = [float(row[SKATER_DB_ES_SH_PCG])/100,0.0,0.0]
					
					if str(row[SKATER_DB_ES_IXG]) == '-':
						player_data[player_id]['ind']['ixg'] = [0.0,0.0,0.0]
					else:
						player_data[player_id]['ind']['ixg'] = [float(row[SKATER_DB_ES_IXG]),0.0,0.0]

					player_data[player_id]['ind']['toi_pcg'] = [(toi/get_team(simulation_param['databases']['team_db'],team_id).team_toi_es),0.0,0.0]
					player_data[player_id]['ind']['sf_per_sec'] = [sf/toi,0.0,0.0]
					player_data[player_id]['ind']['pt_per_sec'] = [pt/toi,0.0,0.0]
					player_data[player_id]['ind']['pd_per_sec'] = [pd/toi,0.0,0.0]
	return player_data

def add_pp_data(simulation_param,player_data):
	with open(simulation_param['csvfiles']['skaters_pp'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'Player':
				# Only add players that are playing today.
				player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
				if player_id in ACTIVE_SKATERS:
					team_id = player_data[player_id]['bio'][1]
					if (player_id == 'SEBASTIAN_AHO') and (str(row[SKATER_DB_ES_TEAM_ID]) != 'CAR'):
						#player_id = 'SEBASTIAN_AHO2'
						raise ValueError('Wrong Sebastian Aho')

					if str(row[SKATER_DB_PP_TOI]) == '-':
						player_data[player_id]['ind']['toi'][STAT_PP] = 0						
					else:
						toi = int(60*float(row[SKATER_DB_PP_TOI]))
						player_data[player_id]['ind']['toi'][STAT_PP] = toi
					
					if str(row[SKATER_DB_PP_GOALS]) == '-':
						player_data[player_id]['ind']['gf'][STAT_PP] = 0						
					else:
						player_data[player_id]['ind']['gf'][STAT_PP] = int(row[SKATER_DB_PP_GOALS])
					
					if str(row[SKATER_DB_PP_ASSIST]) == '-':
						player_data[player_id]['ind']['assist'][STAT_PP] = 0						
					else:
						player_data[player_id]['ind']['assist'][STAT_PP] = int(row[SKATER_DB_PP_ASSIST])

					if str(row[SKATER_DB_PP_FIRST_ASSIST]) == '-':
						player_data[player_id]['ind']['f_assist'][STAT_PP] = 0						
					else:
						player_data[player_id]['ind']['f_assist'][STAT_PP] = int(row[SKATER_DB_PP_FIRST_ASSIST])

					if str(row[SKATER_DB_PP_SECOND_ASSIST]) == '-':
						player_data[player_id]['ind']['s_assist'][STAT_PP] = 0						
					else:
						player_data[player_id]['ind']['s_assist'][STAT_PP] = int(row[SKATER_DB_PP_SECOND_ASSIST])

					if str(row[SKATER_DB_PP_SF]) == '-':
						player_data[player_id]['ind']['isf'][STAT_PP] = 0
					else:
						player_data[player_id]['ind']['isf'][STAT_PP] = int(row[SKATER_DB_PP_SF])

					if str(row[SKATER_DB_PP_PT]) == '-':
						player_data[player_id]['ind']['pt'][STAT_PP] = 0
					else:
						player_data[player_id]['ind']['pt'][STAT_PP] = int(row[SKATER_DB_PP_PT])

					if str(row[SKATER_DB_PP_PD]) == '-':
						player_data[player_id]['ind']['pd'][STAT_PP] = 0
					else:
						player_data[player_id]['ind']['pd'][STAT_PP] = int(row[SKATER_DB_PP_PD])

					# Float
					if str(row[SKATER_DB_PP_SH_PCG]) == '-':
						player_data[player_id]['ind']['ish_pcg'][STAT_PP] = 0.0						
					else:
						player_data[player_id]['ind']['ish_pcg'][STAT_PP] = float(row[SKATER_DB_PP_SH_PCG])/100
					
					player_data[player_id]['ind']['toi_pcg'][STAT_PP] = (toi/get_team(simulation_param['databases']['team_db'],team_id).team_toi_pp)
	return player_data

def add_pk_data(simulation_param,player_data):
	with open(simulation_param['csvfiles']['skaters_pk'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'Player':
				# Only add players that are playing today.
				player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
				if player_id in ACTIVE_SKATERS:
					team_id = player_data[player_id]['bio'][1]
					if (player_id == 'SEBASTIAN_AHO') and (str(row[SKATER_DB_ES_TEAM_ID]) != 'CAR'):
						#player_id = 'SEBASTIAN_AHO2'
						raise ValueError('Wrong Sebastian Aho')

					if str(row[SKATER_DB_PP_TOI]) == '-':
						player_data[player_id]['ind']['toi'][STAT_PK] = 0						
					else:
						toi = int(60*float(row[SKATER_DB_PP_TOI]))
						player_data[player_id]['ind']['toi'][STAT_PK] = toi
					
					if str(row[SKATER_DB_PP_GOALS]) == '-':
						player_data[player_id]['ind']['gf'][STAT_PK] = 0						
					else:
						player_data[player_id]['ind']['gf'][STAT_PK] = int(row[SKATER_DB_PP_GOALS])
					
					if str(row[SKATER_DB_PP_ASSIST]) == '-':
						player_data[player_id]['ind']['assist'][STAT_PK] = 0						
					else:
						player_data[player_id]['ind']['assist'][STAT_PK] = int(row[SKATER_DB_PP_ASSIST])

					if str(row[SKATER_DB_PP_FIRST_ASSIST]) == '-':
						player_data[player_id]['ind']['f_assist'][STAT_PK] = 0						
					else:
						player_data[player_id]['ind']['f_assist'][STAT_PK] = int(row[SKATER_DB_PP_FIRST_ASSIST])

					if str(row[SKATER_DB_PP_SECOND_ASSIST]) == '-':
						player_data[player_id]['ind']['s_assist'][STAT_PK] = 0						
					else:
						player_data[player_id]['ind']['s_assist'][STAT_PK] = int(row[SKATER_DB_PP_SECOND_ASSIST])

					if str(row[SKATER_DB_PP_SF]) == '-':
						player_data[player_id]['ind']['isf'][STAT_PK] = 0
					else:
						player_data[player_id]['ind']['isf'][STAT_PK] = int(row[SKATER_DB_PP_SF])

					if str(row[SKATER_DB_PP_PT]) == '-':
						player_data[player_id]['ind']['pt'][STAT_PK] = 0
					else:
						player_data[player_id]['ind']['pt'][STAT_PK] = int(row[SKATER_DB_PP_PT])

					if str(row[SKATER_DB_PP_PD]) == '-':
						player_data[player_id]['ind']['pd'][STAT_PK] = 0
					else:
						player_data[player_id]['ind']['pd'][STAT_PK] = int(row[SKATER_DB_PP_PD])

					# Float
					if str(row[SKATER_DB_PP_SH_PCG]) == '-':
						player_data[player_id]['ind']['ish_pcg'][STAT_PK] = 0.0						
					else:
						player_data[player_id]['ind']['ish_pcg'][STAT_PK] = float(row[SKATER_DB_PP_SH_PCG])/100
					
					player_data[player_id]['ind']['toi_pcg'][STAT_PK] = (toi/get_team(simulation_param['databases']['team_db'],team_id).team_toi_pp)
	return player_data

def add_on_ice_data(simulation_param,player_data):
	with open(simulation_param['csvfiles']['skaters_on_ice'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'Player':

				# Only add players that are playing today.
				player_id = generate_player_id(row[SKATER_DB_BIO_NAME])
				if player_id in ACTIVE_SKATERS: 
					team_id = player_data[player_id]['bio'][1]
					if (player_id == 'SEBASTIAN_AHO') and (str(row[SKATER_DB_ES_TEAM_ID]) != 'CAR'):
						#player_id = 'SEBASTIAN_AHO2'
						raise ValueError('Wrong Sebastian Aho')

					player_data[player_id]['on_ice'] = {}

					if str(row[SKATER_DB_ON_ICE_GP]) == '-':
						player_data[player_id]['on_ice']['gp'] = 0						
					else:
						player_data[player_id]['on_ice']['gp'] = int(row[SKATER_DB_ON_ICE_GP])

					if str(row[SKATER_DB_ON_ICE_CF]) == '-':
						player_data[player_id]['on_ice']['cf'] = 0						
					else:
						player_data[player_id]['on_ice']['cf'] = int(row[SKATER_DB_ON_ICE_CF])

					if str(row[SKATER_DB_ON_ICE_CA]) == '-':
						player_data[player_id]['on_ice']['ca'] = 0
					else:
						player_data[player_id]['on_ice']['ca'] = int(row[SKATER_DB_ON_ICE_CA])

					if str(row[SKATER_DB_ON_ICE_CF_PERCENT]) == '-':
						player_data[player_id]['on_ice']['cf_pcg'] = 0.0						
					else:
						player_data[player_id]['on_ice']['cf_pcg'] = float(row[SKATER_DB_ON_ICE_CF_PERCENT])/100

					if str(row[SKATER_DB_ON_ICE_SF]) == '-':
						player_data[player_id]['on_ice']['sf'] = 0						
					else:
						player_data[player_id]['on_ice']['sf'] = int(row[SKATER_DB_ON_ICE_SF])

					if str(row[SKATER_DB_ON_ICE_SA]) == '-':
						player_data[player_id]['on_ice']['sa'] = 0						
					else:
						player_data[player_id]['on_ice']['sa'] = int(row[SKATER_DB_ON_ICE_SA])

					if str(row[SKATER_DB_ON_ICE_SF_PERCENT]) == '-':
						player_data[player_id]['on_ice']['sf_pcg'] = 0.0						
					else:
						player_data[player_id]['on_ice']['sf_pcg'] = float(row[SKATER_DB_ON_ICE_SF_PERCENT])/100

					if str(row[SKATER_DB_ON_ICE_SCF]) == '-':
						player_data[player_id]['on_ice']['scf'] = 0						
					else:
						player_data[player_id]['on_ice']['scf'] = int(row[SKATER_DB_ON_ICE_SCF])

					if str(row[SKATER_DB_ON_ICE_SCA]) == '-':
						player_data[player_id]['on_ice']['sca'] = 0						
					else:
						player_data[player_id]['on_ice']['sca'] = int(row[SKATER_DB_ON_ICE_SCA])

					if str(row[SKATER_DB_ON_ICE_SCF_PERCENT]) == '-':
						player_data[player_id]['on_ice']['scf_pcg'] = 0.0						
					else:
						player_data[player_id]['on_ice']['scf_pcg'] = float(row[SKATER_DB_ON_ICE_SCF_PERCENT])/100

					if str(row[SKATER_DB_ON_ICE_HDCF]) == '-':
						player_data[player_id]['on_ice']['hdcf'] = 0						
					else:
						player_data[player_id]['on_ice']['hdcf'] = int(row[SKATER_DB_ON_ICE_HDCF])

					if str(row[SKATER_DB_ON_ICE_HDCA]) == '-':
						player_data[player_id]['on_ice']['hdca'] = 0						
					else:
						player_data[player_id]['on_ice']['hdca'] = int(row[SKATER_DB_ON_ICE_HDCA])

					if str(row[SKATER_DB_ON_ICE_HDCF_PERCENT]) == '-':
						player_data[player_id]['on_ice']['hdcf_pcg'] = 0.0
					else:
						player_data[player_id]['on_ice']['hdcf_pcg'] = float(row[SKATER_DB_ON_ICE_HDCF_PERCENT])/100

					if str(row[SKATER_DB_ON_ICE_OZS]) == '-':
						player_data[player_id]['on_ice']['ozs'] = 0
						ozs = 0		
					else:
						player_data[player_id]['on_ice']['ozs'] = int(row[SKATER_DB_ON_ICE_OZS])
						ozs = int(row[SKATER_DB_ON_ICE_OZS])

					if str(row[SKATER_DB_ON_ICE_NZS]) == '-':
						player_data[player_id]['on_ice']['nzs'] = 0
						nzs = 0			
					else:
						player_data[player_id]['on_ice']['nzs'] = int(row[SKATER_DB_ON_ICE_NZS])
						nzs = int(row[SKATER_DB_ON_ICE_NZS])

					if str(row[SKATER_DB_ON_ICE_DZS]) == '-':
						player_data[player_id]['on_ice']['dzs'] = 0						
						dzs = 0
					else:
						player_data[player_id]['on_ice']['dzs'] = int(row[SKATER_DB_ON_ICE_DZS])	
						dzs = int(row[SKATER_DB_ON_ICE_DZS])

					if str(row[SKATER_DB_ON_ICE_OZFO]) == '-':
						player_data[player_id]['on_ice']['ozfo'] = 0
						ozfo = 0
					else:
						player_data[player_id]['on_ice']['ozfo'] = int(row[SKATER_DB_ON_ICE_OZFO])
						ozfo = int(row[SKATER_DB_ON_ICE_OZFO])

					if str(row[SKATER_DB_ON_ICE_NZFO]) == '-':
						player_data[player_id]['on_ice']['nzfo'] = 0
						nzfo = 0
					else:
						player_data[player_id]['on_ice']['nzfo'] = int(row[SKATER_DB_ON_ICE_NZFO])
						nzfo = int(row[SKATER_DB_ON_ICE_NZFO])

					if str(row[SKATER_DB_ON_ICE_DZFO]) == '-':
						player_data[player_id]['on_ice']['dzfo'] = 0
						dzfo = 0
					else:
						player_data[player_id]['on_ice']['dzfo'] = int(row[SKATER_DB_ON_ICE_DZFO])
						dzfo = int(row[SKATER_DB_ON_ICE_DZFO])

	return player_data

def add_corsica_data(simulation_param,player_data):
	with open(simulation_param['csvfiles']['skaters_corsica'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if str(row[0].upper()) != 'PLAYER':
				player_id = generate_player_id(row[SKATER_DB_CORSICA_NAME])
				if player_id == 'ALEX_EDLER':
					player_id = 'ALEXANDER_EDLER'
				elif player_id == 'ALEX_KERFOOT':
					player_id = 'ALEXANDER_KERFOOT'
				elif player_id == 'ALEX_RADULOV':
					player_id = 'ALEXANDER_RADULOV'
				elif player_id == 'ALEX_STEEN':
					player_id = 'ALEXANDER_STEEN'
				elif player_id == 'ALEX_WENNBERG':
					player_id = 'ALEXANDER_WENNBERG'
				elif player_id == 'ALEX_FORTIN':
					player_id = 'ALEXANDRE_FORTIN'
				elif player_id == 'ALEX_NYLANDER':
					player_id = 'ALEXANDER_NYLANDER'
				elif player_id == 'ALEX_TEXIER':
					player_id = 'ALEXANDRE_TEXIER'
				elif player_id == 'CHRIS_TANEV':
					player_id = 'CHRISTOPHER_TANEV'
				elif player_id == 'EVGENY_DADONOV':
					player_id = 'EVGENII_DADONOV'
				elif player_id == 'MATT_BENNING':
					player_id = 'MATTHEW_BENNING'	
				elif player_id == 'MITCH_MARNER':
					player_id = 'MITCHELL_MARNER'
				elif player_id == 'NICHOLAS_SHORE':
					player_id = 'NICK_SHORE'
				elif player_id == '5EBASTIAN_AHO':
					player_id = 'SEBASTIAN_AHO2'


				# Only add players that are playing today.
				if player_id in ACTIVE_SKATERS:
					if str(row[SKATER_DB_CORSICA_REL_CF]) == '-':
						player_data[player_id]['on_ice']['rel_cf'] = 0		
						player_data[player_id]['on_ice']['rel_ca'] = 0
					else:
						player_data[player_id]['on_ice']['rel_cf'] = 1+(float(row[SKATER_DB_CORSICA_REL_CF])/100)
						player_data[player_id]['on_ice']['rel_ca'] = 1-(player_data[player_id]['on_ice']['rel_cf']-1)

	return player_data

def create_goalie_db(simulation_param):
	output = get_active_goalies(simulation_param)
	team_db = simulation_param['databases']['team_db']
	with open(simulation_param['csvfiles']['goalies'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'Player':
				# Get data from row.
				[name,toi,sa,sv,ga,sv_pcg,gaa,gsaa,xga,avg_shot_dist,avg_goal_dist] = get_row_values_for_goalie_db(row)
				if name in ACTIVE_GOALIES:
					team_id = output[name]

					# Create specifc stats.
					toi_pcg = (toi/get_team(team_db,team_id).team_toi_es)

					# DEBUG:
					'''
					if team_id == 'SJS':
						print('Name: ' + name)
						print('TOI: ' + str(toi))
						print('TOI-PCG: ' + str(toi_pcg))
						print('Shots against: ' + str(sa))
						print('Saves: ' + str(sv))
						print('Sv%: ' + str(sv_pcg))
					'''
					output[name] = Goalie(name,team_id,[toi,toi_pcg,sa,sv,ga,sv_pcg,gaa,gsaa,xga,avg_shot_dist,avg_goal_dist])
	return output

def get_active_goalies(simulation_param):
	global ACTIVE_GOALIES
	output = {}
	with open(simulation_param['csvfiles']['goalies_bio'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[1] != 'Player':
				if str(row[GOALIE_DB_NAME]) == '-':
					raise ValueError('Incorrect Player-ID')
				else:
					name = generate_player_id(row[GOALIE_DB_NAME])
				# TEAM
				if str(row[SKATER_DB_BIO_TEAM_ID]) == '-':
					raise ValueError('Incorrect Team-ID')
				else:
					team_id = get_team_id_for_player(name,str(row[SKATER_DB_BIO_TEAM_ID]))
				if team_id != None:
					ACTIVE_GOALIES.add(name)
					output[name] = team_id
	return output

def create_team_db(simulation_param):
	global TOTAL_GOALS_PER_GAME
	global TOTAL_POINTS_PER_GAME
	global PROBABILITY_FOR_OT
	output = {}
	with open(simulation_param['csvfiles']['teams_es'],'rt') as f:
		reader = csv.reader(f, delimiter=',')
		#reader = csv.reader(f)
		names = []
		reg_arrays = []
		adv_arrays = []
		total_gp = 0
		total_otl = 0
		total_gf = 0
		for row in reader:
			if row[1] != 'Team':
				# Get data from row.
				[name,gp,team_toi_es,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)

				# Create special metrics.
				sa_per_sec = sa/team_toi_es

				reg_array = [gp,team_toi_es,w,l,otl,p,gf,ga,p_pcg]
				adv_array = [sf,sa,sf_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,scf,sca,scf_pcg,hdcf,hdca,hdcf_pcg,sv_pcg,pdo,sa_per_sec]

				total_gp += gp
				total_otl += otl
				total_gf += gf

				output[name] = Team(name,reg_array,adv_array,simulation_param['databases']['team_schedules'][name])
	
	with open(simulation_param['csvfiles']['teams_pp'],'rt') as f:
		reader = csv.reader(f,delimiter=',')		
		for row in reader:
			if row[1] != 'Team':
				[name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
				total_gf += gf
				output[name].team_toi_pp = team_toi
				output[name].team_toi_pp_per_gp = team_toi/gp


	with open(simulation_param['csvfiles']['teams_pk'],'rt') as f:
		reader = csv.reader(f,delimiter=',')
		for row in reader:
			if row[1] != 'Team':
				[name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo] = get_row_values_for_team_db(row)
				total_gf += gf
				output[name].team_toi_pk = team_toi
				output[name].team_toi_pk_per_gp = team_toi/gp

	return output

def add_experimental_data(team_db,skater_db,goalie_db,unavailable_players=None,debug_team_id=None):
	sf_dict,gf_dict,cf_dict,ca_dict,scf_dict,sca_dict = defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list)
	#es_toi_per_gp, pp_toi_per_gp, pk_toi_per_gp = 
	estimated_off_dict, estimated_def_dict = defaultdict(list),defaultdict(list)
	shots_against_dict,shots_saved_dict = defaultdict(list),defaultdict(list)
	gp_array = []

	if debug_team_id != None:
		print('\n' + debug_team_id + ' roster (DEBUG):')
	for skater_id in skater_db.keys():
		skater = get_player(skater_db,skater_id)

		# Calculate total shots/scf taken per team, only if player is available
		if skater_id not in unavailable_players:
			sf_dict[skater.bio['team_id']].append(skater.ind['isf'][STAT_ES])
			gf_dict[skater.bio['team_id']].append(skater.ind['gf'][STAT_ES])
			scf_dict[skater.bio['team_id']].append(skater.on_ice['scf'])
			sca_dict[skater.bio['team_id']].append(skater.on_ice['sca'])

		skater.ind['toi_pcg'] = [0,0,0]
		for index in STAT_INDEX:
			skater.ind['toi_pcg'][index] = skater.ind['toi_per_gp'][index] / team_db[skater.bio['team_id']].team_toi_es_per_gp

		# Estimate offensive and defensive capabilities. Different depending on the skater has played for multiple teams or not.
		estimated_off = skater.on_ice['scf']
		estimated_def = skater.on_ice['sca']
		skater.on_ice['estimated_off_per_sec'] = skater.on_ice['scf'] * skater.on_ice['rel_cf'] / skater.ind['toi'][STAT_ES] 		# Yes, it _SHOULD_ be "scf" and "rel_cf"
		skater.on_ice['estimated_def_per_sec'] = skater.on_ice['sca'] * skater.on_ice['rel_ca'] / skater.ind['toi'][STAT_ES]

		if skater.bio['multiple_teams'] == True:
			estimated_off = team_db[skater.bio['team_id']].scf_per_sec * skater.ind['toi'][STAT_ES] * skater.on_ice['rel_cf']
			estimated_def = team_db[skater.bio['team_id']].sca_per_sec * skater.ind['toi'][STAT_ES] * skater.on_ice['rel_ca']
			skater.on_ice['estimated_off_per_sec'] = estimated_off/ skater.ind['toi'][STAT_ES]
			skater.on_ice['estimated_def_per_sec'] = estimated_def/ skater.ind['toi'][STAT_ES]

		# Store estimated offensive and defensive capabilities per team.
		estimated_off_dict[skater.bio['team_id']].append(estimated_off)
		estimated_def_dict[skater.bio['team_id']].append(estimated_def)
		# Error/warning handling for weird input
		if (skater.on_ice['estimated_off_per_sec']+skater.on_ice['estimated_def_per_sec']) == 0:
			warnings.warn('Bad input for player ' + skater.bio['name'] + '. Setting value ESTIMATED_OFF_PCG to 0.')
			skater.on_ice['estimated_off_pcg'] = 0
		else:
			skater.on_ice['estimated_off_pcg'] = skater.on_ice['estimated_off_per_sec'] / (skater.on_ice['estimated_off_per_sec']+skater.on_ice['estimated_def_per_sec'])


		if skater.bio['team_id'] == debug_team_id:
			print('   {0}: Estimated offense/60: {1:.1f}. Estimated defense/60: {2:.1f}. Estimated off-pcg: {3:.1f}%'.format(skater.bio['name'],3600*skater.on_ice['estimated_off_per_sec'],3600*skater.on_ice['estimated_def_per_sec'],100*skater.on_ice['estimated_off_pcg']))

	for goalie_id in goalie_db.keys():
		# Calculate total sa/ss per team, only if player is available
		if goalie_id not in unavailable_players:
			goalie = get_player(goalie_db,goalie_id)
			shots_against_dict[goalie.bio['team_id']].append(goalie.sa)
			shots_saved_dict[goalie.bio['team_id']].append(goalie.sv)
	
	for team_id in team_db.keys():
		gp_array.append(team_db[team_id].gp)
		avg_gp = np.mean(gp_array)
	if avg_gp > 20:
		avg_gp = 20

	print('\nTeam metrics:')
	for team_id in ACTIVE_TEAMS:
		team_sh_pcg = sum(gf_dict[team_id])/sum(sf_dict[team_id])
		team_sv_pcg = sum(shots_saved_dict[team_id])/sum(shots_against_dict[team_id])
		team_estimated_off = sum(estimated_off_dict[team_id])
		team_estimated_def = sum(estimated_def_dict[team_id])
		team_scf = sum(scf_dict[team_id])
		team_sca = sum(sca_dict[team_id])
		team_db[team_id].exp_data['sh_pcg'] = team_sh_pcg
		team_db[team_id].exp_data['sv_pcg'] = team_sv_pcg
		team_db[team_id].exp_data['estimated_team_off'] = team_estimated_off*team_db[team_id].exp_data['sh_pcg']
		team_db[team_id].exp_data['estimated_team_def'] = team_estimated_def*(1-team_db[team_id].exp_data['sv_pcg'])
		team_db[team_id].exp_data['pdo'] = team_db[team_id].exp_data['sh_pcg']+team_db[team_id].exp_data['sv_pcg']
		team_db[team_id].exp_data['scf_pcg'] = (team_scf/(team_scf+team_sca))
		
		# Assign ratings
		team_db[team_id].exp_data['pre_season_rating'] = team_db[team_id].exp_data['estimated_team_off']/(team_db[team_id].exp_data['estimated_team_off']+team_db[team_id].exp_data['estimated_team_def'])
		
		# Two (three) different ways of calculating ratings.
		#team_db[team_id].exp_data['in_season_rating'] = team_db[team_id].exp_data['scf_pcg']*(team_db[team_id].exp_data['pdo']+team_db[team_id].p_pcg)
		#team_db[team_id].exp_data['in_season_rating'] = team_db[team_id].exp_data['estimated_team_off']/(team_db[team_id].exp_data['estimated_team_off']+team_db[team_id].exp_data['estimated_team_def'])
		team_db[team_id].exp_data['in_season_rating'] = (team_db[team_id].p_pcg*0.5*P_PCG_FACTOR*avg_gp/20) + (team_db[team_id].exp_data['estimated_team_off']/(team_db[team_id].exp_data['estimated_team_off']+team_db[team_id].exp_data['estimated_team_def']))

		print('   {0}: Rating: {1:.3f}. PDO: {2:.3f}. Shooting: {3:.1f}%. Saving: {4:.1f}%'.format(team_id,team_db[team_id].exp_data['in_season_rating'],team_db[team_id].exp_data['pdo'],100*team_db[team_id].exp_data['sh_pcg'],100*team_db[team_id].exp_data['sv_pcg']))

	return [team_db,skater_db]

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
		skater = get_player(simulation_param['databases']['skater_db'],skater_id)
		if (skater_id not in simulation_param['databases']['unavailable_players']):
			output[skater.bio['team_id']][skater.bio['name']] = skater
	return output

def get_row_values_for_goalie_db(row):
	if str(row[GOALIE_DB_NAME]) == '-':
		raise ValueError('Incorrect Player-ID')
	else:
		name = generate_player_id(row[GOALIE_DB_NAME])
	"""
	if str(row[GOALIE_DB_TEAM_ID]) == '-':
		raise ValueError('Incorrect Team-ID')
	else:
		team_id = get_team_id_for_player(name,str(row[GOALIE_DB_TEAM_ID]))
	"""
	
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
	
	return [name,gp,team_toi,w,l,otl,p,sf,sa,sf_pcg,gf,ga,p_pcg,cf,ca,cf_pcg,ff,fa,ff_pcg,scf,sca,scf_pcg,hdca,hdcf,hdcf_pcg,sv_pcg,pdo]


def modify_player_db(s_db,g_db):
	"""
	ISOLATED TEAM IMPACT: BEFORE (AFTER) [DIFF]  
	 =       --> within 0.0049 difference 
	 + (-)   --> between 0.005 and 0.0099 difference
	 ++ (--) --> between 0.010 and 0.0149 difference
	 ++ (--) --> between 0.015 and 0.0199 difference
	 ...
	 """
	# Retiring / signing out of NHL
	s_db = update_new_team(s_db,'BROOKS_ORPIK',None)			# WSH: 0.5140 (0.5194) [+]
	g_db = update_new_team(g_db,'ROBERTO_LUONGO',None)
	g_db = update_new_team(g_db,'SCOTT_DARLING',None)			# CAR: 0.4998 (0.5279) [+++++]
	s_db = update_new_team(s_db,'RYAN_CALLAHAN',None)			# CAR: 0.4998 (0.5279) [+++++]
	s_db = update_new_team(s_db,'JORI_LEHTERA',None)			# 
	s_db = update_new_team(s_db,'RYAN_SPOONER',None)			# 
	s_db = update_new_team(s_db,'CHRIS_KUNITZ',None)			# 
	s_db = update_new_team(s_db,'MATT_CULLEN',None)				#
	s_db = update_new_team(s_db,'MARCUS_KRUGER',None)			# 
	s_db = update_new_team(s_db,'SVEN_ANDRIGHETTO',None)		# 
	s_db = update_new_team(s_db,'DEREK_MACKENZIE',None)			# 
	s_db = update_new_team(s_db,'ANDREJ_SUSTR',None)			# 
	s_db = update_new_team(s_db,'TOM_PYATT',None)				#
	s_db = update_new_team(s_db,'ERIC_FEHR',None)				#
	s_db = update_new_team(s_db,'JAKUB_JERABEK',None)			#
	s_db = update_new_team(s_db,'IGOR_OZHIGANOV',None)			#
	s_db = update_new_team(s_db,'EGOR_YAKOVLEV',None)			#
	s_db = update_new_team(s_db,'BOGDAN_KISELEVICH',None)		#
	s_db = update_new_team(s_db,'TY_RATTIE',None)
	s_db = update_new_team(s_db,'MATT_HENDRICKS',None)	
	s_db = update_new_team(s_db,'TOMAS_HYKA',None)	
	s_db = update_new_team(s_db,'CORBAN_KNIGHT',None)
	s_db = update_new_team(s_db,'JASON_GARRISON',None)		
	g_db = update_new_team(g_db,'ANTTI_NIEMI',None)
	s_db = update_new_team(s_db,'MAX_MCCORMICK',None)			#
	s_db = update_new_team(s_db,'PATRIK_BERGLUND',None)
	s_db = update_new_team(s_db,'JUSTIN_WILLIAMS',None)
	s_db = update_new_team(s_db,'NIKLAS_KRONWALL',None)
	s_db = update_new_team(s_db,'DAN_GIRARDI',None)

	# Trades and signings
	# 2019-06-14
	s_db = update_new_team(s_db,'RADKO_GUDAS','WSH') 			# WSH: 0.5327 (0.5303) [=] 		PHI: 0.5015  (0.5042)  [=]
	s_db = update_new_team(s_db,'MATT_NISKANEN','PHI')
	# 2019-06-15
	s_db = update_new_team(s_db,'OLLI_MAATTA','CHI') 			# CHI: 0.4949 (0.4879) [-] 		PIT: 0.5238  (0.5316)  [+]
	s_db = update_new_team(s_db,'DOMINIK_KAHUN','PIT')
	# 2019-06-17
	s_db = update_new_team(s_db,'JACOB_TROUBA','NYR') 			# NYR: 0.4643 (0.4627) [=] 		WPG: 0.5172  (0.5194)  [=]
	s_db = update_new_team(s_db,'NEAL_PIONK','WPG') 
	# 2019-06-18
	s_db = update_new_team(s_db,'JUSTIN_BRAUN','PHI') 			# PHI: 0.5042 (0.4972) [-]		SJS: 0.5067  (0.5156)  [+]
	# 2019-06-22
	s_db = update_new_team(s_db,'P_K__SUBBAN','NJD')			# NJD: 0.4565 (0.4580) [=] 		NSH: 0.5379  (0.5373)  [=]
	s_db = update_new_team(s_db,'STEVEN_SANTINI','NSH')			
	s_db = update_new_team(s_db,'J_T__MILLER','VAN')			# VAN: 0.4395 (0.4460) [+]		TBL: 0.5761  (0.5763)  [=]
	s_db = update_new_team(s_db,'JOHN_HAYDEN','NJD')			
	s_db = update_new_team(s_db,'JOHN_QUENNEVILLE','CHI')
	#2019-06-25
	s_db = update_new_team(s_db,'CALVIN_DE_HAAN','CHI')			# CHI: 0.4909 (0.4911) [=]		CAR: 0.4952 (0.4954) [=]
	s_db = update_new_team(s_db,'GUSTAV_FORSLING','CAR')
	s_db = update_new_team(s_db,'CARL_SODERBERG','ARI')			# ARI: 0.4858 (0.4930) [+]		COL: 0.5281 (0.5217) [-]
	s_db = update_new_team(s_db,'KEVIN_CONNAUTON','COL')
	# 2019-06-30
	s_db = update_new_team(s_db,'ANDREW_SHAW','CHI')			# CHI: 0.4911 (0.4960) [=] 		MTL: 0.4981 (0.4843) [--]
	g_db = update_new_team(g_db,'JAMES_REIMER','CAR')			# CAR: 0.5279 (0.5121) [---]
	s_db = update_new_team(s_db,'ALEX_GALCHENYUK','PIT')		# ARI: 0.4930 (0.5014) [+]		PIT: 0.5196 (0.5122) [-]
	s_db = update_new_team(s_db,'PHIL_KESSEL','ARI')
	s_db = update_new_team(s_db,'ANDRE_BURAKOVSKY','COL')		# COL: 0.5217 (0.5272) [+]		WSH: 0.5194 (0.5153) [=]
	s_db = update_new_team(s_db,'COLIN_MILLER','BUF')			# BUF: 0.4593 (0.4544) [=]		VGK: 0.5385 (0.5471) [+]
	s_db = update_new_team(s_db,'ERIK_HAULA','CAR')				# CAR: 0.4954 (0.4998) [=]		VGK: 0.5403 (0.5385) [=]
	# 2019-07-01
	s_db = update_new_team(s_db,'PAR_LINDHOLM','BOS')			# BOS: 0.5406 (0.5376) [=]
	s_db = update_new_team(s_db,'BRETT_RITCHIE','BOS')			 
	s_db = update_new_team(s_db,'BRENDAN_GAUNCE','BOS')			 
	s_db = update_new_team(s_db,'JEAN-SEBASTIEN_DEA','BUF')		# BUF: 0.4616 (0.4638) [=]
	s_db = update_new_team(s_db,'JOHN_GILMOUR','BUF')			# BUF: 0.4650 (0.4616) [=]
	s_db = update_new_team(s_db,'JIMMY_VESEY','BUF')			# BUF: 0.4638 (0.4704) [+]
	s_db = update_new_team(s_db,'CURTIS_LAZAR','BUF')			# BUF: 0.4640 (0.4619) [=]
	s_db = update_new_team(s_db,'GUSTAV_NYQUIST','CBJ')			# CBJ: 0.4748 (0.4797) [=]		SJS: 0.5096 (0.5016) [-]
	s_db = update_new_team(s_db,'RYAN_CARPENTER','CHI')			# CHI: 0.5145 (0.5132) [=]
	s_db = update_new_team(s_db,'JOONAS_DONSKOI','COL')			# COL: 0.5342 (0.5406) [+] 		SJS: 0.5188 (0.5134) [-]
	s_db = update_new_team(s_db,'NAZEM_KADRI','COL') 			# TOR: 0.5400 (0.5374) [=]		COL: 0.5409 (0.5454) [=]
	s_db = update_new_team(s_db,'CALLE_ROSEN','COL') 			# TOR: 0.5374 (0.5371) [=]		COL: 0.5454 (0.5457) [=]
	s_db = update_new_team(s_db,'PIERRE-EDOUARD_BELLEMARE','COL') # COL: 0.5406 (0.5377) [=]  	VGK: 0.5457 (0.5500) [-]
	s_db = update_new_team(s_db,'JOE_PAVELSKI','DAL')			# DAL: 0.4963 (0.5074) [++] 	SJS: 0.5134 (0.5050) [-]
	s_db = update_new_team(s_db,'COREY_PERRY','DAL')			# DAL: 0.5074 (0.5088) [=] 		ANA: 0.5330 (0.5325) [=]
	s_db = update_new_team(s_db,'ANDREJ_SEKERA','DAL')			# DAL: 0.5060 (0.5009) [-]
	s_db = update_new_team(s_db,'PATRIK_NEMETH','DET')			# DET: 0.4789 (0.4736) [-]
	s_db = update_new_team(s_db,'VALTTERI_FILPPULA','DET')		# DET: 0.4736 (0.4817) [+]
	s_db = update_new_team(s_db,'MARKUS_GRANLUND','EDM')		# EDM: 0.4590 (0.4592) [=]
	s_db = update_new_team(s_db,'ANTON_STRALMAN','FLA')			# FLA: 0.5103 (0.5023) [-]
	s_db = update_new_team(s_db,'NOEL_ACCIARI','FLA')			# FLA: 0.5037 (0.5052) [=]
	s_db = update_new_team(s_db,'BRETT_CONNOLLY','FLA')			# FLA: 0.5052 (0.5170) [++]
	s_db = update_new_team(s_db,'JOAKIM_RYAN','LAK') 			# LAK: 0.4875 (0.4819) [-]		SJS: 0.5046 (0.5096) [+]
	s_db = update_new_team(s_db,'MARIO_KEMPE','LAK')			# LAK: 0.4864 (0.4846) [=]
	s_db = update_new_team(s_db,'MATS_ZUCCARELLO','MIN')		# MIN: 0.4803 (0.4875) [+] 		DAL: 0.5088 (0.5036) [-]
	s_db = update_new_team(s_db,'RYAN_HARTMAN','MIN')			# MIN: 0.4875 (0.4898) [=]
	s_db = update_new_team(s_db,'LUKE_JOHNSON','MIN')			# MIN: 0.4879 (0.4868) [=]
	s_db = update_new_team(s_db,'WAYNE_SIMMONDS','NJD')			# NJD: 0.4491 (0.4495) [=]
	s_db = update_new_team(s_db,'MATT_DUCHENE','NSH')			# NSH: 0.5525 (0.5650) [++] 	CBJ: 0.4955 (0.4861) [-]
	s_db = update_new_team(s_db,'DANIEL_CARR','NSH')			
	s_db = update_new_team(s_db,'ARTEMI_PANARIN','NYR')			# CBJ: 0.4861 (0.4748) [--]		NYR: 0.4393 (0.4562) [+++]
	s_db = update_new_team(s_db,'RON_HAINSEY','OTT')			# OTT: 0.4116 (0.4066) [-]		TOR: 0.5496 (0.5560) [+]
	s_db = update_new_team(s_db,'TYLER_ENNIS','OTT')			# OTT: 0.4066 (0.4096) [=]
	s_db = update_new_team(s_db,'NIKITA_ZAITSEV','OTT') 		# OTT: 0.4094 (0.4111) [=]
	s_db = update_new_team(s_db,'CONNOR_BROWN','OTT')			# OTT: 0.4111 (0.4152) [=]
	s_db = update_new_team(s_db,'KEVIN_HAYES','PHI')			# PHI: 0.4967 (0.5015) [+] 		WPG: 0.5213  (0.5172) [-]
	s_db = update_new_team(s_db,'NATE_PROSSER','PHI')			# PHI: 0.5058 (0.5041) [=]
	s_db = update_new_team(s_db,'ANDY_WELINSKI','PHI')			 
	s_db = update_new_team(s_db,'TYLER_PITLICK','PHI')			# PHI: 0.4982 (0.5008) [=]
	s_db = update_new_team(s_db,'BRANDON_TANEV','PIT')			# PIT: 0.5047 (0.5055) [=]
	s_db = update_new_team(s_db,'ANDREW_AGOZZINO','PIT')		
	s_db = update_new_team(s_db,'NATHAN_WALKER','STL')			# STL: 0.4886 (0.4889) [=]
	s_db = update_new_team(s_db,'LUKE_SCHENN','TBL')			# TBL: 0.5698 (0.5740) [=]
	s_db = update_new_team(s_db,'CODY_CECI','TOR')				# TOR: 0.5624 (0.5471) [---] 
	s_db = update_new_team(s_db,'BEN_HARPUR','TOR')				# TOR: 0.5471 (0.5405) [-]
	s_db = update_new_team(s_db,'JASON_SPEZZA','TOR')			# TOR: 0.5540 (0.5496) [=]		DAL: 0.5036 (0.5060) [=]
	s_db = update_new_team(s_db,'KENNY_AGOSTINO','TOR')			# TOR: 0.5560 (0.5553) [=]
	s_db = update_new_team(s_db,'KEVIN_GRAVEL','TOR')			# TOR: 0.5448 (0.5405) [=]
	s_db = update_new_team(s_db,'TYSON_BARRIE','TOR') 			# TOR: 0.5405 (0.5340) [-] 		COL: 0.5436 (0.5483) [=] 
	s_db = update_new_team(s_db,'ALEXANDER_KERFOOT','TOR')		# TOR: 0.5340 (0.5400) [+] 		COL: 0.5483 (0.5409) [-]	
	s_db = update_new_team(s_db,'TYLER_MYERS','VAN')			# VAN: 0.4604 (0.4563) [=]
	s_db = update_new_team(s_db,'JORDIE_BENN','VAN')			# VAN: 0.4614 (0.4587) [=]
	s_db = update_new_team(s_db,'OSCAR_FANTENBERG','VAN')		# VAN: 0.4587 (0.4570) [=]
	s_db = update_new_team(s_db,'BRENDAN_LEIPSIC','WSH')		# WSH: 0.5088 (0.5060) [=]
	s_db = update_new_team(s_db,'GARNET_HATHAWAY','WSH')		# WSH: 0.5163 (0.5173) [=]
	s_db = update_new_team(s_db,'RICHARD_PANIK','WSH')			# WSH: 0.5173 (0.5090) [-]
	g_db = update_new_team(g_db,'SERGEI_BOBROVSKY','FLA') 		# FLA: 0.4798 (0.5103) [+++++]	CBJ: 0.5436 (0.4955) [---------]
	g_db = update_new_team(g_db,'SEMYON_VARLAMOV','NYI')		# NYI: 0.5150 (0.5128) [=]		COL: 0.5269 (0.5406) [++]
	g_db = update_new_team(g_db,'ROBIN_LEHNER','CHI')			# CHI: 0.5027 (0.5104) [+]  	NYI: 0.5150 (0.5128) [=]
	g_db = update_new_team(g_db,'CAM_TALBOT','CGY')				# CGY: 0.5451 (0.5383) [-]  	
	g_db = update_new_team(g_db,'MIKE_SMITH','EDM')				# EDM: 0.4562 (0.4590) [=] 		CGY: 0.5451 (0.5383) [-]
	g_db = update_new_team(g_db,'KEITH_KINKAID','MTL')			
	g_db = update_new_team(g_db,'MAXIME_LAGACE','BOS')			
	g_db = update_new_team(g_db,'CURTIS_MCELHINNEY','TBL')		
	g_db = update_new_team(g_db,'CALVIN_PICKARD','DET')			

	# Non-signed UFA; removed from this list if signing a contract.
	# List from capfriendly.com
	s_db = update_new_team(s_db,'DION_PHANEUF',None)			 
	s_db = update_new_team(s_db,'PATRICK_MARLEAU',None)		 
	s_db = update_new_team(s_db,'JASON_POMINVILLE',None)		
	s_db = update_new_team(s_db,'DERICK_BRASSARD',None)			 
	s_db = update_new_team(s_db,'ANDREW_MACDONALD',None)		 
	s_db = update_new_team(s_db,'MARC_METHOT',None)				 			 
	s_db = update_new_team(s_db,'JAMIE_MCGINN',None)			 
	s_db = update_new_team(s_db,'THOMAS_VANEK',None)			 
	s_db = update_new_team(s_db,'BEN_HUTTON',None)				 
	s_db = update_new_team(s_db,'ADAM_MCQUAID',None)			
	s_db = update_new_team(s_db,'BEN_LOVEJOY',None)				
	s_db = update_new_team(s_db,'BRIAN_BOYLE',None)				 
	s_db = update_new_team(s_db,'DAVID_SCHLEMKO',None)			
	s_db = update_new_team(s_db,'RILEY_SHEAHAN',None)			
	s_db = update_new_team(s_db,'TOBIAS_RIEDER',None)			 
	s_db = update_new_team(s_db,'ALEX_PETROVIC',None)			 
	s_db = update_new_team(s_db,'STEFAN_NOESEN',None)			 
	s_db = update_new_team(s_db,'OSCAR_LINDBERG',None)			 
	s_db = update_new_team(s_db,'LUCA_SBISA',None)				 
	s_db = update_new_team(s_db,'DMITRIJ_JASKIN',None)			
	s_db = update_new_team(s_db,'DEVANTE_SMITH-PELLY',None) 
	s_db = update_new_team(s_db,'JOE_MORROW',None)				
	s_db = update_new_team(s_db,'GABRIEL_BOURQUE',None)			
	s_db = update_new_team(s_db,'CHRIS_THORBURN',None)			
	s_db = update_new_team(s_db,'MAGNUS_PAAJARVI',None)			
	s_db = update_new_team(s_db,'TROY_BROUWER',None)			
	s_db = update_new_team(s_db,'MICHEAL_HALEY',None)			
	s_db = update_new_team(s_db,'DREW_STAFFORD',None)			
	s_db = update_new_team(s_db,'CODY_MCLEOD',None)				
	s_db = update_new_team(s_db,'ERIC_GRYBA',None)				
	s_db = update_new_team(s_db,'FREDRIK_CLAESSON',None)		
	s_db = update_new_team(s_db,'ROURKE_CHARTIER',None)			
	s_db = update_new_team(s_db,'WADE_MEGAN',None)				
	s_db = update_new_team(s_db,'ZAC_RINALDO',None)				
	s_db = update_new_team(s_db,'CONNOR_BRICKLEY',None)			
	s_db = update_new_team(s_db,'MATT_READ',None)				
	s_db = update_new_team(s_db,'JUSTIN_FALK',None)				
	s_db = update_new_team(s_db,'CHRIS_BUTLER',None)			
	g_db = update_new_team(g_db,'CAM_WARD',None)
	g_db = update_new_team(g_db,'MICHAL_NEUVIRTH',None)
	g_db = update_new_team(g_db,'CHAD_JOHNSON',None)
	g_db = update_new_team(g_db,'MIKE_MCKENNA',None)	
	# 2019-07-05
	s_db = update_new_team(s_db,'BLAKE_PIETILA','ANA')			 
	s_db = update_new_team(s_db,'DALTON_PROUT','SJS')			# SJS: 0.5050 (0.5046) [=]
	s_db = update_new_team(s_db,'JONNY_BRODZINSKI','SJS')		# SJS: 0.4947 (0.4942) [=]
	s_db = update_new_team(s_db,'MARK_LETESTU','WPG')			# WPG: 0.5285 (0.5271) [=]
	s_db = update_new_team(s_db,'PHIL_VARONE','MTL')			 
	s_db = update_new_team(s_db,'BEN_CHIAROT','MTL')			
	s_db = update_new_team(s_db,'NICK_COUSINS','MTL')			# MTL: 0.4970 (0.4958) [=]
	# 2019-07-09
	s_db = update_new_team(s_db,'MARCUS_JOHANSSON','BUF')		# BOS: 0.5433 (0.5406) [=]		BUF: 0.4602 (0.4640) [=]
	s_db = update_new_team(s_db,'ALEXANDER_NYLANDER','CHI') 	# CHI: 0.5092 (0.5115) [=]		BUF: 0.4713 (0.4681) [=]
	s_db = update_new_team(s_db,'HENRI_JOKIHARJU','BUF')
	# 2019-07-10
	s_db = update_new_team(s_db,'MICHEAL_FERLAND','VAN')		 
	# 2019-07-12
	s_db = update_new_team(s_db,'MICHAEL_DEL_ZOTTO','ANA')		 
	s_db = update_new_team(s_db,'RYAN_DZINGEL','CAR')			 
	# 2019-07-19
	s_db = update_new_team(s_db,'CHRIS_WIDEMAN','ANA')			
	s_db = update_new_team(s_db,'ARTEM_ANISIMOV','OTT')
	s_db = update_new_team(s_db,'ZACK_SMITH','CHI')
	s_db = update_new_team(s_db,'JOSH_ARCHIBALD','EDM')			
	s_db = update_new_team(s_db,'MILAN_LUCIC','CGY')
	s_db = update_new_team(s_db,'JAMES_NEAL','EDM')				
	# 2019-07-26
	g_db = update_new_team(g_db,'GARRET_SPARKS','VGK')
	s_db = update_new_team(s_db,'KALLE_KOSSILA','TOR')			
	s_db = update_new_team(s_db,'GARRETT_WILSON','TOR')			
	s_db = update_new_team(s_db,'PONTUS_ABERG','TOR')			
	s_db = update_new_team(s_db,'JORDAN_SCHMALTZ','TOR')		
	# 2019-08-02
	g_db = update_new_team(g_db,'MIKE_CONDON','TBL')
	s_db = update_new_team(s_db,'PHILLIP_DI_GIUSEPPE','NYR')	
	s_db = update_new_team(s_db,'DARREN_ARCHIBALD','TOR')
	s_db = update_new_team(s_db,'MICHAEL_STONE','CAR')  			
	# 2019-08-09
	s_db = update_new_team(s_db,'KEVIN_SHATTENKIRK','TBL')  	
	s_db = update_new_team(s_db,'MARKO_DANO','CBJ')  			
	s_db = update_new_team(s_db,'TREVOR_CARRICK','SJS')
	# 2019-08-16
	s_db = update_new_team(s_db,'ADAM_ERNE','DET')
	# 2019-08-23
	s_db = update_new_team(s_db,'VALERI_NICHUSHKIN','COL')
	s_db = update_new_team(s_db,'PAT_MAROON','TBL')
	s_db = update_new_team(s_db,'JAKE_GARDINER','CAR')
	s_db = update_new_team(s_db,'JOEL_EDMUNDSON','CAR')
	s_db = update_new_team(s_db,'JUSTIN_FAULK','STL')
	'''
	'''
	return [s_db, g_db]

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

def get_unavailable_players():
	# This structure is stored for historical reasons.
	unavailable_players = defaultdict(list)
	unavailable_players['ARI'].append('NIKLAS_HJALMARSSON')
	unavailable_players['COL'].append('MIKKO_RANTANEN')
	unavailable_players['COL'].append('GABRIEL_LANDESKOG')
	unavailable_players['EDM'].append('ADAM_LARSSON')
	unavailable_players['PIT'].append('EVGENI_MALKIN')
	unavailable_players['PIT'].append('NICK_BJUGSTAD')
	unavailable_players['SJS'].append('DALTON_PROUT')
	unavailable_players['SJS'].append('JACOB_MIDDLETON')
	unavailable_players['STL'].append('VLADIMIR_TARASENKO')
	unavailable_players['TOR'].append('JOHN_TAVARES')
	unavailable_players['VGK'].append('VALENTIN_ZYKOV')

	all_unavailable_players = set()
	for team_id in unavailable_players.keys():
		for player_id in unavailable_players[team_id]:
			all_unavailable_players.add(player_id)

	return all_unavailable_players

def get_team_id_for_player(name,team_id):
	
	manually_checked_players = set()
	'''
	manually_checked_players.add('CARL_HAGELIN')
	manually_checked_players.add('CHRIS_WIDEMAN')
	manually_checked_players.add('DERICK_BRASSARD')
	manually_checked_players.add('JORDAN_WEAL')
	manually_checked_players.add('MICHAEL_DEL_ZOTTO')
	manually_checked_players.add('RYAN_SPOONER')
	manually_checked_players.add('TANNER_PEARSON')
	manually_checked_players.add('VALENTIN_ZYKOV')
	'''
	new_team = {}
	team_id_arr = (team_id.replace(' ','').split(','))
	if len(team_id_arr) > 1:
		if len(team_id_arr) > 2:
			if name not in manually_checked_players:
				raise ValueError('Player ' + name + ' changed club more than once. Please add to "manually_checked_players" to continue.')
		new_team['VLADISLAV_NAMESTNIKOV'] = 'OTT'
		new_team['ERIK_GUDBRANSON'] = 'ANA'
		new_team['ANDREAS_MARTINSEN'] = 'PTI'

		if name not in set(new_team.keys()):
			raise ValueError('Player ' + name + ' has more than one team(s). Team-ID: ' + team_id)		

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

'''
def modify_attribute(db,player_id,attribute,value):
	# This only works with even-strength
	if attribute == 'sv_pcg':
		db[player_id].sv_pcg = value
#g_db = modify_attribute(g_db,'MARTIN_JONES','sv_pcg',,0.915)
	return db
'''
