import datetime
import time
import itertools
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math
import inspect
import csv
import copy
import random
import copy
import warnings
from collections import defaultdict
from nhl_defines import *

def generate_long_name():
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
	output['SJS'] = return_type
	output['STL'] = return_type
	output['TBL'] = return_type
	output['TOR'] = return_type
	output['VAN'] = return_type
	output['VGK'] = return_type
	output['WPG'] = return_type
	output['WSH'] = return_type
	return output

def get_long_name(team_id):
	tmp = generate_long_name()
	return tmp[team_id]

def get_team_id(long_name):
	tmp = generate_long_name()
	for team_id in tmp:
		if tmp[team_id] == long_name:
			return team_id

def get_team(team_db,team_id):
	return team_db[team_id]

def get_player(player_db,player_id):
	return player_db[player_id]

def get_unavailable_players():
	unavailable_players = defaultdict(list)
	unavailable_players['SJS'].append('DALTON_PROUT')
	unavailable_players['SJS'].append('JACOB_MIDDLETON')
	unavailable_players['SJS'].append('JONNY_BRODZINSKI')
	unavailable_players['SJS'].append('TREVOR_CARRICK')
	unavailable_players['SJS'].append('DANIL_YURTAYKIN')
	return unavailable_players

def print_progress(i,N,t0,step=10):
	time_unit = ['min','min']
	printed = False
	if ((i%(N/(100/step))) == 0) and (i>0):
		t_elp = (time.time() - t0)/60
		t_left = t_elp*((N/i) - 1)
		if t_elp < 1.0:
			t_elp *= 60
			time_unit[0] = 'sec'
		if t_left < 1.0:
			t_left *= 60
			time_unit[1] = 'sec'
		n = datetime.datetime.now()
		print_n = str(datetime.time(n.hour,n.minute,n.second))
		if time_unit[1] == 'sec':
			eta = n+datetime.timedelta(seconds=t_left)
		else:
			eta = n+datetime.timedelta(minutes=t_left)
		print_eta = str(datetime.time(eta.hour,eta.minute,eta.second))
		print('{0}: {1:.0f} % completed. Time elapsed: {2:.0f} {3}. Estimated time left: {4:.0f} {5} (ETA: {6}).'.format(print_n,100*i/N,t_elp,time_unit[0],t_left,time_unit[1],print_eta))
		printed = True
	return printed

def val_in_list(val,lst):
	''' Returns the number of times the value val appears in the list lst. '''
	o = 0
	for vl in lst:
		if vl == val: 
			o += 1
	return o

def get_list_pcg(lst):
	new_lst = []
	for i in range(len(lst)):
		new_lst.append(100*lst[i]/sum(lst))
	return new_lst

def get_time_str_from_sec(seconds):
	m = seconds//60
	s = seconds%60
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
	player_id = str(raw_str).upper().replace(' ','_')
	player_id = player_id.replace('.','_')
	player_id = player_id.replace("'",'')
	return player_id

def print_sorted_list(db,attributes,playform,operation=None,toi_filter=200,position_filter=['F','D'],team=None,print_list_length=50,scale_factor=1,high_to_low=True,do_print=True,normalize=False):
	output = {}
	toi_filter *= 60
	sorted_list = []
	data_list = []
	for skater_id in db.keys():
		skater = db[skater_id]
		if skater.es['toi'] >= toi_filter and skater.bio['position'] in position_filter:
			if len(attributes) > 1:
				val_a = get_attribute_value(skater,attributes[0],playform)
				val_b = get_attribute_value(skater,attributes[1],playform)
				val = operation(val_a,val_b)
			else:
				val = get_attribute_value(skater,attributes[0],playform)
			val *= scale_factor

			if team == None:		
				sorted_list.append((val,skater_id))
				data_list.append(val)
			else:
				if skater.bio['team_id'] == team:
					sorted_list.append((val,skater_id))
					data_list.append(val)
			
	sorted_list.sort(reverse=high_to_low)
	data_list.sort(reverse=high_to_low)
	output['mu'] = np.mean(data_list)
	output['sigma'] = np.std(data_list)
	output['list'] = sorted_list
	output['data'] = data_list
	if normalize == True:
		norm_factor = 1/np.max(data_list)
	else:
		norm_factor = 1
	if do_print == True:
		print('\n' + str(attributes) + ' (scale factor=' + str(scale_factor) + '):')
		ranking = 1
		for pair in sorted_list:
			skater = db[pair[1]]
			if ranking <= print_list_length:
				#print('{0}: {1} ({2}) - "{3}"({4}): {5:.1f}.'.format(ranking,skater.bio['name'],skater.bio['team_id'],attributes,playform.upper(),pair[0]))
				print('{0}: {1} ({2}) - {3:.2f}'.format(ranking,skater.bio['name'],skater.bio['team_id'],norm_factor*pair[0]))
				for attribute in attributes:
					print('   {0}: {1:.2f}'.format(attribute,scale_factor*get_attribute_value(skater,attribute,playform)))
				ranking += 1
	return output



def get_attribute_value(player,attribute,playform='es'):
	# attribute should be on the form "attribute-playform", where playform is either "es", "pp" or "pk".
	if player.bio['position'] == 'G':
		raise ValueError('Function "get_attribute_value" does not support Class Goalies.')

	if attribute in player.es.keys():
		if playform == 'es':
			return player.es[attribute]
		elif playform == 'pp':
			return player.pp[attribute]
		elif playform == 'pk':
			return player.pk[attribute]
		else:
			raise ValueError('Unknown playform ' + playform + '.')
	elif attribute in player.on_ice.keys():
		return player.on_ice[attribute]
	elif attribute in player.bio.keys():
		return player.bio[attribute]
	else:
		raise ValueError('Unknown attribute ' + attribute)

def get_pair_index(pair_list,key):
	for idx,pair in enumerate(pair_list):
		val = pair[0]
		name = pair[1]
		if name == key:
			return [idx,val]
	raise ValueError('No key ' + key + ' found in list')

def get_sigma_difference(db,player_id,attribute,playform='es'):
	op = print_sorted_list(db,[attribute],playform,operation=None,toi_filter=200,position_filter=['F','D'],team=None,print_list_length=50,scale_factor=1,high_to_low=True,do_print=False,normalize=False)
	player_val = get_attribute_value(db[player_id],attribute,playform)
	return (player_val-op['mu'])/op['sigma']

def plot_player_cards(ax,axes_info,p_db,player_ids,flter):
	# Init
	gen_x,gen_y,spec_x,spec_y,markers = [],[],[],[],[]
	output = {}
	output['pair_list'], output['data_list'] = [],[]
	ydata_only = False
	tmp_index = 0
	
	# Set up additional axes information
	if axes_info['x']['attribute'] == None:
		axes_info['fit_data'] = False
		ydata_only = True
		axes_info['x']['label'] = 'Player no.'
		axes_info['x']['invert'] = False
	
	# Set up color/markers
	colors = ['c','m','g','r','b'] # black and yellow are protected colors.
	forms = ['o','v','s','*','x','p','d']
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
		if tmp_player.bio['position'] == 'G':
			if tmp_player.get_attribute('toi') > flter['toi']*60:
				if ydata_only == True:
					gen_x.append(tmp_index)
					tmp_index += 1
				else:
					gen_x.append(axes_info['x']['scale']*tmp_player.get_attribute(axes_info['x']['attribute']))
				gen_y.append(axes_info['y']['scale']*tmp_player.get_attribute(axes_info['y']['attribute']))
		else:
			if (get_attribute_value(tmp_player,'toi','es') > flter['toi']*60):# and (tmp_player.bio['position'] == flter['position']):
				if ydata_only == True:
					gen_x.append(tmp_index)
					tmp_index += 1
				else:
					gen_x.append(axes_info['x']['scale']*get_attribute_value(tmp_player,axes_info['x']['attribute']))
				gen_y.append(axes_info['y']['scale']*get_attribute_value(tmp_player,axes_info['y']['attribute']))
	plt.scatter(gen_x,gen_y,c='k',marker='.')

	# Add mean value.
	plt.scatter(np.mean(gen_x),np.mean(gen_y),c='y',marker='s',label='NHL mean')
	
	# Fit linear model to (scatter) data.
	if axes_info['fit_data'] == True:
		fit = np.polyfit(gen_x, gen_y, 1)
		fit_fn = np.poly1d(fit)
		k = round(fit[0],4)
		output['fit'] = fit
		output['fit_fn'] = fit_fn
		x_val = range(int(np.min(ax.get_xlim())),int(np.max(ax.get_xlim())))
		plt.plot(x_val,fit_fn(x_val),'y--',label='Data fit (k=' + str(k) + ')')
	
	# Add 50% threshold.
	if axes_info['add_threshold'] == True:
		start = int(np.min([np.min(ax.get_xlim()),np.min(ax.get_ylim())]))
		stop = int(np.max([np.max(ax.get_xlim()),np.max(ax.get_ylim())]))
		plt.plot(range(start,stop),range(start,stop),'k--',label='50% threshold')

	# Plot data for the specified players.
	marker_idx = 0
	for i, player_id in enumerate(player_ids):
		player = p_db[player_id]
		if player.bio['position'] == 'G':
			# Different functions for getting data from goalies vs. skaters
			if player.get_attribute('toi') < flter['toi']*60:
				warnings.warn('Player ' + player_id + ' has played less than ' + str(flter['toi']) + ' minutes even strength (' + str(int(player.get_attribute('toi')/60)) + '). Data not included in plot(s).')
			else:
				current_marker = markers[marker_idx]
				if ydata_only == True:
					plt.scatter(i,axes_info['y']['scale']*player.get_attribute(axes_info['y']['attribute']),c=current_marker[1],marker=current_marker[0],label=player_id)
				else:
					if axes_info['fit_data'] == True:
						x_val = axes_info['x']['scale']*player.get_attribute(axes_info['x']['attribute'])
						y_val = axes_info['y']['scale']*player.get_attribute(axes_info['y']['attribute'])
						y_est = fit_fn(x_val)
						y_diff = y_val - y_est
						if y_diff > 0:
							sign = '+'
						else:
							sign = ''
						lbl_val_str = ' (' + sign + str(int(100*y_diff/y_est)) + '%)'
					else:
						lbl_val_str = ''
					plt.scatter(axes_info['x']['scale']*player.get_attribute(axes_info['x']['attribute']),axes_info['y']['scale']*player.get_attribute(axes_info['y']['attribute']),c=current_marker[1],marker=current_marker[0],label=player_id+lbl_val_str)
				marker_idx += 1
		else:
			if get_attribute_value(player,'toi','es') < flter['toi']*60:
				warnings.warn('Player ' + player_id + ' has played less than ' + str(flter['toi']) + ' minutes even strength (' + str(int(get_attribute_value(player,'toi','es')/60)) + '). Data not included in plot(s).')
			else:
				if do_plots == True:
					current_marker = markers[marker_idx]
				if (ydata_only == True) and (do_plots == True):
					plt.scatter(i,axes_info['y']['scale']*get_attribute_value(player,axes_info['y']['attribute'],'es'),c=current_marker[1],marker=current_marker[0],label=player_id)
				else:
					if axes_info['fit_data'] == True:
						x_val = axes_info['x']['scale']*get_attribute_value(player,axes_info['x']['attribute'],'es')
						y_val = axes_info['y']['scale']*get_attribute_value(player,axes_info['y']['attribute'],'es')
						y_est = fit_fn(x_val)
						y_diff = y_val - y_est
						output['pair_list'].append((y_diff,player_id))
						output['data_list'].append(y_diff)
						if y_diff > 0:
							sign = '+'
						else:
							sign = ''
						lbl_val_str = ' (' + sign + str(int(100*y_diff/y_est)) + '%)'
					else:
						lbl_val_str = ''
					if do_plots == True:
						plt.scatter(axes_info['x']['scale']*get_attribute_value(player,axes_info['x']['attribute']),axes_info['y']['scale']*get_attribute_value(player,axes_info['y']['attribute'],'es'),c=current_marker[1],marker=current_marker[0],label=player_id+lbl_val_str)
				marker_idx += 1
	
	# Invert axis for readability.
	if axes_info['x']['invert'] == True:
		ax.invert_xaxis() 
	if axes_info['y']['invert'] == True:
		ax.invert_yaxis()

	# Plot stuff
	plt.xlabel(axes_info['x']['label'])
	plt.ylabel(axes_info['y']['label'])
	font_size = np.min([140/len(player_ids),9])
	ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.03), ncol=1, fontsize=font_size)
	plt.subplots_adjust(left=0.05,bottom=0.07,top=0.95,right=0.82,hspace=0.3)
	plt.grid(True)

	output['pair_list'].sort(reverse=True)
	return [plt,ax,output]



def weighted_sum(lst,w_lst):
	op = 0
	if len(lst) != len(w_lst):
		raise ValueError('Incompatible lengths')
	for i in range(len(lst)):
		op += w_lst[i]*lst[i]

	return op







