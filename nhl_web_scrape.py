# Import modules
import requests
from bs4 import BeautifulSoup
from nhl_helpers import *
from nhl_defines import *


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

