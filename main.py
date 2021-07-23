import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import base64
import json
import logging
import smtplib
import requests
from datetime import datetime

# opens the log file
with open('logs.json') as json_file:
    data_json = json.load(json_file)
#print(type(data_json))
# get the principleEmail
for data in data_json:
    print("--------------------------------------------------------------")
    principalEmail=data['protoPayload']['authenticationInfo']['principalEmail']
    #print("Principal Email:" , principalEmail)
    # get the project id
    project_id=data['resource']['labels']['project_id']
    #print("project id:", project_id)
    # get the email_id of the user
    email_id=data['resource']['labels']['email_id']
    #print("email id:", email_id)
    # get the details user email
    details = data['protoPayload']['authenticationInfo']['principalSubject']
    #print("details:",details)
    details= details.split(":")[1]
    print("created_by:",details)
    domain = details.split('@')[1]
    print("domain", domain)
    try:
        create_date= data['protoPayload']['response']['valid_after_time']['seconds']
        #print("create_date:",create_date)
        expiry_date = data['protoPayload']['response']['valid_before_time']['seconds']
        #print("expiry_date:", expiry_date)
        create_date_format = datetime.fromtimestamp(create_date).strftime('%Y-%m-%d %I:%M:%S %p')
        create_date_format = datetime.strptime(create_date_format,'%Y-%m-%d %I:%M:%S %p' )
        print("create date:", create_date_format )
        expiry_date_format = datetime.fromtimestamp(expiry_date).strftime('%Y-%m-%d %I:%M:%S %p')
        expiry_date_format = datetime.strptime(expiry_date_format,'%Y-%m-%d %I:%M:%S %p' )
        print("expiry_date:", expiry_date_format)
        check = 90
        now = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        now = datetime.strptime(now,'%Y-%m-%d %I:%M:%S %p' )
        #print("now:", now)
        #print(type(now))
        delta = (expiry_date_format - create_date_format).days
        #print(delta)
        delta1 = (now - create_date_format).days
        #print(delta1)

        if delta > 90:
            print("level1 check")
            print("reset service account key ")
        elif delta1 > 90:
            print("level2 check")
            print("reset service account key")
        else:
            print("service account key")
    except:
        print("cannot find service account key so skip")


    for project in project_id.split(","):
        for svc_email_id in email_id.split(","):
            print(project)
            print(svc_email_id)
    

        
