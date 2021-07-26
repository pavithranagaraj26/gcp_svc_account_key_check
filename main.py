import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from jinja2 import Environment, FileSystemLoader
import base64
import json
import logging
import smtplib
import datetime
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

with open('org_level_check.json') as json_file:
    data = json.load(json_file)
principalEmail=data['protoPayload']['authenticationInfo']['principalEmail']
#print(principalEmail)
project_id=data['resource']['labels']['project_id']
#print(project_id)
details = data['protoPayload']['serviceData']['policyDelta']['bindingDeltas']
#print(details)
user_details = [i['member'] for i in details]
#print(user_details)
email = "\r\n".join(user_details)
#print(email)
member_details = email.split(':')[0]
member_details_email = email.split(':')[1]
if member_details == 'serviceAccount':
    print("It is a service account")
    print (member_details_email)
# def list_key(service_account_email):

credentials = GoogleCredentials.get_application_default()
service = discovery.build('iam', 'v1', credentials=credentials)
key = service.projects().serviceAccounts().keys().list(name='projects/-/serviceAccounts/' + member_details_email").execute()
#key = service.projects().serviceAccounts().keys().list(name='projects/-/serviceAccounts/' + member_details_email, keyTypes="USER_MANAGED").execute()
#key = service.projects().serviceAccounts().keys().list(name='projects/-/serviceAccounts/' + member_details_email, keyTypes="SYSTEM_MANAGED").execute()
#pprint(key)

for ukey in key["keys"]:
    keyname = ukey['name'].split("/")[-1]
    validFrom = ukey['validAfterTime']
    validUntil = ukey['validBeforeTime']
    korigin = ukey['keyOrigin']
    ktype = ukey['keyType']
    print(f"Key_name:{keyname},\nValid_from:{validFrom},\nValid_until:{validUntil},\nKey_origin:{korigin},\nKey_type:{ktype}")

    timestringa = ukey['validAfterTime']
    timestringb = ukey['validBeforeTime'] 
    # Create datetime objects (now-createdate)
    d0 = datetime.datetime.strptime(timestringa, "%Y-%m-%dT%H:%M:%SZ")
    d1 = datetime.datetime.now() # Current time

    # Calculate timedelta (now-createdate)
    dt = d1 - d0

    # Create datetime objects (now-createdate)
    d2 = datetime.datetime.strptime(timestringb, "%Y-%m-%dT%H:%M:%SZ")
    #calculate the rotation period (validuntil - validfrom)
    de = d2 - d0
    rotation_age = de.days
    print(f'{member_details_email} roation_age:',rotation_age )
    passed_days = dt.days
    passed_seconds = dt.days # remaining seconds
    passed_microseconds = dt.microseconds # remaining microseconds
    total_seconds = dt.total_seconds()
    print(f'{member_details_email} keyage:',passed_days)
    
    if rotation_age > 90 :
        print("change the roation period to 90 days")
        if passed_days > 90: 
            print("compliant")       
    else:
        pass
