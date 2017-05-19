#!/usr/bin/python
## -*- coding: utf-8 -*- 
#by ferz

import requests
#you need to install requests package
import time
import datetime
import threading
import subprocess
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

hts = {}
hts[000]="Timedout/Down"
hts[100]="Continue"
hts[101]="Switching Protocols"
hts[102]="Processing"
hts[200]="OK"
hts[201]="Created"
hts[202]="Accepted"
hts[203]="Non-Authoritative Information"
hts[204]="No Content"
hts[205]="Reset Content"
hts[206]="Partial Content"
hts[207]="Multi-Status"
hts[300]="Multiple Choices"
hts[301]="Moved Permanently"
hts[302]="Found"
hts[303]="See Other"
hts[304]="Not Modified"
hts[305]="Use Proxy"
hts[306]="Switch Proxy"
hts[307]="Temporary Redirect"
hts[400]="Bad Request"
hts[401]="Unauthorized"
hts[402]="Payment Required"
hts[403]="Forbidden"
hts[404]="Not Found"
hts[405]="Method Not Allowed"
hts[406]="Not Acceptable"
hts[407]="Proxy Authentication Required"
hts[408]="Request Timeout"
hts[409]="Conflict"
hts[410]="Gone"
hts[411]="Length Required"
hts[412]="Precondition Failed"
hts[413]="Request Entity Too Large"
hts[414]="Request-URI Too Long"
hts[415]="Unsupported Media Type"
hts[416]="Requested Range Not Satisfiable"
hts[417]="Expectation Failed"
hts[418]="Im a teapot"
hts[422]="Unprocessable Entity"
hts[423]="Locked"
hts[424]="Failed Dependency"
hts[425]="Unordered Collection"
hts[426]="Upgrade Required"
hts[449]="Retry With"
hts[450]="Blocked by Windows Parental Controls"
hts[500]="Internal Server Error"
hts[501]="Not Implemented"
hts[502]="Bad Gateway"
hts[503]="Service Unavailable"
hts[504]="Gateway Timeout"
hts[505]="HTTP Version Not Supported"
hts[506]="Variant Also Negotiates"
hts[507]="Insufficient Storage"
hts[509]="Bandwidth Limit Exceeded"
hts[510]="Not Extended"

hosts ={}
hosts["google"]="https://www.google.com/"
hosts["yahoo"]="https://www.yahoo.com/"

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'serveralerts pyscript',
    }
)


def serveralerts( key, value):
	global hosts,hts
	genarray = {}
	genarray[key]= {"sct":0}
	
	while True:
		time.sleep(1)
		try:
			resp = requests.head(value,timeout=(5,3),verify=True,headers=headers)
			#verify=False
			scode =  resp.status_code	
		except requests.exceptions.RequestException as e:
		    scode = 000	
		    # print e
		surl = value
		genarray[key]["sta"]= scode
		genarray[key]["url"]= surl
		timestamp = int(time.time())
		#exit(0)
		
		if(scode != 200 and genarray[key]["sct"] != 1):
			genarray[key]["cdt"]  =timestamp
			genarray[key]["ctd2"] =timestamp
			#print genarray[key]["url"]+": "+str(genarray[key]["sta"])+"---"+hts[genarray[key]["sta"]]
			msg = MIMEText(value+" is responded with status code :"+str(genarray[key]["sta"])+" with 5 seconds Conn timeout - fenix")
			msg["From"] = "from@gmail.com"
			msg["To"] = "to@gmail.com"
			msg["Subject"] = "󾭥 "+key+": "+str(genarray[key]["sta"])+" ("+hts[genarray[key]["sta"]]+")"
			p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
			p.communicate(msg.as_string())

			genarray[key]["chk"]=1
			genarray[key]["sct"]=1
		elif(scode == 200 and genarray[key]["sct"] == 1):
				genarray[key]["ctd1"]=timestamp
				tstamp1=genarray[key]["ctd1"]
				tstamp2=genarray[key]["ctd2"]

				if tstamp1 > tstamp2:
				    rd = tstamp1 - tstamp2
				else:
				    rd = tstamp2 - tstamp1

				if(rd <= 60):
					genarray[key]["ctres"]=str(rd) + "second(s)"
				else:
					genarray[key]["ctres"]=str(rd/60) + "min(s)"

				msg = MIMEText(value+" is responded with status code :"+str(genarray[key]["sta"])+" with 5 seconds Conn timeout - fenix")
				msg["From"] = "from@gmail.com"
				msg["To"] = "to@gmail.com"
				msg["Subject"] = "󾭦 "+key+"is UP :"+str(genarray[key]["sta"])+" ("+hts[genarray[key]["sta"]]+") ("+genarray[key]["ctres"]+")"
				p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
				p.communicate(msg.as_string())
				
				#print surl+": "+str(genarray[key]["sta"])+"-"+genarray[key]["ctres"]
				genarray[key]["sct"]=0
				genarray[key]["ctd2"]=""
				genarray[key]["ctres"]=""


		
a1=threading.Thread(name='goog',target=serveralerts,args=("google","https://www.google.com/"))
a1.daemon = True
a1.start()
a2=threading.Thread(name='yaho',target=serveralerts,args=("yahoo","https://www.yahoo.com"))
a2.daemon = True
a2.start()

while True:
    time.sleep(1)
