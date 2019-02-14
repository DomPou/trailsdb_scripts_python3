import sys, arcpy

sys.path.append("C:\\Trailsdb_Scripts\\Variables")
from Connection_to_trailsdb_ArcGIS_Pro import *

sys.path.append(functionsFolder)
from Build_SQL_Where_Clause import *

tableName = "trailsdb_queries.sde.trail_code_last_edits_reg"
tablePath = gdbPath_queries + tableName

if arcpy.Exists(tablePath):
	fieldPositionDict = {}
	count = 0
	for field in arcpy.ListFields(tablePath):
		name = field.name
		position = count
		fieldPositionDict.update({name:position})
		count += 1
