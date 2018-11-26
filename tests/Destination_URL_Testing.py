# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 12:10:40 2018

@author: mohammedsoukat
"""
# Base Code for Linked In API Authentication and Access
# https://requests-oauthlib.readthedocs.io/en/latest/examples/linkedin.html
import selenium
import webbrowser
import re
from urllib.parse import urlparse,parse_qs
import urllib
from urllib import parse
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import requests
#import ConfigParser as cp
#import urlparse


def parse_url(msg):
    url_l = re.findall("((https|http?:\/\/|[a-z]+\.[a-z]+)(?:[-\w.\/?=&:#]|(?:%[\da-fA-F]{2}))+)", msg)
    print ("Extracted URL:" ,url_l) 
    #(https|http:\/\/|[a-z]+\.\w+)(?:[-\w./?=&:#]|(?:%[\da-fA-F]{2}))+
    if url_l != []:
        url_t = url_l[0]  # list
        url = url_t[0]  # tuple
        print(url)
        print(msg)
        flag = url.find("cid=")
        if flag == -1:
            try:
                session = requests.Session()  # so connections are recycled
                resp = session.head(url, allow_redirects=True)
                dest_url = str(resp.url)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ " + str(dest_url))
                session.close()
            except:
                dest_url = None
                pass
        else:
            dest_url = str(url)
            
    else:
        dest_url = None

    return dest_url

def getcampaignattributes(campaign_id,headers):
    ad_analytics_api_url_campaign_desc = 'https://api.linkedin.com/v2/adCampaignsV2/{}'.format(campaign_id)
    r = requests.get(url = ad_analytics_api_url_campaign_desc, headers = headers)
    data = r.json()
    campaign_name = data['name']
    account_id = re.findall('\d+', data['account'])
    account_name = getaccountattributes(account_id[0],headers)
    print (campaign_name)
    print (account_name)
    
def getcreativeattributes(creative_id,headers):
    ad_analytics_api_url_creative_desc = 'https://api.linkedin.com/v2/adCreativesV2/{}'.format(creative_id)
    r = requests.get(url = ad_analytics_api_url_creative_desc, headers = headers)
    data = r.json()
    #creative_name = data['name']
    #print (creative_name)    
    

def getaccountattributes(account_id,headers):
    ad_analytics_api_url_account_desc = 'https://api.linkedin.com/v2/adAccountsV2/{}'.format(account_id)
    r = requests.get(url = ad_analytics_api_url_account_desc, headers = headers)
    data = r.json()
    account_name = data['name']
    #print (account_name)   
    return (account_name)

def get_cid(url):
    cid = re.findall('(cid=\w+)(?i)', url)
    print(cid)
    if cid != []:
        #print(cid[0])
        cid = cid[0].split('=')
        #print(cid[1])
        cid = cid[1]
    else:
        cid = None
    return cid

def getsharesdestinationurl(shares_url_id,headers):
    ad_analytics_api_url_creative_shares_url = 'https://api.linkedin.com/v2/shares/{}'.format(shares_url_id)
    r = requests.get(url = ad_analytics_api_url_creative_shares_url, headers = headers)
    data = r.json()
    bit_link_url_text = data['text']['text']
    bit_link_url_info = parse_url(bit_link_url_text)
    print ("=============================")
    print ("Destination URL: " ,bit_link_url_info )
    cid=""
    if bit_link_url_info :
        cid = get_cid(bit_link_url_info)
    else:
        cid=None
    print ("CID============" , cid)
    
def get_creatives_metrics(creative_id,headers):
    start = 0 
    ad_analytics_api_url_creative = 'https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&dateRange.start.month=11&dateRange.start.day=20&dateRange.start.year=2018&timeGranularity=DAILY&pivot=CREATIVE&creatives[0]=urn:li:sponsoredCreative:{}'.format(creative_id)      
    r = requests.get(url = ad_analytics_api_url_creative, headers = headers)
    data = r.json()
    ad_creative_elements_metrics_null_check = data['elements']
    if  ad_creative_elements_metrics_null_check:
        print ("Creatives Metrics Data ==========",data)
        print ("Likes =======:" , data['elements'][0]['clicks'])
        print ("Impressions =======:" , data['elements'][0]['impressions'])
        print ("Spent =======:" , data['elements'][0]['costInUsd'])

#    while(start >= 0):
#        ad_analytics_api_url_creative = 'https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&dateRange.start.month=11&dateRange.start.day=20&dateRange.start.year=2018&timeGranularity=DAILY&pivot=CREATIVE&creatives[0]=urn:li:sponsoredCreative:{}'.format(creative_id)      
#        r = requests.get(url = ad_analytics_api_url_creative, headers = headers)
#        data = r.json()d
#        print (data)
#        start=start+10
#        print ("===============================")
#        print ("start:" , start)
#        ad_creative_elements_metrics_null_check = data['elements']
#        print ("ad_creative_elements_metrics_null_check: ", ad_creative_elements_metrics_null_check)
#        if  ad_creative_elements_metrics_null_check:
#            print ("Creatives Metrics Data ==========",data)
#            print ("Likes =======:" , data['elements'][0]['clicks'])
#            print ("Impressions =======:" , data['elements'][0]['impressions'])
#            print ("Spent =======:" , data['elements'][0]['costInUsd'])
#            #continue
#        #start =-1
#        else:
#            start=-1
#            break
    
    #print ("Impressions =======:" , data['elements'][0]['impressions'])
    #print ("Shares =======:" , data['elements'][0]['costInUsd'])
    
#Initilization Parameters - Read from a JSON File
linkedin_paramters_file_path ="C:\Soukath\Projects\Digital Marketing\Linked In API Access\LinkedIn_Config_Parameters.json"
with open(linkedin_paramters_file_path) as read_file:
    linkedin_parameters = json.load(read_file)
#authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
authorization_base_url = linkedin_parameters['authorization_base_url']
#token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
token_url = linkedin_parameters['token_url']
#client_id = 'XXXXX'
#Get the Client ID for the application created in Linked In API My Apps 
client_id = linkedin_parameters['client_id']
#client_secret = 'XXXX'
#Get the Client Secret for the application created in Linked In API My Apps 
client_secret = linkedin_parameters['client_secret']
session_key = linkedin_parameters['session_key']
session_password = linkedin_parameters['session_password']
#print (linkedin_parameters['token_url'])

#Initialize the Headless Browser to Open a the linked In Web page Authorization URL and authenticate the username and password
options = Options()
#options.add_argument("--headless")
#options.set_headless(headless=True)
options.headless = True
# Create a Firefox Driver Session
driver = webdriver.Firefox(firefox_options=options)
#driver = webdriver.Firefox()

# Read secrets:
#Initialize the Linked In Session to get the Authorization URL
linkedin = OAuth2Session(client_id, redirect_uri='https://www.getpostman.com/oauth2/callback')
linkedin = linkedin_compliance_fix(linkedin)
authorization_url, state = linkedin.authorization_url(authorization_base_url)
start = 0 

# Open the Authorization URL in the Broswer
driver.get(authorization_url)
# Key in the Username and Password
id_box = driver.find_element_by_name('session_key')
id_box.send_keys(session_key)

id_password = driver.find_element_by_name('session_password')
id_password.send_keys(session_password)

#buttons = driver.find_elements_by_xpath(".//form//input[@type='button']")
# click on the Sign In Button
driver.find_element_by_name("signin").click()

try :
    driver.find_element_by_id("oauth__auth-form__submit-btn").click()
except NoSuchElementException :
    print ("Already Captured")
        #driver.find_element_by_id("oauth__auth-form__submit-btn").click()

#Get the Target URL for the browser and to get the Authorization Code
#https://developer.linkedin.com/docs/rest-api
#print (driver.current_url)

o = urlparse(driver.current_url)
#authorization_code = urlparse.parse_qs(urlparse.urlsplit(driver.current_url).query)['code']
#print (o)
#print (o.query)
#print (parse_qs(o.query))

#Get the Authorization Code
authorization_code = dict(parse.parse_qsl(parse.urlsplit(driver.current_url).query))

#print (dict(parse.parse_qsl(parse.urlsplit(driver.current_url).query)))

#print (authorization_code['code'])
#print (urlparse.urlsplit(o).query)
#driver.close()

#Pass the Authorization Token and get the access token
access_token = linkedin.fetch_token(token_url, client_secret=client_secret, authorization_response=driver.current_url)

print (access_token)

access_token1 = access_token['access_token']

# Use the API comments to get the required information
#r_xml = linkedin.get('https://api.linkedin.com/v2/me')
#r_xml = linkedin.get('https://api.linkedin.com/v2/audienceCountsV2?q=targetingCriteria&target.includedTargetingFacets.locations[0]=urn:li:country:ca&target.includedTargetingFacets.locations[1]=urn:li:country:us&target.excludingTargetingFacets.ageRanges[0]=AGE_55_PLUS')

#print (r_xml.content)

#r_json = linkedin.get('https://api.linkedin.com/v2/people/~?format=json')

#print (r_json.content)

headers={
'Host': 'api.linkedin.com'  ,
'Connection':'Keep-Alive',
'Authorization': 'Bearer {}'.format(access_token1)}

print (headers)

#api_url = 'https://api.linkedin.com/v1/people/~'

#api_url = 'https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&dateRange.start.month=10&dateRange.start.day=1&dateRange.start.year=2018&timeGranularity=MONTHLY&pivot=CAMPAIGN&accounts[0]=urn:li:sponsoredAccount:507668164,accounts[1]=urn:li:sponsoredAccount:507665849,accounts[2]=urn:li:sponsoredAccount:507666814,accounts[3]=urn:li:sponsoredAccount:504277221'
ad_analytics_api_url_campaign = 'https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&dateRange.start.month=5&dateRange.start.day=1&dateRange.start.year=2018&timeGranularity=MONTHLY&pivot=CAMPAIGN&campaigns[0]=urn:li:sponsoredCampaign:122565425'

ad_analytics_api_url_account = 'https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&dateRange.start.month=10&dateRange.start.day=1&dateRange.start.year=2018&timeGranularity=MONTHLY&pivot=ACCOUNT&accounts[0]=urn:li:sponsoredAccount:507668164'

ad_analytics_api_url_creative = 'https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&dateRange.start.month=5&dateRange.start.day=1&dateRange.start.year=2018&timeGranularity=MONTHLY&pivot=CREATIVE&creatives[0]=urn:li:sponsoredCreative:42168735'

ad_analytics_api_url_creative_desc = 'https://api.linkedin.com/v2/adCreativesV2/72713244'

ad_analytics_api_url_campaign_desc = 'https://api.linkedin.com/v2/adCampaignsV2/122565425'

ad_analytics_api_url_account_desc = 'https://api.linkedin.com/v2/adAccountsV2/507668164'

ad_analytics_api_url_all_accounts = 'https://api.linkedin.com/v2/adAccountsV2?q=search'

ad_analytics_api_url_all_campaigns = 'https://api.linkedin.com/v2/adCampaignsV2?q=search'

# Creatives using Pagination - Pagination
#https://docs.microsoft.com/en-us/linkedin/shared/api-guide/concepts/pagination?context=linkedin/marketing/context
#ad_analytics_api_url_all_creatives = 'https://api.linkedin.com/v2/adCreativesV2?q=search&start=0&count=10'


#Creatives using only selected fields - Field Projections
#https://docs.microsoft.com/en-us/linkedin/shared/api-guide/concepts/projections?context=linkedin/marketing/context
ad_analytics_api_url_all_creatives_projected_fields = 'https://api.linkedin.com/v2/adCreativesV2?q=search&start=10&count=10&fields=reference,campaign,variables'
#ad_analytics_api_url_all_creatives_projected_fields = 'https://api.linkedin.com/v2/adCreativesV2?q=search&start=10&count=10&fields=reference,campaign'

#Third Party Tracking Tags
ad_analytics_api_url_all_creatives_lnd_pg_url= 'https://api.linkedin.com/v2/thirdPartyTrackingTags?creative=urn:li:sponsoredCreative:42168735&q=creative&sortOrder=DESCENDING&totals=true'

# Shares API to get the bit link URL
ad_analytics_api_url_creative_shares_url = 'https://api.linkedin.com/v2/shares/6458422842659786753'

print ("API Data Execution")

print ("===================================================")





r = requests.get(url = ad_analytics_api_url_creative_desc, headers = headers)
data = r.json()
print (data)
#ad_creative_landing_page_url = data['elements'][0]['reference']
#ad_creative_campaign_id = data['elements'][0]['campaign']

#print ("Landing Page URL - ",ad_creative_landing_page_url)
#print ("Ad Creative Campaign ID - ",ad_creative_campaign_id)
#print (data)

try:
    r = requests.get(url = ad_analytics_api_url_creative_shares_url, headers = headers)
    r.raise_for_status()   
    data = r.json()
    print("===========================")
    print ("Shares URL")        
    print (data)
    print ("============================================")
    
    print ("Extract the Text from Shares API URL")

    print (data['text'])

    print (data['text']['text'])

    bit_link_url_text = data['text']['text']

    bit_link_url_info = parse_url(bit_link_url_text)

    print ("=============================")

    print ("Bit Link URL: " ,bit_link_url_info )
except requests.exceptions.HTTPError as err:
    print (err)


#print (r.content)

#print (r.headers)

#adaccount_url = 'https://api.linkedin.com/v2/adAccounts/504277221'

#data_adaccount = requests.get(url = adaccount_url, headers = headers)

#print (data_adaccount.json())

driver.close()
