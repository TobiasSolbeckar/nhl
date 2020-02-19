# Import modules
import requests
from bs4 import BeautifulSoup
from nhl_helpers import *
from nhl_defines import *
from nhl_classes import *
from nhl_database import *

def translate_web_name(web_name):
	if web_name == "N.Y. Islanders":
		team_name = 'New York Islanders'
	elif web_name == 'N.Y. Rangers':
		team_name = 'New York Rangers'
	else:
		team_name = web_name
	return team_name

def get_team_data_from_url():
	#headers = ['name','gp','w','l','otl','pts','row','gf','ga','diff','home','road','l10','strk','w','div','post']
	url = "https://www.cbssports.com/nhl/standings/"
	soup = BeautifulSoup(requests.get(url).text,'html.parser')
	tables = soup.find_all('table')
	td_east = tables[0].find_all('td')
	td_west = tables[1].find_all('td')

	team_dict = {}

	for i in range(16):
		link_items = td_east[i*17].find_all('a')
		name_item = link_items[1]
		name = translate_web_name(name_item.contents[0])
		gp = int(td_east[i*17+1].contents[0])
		w = int(td_east[i*17+2].contents[0])
		l = int(td_east[i*17+3].contents[0])
		otl = int(td_east[i*17+4].contents[0])
		pts = int(td_east[i*17+5].contents[0])
		gf = int(td_east[i*17+7].contents[0])
		ga = int(td_east[i*17+8].contents[0])
		p_pcg = pts/(2*gp)
		for team_id in ACTIVE_TEAMS:
			if name in get_long_name(team_id):
				team_dict[team_id] = [gp,w,l,otl,pts,gf,ga,p_pcg]

	for i in range(15):
		link_items = td_west[i*17].find_all('a')
		name_item = link_items[1]
		name = translate_web_name(name_item.contents[0])
		gp = int(td_west[i*17+1].contents[0])
		w = int(td_west[i*17+2].contents[0])
		l = int(td_west[i*17+3].contents[0])
		otl = int(td_west[i*17+4].contents[0])
		pts = int(td_west[i*17+5].contents[0])
		gf = int(td_west[i*17+7].contents[0])
		ga = int(td_west[i*17+8].contents[0])
		p_pcg = pts/(2*gp)
		for team_id in ACTIVE_TEAMS:
			if name in get_long_name(team_id):
				team_dict[team_id] = [gp,w,l,otl,pts,gf,ga,p_pcg]
	return team_dict

def write_skater_bio_csv(url,filename):
	is_ok = True
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(CONNECTION_TIMEOUT)
	try:
		soup = BeautifulSoup(requests.get(url).text,'html.parser')
		tables = soup.find_all('table')
		data_table = tables[0].find_all('td')
		data_length = SKATER_DB_BIO_LENGTH
		number_of_players = int(len(data_table)/data_length)
		with open(filename, mode='w', newline='') as csv_file:
			fieldnames = ['id','player_name','team','position','age','dob','birth_city','birth_state','birth_country','nationality','height','weight','draft_year','draft_team','draft_round','draft_round_pick','total_draft_pick']
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writeheader()
			for i in range(number_of_players):
				player_dict = {}
				
				player_dict['id'] = str(data_table[0+i*data_length].contents[0]) # 0
				#name_item = data_table[1+i*data_length]
				player_dict['player_name'] = str(data_table[1+i*data_length].find('a').contents[0])
				player_dict['team'] = str(data_table[2+i*data_length].contents[0])
				player_dict['position'] = str(data_table[3+i*data_length].contents[0])
				player_dict['age'] = str(data_table[4+i*data_length].contents[0])
				player_dict['dob'] = str(data_table[5+i*data_length].contents[0])
				player_dict['birth_city'] = str(data_table[6+i*data_length].contents[0])
				player_dict['birth_state'] = '-' #str(data_table[7+i*data_length].contents[0])
				player_dict['birth_country'] = str(data_table[8+i*data_length].contents[0])
				player_dict['nationality'] = '-' #str(data_table[9+i*data_length].contents[0])
				player_dict['height'] = str(data_table[10+i*data_length].contents[0])
				player_dict['weight'] = str(data_table[11+i*data_length].contents[0])
				player_dict['draft_year'] = str(data_table[12+i*data_length].contents[0])
				player_dict['draft_team'] = str(data_table[13+i*data_length].contents[0])
				player_dict['draft_round'] = str(data_table[14+i*data_length].contents[0])
				player_dict['draft_round_pick'] = str(data_table[15+i*data_length].contents[0])
				player_dict['total_draft_pick'] = str(data_table[16+i*data_length].contents[0])
				writer.writerow(player_dict)
	except Exception: 
		print('Connection timed out for ' + url)
		is_ok = False
	signal.alarm(0)
	return is_ok

def write_skater_ind_csv(url,filename):
	is_ok = True
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(CONNECTION_TIMEOUT)
	try:
		soup = BeautifulSoup(requests.get(url).text,'html.parser')
		tables = soup.find_all('table')
		data_table = tables[0].find_all('td')
		data_length = SKATER_DB_IND_LENGTH
		number_of_players = int(len(data_table)/data_length)
		with open(filename, mode='w', newline='') as csv_file:
			fieldnames = ['id','player_name','team','position','gp','toi','goals','assist','first_assist','second_assit','total_points','ipp','sf','sh_pcg','ixg','icf','iff','iscf','ihdcf','rush_attempts','rebounds_created','pim','total_penalties','minor','major','misconduct','penalties_drawn','giveaways','takeaways','hits','hits_taken','shots_blocked','faceoffs_won','faceoffs_lost','faceoffs_won_pcg']
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writeheader()
			for i in range(number_of_players):
				player_dict = {}
				for j,field in enumerate(fieldnames):
					if j == 1:
						name_item = data_table[1+i*data_length]
						player_dict['player_name'] = str(name_item.find('a').contents[0])
					else:
						player_dict[field] = str(data_table[j+i*data_length].contents[0])
				writer.writerow(player_dict)
	except Exception: 
		print('Connection timed out for ' + url)
		is_ok = False
	signal.alarm(0)
	return is_ok

def write_skater_on_ice_csv(url,filename):
	is_ok = True
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(CONNECTION_TIMEOUT)
	try:
		soup = BeautifulSoup(requests.get(url).text,'html.parser')
		tables = soup.find_all('table')
		data_table = tables[0].find_all('td')
		fieldnames = ['id','player_name','team','position','gp','toi','cf','ca','cf_pcg','ff','fa','ff_pcg','sf','sa','sf_pcg','gf','ga','gf_pcg','xgf','xga','xgf_pcg','scf','sca','scf_pcg','hdcf','hdca','hdcf_pcg','hdgf','hdga','hdgf_pcg','mdcf','mdca','mdcf_pcg','mdgf','mdga','mdgf_pcg','ldcf','ldca','ldcf_pcg','ldgf','ldga','ldgf_pcg','on_ice_sh_pcg','on_ice_sv_pcg','pdo','ozs','nzs','dzs','on_the_fly_starts','ofz_pcg','ozfo','nzfo','dzfo','ozfo_ocg']
		data_length = len(fieldnames)
		number_of_players = int(len(data_table)/data_length)
		with open(filename, mode='w', newline='') as csv_file:
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writeheader()
			for i in range(number_of_players):
				player_dict = {}
				for j,field in enumerate(fieldnames):
					if j == 1:
						name_item = data_table[1+i*data_length]
						player_dict['player_name'] = str(name_item.find('a').contents[0])
					else:
						player_dict[field] = str(data_table[j+i*data_length].contents[0])
				writer.writerow(player_dict)
	except Exception: 
		print('Connection timed out for ' + url)
		is_ok = False
	signal.alarm(0)
	return is_ok

def write_skater_relative_csv(url,filename):
	is_ok = True
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(CONNECTION_TIMEOUT)
	try:
		soup = BeautifulSoup(requests.get(url).text,'html.parser')
		tables = soup.find_all('table')
		data_table = tables[0].find_all('td')
		fieldnames = ['id','player_name','team','position','gp','toi','toi_per_gp','cf_60_rel','ca_60_rel','cf_pcg_rel','ff_60_rel','fa_60_rel','ff_pcg_rel','sf_60_rel','sa_60_rel','sf_pcg_rel','gf_60_rel','ga_60_rel','gf_pcg_rel','xgf_60_rel','xga_60_rel','xgf_pcg_rel','scf_60_rel','sca_60_rel','scf_pcg_rel','hdcf_60_rel','hdca_60_rel','hdcf_pcg_rel','hdgf_60_rel','hdga_60_rel','hdgf_pcg_rel','mdcf_60_rel','mdca_60_rel','mdcf_pcg_rel','mdgf_60_rel','mdga_60_rel','mdgf_pcg_rel','ldcf_60_rel','ldca_60_rel','ldcf_pcg_rel','ldgf_60_rel','ldga_60_rel','ldgf_pcg_rel','on_ice_sh_pcg','on_ice_sv_pcg','pdo','ozs_60','nzs_60','dzs_60','on_the_fly_starts_60','ozs_pcg','ozfo_60','nzfo_60','dzfo_60','ozfo_pcg']
		data_length = len(fieldnames)
		number_of_players = int(len(data_table)/data_length)
		with open(filename, mode='w', newline='') as csv_file:
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writeheader()
			for i in range(number_of_players):
				player_dict = {}
				for j,field in enumerate(fieldnames):
					if j == 1:
						name_item = data_table[1+i*data_length]
						player_dict['player_name'] = str(name_item.find('a').contents[0])
					else:
						player_dict[field] = str(data_table[j+i*data_length].contents[0])
				writer.writerow(player_dict)
	except Exception: 
		print('Connection timed out for ' + url)
		is_ok = False
	signal.alarm(0)
	return is_ok

def write_team_csv(url,filename):
	is_ok = True
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(CONNECTION_TIMEOUT)
	try:
		soup = BeautifulSoup(requests.get(url).text,'html.parser')
		tables = soup.find_all('table')
		data_table = tables[0].find_all('td')
		data_length = TEAM_DB_LENGTH
		number_of_teams = int(len(data_table)/data_length)
		with open(filename, mode='w', newline='') as csv_file:
			fieldnames = ['id','team_name','gp','toi','w','l','otl','row','points','points_pcg','cf','ca','cf_pcg','ff','fa','ff_pcg','sf','sa','sf_pcg','gf','ga','gf_pcg','xgf','xga','xgf_pcg','scf','sca','scf_pcg','scsf','scsa','scsf_pcg','scgf','scga','scgf_pcg','scsh_pcg','scsv_pcg','hdcf','hdca','hdcf_pcg','hdsf','hdsa','hdsf_pcg','hdgf','hdga','hdgf_pcg','hdsh_pcg','hdsv_pcg','mdcf','mdca','mdcf_pcg','mdsf','mdsa','mdsf_pcg','mdgf','mdga','mdgf_pcg','mdsh_pcg','mdsv_pcg','ldcf','ldca','ldcf_pcg','ldsf','ldsa','ldsf_pcg','ldgf','ldga','ldgf_pcg','ldsh_pcg','ldsv_pcg','sh_pcg','sv_pcg','pdo']
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writeheader()
			for i in range(number_of_teams):
				team_dict = {}
				for j,field in enumerate(fieldnames):
					team_dict[field] = str(data_table[j+i*data_length].contents[0])
				writer.writerow(team_dict)
	except Exception: 
		print('Connection timed out for ' + url)
		is_ok = False
	signal.alarm(0)
	return is_ok

def write_unavailable_players_csv(filename):
	is_ok = True
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(CONNECTION_TIMEOUT)
	try:
		with open(filename, mode='w', newline='') as csv_file:
			writer = csv.writer(csv_file,delimiter=',')
			unavailable_players = defaultdict(list)
			writer.writerow(['team_id','unavailable_players'])		# Write header manually.
			for team_id in ACTIVE_TEAMS:
				url = get_daily_fo_url(team_id)
				scraper = cfscrape.create_scraper()
				html = scraper.get(url).content
				soup = BeautifulSoup(html, 'html.parser')
				ir_container = soup.find("div", {"id": "ir-container"})
				try:
					ir_players = ir_container.find_all("td")
					for i in range(len(ir_players)):
						name_content = ir_players[i].contents[2].find_all("span")[1].contents[0]
						unavailable_players[team_id].append(generate_player_id(name_content))
				except:
					unavailable_players[team_id] = []
					print('Could not read injury reserve for ' + team_id)
				writer.writerow([team_id,unavailable_players[team_id]])
	except Exception: 
		print('Connection timed out for ' + url)
		is_ok = False
	signal.alarm(0)
	return is_ok

def write_goalie_csv(url,filename):
	is_ok = True
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(CONNECTION_TIMEOUT)
	try:
		soup = BeautifulSoup(requests.get(url).text,'html.parser')
		tables = soup.find_all('table')
		data_table = tables[0].find_all('td')
		fieldnames = ['id','player_name','team','gp','toi','sa','sv','ga','sv_pcg','gaa','gsaa','xga','hdsa','hdsv','hdga','hdsv_pcg','hdgaa','hdgsaa','mdsa','mdsv','mdga','mdsv_pcg','mdgaa','mdgsaa','ldsa','ldsv','ldga','ldsv_pcg','ldgaa','ldgsaa','rush_attempts_against','rebound_attempts_against','avg_shot_dist','avg_goal_dist']
		data_length = len(fieldnames)
		number_of_players = int(len(data_table)/data_length)
		with open(filename, mode='w', newline='') as csv_file:
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writeheader()
			for i in range(number_of_players):
				player_dict = {}
				for j,field in enumerate(fieldnames):
					if j == 1:
						name_item = data_table[1+i*data_length]
						player_dict['player_name'] = str(name_item.find('a').contents[0])
					else:
						player_dict[field] = str(data_table[j+i*data_length].contents[0])
				writer.writerow(player_dict)
	except Exception: 
		print('Connection timed out for ' + url)
		is_ok = False
	signal.alarm(0)
	return is_ok

def get_hits_dict(url='https://www.foxsports.com/nhl/team-stats?season=2019&category=miscellaneous&group=1&sort=9&time=0'):
	soup = BeautifulSoup(requests.get(url).text,'html.parser')
	tables = soup.find_all('table')
	data_table = tables[0].find_all('td')
	hits_dict = {}
	for i in range(31):
		stuff = data_table[0+i*13].find_all('span')
		team_id = str(stuff[2])[6:9]
		if team_id == 'LA<':
			team_id = 'LAK'
		elif team_id == 'SJ<':
			team_id = 'SJS'
		elif team_id == 'NJ<':
			team_id = 'NJD'
		elif team_id == 'TB<':
			team_id = 'TBL'
		hits_dict[team_id] = float(data_table[10+i*13].contents[0])
	return hits_dict
