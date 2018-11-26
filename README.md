This project is used to get the LinkedIn API data related to AdsReporting API's using python 2 & 3 versions. We need to request LinkedIn Team to grant privileges to access the AdsReporting API.This uses OAuth 2.0 authentication to further fetch the AdsReporting metrics. We need to create a application API and ask LinkedIn Team to grant the privileges to application API.
The python code uses application Client ID and Client Secret Key & linked in username and password to acquire the authorization code. We use authorization code to further access the AdReporting metrics. We may need to install few packages for the python code to run successfully.

We need to install the below python packages.

pip install selenium

pip install requests_oauthlib

Please make sure Firefox is installed in the linux machine. The python code uses firefox browser for authentication purposes. However the code can be modified for chrome as well. Please make sure geckodriver is downloaded in any path for the firefox to work properly.  The suggested path is bin folder. The path of the geckodriver needs to be provided in the python code. The version that is used in the code is geckodriver-v0.17.0-linux64.tar. This can be downloaded from https://github.com/mozilla/geckodriver/releases/tag/v0.17.0


Make the linked_in_api_main.sh as executable file under bin folder

chmod 755 linked_in_api_main

The file can be executed by running the below command.

bin/linked_in_api_main.sh LinkedIn_Config_Parameters.json outfile.csv 


The LinkedIn_Config_Parameters.json contains the Client ID, Client Secret Key , LinkedIn Username and password configuration paramaters. Please modify these paramters accordingly.


There is another python code(src/linked_in_api_mechanical_soup.py) which can used to fetch the AdsReporting metrics which does not use selenium package instead it uses mechanicalsoup package.For this python code to work please install the below package

pip install mechanicalsoup

Make the linked_in_api_main_mechanical_soup as executable file under bin folder

chmod 755 linked_in_api_main_mechanical_soup

please use the below command to execute the python code.

bin/linked_in_api_main_mechanical_soup.sh LinkedIn_Config_Parameters.json outfile.csv

