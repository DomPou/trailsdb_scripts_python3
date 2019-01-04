import sys
sys.path.append("C:\\Trailsdb_Scripts\\Variables")
from Connection_to_trailsdb_ArcGIS_Pro import *

sys.path.append(functionsFolder)
from trailsdb_queries_table_last_changes import intersectionsTrailsDB_queries_v1


intersectionsTrailsDB_queries_v1()
print(done)