import re
import urlparse
import json
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
#from linkedin import linkedin
import requests
import urllib
import urllib2
import webbrowser
from bs4 import BeautifulSoup
import mechanicalsoup
from urlparse import urlparse
import requests

#Read LinkedIn Parameters File
linkedin_paramters_file_path ='/root/LinkedIn_API_Access/bin/LinkedIn_Config_Parameters.json'
with open(linkedin_paramters_file_path) as read_file:
    linkedin_parameters = json.load(read_file)

#Parameters Initialization
#authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
authorization_base_url =  linkedin_parameters['authorization_base_url']
#token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
token_url = linkedin_parameters['token_url']
#client_id = '81czqzwkuv00m2'
client_id  = linkedin_parameters['client_id']
#client_secret = '1taiQYu9VS91GrOF'
client_secret = linkedin_parameters['client_secret']
session_key = linkedin_parameters['session_key']
session_password = linkedin_parameters['session_password']
#print (data_json)
#config = cp.ConfigParser()
#config.read(cfg_file)
#if not config.has_section('Secrets'):
 #   raise RuntimeError('no secrets specified')
#secrets = {}
#for s in config.items('Secrets'):
#    secrets[s[0]] = s[1]

#LinkedIn OAuth2.0 Session
linkedin = OAuth2Session(client_id, redirect_uri='https://www.getpostman.com/oauth2/callback')
linkedin = linkedin_compliance_fix(linkedin)
authorization_url, state = linkedin.authorization_url(authorization_base_url)

# Open the Browser using Mechanical Soup to validate the Username and Password for Authentication
browser = mechanicalsoup.StatefulBrowser()
browser.open(authorization_url)
#print ("Browser URL 1 " , browser.get_url())
browser.select_form("form[action=https://www.linkedin.com/uas/login-submit]")
browser['session_key'] = session_key
browser['session_password'] = session_password
browser.submit_selected()
#print ("Page2", browser.get_url())
urlparse(browser.get_url())
#print ("URL Parse" , urlparse(browser.get_url()))
access_token = linkedin.fetch_token(token_url, client_secret=client_secret, authorization_response=browser.get_url())
print (access_token)

print (access_token)

access_token1 = access_token['access_token']

headers={
'Host': 'api.linkedin.com'  ,
'Connection':'Keep-Alive',
'Authorization': 'Bearer {}'.format(access_token1)}

print (headers)

api_url = 'https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&dateRange.start.month=10&dateRange.start.day=1&dateRange.start.year=2018&timeGranularity=MONTHLY&pivot=CAMPAIGN&accounts[0]=urn:li:sponsoredAccount:504277221'

r = requests.get(url = api_url, headers = headers)

data = r.json()

print (data)
#r_xml = linkedin.get('https://api.linkedin.com/v1/people/~')
#r_xml = linkedin.get('https://api.linkedin.com/v2/dmpSegments')
#print (r_xml.content)

#r_json = linkedin.get('https://api.linkedin.com/v1/people/~?format=json')

#print (r_json.content)

