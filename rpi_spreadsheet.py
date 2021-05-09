import json
import sys
import time
import datetime
import gspread
import psutil
import subprocess
from system_info import get_temperature
from oauth2client.service_account import ServiceAccountCredentials
GDOCS_OAUTH_JSON       = 'RPI_JSON_KEY.json' #Removed .json for security reasons
GDOCS_SPREADSHEET_NAME = 'digipunch'
def login_open_sheet(oauth_key_file, spreadsheet):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, 
                      scopes = ['https://spreadsheets.google.com/feeds',
                                'https://www.googleapis.com/auth/drive'])
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet. Check OAuth credentials, spreadsheet name, and')
        print('make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)
#print('Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')
worksheet = None
if worksheet is None:
    worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
dat = datetime.datetime.now()
id = sys.argv[1]
worksheet.update_cell(1,10,id)
time.sleep(0.5)
status = worksheet.cell(1,11).value
clock_in = 'Clocked in'
clock_out = 'Clocked out'
if status == 'Clocked in':
    status = clock_out
else:
    status = clock_in
try:
    worksheet.append_row((str(dat), id, status))
#        worksheet.append_row((dat, id, status))
# gspread==0.6.2
# https://github.com/burnash/gspread/issues/511
except:
    print('Append error, logging in again')
    worksheet = None
print('Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME))

