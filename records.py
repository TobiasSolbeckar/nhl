import datetime
import random
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

# Access gSheet and read data from the worksheet.
name_of_ws = "SharksData_Public"
credential_path = 'creds.json' 			# Old version
print('Authentication Google Sheet "' + name_of_ws +'"...')
json_key = json.load(open(credential_path)) # json credentials you downloaded earlier
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds
g_file = gspread.authorize(credentials) # authenticate with Google
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
print('Play: {0} -  {1}. You have listened to {2:.0f} albums out of {3:.0f} ({4:.1f}%)'.format(unplayed_albums[play_id][1],unplayed_albums[play_id][2],N_played,N_all,100*N_played/N_all))

# Update gSheet
input_data.update_cell(play_id+1,4,'TRUE')
date_print = str(datetime.datetime.now().strftime("%x"))
input_data.update_cell(play_id+1,5,date_print)