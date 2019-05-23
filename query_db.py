#!/usr/bin/env python

import con_db
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def pushdt(arga, arg_1, arg_2, arg_3, arg_4, arg_5, arg_6, arg_7, arg_8):
    conn=con_db.mkcodb()
    try:
        cursor=conn.cursor()
        sql="INSERT INTO "+arga+" (des_num, cha_uuid, cal_num, cal_context, cal_note_1, cal_note_2, cal_note_3, status)"
        sql+=" VALUES ('"+arg_1+"','"+arg_2+"','"+arg_3+"','"+arg_4+"','"+arg_5+"','"+arg_6+"','"+arg_7+"','"+arg_8+"');"
        act=cursor.execute(sql,)
        conn.commit()
        return act
    except:
        conn.close()

def updatedt(arga,arg_1,arg_2,arg_3):
    conn=con_db.mkcodb()
    try:
        cursor=conn.cursor()
        sql="UPDATE "+arga+" SET agent_8_tdea = (%s), agent_10_thup = '"+arg_2+"', agent_9_thgu = now()"
        sql+=" WHERE agent_col5 = '"+arg_3+"';"
        act=cursor.execute(sql,[arg_1])
        conn.commit()
        return act
    except:
        conn.close()

def getdtcy(arga,argb,argc,argd):
    conn=con_db.mkcodb()
    smtp=[]
    try:
        cursor=conn.cursor()
        sql="SELECT "+arga+" from "+argb
        sql+=" where "+argc+"='"+argd+"';"
        cursor.execute(sql)
        row = cursor.fetchone()
        smtp.append(row[0])
        for row in cursor:
            smtp.append(row[0])
        return smtp
    except:
        conn.close()
def getdtcn(arga,argb):
    conn=con_db.mkcodb()
    sim=[]
    try:
        cursor=conn.cursor()
        sql="SELECT "+arga+" from "+argb+";"
        cursor.execute(sql)
        row = cursor.fetchone()
        sim.append(row[0])
        for row in cursor:
            sim.append(row[0])
        return sim
    except:
        conn.close()        