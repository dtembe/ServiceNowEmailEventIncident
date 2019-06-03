#!/usr/bin/env python3

'''
This is a script with a list of useful functions and snippets for sending events and emails to ServiceNow. This works as a standalone script but you need to code your own "stuff".
Dan Tembe
dtembe@yahoo.com
06/03/2019
'''


import json
import datetime
from datetime import timedelta
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import logging
import glob
import os
import smtplib, ssl

#Remove all old log files ( uncomment and add in log file path/name )
for f in glob.glob('/tmp/dt_script.log'):
    try:
        os.remove(f)
    except:
        pass

for f in glob.glob('/var/log/scriptlog.log'):
    try:
        os.remove(f)
    except:
        pass


#Global Vars -

# Useful vars (not needed but I like to keep these in my script in case I need to manipulate date/time in any of my functions
day = datetime.date.today()
daystring = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S-%f')
today = datetime.datetime.today().strftime('%Y-%m-%d')
minus5days = datetime.date.today() - timedelta(5)
todayminus5days = minus5days.strftime('%Y-%m-%d')
#comment it out later -
print('variables - Day: ' , day,  ' daystring:  ' , daystring ,  ' today: ' , today , '  minus5days: ' , minus5days , ' todayminus5days:  ' , todayminus5days , ' ' )


#Vars Used to Post Data to ServiceNow -
snowemurlevent = "https://instanceName.service-now.com/api/now/table/em_event"
snowurlincident = "https://instanceName.service-now.com/api/now/table/incident"
#Make sure the user has API access to SN Instance
snowemuser = "SNUserName"
snowempassword = "SNPassword"

# smtplib module send mail to be able to create an inbound action in SN. I am using gmail for testing
mailuser = "user@company.com"
mailpass = "emailPassword"
mailsmtp = 'smtp.gmail.com'
#make sure you are aware of the correct port. Gmail SSL is 587 for testing
mailport = '587'
TO = 'instanceName@service-now.com'

# Creating Logger Environment
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('/tmp/dt_script.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)
logger.info('\n')
logger.info('Starting Script')

#SSL Warnings Disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




###Start SN Incident Def - Standard Incident Workflow

'''
Priority calculation
Priority is calculated according to the following data lookup rules:

Data lookup rules
Impact	    Urgency	     Priority
1 - High	1 - High	1 - Critical
1 - High	2 - Medium	2 - High
1 - High	3 - Low	    3 - Moderate
2 - Medium	1 - High	2 - High
2 - Medium	2 - Medium	3 - Moderate
2 - Medium	3 - Low	    4 - Low
3 - Low	    1 - High	3 - Moderate
3 - Low	    2 - Medium	4 - Low
3 - Low	    3 - Low	    5 - Planning
By default, the Priority field is read-only and must be set by selecting the Impact and Urgency values. To change how priority is calculated, administrators can either alter the priority lookup rules or disable the Priority is managed by Data Lookup - set as read-only UI policy and create their own business logic.
'''


def SnCriticalIncident(caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, short_description, description):
    try:
        #jsonarray = l
        o_caller = (caller)
        o_category = (categoryList)
        o_subcategory = (subcategoryList)
        o_business_service = (businessServiceLookup)
        o_configuration_item = (cmdb_ciLookup)
        o_contact_type = (contact_typeList)
        o_state = (stateList)
        o_impact = ('1')  #this works
        o_urgency = ('1')
        o_assignment_group = (assignmentGroupLookup)
        o_assigned_to = (assigned_toLookup)
        o_short_description = (short_description)
        o_description = (description)
        print ("-" * 50)
        print (o_caller, o_category, o_subcategory, o_business_service, o_configuration_item, o_contact_type, o_state, o_impact, o_urgency, o_assignment_group, o_assigned_to, o_short_description, o_description )
        print ("-" * 50)
        data = {"caller_id": o_caller, "category": o_category, "subcategory": o_subcategory, "business_service": o_business_service, "cmdb_ci": o_configuration_item, "contact_type": o_contact_type, "state": o_state, "impact": o_impact, "urgency": o_urgency, "assignment_group": o_assignment_group, "assigned_to": o_assigned_to, "short_description": o_short_description, "description": o_description}
        postData = json.dumps(data)

        try:
            url = snowurlincident
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass

def SnModerateIncident(caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, short_description, description):
    try:
        #jsonarray = l
        o_caller = (caller)
        o_category = (categoryList)
        o_subcategory = (subcategoryList)
        o_business_service = (businessServiceLookup)
        o_configuration_item = (cmdb_ciLookup)
        o_contact_type = (contact_typeList)
        o_state = (stateList)
        o_impact = ('2')  #this works
        o_urgency = ('2')
        o_assignment_group = (assignmentGroupLookup)
        o_assigned_to = (assigned_toLookup)
        o_short_description = (short_description)
        o_description = (description)
        print ("-" * 50)
        print (o_caller, o_category, o_subcategory, o_business_service, o_configuration_item, o_contact_type, o_state, o_impact, o_urgency, o_assignment_group, o_assigned_to, o_short_description, o_description )
        print ("-" * 50)
        data = {"caller_id": o_caller, "category": o_category, "subcategory": o_subcategory, "business_service": o_business_service, "cmdb_ci": o_configuration_item, "contact_type": o_contact_type, "state": o_state, "impact": o_impact, "urgency": o_urgency, "assignment_group": o_assignment_group, "assigned_to": o_assigned_to, "short_description": o_short_description, "description": o_description}
        postData = json.dumps(data)

        try:
            url = snowurlincident
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass

def SnPlanningIncident(caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, short_description, description):
    try:
        #jsonarray = l
        o_caller = (caller)
        o_category = (categoryList)
        o_subcategory = (subcategoryList)
        o_business_service = (businessServiceLookup)
        o_configuration_item = (cmdb_ciLookup)
        o_contact_type = (contact_typeList)
        o_state = (stateList)
        o_impact = ('3')  #this works
        o_urgency = ('3')
        o_assignment_group = (assignmentGroupLookup)
        o_assigned_to = (assigned_toLookup)
        o_short_description = (short_description)
        o_description = (description)
        print ("-" * 50)
        print (o_caller, o_category, o_subcategory, o_business_service, o_configuration_item, o_contact_type, o_state, o_impact, o_urgency, o_assignment_group, o_assigned_to, o_short_description, o_description )
        print ("-" * 50)
        data = {"caller_id": o_caller, "category": o_category, "subcategory": o_subcategory, "business_service": o_business_service, "cmdb_ci": o_configuration_item, "contact_type": o_contact_type, "state": o_state, "impact": o_impact, "urgency": o_urgency, "assignment_group": o_assignment_group, "assigned_to": o_assigned_to, "short_description": o_short_description, "description": o_description}
        postData = json.dumps(data)

        try:
            url = snowurlincident
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass

### End SN Inc Def


###Start SN Event Def - Needs ITOM Module
# Custom Functions to post messages to SN em_event Table. This requires ITOM EMM enabled.
#
#
def SnCriticalEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        #jsonarray = l
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ('1')
        o_resource = (resource)
        o_description = ("Critical: On " + hostname + " Message: " + message)  #this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print ("-" * 50)
        print (o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class, o_additional_info)
        print ("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type, "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class, "description": o_description, "additional_info": o_additional_info}
        postData = json.dumps(data)

        try:
            url = snowemurlevent
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass

def SnMajorEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("2")
        o_resource = (resource)
        o_description = ("Major: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        postData = json.dumps(data)

        try:
            url = snowemurlevent
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass

def SnMinorEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("3")
        o_resource = (resource)
        o_description = ("Minor: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        postData = json.dumps(data)

        try:
            url = snowemurlevent
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass

def SnWarningEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("4")
        o_resource = (resource)
        o_description = ("Warning: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        postData = json.dumps(data)

        try:
            url = snowemurlevent
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass

def SnInfoEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("5")
        o_resource = (resource)
        o_description = ("Info: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        postData = json.dumps(data)

        try:
            url = snowemurlevent
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass

def SnClearEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("0")
        o_resource = (resource)
        o_description = ("Clear: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        postData = json.dumps(data)

        try:
            url = snowemurlevent
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth , data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            logger.error(e)
            pass
    except IOError as e:
        print(e)
        logger.error(e)
        pass


###End SN Event Def

### Start SN Email Def

def SnClearEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("0")
        o_resource = (resource)
        o_description = ("Clear: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        TEXT = json.dumps(data, indent=4, sort_keys=True)
        gmail_sender = mailuser
        gmail_passwd = mailpass
        SUBJECT = 'Monitoring Email - Clear'
        #TEXT = 'Here is a message from python.'
        mserver = smtplib.SMTP(mailsmtp, mailport)
        mserver.ehlo()
        mserver.starttls()
        mserver.login(gmail_sender, gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            mserver.sendmail(gmail_sender, [TO], BODY)
            logger.info('email sent')
            print('email sent')
        except:
            logger.error('error sending mail')
            print('error sending mail')
        mserver.quit()
    except IOError as e:
        logger.error("Error: ", e)
        print(e)
        pass


def SnCriticalEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("1")
        o_resource = (resource)
        o_description = ("Critical: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        TEXT = json.dumps(data, indent=4, sort_keys=True)
        gmail_sender = mailuser
        gmail_passwd = mailpass
        SUBJECT = 'Monitoring Email - Critical'
        #TEXT = 'Here is a message from python.'
        mserver = smtplib.SMTP(mailsmtp, mailport)
        mserver.ehlo()
        mserver.starttls()
        mserver.login(gmail_sender, gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            mserver.sendmail(gmail_sender, [TO], BODY)
            logger.info('email sent')
            print('email sent')
        except:
            logger.error('error sending mail')
            print('error sending mail')
        mserver.quit()
    except IOError as e:
        logger.error("Error: ", e)
        print(e)
        pass

def SnMajorEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("2")
        o_resource = (resource)
        o_description = ("Major: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        TEXT = json.dumps(data, indent=4, sort_keys=True)
        gmail_sender = mailuser
        gmail_passwd = mailpass
        SUBJECT = 'Monitoring Email - Major'
        #TEXT = 'Here is a message from python.'
        mserver = smtplib.SMTP(mailsmtp, mailport)
        mserver.ehlo()
        mserver.starttls()
        mserver.login(gmail_sender, gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            mserver.sendmail(gmail_sender, [TO], BODY)
            logger.info('email sent')
            print('email sent')
        except:
            logger.error('error sending mail')
            print('error sending mail')
        mserver.quit()
    except IOError as e:
        logger.error("Error: ", e)
        print(e)
        pass

def SnMinorEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("3")
        o_resource = (resource)
        o_description = ("Minor: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        TEXT = json.dumps(data, indent=4, sort_keys=True)
        gmail_sender = mailuser
        gmail_passwd = mailpass
        SUBJECT = 'Monitoring Email - Minor'
        #TEXT = 'Here is a message from python.'
        mserver = smtplib.SMTP(mailsmtp, mailport)
        mserver.ehlo()
        mserver.starttls()
        mserver.login(gmail_sender, gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            mserver.sendmail(gmail_sender, [TO], BODY)
            logger.info('email sent')
            print('email sent')
        except:
            logger.error('error sending mail')
            print('error sending mail')
        mserver.quit()
    except IOError as e:
        logger.error("Error: ", e)
        print(e)
        pass

def SnWarningEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("4")
        o_resource = (resource)
        o_description = ("Warning: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        TEXT = json.dumps(data, indent=4, sort_keys=True)
        gmail_sender = mailuser
        gmail_passwd = mailpass
        SUBJECT = 'Monitoring Email - Warning'
        #TEXT = 'Here is a message from python.'
        mserver = smtplib.SMTP(mailsmtp, mailport)
        mserver.ehlo()
        mserver.starttls()
        mserver.login(gmail_sender, gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            mserver.sendmail(gmail_sender, [TO], BODY)
            logger.info('email sent')
            print('email sent')
        except:
            logger.error('error sending mail')
            print('error sending mail')
        mserver.quit()
    except IOError as e:
        logger.error("Error: ", e)
        print(e)
        pass

def SnInfoEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info):
    try:
        o_source = (source)
        o_node = (hostname)
        o_metric_name = (metric_name)
        o_type = (sntype)
        o_message_key = (message_key)
        o_severity = ("5")
        o_resource = (resource)
        o_description = ("Info: On " + hostname + " Message: " + message)  # this works
        o_event_class = (event_class)
        o_additional_info = (additional_info)
        print("-" * 50)
        print(o_source, o_node, o_metric_name, o_type, o_message_key, o_severity, o_resource, o_description, o_event_class,
              o_additional_info)
        print("-" * 50)
        data = {"source": o_source, "node": o_node, "metric_name": o_metric_name, "type": o_type,
                "message_key": o_message_key, "severity": o_severity, "resource": o_resource, "event_class": o_event_class,
                "description": o_description, "additional_info": o_additional_info}
        TEXT = json.dumps(data, indent=4, sort_keys=True)
        gmail_sender = mailuser
        gmail_passwd = mailpass
        SUBJECT = 'Monitoring Email - Informational'
        #TEXT = 'Here is a message from python.'
        mserver = smtplib.SMTP(mailsmtp, mailport)
        mserver.ehlo()
        mserver.starttls()
        mserver.login(gmail_sender, gmail_passwd)

        BODY = '\r\n'.join(['To: %s' % TO,
                            'From: %s' % gmail_sender,
                            'Subject: %s' % SUBJECT,
                            '', TEXT])

        try:
            mserver.sendmail(gmail_sender, [TO], BODY)
            logger.info ('email sent')
            print('email sent')
        except:
            logger.error ('error sending mail')
            print('error sending mail')
        mserver.quit()
    except IOError as e:
        logger.error( "Error: ", e)
        print(e)
        pass

### End SN Email Def

##### For testing, creating static values to populate variables. Comment out.

#event&email -
hostname = 'test_hostname'
message = 'device failed'
source = 'test_source'
metric_name = 'test_metric_name'
sntype = 'test_type'
message_key = 'test_messageKey'
severity = '1'
resource = 'test_resource'
description =  'test_description'
event_class = 'test_eventClass'
additional_info = 'test_additionalInfo'
#Incidents -
caller = ''
categoryList = 'Network'
subcategoryList = 'Wireless'
businessServiceLookup = 'Sales Force Automation'
cmdb_ciLookup = ''
contact_typeList = 'PythonAPI'
stateList = ''
impact = ''
urgency = ''
assignmentGroupLookup = 'Incident Management'
assigned_toLookup = 'Incident Manager'
short_description = 'This is a short description from Python API'
####### End Static Values for variables.


#Test Function to post events, emails and incidents to ServiceNow. Comment out or delete the rest, and create your own main function.
##Testing purpose only
def main():
    try:
        #send email
        SnInfoEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description,event_class, additional_info)
        SnWarningEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnMinorEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnMajorEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnCriticalEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnClearEmail(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        logger.info("All Emails Sent to ServiceNow")
        print("All Emails Sent to ServiceNow")
    except IOError as e:
        logger.error(e)
        pass

    try:
        #Post event
        SnInfoEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnWarningEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnMinorEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnMajorEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnCriticalEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        SnClearEvent(hostname, message, source, metric_name, sntype, message_key, severity, resource, description, event_class, additional_info)
        logger.info("All SN Events POSTED")
        print("All SN Events POSTED")
    except IOError as e:
        logger.error(e)
        print(e)
        pass

    try:
        #Post Incident
        SnPlanningIncident(caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, short_description, description)
        SnModerateIncident(caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, short_description, description)
        SnCriticalIncident(caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, short_description, description)
        logger.info("All SN Incidents POSTED")
        print("All SN Incidents POSTED")
    except IOError as e:
        logger.error(e)
        print(e)
        pass
    finally:
        pass
    # endTry
###end main- Comment all of the abouve and create your own function.


if __name__ == "__main__":
    main()
