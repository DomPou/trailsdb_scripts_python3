import sys, time
sys.path.append("C:\\Trailsdb_Scripts\\Variables")
from Connection_to_trailsdb_ArcGIS_Pro import *

sys.path.append(functionsFolder)
from trailsdb_queries_table_last_changes_v2 import intersectionsTrailsDB_queries_v2

start = time.time()

intersectionsTrailsDB_queries_v1()

stop = time.time()

print("Time to make trailsdb gdb = %02d:%02d:%02d" % (int(stop-start)/3600,int(((stop-start)%3600)/60),int((stop-start)%60)))