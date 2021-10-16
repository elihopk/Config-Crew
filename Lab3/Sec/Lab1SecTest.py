#!/usr/bin/python

import os
import sys
config = '/etc/httpd/conf/httpd.conf'

print("Testing Apache Policies")
if ( os.system('grep -i "ServerSignature Off" '+config+' > /dev/null' ) != 0 ) and ( os.system('grep -i "ServerTokens Prod" '+config+' > /dev/null')  != 0 ):
    print('WARNING: Apache Version Not Hidden')
    sys.exit()
if ( os.system('grep -i "Options FollowSymLinks" '+config+' > /dev/null' ) != 0 ):
    print('WARNING: Directory Listing not Disabled')
    sys.exit()    
if ( os.system('grep -i  "LimitRequestBody" '+config+' > /dev/null' ) != 0):
    print('WARNING: Request Body not Limited')
    sys.exit()
if ( os.system('grep -i "HttpOnly;Secure" '+config+' > /dev/null') !=0):
    print('WARNING: HTTP Only and Secure Flags not on')
    sys.exit()
if ( os.system('grep -A1 -i "RewriteCond" /var/www/html/.htaccess > /dev/null') !=0):
    print('WARNING: Methods not disabled')
    sys.exit()
if ( os.system('grep -i "FileETag None" /var/www/html/.htaccess > /dev/null') !=0):
    print('WARNING: e-tag not disabled')
    sys.exit
if ( os.system('grep -i "User Apache" ' +config+ ' > /dev/null') != 0):
    print('WARNING!  Apache not running under unpriveledged account Apache')
    sys.exit

#Modules Count - Will be counted and continued based off previous count
os.system('grep LoadModule /etc/httpd/conf.modules.d/00-base.conf > Modules.txt')
f = open('Modules.txt', 'r')
line = f.readline()
enabled = 0
disabled = 0
while line:
    if line.startswith( '#'):
        disabled += 1
    else:
        enabled += 1
    line = f.readline()

print('Enabled Modules:  '+ str(enabled))
print('Disabled Modules: '+str(disabled))

LAST_CHECK = 45

if(enabled > LAST_CHECK):
   print('MORE MODULES ARE ENABLED NOW THAN AT LAST CHECK')
   print('ENSURE YOUR SYSTEM IS SECURE')

# Check if all packages are up to date
if os.WEXITSTATUS(os.system('yum check-update &>/dev/null')) == 0:
   print('All packages are up to date')
else:
   print('WARNING: Not all packages are up to date')

# Use ab to show some data about the server under load
print('Starting benchmarking... Data is for 50000 requests with 1000 concurrently.')
os.system('ab -n 50000 -c 1000 -t 30 http://localhost/ | tail -n 10')

# Check for Opened Services in Firewall
print('Checking opened firewall services...')
services = os.popen('firewall-cmd --list-services').read().split()
badservice = False
for i in services:
   if i not in ['dhcpv6-client', 'http', 'https', 'ssh']:
      print('WARNING: Service ' + i + ' is open but should not be')
      badservice = True
      break

if not badservice:
   print('No bad services were enabled on the firewall')

