import sys
import os.path
import json
import simplejson
import cherrypy
import requests
import random
import json
import gspread
import wget
import numpy as np
from collections import defaultdict
from oauth2client.client import SignedJwtAssertionCredentials
from google_images_download import google_images_download
from bs4 import BeautifulSoup

class MyUI:

	def __init__(self):
		self.credentials = None

	@cherrypy.expose
	def index(self):

		soup_string = ''
		soup_string += '<form action="generate_new_record" method="POST">'
		soup_string += 'Update Google Doc?'
		soup_string += '<select name="update_records" id="update_records">'
		soup_string += '<option value="1">' + 'Yes' + '</option>'
		soup_string += '<option value="0">' + 'No' + '</option>'
		soup_string += '<input type="submit" value="Randomize new record">'
		soup_string += '</form>'

		return BeautifulSoup(soup_string,'lxml').prettify()
	
	@cherrypy.expose
	def generate_new_record(self,update_records):
		print('Update GDoc: ' + str(update_records))
		name_of_ws = "SharksData_Public"

		if self.credentials == None:
			# Access gSheet and read data from the worksheet.
			
			credential_path = 'creds.json' 			# Old version
			print('Authentication Google Sheet "' + name_of_ws +'"...')
			json_key = json.load(open(credential_path)) # json credentials you downloaded earlier
			scope = ['https://spreadsheets.google.com/feeds',
			         'https://www.googleapis.com/auth/drive']
			credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds
			self.credentials = credentials
		
		g_file = gspread.authorize(self.credentials) # authenticate with Google
		print('Authentication done')
		g_wb = g_file.open(name_of_ws) # Open Google WorkBook
		input_data = g_wb.worksheet("Records")
		list_of_lists = input_data.get_all_values()

		# Process data from worksheet
		unplayed_albums = dict()
		N_all = len(list_of_lists)-1 # Remove header row
		for i,row in enumerate(list_of_lists):
			if (i != 0) and (row[3] == 'FALSE'): # Assuming header row is first row.
				unplayed_albums[i] = row
		unplayed_albums_idx = list(unplayed_albums.keys())
		N_unplayed = len(unplayed_albums_idx)
		N_played = N_all - N_unplayed

		# Randomly select the album to play
		rand_n = round(random.uniform(0,N_unplayed))
		play_id = unplayed_albums_idx[rand_n]
		artist = unplayed_albums[play_id][1]
		album = unplayed_albums[play_id][2]
		image_search_url = 'https://www.google.com/search?q=' + artist + ' + ' + album + 'album+art&hl=en&tbm=isch'
		tmp_soup = BeautifulSoup(requests.get(image_search_url).text,'lxml')
		images = tmp_soup.find_all('img')
		image_url = images[3]['src']
		filepath = wget.download(image_url,artist + '_' + album + '.png')
		
		soup_string = ''
		soup_string += 'Listen to <b> ' + artist + ' - ' + album + '</b>.<br/>'
		#soup_string += '<img src="' + os.path.join(os.getcwd(),filepath) + '">'
		
		soup_string += 'You have listen to ' + str(N_played) + ' albums out of ' + str(N_all) + '(' + str(np.floor(100*N_played/N_all)) +'%)'
		soup_string += '<br/><br/>'
		soup_string += '<form action="index"><input type="submit" value="Home"></form>'
		soup_string += '<img src="/Users/tobiassolbeckarandersson/Documents/Work/Ictech/ictech-cv-gen2/modules/cv_generator/images/ruler.png"/>'
		soup = BeautifulSoup(soup_string,'lxml')

		if update_records == "1":
			# Update gSheet
			input_data.update_cell(play_id+1,4,'TRUE')
			date_print = str(datetime.datetime.now().strftime("%x"))
			input_data.update_cell(play_id+1,5,date_print)

		return soup.prettify()

if __name__ == '__main__':
	cherrypy.config.update({
		'server.socket_host': '0.0.0.0',
		'server.socket_port': 8090,
        })
	cherrypy.quickstart(MyUI())