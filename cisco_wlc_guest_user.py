"""
This script create a wireless guest user for one day duration on a Cisco wireless lan controller
by using the LobbyAdmin account

"""

import requests
import string
import random
import os
import smtplib
import sys


#Variables passed as arguments
username = sys.argv[1]
password=sys.argv[2]
email_server=sys.argv[3]
wlc_ip = sys.argv[4]
url = 'https://'+wlc_ip

y = requests.get(url)
cook = y.headers["set-cookie"]
z = cook.split(";")
cooki = z[0]
cookies = dict(Cookie = cooki)

#Generate an 8-characters random user and password
chars = string.ascii_letters + string.digits
random.seed(os.urandom(1024))
user = ''.join(random.choice(chars) for i in range(8))
userpwd = user

#Connecting and authenticate to the WLC by using LobbyAdmin account and create wireless guest user
requests.get(url+'/screens/frameset.html',verify = False, auth = (username, password),  headers = {"Referer":"https://wlc_ip/screens/frameset.html","Cookie":"cooki"}) 
requests.get(url+'/screens/lobbyadmin_frameset.html', verify = False, auth = (username, password), headers = {"Referer":"https://wlc_ip/screens/frameset.html","Cookie":"cooki"})
requests.get(url+'/screens/lobbyAdminBanner.html', verify = False, auth = (username, password),headers = {"Referer":"https://wlc_ip/screens/lobbyAdminBanner.html","Cookie":"cooki"})
payload ={"access_control":1,"username":user,"userpwd":userpwd,"lifetime_days":1,"lifetime_hours":0,"lifetime_mins":0,"lifetime_secs":0,"GuestWlanID":3,"description":"This is a user created by script","err_flag":"","err_msg":"","buttonClicked":4}
requests.post(url+"/screens/aaa/guestuser_create.html", data = payload,  verify = False, auth = (username, password), headers = {"Referer":"https://wlc_ip/screens/aaa/guestuser_create.html","Cookie":"cooki"})

#Send an email with the user's credentials

HOST = email_server
SUBJECT = 'Wireless guest access credentials'
TO = destination_account  #  Set the destination account, it could be a group 
FROM = sender_account     #  Set the sender account (must have permission on the email server)

BODY = """From: sender_account
To: destination_account
MIME-Version: 1.0
Content-type: text/html
Subject: Wireless guest access credentials

    <span>Dear users, </span>
     <p>The guest user to be used during this week will be:</p>
       <td width="206" valign="top">
       <p>Username:&nbsp&nbsp <strong>%s</strong><br />Password:&nbsp&nbsp <strong> %s </strong> </p>
       </td>
       <td width="206" valign="top">
        </td>
          <p>Best regards.</p>
       </td>
   """ %(user,userpwd) 

server = smtplib.SMTP(HOST)
server.starttls()
server.sendmail(FROM, TO, BODY)

server.quit()

