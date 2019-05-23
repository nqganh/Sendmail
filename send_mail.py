"""
    detect answer call
        send mail with content: Customer phone number <9562153625> assigned to Robert Zimmer(who pickup the call)
   detect miss call
        send mail with content: Customer phone number <9562153625> is unanswered
    send to avmd
    send message
"""
import os
import sys
import string
import random
import ESL as ESL
import datetime
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import con_db
import query_db

"""
    setttings values 
"""
ESL_HOST='127.0.0.1'
ESL_PORT='8021'
ESL_USER='ClueCon'

import syslog

c = ESL.ESLconnection(ESL_HOST, ESL_PORT, ESL_USER)

if c.connected:
    syslog.syslog(syslog.LOG_DEBUG, "EVENT_HANDLE.PY - Start Event Handler")
    c.events("plain", "all")
    while c.connected:
        e = c.recvEvent()
        if e:
            ev_name = e.getHeader('Event-Name')
            va_ev_name = e.getHeader('variable_Event-Name')
            ev_name = str(ev_name)
            ca_context = e.getHeader('Caller-Context')
            smtp = query_db.getdtcy("default_setting_value","v_default_settings","default_setting_category","email")
#            print ev_name
            if ev_name == 'HEARTBEAT':
                syslog.syslog(syslog.LOG_DEBUG, ev_name)
            if ev_name == 'CHANNEL_CREATE' and va_ev_name == 'REQUEST_PARAMS' and ca_context == 'pbx.optionwide.com':
                des_numb_chcreate = e.getHeader("Caller-Destination-Number")
                cal_numb_chcreate = e.getHeader("Caller-Caller-ID-Number")
                cha_uuid_chcreate = e.getHeader('Channel-Call-UUID')
                un_uuid_chcreate = e.getHeader('Unique-ID')
                cal_context_chcreate = e.getHeader('Caller-Context')
# check destination number in call
                calcen_extensions = query_db.getdtcn("queue_extension","v_call_center_queues")
                destination_ib = query_db.getdtcy("destination_data", "v_destinations", "destination_number", des_numb_chcreate)

                if des_numb_chcreate in calcen_extensions:
                    #push_internal = query_db.pushdt('agentac_callcentercurrent', des_numb_chcreate, cha_uuid_chcreate, cal_numb_chcreate, cal_context_chcreate, un_uuid_chcreate, '', '', 'start')
                    status_temp = ""
            if ('CHANNEL_BRIDGE' in ev_name):
                des_numb_bridge = e.getHeader("Caller-Destination-Number")
                cal_numb_bridge = e.getHeader("Caller-Caller-ID-Number")
                cha_uuid_bridgea = e.getHeader('Channel-Call-UUID')
                cha_uuid_bridgeb = e.getHeader('Bridge-B-Unique-ID')
                des_numb_final = e.getHeader("Caller-Callee-ID-Number")
                var_sip = e.getHeader('variable_sip_to_user')
                calcen_extensions = query_db.getdtcn("queue_extension","v_call_center_queues")
# check destination number in call
                if des_numb_bridge in calcen_extensions:
                    calcen_email = query_db.getdtcy("queue_email","v_call_center_queues","queue_extension", des_numb_bridge)
                    calcen_name = query_db.getdtcy("queue_name","v_call_center_queues","queue_extension", des_numb_bridge)
                    calcen_des = query_db.getdtcy("queue_description","v_call_center_queues","queue_extension", des_numb_bridge)
                    extens_des = query_db.getdtcy("description","v_extensions","extension", des_numb_final)
                    if calcen_email[0] != None:
                        server = smtplib.SMTP(str(smtp[2]),int(smtp[5]))
                        server.ehlo()
                        server.starttls()
                        server.ehlo()
                        server.login(str(smtp[4]),str(smtp[8]))
                        fromaddr = smtp[4]
                        toaddr = calcen_email[0]
                        msg = MIMEMultipart()
                        msg['From'] = fromaddr
                        msg['To'] = toaddr
                        if calcen_des[0] != None:
                            msg['Subject'] = "Call-centers "+str(calcen_name[0]) + " " + str(calcen_des[0]) + " "# + des_numb_bridge
                            if var_sip == None:
                                msg['Subject'] = msg['Subject'] + des_numb_bridge
                            else:
                                msg['Subject'] = msg['Subject'] + var_sip
                        if calcen_des[0] == None:
                            msg['Subject'] = "Call-centers "+str(calcen_name[0]) + " "# + des_numb_bridge
                            if var_sip == None:
                                msg['Subject'] = msg['Subject'] + des_numb_bridge
                            else:
                                msg['Subject'] = msg['Subject'] + var_sip
                        # Customer phone number <9562153625> assigned to Robert Zimmer
                        if extens_des[0] != None:
                            body = "Customer phone number <"+ cal_numb_bridge + "> assigned to " + str(extens_des[0])
                        else:
                            body = "Customer phone number <"+ cal_numb_bridge + "> assigned to " + des_numb_final
                        msg.attach(MIMEText(body, 'plain'))
                        text = msg.as_string()
                        server.sendmail(fromaddr, toaddr.split(','), text)
#               # print e.serialize()
            if ('PLAYBACK_STOP' in ev_name):
                des_numb_bridge = e.getHeader("Caller-Destination-Number")
                cal_numb_bridge = e.getHeader("Caller-Caller-ID-Number")
                cha_uuid_bridgea = e.getHeader('Channel-Call-UUID')
                des_numb_final = e.getHeader("Caller-Callee-ID-Number")
                var_sip = e.getHeader('variable_sip_to_user')
                calcen_extensions = query_db.getdtcn("queue_extension","v_call_center_queues")
# check destination number in call
                if des_numb_bridge in calcen_extensions:
                    calcen_email = query_db.getdtcy("queue_email","v_call_center_queues","queue_extension", des_numb_bridge)
                    calcen_name = query_db.getdtcy("queue_name","v_call_center_queues","queue_extension", des_numb_bridge)
                    calcen_des = query_db.getdtcy("queue_description","v_call_center_queues","queue_extension", des_numb_bridge)
                    if des_numb_final is None:
                        if calcen_email[0] != None:
                            server = smtplib.SMTP(str(smtp[2]),int(smtp[5]))
                            server.ehlo()
                            server.starttls()
                            server.ehlo()
                            server.login(str(smtp[4]),str(smtp[8]))
                            fromaddr = smtp[4]
                            toaddr = calcen_email[0]
                            msg = MIMEMultipart()
                            msg['From'] = fromaddr
                            msg['To'] = toaddr
                            if calcen_des[0] != None:
                                msg['Subject'] = "Call-centers "+str(calcen_name[0]) + " " + str(calcen_des[0]) + " "# + des_numb_bridge
                                if var_sip == None:
                                    msg['Subject'] = msg['Subject'] + des_numb_bridge
                                else:
                                    msg['Subject'] = msg['Subject'] + var_sip
                            if calcen_des[0] == None:
                                msg['Subject'] = "Call-centers "+str(calcen_name[0]) + " " + des_numb_bridge
                                if var_sip == None:
                                    msg['Subject'] = msg['Subject'] + des_numb_bridge
                                else:
                                    msg['Subject'] = msg['Subject'] + var_sip
                            # send mail with conten: Customer phone number <9562153625> is unanswered
                            body = "Customer phone number <"+ cal_numb_bridge + "> is unanswered"
                            msg.attach(MIMEText(body, 'plain'))
                            text = msg.as_string()
