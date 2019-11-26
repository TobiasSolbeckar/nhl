from nhl_helpers import *
from nhl_defines import *
from nhl_simulation import *

class Skater():
	def __init__(self,bio,ind,on_ice):
		# player_data[name]['bio'] = [name,team_id,position,age,height,weight,draft_team,draft_year,draft_round,round_pick,total_draft_pos]
		
		# Bio-data
		self.bio = bio
		self.bio['multiple_teams'] = ind['multiple_teams']
		
		# Ind
		self.ind = {}
		for attribute in ind.keys():
			if attribute not in ['multiple_teams']:
				self.ind[attribute] = ind[attribute]

		# Special attributes
		self.ind['toi_per_gp'] = [None,None,None]							# Time on ice per game
		self.ind['points'] = [None,None,None]								# Total points
		self.ind['primary_points'] = [None,None,None]						# Primary points
		self.ind['gf_above_xgf'] = [None,None,None]							# Goals scored above (individual) expected goals
		self.ind['points_per_60'] = [None,None,None]						# Total points scored per 60 min
		self.ind['primary_points_per_60'] = [None,None,None]				# Primary points scored per 60 min
		self.ind['isf_per_sec'] = [None,None,None]							# Individual shots forward per second
		self.ind['isf_per_60'] = [None,None,None]							# Individual shots forward per 60 min
		self.ind['pt_per_sec'] = [None,None,None]							# Penalties taken per second
		self.ind['pd_per_sec'] = [None,None,None]							# Peanlties draw per second
		self.ind['pt_per_60'] = [None,None,None]							# Penalties taken per 60 min
		self.ind['pd_per_60'] = [None,None,None]							# Penalties draw per 60 min
		self.ind['pd_diff_per_60'] = [None,None,None]						# Difference between penalties drawn and taken per 60 min. Higher number is better.
		self.ind['pd_pcg'] = [None,None,None]								# Quota between penalties drawn and taken. Higher number is better.
		self.ind['ixgf_per_60'] = [None,None,None]							# Individual expected goals forward per 60 min.
		self.ind['icf_per_60'] = [None,None,None]							# Individual CF per 60 min
		self.ind['part_primary'] = [None,None,None]							# Quota of totals points that is primary points. Higher number is better.
		self.ind['icf_pcg'] = [None,None,None]								# "Shooting percentage", for individual CF.
		#self.ind['ixgf'] = [None,None,None]									# Individual expected goals forward
		self.ind['ixgf_pcg'] = [None,None,None]								# Quota between individual expected goals and goals scored.
		self.ind['goal_scoring_rating'] = [None,None,None]					# Metric showing goal scoring potential.
		
		for index in [STAT_ES,STAT_PP,STAT_PK]:
			# For readability
			toi = ind['toi'][index]
			gf = ind['gf'][index]
			assist = ind['assist'][index]
			f_assist = ind['f_assist'][index]
			s_assist = ind['s_assist'][index]
			points = gf + assist
			p_points = gf + f_assist
			pt = ind['pt'][index]
			pd = ind['pd'][index]
			isf = ind['isf'][index]
			ixgf = ind['ixgf'][index]
			icf = ind['icf'][index]
			
			if toi == 0:
				self.ind['points_per_60'][index] = 0
				self.ind['primary_points_per_60'][index] = 0
				self.ind['isf_per_sec'][index] = 0
				self.ind['pt_per_sec'][index] = 0
				self.ind['pd_per_sec'][index] = 0
				self.ind['pt_per_60'][index] = 0
				self.ind['pd_per_60'][index] = 0
				self.ind['ixgf_per_60'][index] = 0
				self.ind['icf_per_60'][index] = 0
				self.ind['isf_per_60'][index] = 0
			else:
				self.ind['points_per_60'][index] = (points/toi) * 3600
				self.ind['primary_points_per_60'][index] = (p_points/toi) * 3600
				self.ind['isf_per_sec'][index] = isf/toi
				self.ind['pt_per_sec'][index] = pt/toi			# penalties taken per second
				self.ind['pd_per_sec'][index] = pd/toi			# penalties drawn per second
				self.ind['pt_per_60'][index] = self.ind['pt_per_sec'][index] * 3600
				self.ind['pd_per_60'][index] = self.ind['pd_per_sec'][index] * 3600
				self.ind['ixgf_per_60'][index] = (ixgf/toi) * 3600
				self.ind['icf_per_60'][index] = (icf/toi) * 3600
				self.ind['isf_per_60'][index] = self.ind['isf_per_sec'][index] * 3600

			if points == 0:
				self.ind['part_primary'][index] = 0
			else:
				self.ind['part_primary'][index] = p_points/points
			if icf == 0:
				self.ind['icf_pcg'][index] = 0
			else:
				self.ind['icf_pcg'][index] = gf/icf
			if self.ind['pt_per_60'][index] + self.ind['pd_per_60'][index] == 0:
				self.ind['pd_pcg'][index] = 0
			else:
				self.ind['pd_pcg'][index] = self.ind['pd_per_60'][index]/(self.ind['pd_per_60'][index]+self.ind['pt_per_60'][index])
			if gf + ixgf == 0:
				self.ind['ixgf_pcg'][index] = 0
			else:
				self.ind['ixgf_pcg'][index] = gf/(gf+ixgf)
			
			self.ind['toi_per_gp'][index] = toi/on_ice['gp']
			self.ind['points'][index] = gf + assist
			self.ind['primary_points'][index] = gf + f_assist
			self.ind['gf_above_xgf'][index] = gf-ixgf
			self.ind['pd_diff_per_60'][index] = self.ind['pd_per_60'][index] - self.ind['pt_per_60'][index]
			self.ind['goal_scoring_rating'][index] = self.ind['ixgf_pcg'][index] * self.ind['icf_per_60'][index]
		
		# OnIce
		self.on_ice = {}
		for attribute in on_ice.keys():
			self.on_ice[attribute] = on_ice[attribute]

		# Special attributes
		toi = ind['toi'][STAT_ES]
		self.on_ice['cf_per_sec'] = self.on_ice['cf']/ind['toi'][STAT_ES]
		self.on_ice['ca_per_sec'] = self.on_ice['ca']/ind['toi'][STAT_ES]
		self.on_ice['cf_per_60'] = 3600 * self.on_ice['cf_per_sec']
		self.on_ice['ca_per_60'] = 3600 * self.on_ice['ca_per_sec']
		self.on_ice['sf_per_sec'] = self.on_ice['sf']/ind['toi'][STAT_ES]
		self.on_ice['sa_per_sec'] = self.on_ice['sa']/ind['toi'][STAT_ES]
		self.on_ice['sf_per_60'] = 3600 * self.on_ice['sf_per_sec']
		self.on_ice['sa_per_60'] = 3600 * self.on_ice['sa_per_sec']
		self.on_ice['xgf_per_sec'] = self.on_ice['xgf']/ind['toi'][STAT_ES]
		self.on_ice['xga_per_sec'] = self.on_ice['xga']/ind['toi'][STAT_ES]
		self.on_ice['xgf_per_60'] = 3600 * self.on_ice['xgf_per_sec']
		self.on_ice['xga_per_60'] = 3600 * self.on_ice['xga_per_sec']
		self.on_ice['scf_per_sec'] = self.on_ice['scf']/ind['toi'][STAT_ES]
		self.on_ice['sca_per_sec'] = self.on_ice['sca']/ind['toi'][STAT_ES]
		self.on_ice['scf_per_60'] = 3600 * self.on_ice['scf_per_sec']
		self.on_ice['sca_per_60'] = 3600 * self.on_ice['sca_per_sec']
		self.on_ice['hdcf_per_sec'] = self.on_ice['hdcf']/ind['toi'][STAT_ES]
		self.on_ice['hdca_per_sec'] = self.on_ice['hdca']/ind['toi'][STAT_ES]
		self.on_ice['hdcf_per_60'] = 3600 * self.on_ice['hdcf_per_sec']
		self.on_ice['hdca_per_60'] = 3600 * self.on_ice['hdca_per_sec']

		self.on_ice['ozs_pcg'] = self.on_ice['ozs']/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs'])
		self.on_ice['nzs_pcg'] = self.on_ice['nzs']/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs'])
		self.on_ice['dzs_pcg'] = self.on_ice['dzs']/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs'])
		self.on_ice['ozfo_pcg'] = self.on_ice['ozfo']/(self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
		self.on_ice['nzfo_pcg'] = self.on_ice['nzfo']/(self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
		self.on_ice['dzfo_pcg'] = self.on_ice['dzfo']/(self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
		self.on_ice['oz_pcg'] = (self.on_ice['ozs'] + self.on_ice['ozfo'])/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs']+self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
		self.on_ice['nz_pcg'] = (self.on_ice['nzs'] + self.on_ice['nzfo'])/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs']+self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
		self.on_ice['dz_pcg'] = (self.on_ice['dzs'] + self.on_ice['dzfo'])/(self.on_ice['ozs']+self.on_ice['nzs']+self.on_ice['dzs']+self.on_ice['ozfo']+self.on_ice['nzfo']+self.on_ice['dzfo'])
		self.on_ice['non_dz_pcg'] = self.on_ice['oz_pcg'] + self.on_ice['nz_pcg']
		self.on_ice['non_oz_pcg'] = self.on_ice['dz_pcg'] + self.on_ice['nz_pcg']
		self.on_ice['non_nz_pcg'] = self.on_ice['oz_pcg'] + self.on_ice['dz_pcg']
		self.on_ice['avg_zone_start'] = (self.on_ice['oz_pcg']*3 + self.on_ice['nz_pcg']*2 + self.on_ice['dz_pcg']*1)-2
		self.rating = []
		# Simulated stats
		self.in_game_stats = defaultdict(int)
		
		# All "estimated_off/def" attributes need to be added after the construction, as they depend on the overall team.
		self.on_ice['estimated_off_per_sec'] = 0 
		self.on_ice['estimated_def_per_sec'] = 0
		self.on_ice['estimated_off_per_60'] = 0
		self.on_ice['estimated_def_per_60'] = 0
		self.on_ice['estimated_def_per_60_diff'] = 0
		self.on_ice['estimated_off_pcg'] = 0

	def print_player(self,s_db=None):
		print('Information for player ' + self.bio['name'])
		print('   5v5: ')
		for attribute in self.es.keys():
			if s_db == None:
				print('      ' + str(attribute) + ': ' + str(self.es[attribute]))
			else:
				op = print_sorted_list(s_db,[attribute],'es',operation=None,toi_filter=200,position_filter=['F','D'],team=None,print_list_length=100,scale_factor=1,high_to_low=True,do_print=False)
				[idx,__] = get_pair_index(op['list'],self.bio['name'])
				idx += 1
				N = len(op['data']) + 1
				print('      ' + str(attribute) + ': ' + str(self.es[attribute]) + ' (' + str(idx) + '/' + str(N)  + '). League average: ' + str(op['mu']))
		print('   OnIce: ')
		for attribute in self.on_ice.keys():
			if s_db == None:
				print('      ' + str(attribute) + ': ' + str(self.on_ice[attribute]))
			else:
				op = print_sorted_list(s_db,[attribute],'es',operation=None,toi_filter=200,position_filter=['F','D'],team=None,print_list_length=100,scale_factor=1,high_to_low=True,do_print=False)
				[idx,__] = get_pair_index(op['list'],self.bio['name'])
				idx += 1
				N = len(op['data']) + 1
				print('      ' + str(attribute) + ': ' + str(self.on_ice[attribute]) + ' (' + str(idx) + '/' + str(N)  + '). League average: ' + str(op['mu']))


class Goalie():
	def __init__(self,name,team_id,stats_arr):
		# Meta-data
		self.bio = {}
		self.bio['name'] = name
		self.bio['team_id'] = team_id
		self.bio['position'] = 'G'
		# Statistics
		self.toi = stats_arr[0]
		self.toi_pcg = stats_arr[1]
		self.sa = stats_arr[2]
		self.sa_per_sec = self.sa/self.toi
		self.sv = stats_arr[3]
		self.ga = stats_arr[4]
		self.sv_pcg = self.sv/self.sa
		self.gaa = stats_arr[5]
		self.gsaa = stats_arr[6]
		self.gsaa_per_60 = 3600*(self.gsaa/self.toi)
		self.xga = stats_arr[7]
		self.avg_shot_dist = stats_arr[8]
		self.avg_goal_dist = stats_arr[9]
		# Simulated stats
		self.in_game_stats = defaultdict(int)

	def get_attribute(self,attribute):
		if attribute in self.bio.keys():
			return self.bio[attribute]
		elif attribute == 'toi':
			return self.toi
		elif attribute == 'toi_pcg':
			return self.toi_pcg
		elif attribute == 'sa':
			return self.sa
		elif attribute == 'sa_per_sec':
			return self.sa_per_sec
		elif attribute == 'sv':
			return self.sv
		elif attribute == 'ga':
			return self.ga
		elif attribute == 'sv_pcg':
			return self.sv_pcg
		elif attribute == 'gaa':
			return self.gaa
		elif attribute == 'gsaa':
			return self.gsaa
		elif attribute == 'gsaa_per_60':
			return self.gsaa_per_60
		elif attribute == 'xga':
			return self.xga
		elif attribute == 'avg_shot_dist':
			return self.avg_shot_dist
		elif attribute == 'avg_goal_dist':
			return self.avg_goal_dist
		else:
			raise ValueError('Unknown attribute ' + attribute)


class Team():
	def __init__(self,name,reg_array,adv_array,team_schedule):
#		adv_array = [sf,sa,cf,ca,cf_pcg,scf,sca,scf_pcg,hdcf,hdca,hdcf_pcg,sv_pcg,pdo,sa_per_sec]

		self.name = name 		# name = team_id
		[self.conference, self.division] = self.get_division(self.name)
		
		self.gp = reg_array[0]
		self.team_toi_es = reg_array[1]
		self.team_toi_es_per_gp = self.team_toi_es / self.gp
		self.w = reg_array[2]
		self.l = reg_array[3]
		self.otl = reg_array[4]
		self.p = reg_array[5]
		self.gf = reg_array[6]
		self.ga = reg_array[7]
		self.p_pcg = reg_array[8]
		
		# This is directly accessed in the create_team_db()
		self.team_toi_pp = 0
		self.team_toi_pk = 0
		self.team_toi_pp_per_gp = 0
		self.team_toi_pk_per_gp = 0

		self.sf = adv_array[0]
		self.sa = adv_array[1]
		self.sf_pcg = adv_array[2]
		self.cf = adv_array[3]
		self.ca = adv_array[4]
		self.cf_pcg = adv_array[5]
		self.cf_per_sec = self.cf/self.team_toi_es
		self.ca_per_sec = self.ca/self.team_toi_es
		self.ff = adv_array[6]
		self.fa = adv_array[7]
		self.ff_pcg = adv_array[8]
		self.scf = adv_array[9]
		self.sca = adv_array[10]
		self.scf_pcg = adv_array[11]
		self.scf_per_sec = self.scf/self.team_toi_es
		self.sca_per_sec = self.sca/self.team_toi_es
		self.scf_per_60 = 3600 * self.scf_per_sec
		self.sca_per_60 = 3600 * self.sca_per_sec
		self.hdcf = adv_array[12]
		self.hdca = adv_array[13]
		self.hdcf_pcg = adv_array[14]
		self.sv_pcg = adv_array[15]
		self.pdo = adv_array[16]
		self.sa_per_sec = adv_array[17]

		self.rating_1a = self.cf_pcg
		self.rating_1b = self.rating_1a*self.pdo
		self.rating_1c = self.rating_1a*self.p_pcg
		self.rating_1d = self.rating_1a*self.pdo*self.p_pcg
		self.rating_1e = self.rating_1a*(self.pdo+self.p_pcg)
		self.rating_1f = self.rating_1a*(self.pdo+(self.p_pcg/2))

		self.rating_2a = self.scf_pcg
		self.rating_2b = self.rating_2a*self.pdo
		self.rating_2c = self.rating_2a*self.p_pcg
		self.rating_2d = self.rating_2a*self.pdo*self.p_pcg
		self.rating_2e = self.rating_2a*(self.pdo+self.p_pcg)
		self.rating_2f = self.rating_2a*(self.pdo+(self.p_pcg/2))

		self.rating_3a = (self.cf_pcg+self.scf_pcg)
		self.rating_3b = self.rating_3a*self.pdo
		self.rating_3c = self.rating_3a*self.p_pcg
		self.rating_3d = self.rating_3a*self.pdo*self.p_pcg	
		self.rating_3e = self.rating_3a*(self.pdo+self.p_pcg)
		self.rating_3f = self.rating_3a*(self.pdo+(self.p_pcg/2))

		self.rating_4a = (self.cf_pcg*self.scf_pcg)
		self.rating_4b = self.rating_4a*self.pdo
		self.rating_4c = self.rating_4a*self.p_pcg
		self.rating_4d = self.rating_4a*self.pdo*self.p_pcg
		self.rating_4e = self.rating_4a*(self.pdo+self.p_pcg)
		self.rating_4f = self.rating_4a*(self.pdo+(self.p_pcg/2))

		self.rating_5  = self.pdo*self.p_pcg
		
		self.rating = self.rating_2e
		
		self.schedule = team_schedule
		self.remaining_schedule = self.schedule[self.gp:]
		self.game_index = self.gp
		self.simulated_wins = 0
		self.simulated_po_div_final = 0
		self.simulated_po_conf_final = 0
		self.simulated_po_conf_champ = 0
		self.simulated_po_sc_champ = 0
		#if self.game_index >= 0:			
		#	self.previous_opponent = self.schedule[self.game_index]
		#else:
		#	self.previous_opponent = 'N/A'
		if self.game_index == 82:
			self.next_opponent = 'N/A'
		self.gf_in_simulated_game = 0
		self.sf_in_simulated_game = 0
		self.exp_data = {}
		self.exp_data['team_sf_in_simulated_game'] = 0
		self.exp_data['in_season_rating'] = 0
		self.exp_data['pre_season_rating'] = 0
		self.exp_data['total_made_playoffs'] = 0
		self.exp_data['mean_made_playoffs'] = 0
		self.exp_data['total_simulated_points'] = 0
		self.exp_data['mean_simulated_points'] = 0


	def get_division(self,team_id):
		atlantic,metro,central,pacific = set(),set(),set(),set()
		atlantic.update(['BOS'],['BUF'],['DET'],['FLA'],['MTL'],['OTT'],['TBL'],['TOR'])
		metro.update(['CAR'],['CBJ'],['NJD'],['NYI'],['NYR'],['PHI'],['PIT'],['WSH'])
		central.update(['CHI'],['COL'],['DAL'],['MIN'],['NSH'],['STL'],['WPG'])
		pacific.update(['ANA'],['ARI'],['CGY'],['EDM'],['LAK'],['SJS'],['VAN'],['VGK'])		
		western = pacific.union(central)
		eastern = atlantic.union(metro)

		if team_id in atlantic:
			return ['E','A']
		elif team_id in metro:
			return ['E','M']
		elif team_id in central:
			return ['W','C']
		elif team_id in pacific:
			return ['W','P']
		else:
			raise ValueError('Unknown team-ID: ' + str(team_id))

	def add_points(self,p_to_add):
		self.p += p_to_add

	def get_point_projection_for_game(self,opp):
		total_rating = self.rating + opp.rating
		return [TOTAL_POINTS_PER_GAME*self.rating/total_rating, TOTAL_POINTS_PER_GAME*opp.rating/total_rating,self.rating/total_rating,opp.rating/total_rating]

	def get_ratings(self):
		return [self.exp_data['in_season_rating'], self.exp_data['pre_season_rating']]

	def update_score(self,key):
		if key == 'w':
			self.p += 2
			self.w += 1
			self.simulated_wins += 1
		elif key == 'l':
			self.p += 0
			self.l += 1
		elif key == 'otl':
			self.p += 1
			self.otl += 1
		else:
			raise ValueError('Unknown key "' + str(key) + '". Key needs to be "w", "l" or "otl"')

	def reset_schedule(self,simulation_param):
		self.gp = 0
		self.w = 0
		self.l = 0
		self.otl = 0
		self.p = 0
		self.gf = 0
		self.ga = 0
		self.p_pcg = 0
		self.exp_data['in_season_rating'] = self.exp_data['pre_season_rating']
		self.remaining_schedule = (self.schedule).copy()

	def simulate_game(self,opponent,simulation_param,data_param=[]):
		simulation_param['ht_id'] = self.name 									# 
		simulation_param['at_id'] = opponent.name 	

		# Update game data
		self.gp += 1
		opponent.gp += 1
		# Update points
		if (simulation_param['simulation_mode'] == SIMULATION_LIGHT):
			# Simplified simulation, based on team-stats.
			
			# New version of calculating "rating". Old version would be: distribution = self.rating/(self.rating+opponent.rating)
			distribution = self.exp_data['in_season_rating']/(self.exp_data['in_season_rating']+opponent.exp_data['in_season_rating'])

			self.gf_in_simulated_game = distribution*TOTAL_GOALS_PER_GAME
			opponent.gf_in_simulated_game = (1-distribution)*TOTAL_GOALS_PER_GAME
			if random.uniform(0,1) < PROBABILITY_FOR_OT:  # this is not correct.
				if random.uniform(0,1) < distribution:
					self.update_score('w')
					opponent.update_score('otl')
				else:
					self.update_score('otl')
					opponent.update_score('w')
			else:
				if random.uniform(0,1) < distribution:
					self.update_score('w')
					opponent.update_score('l')
				else:
					self.update_score('l')
					opponent.update_score('w')
		else:
			# Advanced (and time demanding) simulation, based on player stats.			
			# Simulate the game
			game_output = simulate_ind_game(simulation_param,data_param)

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

	def simulate_game_in_season(self,opponent,simulation_param,data_param=[]):
		# Simulate one game
		self.simulate_game(opponent,simulation_param,data_param)

		# Update schedule
		#self.previous_opponent = opponent.name
		self.remaining_schedule = self.remaining_schedule[1:]
		if len(self.remaining_schedule) > 0:
			self.next_opponent = self.remaining_schedule[0]
		else:
			self.next_opponent = 'N/A'
		# Remove game from remaining schedule
		opponent.remaining_schedule.remove(self.name)