# Import modules
import requests
import cfscrape
from bs4 import BeautifulSoup
import numpy as np
from math import *
from nhl_helpers import *
from nhl_defines import *
from nhl_classes import *
from nhl_web_scrape import *

seasons = [ADD_DATA_HERE]

def download_old_season_data(seasons=None)
	if seasons == None:
		raise ValueError('No seasons specified for download')
		
	print('Downloading new csv-files from www.naturalstattrick.com')
	for season in seasons:
		url_skater_ind_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
		url_skater_ind_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v4&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
		url_skater_ind_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=4v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single"
		url_skater_on_ice = "http://naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=oi&rate=r&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	 	url_skater_relative = "http://naturalstattrick.com/playerteams.php?fromseason=" season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=oi&rate=r&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	 	url_goalie_es = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season +"&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	 	url_goalie_pp = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season + "&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"
	 	url_goalie_pk = "https://www.naturalstattrick.com/playerteams.php?fromseason=" + season + "&thruseason=" + season +"&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL"

		print('   Downloading individual ES data for season ' + season)
		write_skater_ind_csv(url_skater_ind_es,os.path.join(data_dir,'Skater_Individual_ES_' + season + '.csv'))
		print('   Downloading individual PP data for season ' + season)
		write_skater_ind_csv(url_skater_ind_pp,os.path.join(data_dir,'Skater_Individual_PP_' + season + '.csv'))
		print('   Downloading individual PK data for season ' + season)
		write_skater_ind_csv(url_skater_ind_pk,os.path.join(data_dir,'Skater_Individual_PK_' + season + '.csv'))
		print('   Downloading on-ice data for season ' + season)
		write_skater_on_ice_csv(url_skater_on_ice,os.path.join(data_dir,'Skater_OnIce_' + season + '.csv'))
		print('   Downloading relative data for season ' + season)
		write_skater_relative_csv(url_skater_relative,os.path.join(data_dir,'Skater_Relative_' + season + '.csv'))
		print('   Downloading goalie ES data for season ' + season)
		write_goalie_csv(url_goalie_es,os.path.join(data_dir,'Goalie_ES_' + season + '.csv'))
		print('   Downloading goalie PP data for season ' + season)
		write_goalie_csv(url_goalie_pp,os.path.join(data_dir,'Goalie_PP_' + season + '.csv'))
		print('   Downloading goalie PK data for season ' + season)
		write_goalie_csv(url_goalie_pk,os.path.join(data_dir,'Goalie_PK_' + season + '.csv'))