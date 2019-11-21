# Confidential!!!
# Access to our airtable database
my_url_API = "https://api.airtable.com/v0/URLXXXX"
my_token_TOKEN = "Bearer KEYXXXX"

# Importing libraries
import sys
import requests
import pandas as pd

# Python and Airtable - API connection
fetch = True
URL_BASE = my_url_API
TOKEN = my_token_TOKEN
PARAMS = {'Authorization':TOKEN}
offset = ''
result = []
while(fetch):
    url = URL_BASE + '?offset=' + offset
    r = requests.get(url = url, headers = PARAMS)
    data = r.json()
    for reg in data['records']:
        result.append(reg)
    if 'offset' in data:
        offset = data['offset']
    else:
        fetch = False

#Converting airtable data into a dataframe
df = pd.DataFrame(result)
df = pd.DataFrame(df['fields'])
df = df['fields'].apply(pd.Series)
