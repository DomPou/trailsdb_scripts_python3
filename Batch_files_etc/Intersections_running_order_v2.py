import sys, time, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sys.path.append("C:\\Trailsdb_Scripts\\Variables")
from Connection_to_trailsdb_ArcGIS_Pro import *
from GIS_email_variables import *

sys.path.append(functionsFolder)
from trailsdb_queries_table_last_changes_v2 import intersectionsTrailsDB_queries_v2

def trailsdbScriptSuccess(scriptName, scriptTime):

	msg = MIMEMultipart()
	subject = "Trailsdb script completed - " + scriptName
	body = """
""" + scriptName + """ completed without errors in """ + scriptTime + """
	"""

	msg['From'] = gisAddress
	msg['To'] = trailsdbErrorsAddress
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain', "utf-8"))
	text=msg.as_string()
	# Send the message via our SMTP server
	server = smtplib.SMTP('smtp.office365.com', 587)
	server.ehlo()
	server.starttls()
	server.login(gisAddress, gisPassword)
	server.sendmail(gisAddress, trailsdbErrorsAddress, text)
	server.quit()

start = time.time()

intersectionsTrailsDB_queries_v2()

stop = time.time()

runTime = "%02d:%02d:%02d" % (int(stop-start)/3600,int(((stop-start)%3600)/60),int((stop-start)%60))

trailsdbScriptSuccess("intersectionsTrailsDB_queries_v2", runTime)