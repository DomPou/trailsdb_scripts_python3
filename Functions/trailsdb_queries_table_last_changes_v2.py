import sys, arcpy

sys.path.append("C:\\Trailsdb_Scripts\\Variables")
from Connection_to_trailsdb_ArcGIS_Pro import *

sys.path.append(functionsFolder)
from trailsdb_queries_intersect_main_features_to_all_v2 import intersectMainFeaturesToAll_v2
from Build_SQL_Where_Clause import *

# General Variables
# database_version = trailsdb or trailsdb_tests
database_version = "trailsdb"
gdbVariables = trailsdb_or_tests(database_version)
gdbName = gdbVariables[0]
gdbPath = gdbVariables[1]
gdbFeaturesRoot = gdbVariables[2]
statusList = ["reg","pro"]

# trailsdb
trailsdbFeatureDict = {"trail_code": "trail_code", "project_trail": "project_code", "manager": "salesforceid_manager", "owner": "salesforceid_owner"}

# trailsdb_queries
mainFeatureList = ["trail_code", "project_trail", "manager", "owner"]
mainFieldsIntersectsDict = {"trail_code": "trail_trail_code", "project_trail": "proje_project_code", "manager": "manag_salesforceid_manager", "owner": "owner_salesforceid_owner"}
mainFieldsValidationTableDict = {"trail_code": ["trail_code", "TEXT", 4], "project_trail": ["project_code", "LONG", 10], "manager": ["salesforceid_manager", "TEXT", 18], "owner": ["salesforceid_owner", "TEXT", 18]}

def intersectionsTrailsDB_queries_v2():

	intersectedFeaturesDict = intersectMainFeaturesToAll_v2(database_version)

	for status in statusList:
		for currentMainFeature in mainFeatureList:
			# Variables
			# trailsdb
			trailsdbFeatureName = "fc_" + currentMainFeature + "_" + status
			trailsdbFeaturePath = gdbFeaturesRoot + trailsdbFeatureName
			trailsdbFeatureMainFields = [trailsdbFeatureDict.get(currentMainFeature),"last_edited_date","st_length(shape)"]

			# trailsdb_queries
			validationTableName = currentMainFeature + "_last_edits_" + status
			validationTablePath = gdbFeaturesRoot_queries + validationTableName
			mainFieldIntersects = mainFieldsIntersectsDict.get(currentMainFeature)
			mainFieldValidationTableVariables = mainFieldsValidationTableDict.get(currentMainFeature)
			mainFieldValidationTableName = mainFieldValidationTableVariables[0]
			mainFieldValidationTableType = mainFieldValidationTableVariables[1]
			mainFieldValidationTableLength = mainFieldValidationTableVariables[2]
			mainLastEditsName = mainFieldValidationTableName[:5] + "_last_edited_date"
			currentLastEditsFieldsDict = {validationTableName: [mainLastEditsName]}
			validationTableFieldsNames = [mainFieldValidationTableName, mainLastEditsName]
			intersectFeaturesList = intersectedFeaturesDict.get(currentMainFeature + "_" + status)


			newIntersectedFeaturesList = []

			# Validation values lists and dicts
			mainValuesList = []
			mainValuesLengthDict = {}
			actualLastEditDatesDict = {}
			validationTableMainValuesList = []
			validationTableLastEditDatesDict = {}
			valuesToIntersectList = []

			# Export dataset
			currentOutputDataset = currentMainFeature + "_" + status + "\\"

			# Operations
			# 1 - Make sure the validation table and main fields exist and check if table contains all main values form trailsdb
			if not arcpy.Exists(validationTablePath):
				arcpy.CreateTable_management(gdbPath_queries, validationTableName)
			# Get existing fields in validation table
			existingFields = []
			for field in arcpy.ListFields(validationTablePath):
				existingFields.append(field.name)
			# Check for main field in trailsdb
			if not mainFieldValidationTableName in existingFields:
				arcpy.AddField_management(validationTablePath, mainFieldValidationTableName, mainFieldValidationTableType, "", "", mainFieldValidationTableLength)
			# Check for last edit date field in trailsdb
			if not mainLastEditsName in existingFields:
				arcpy.AddField_management(validationTablePath, mainLastEditsName, "DATE")
			# Check for last edit date fields in trailsdb_queries
			for currentFeature in intersectFeaturesList:
				featurePath = "in_memory\\" + currentFeature
				if arcpy.Exists(featurePath):
					#print("fuck yeah")
					for currentField in arcpy.ListFields(featurePath):
						if "last_edit" in currentField.name:
							if not currentField.name in existingFields:
								arcpy.AddField_management(validationTablePath, currentField.name, "DATE")
							if not currentField.name in validationTableFieldsNames:
								validationTableFieldsNames.append(currentField.name)

			# Get main values and their last edit date from trailsdb
			trailsdbSearchCursor = arcpy.da.SearchCursor(trailsdbFeaturePath, trailsdbFeatureMainFields)
			for row in trailsdbSearchCursor:
				if not row[0] in mainValuesList:
					mainValuesList.append(row[0])
					actualLastEditDatesDict.update({row[0]: row[1]})
					mainValuesLengthDict.update({str(row[0]) + currentMainFeature: row[2]})
				if row[0] in mainValuesList:
					currentMaxDate = actualLastEditDatesDict.get(row[0])
					currentLength = mainValuesLengthDict.get(row[0])
					if not currentLength is None:
						currentLength = currentLength + row[2]
					if currentLength is None:
						currentLength = row[2]
					mainValuesLengthDict.update({row[0]: currentLength})
					if row[1] > currentMaxDate:
						actualLastEditDatesDict.update({str(row[0]) + currentMainFeature: row[1]})
						#print(actualLastEditDatesDict)

			# Get last edit dates from corresponding intersects from trailsdb_queries
			arcpy.env.workspace = "in_memory"
			intersectFeatures = arcpy.ListFeatureClasses()

			for currentFeatureName in intersectFeatures:
				currentFeaturePath = "in_memory\\" + currentFeatureName
				if "int_" + currentMainFeature in currentFeatureName:
					#print("Still fuck yeah")
					if currentFeatureName[-3:] == status:
						for currentField in arcpy.ListFields(currentFeaturePath):
							if currentField.name in validationTableFieldsNames:
								intersectLastEditDateField = currentField.name
								for row in arcpy.da.SearchCursor(currentFeaturePath, [mainFieldIntersects, intersectLastEditDateField]):
									mainValue = row[0]
									lastEditDate = row[1]
									# Ignore when mainValue is none (an error that will be reported in another script)
									if not mainValue is None:
										actualLastEditDatesDictKey = mainValue + intersectLastEditDateField
										currentLastEditDate = actualLastEditDatesDict.get(actualLastEditDatesDictKey)
										if not currentLastEditDate is None:
											if lastEditDate > currentLastEditDate:
												actualLastEditDatesDict.update({actualLastEditDatesDictKey:lastEditDate})
										if currentLastEditDate is None:
											actualLastEditDatesDict.update({actualLastEditDatesDictKey: lastEditDate})

			# Check last edits dates in validation table
			for row in arcpy.da.SearchCursor(validationTablePath, validationTableFieldsNames):
				numberOfFields = len(validationTableFieldsNames)
				fieldCount = 1
				currentValidationTableMainValue = row[0]
				if not currentValidationTableMainValue in validationTableMainValuesList:
					validationTableMainValuesList.append(currentValidationTableMainValue)

				while fieldCount < numberOfFields:
					trailsdbDate = actualLastEditDatesDict.get(
						currentValidationTableMainValue + validationTableFieldsNames[fieldCount])
					validationTableDate = row[fieldCount]
					if not validationTableDate == trailsdbDate:
						if not currentValidationTableMainValue in valuesToIntersectList:
							valuesToIntersectList.append(currentValidationTableMainValue)
					fieldCount += 1

			# Intersects in currentOutputDataset value that are missing or were updated
			for currentMainValue in mainValuesList:
				if not currentMainValue in validationTableMainValuesList:
					if not currentMainValue in valuesToIntersectList:
						valuesToIntersectList.append(currentMainValue)
			print(valuesToIntersectList)

			# Intersection of needed feature classes
			for valueToIntersect in valuesToIntersectList:
				# Ignore None value related to error in the database because another tool identify these daily
				if not valueToIntersect is None:
					print(valueToIntersect)
					tempFeaturesToIntersectList = []
					intersectFeatureName = "int_" + valueToIntersect + "_" + status
					intersectFeaturePath = gdbPath_queries + currentOutputDataset + gdbName_queries + ".sde." + intersectFeatureName
					if arcpy.Exists(intersectFeaturePath):
						arcpy.Delete_management(intersectFeaturePath)
					# Create temporary features for intersect
					for currentFeatureToIntersect in intersectFeaturesList:
						currentFeatureToIntersectPath = "in_memory\\" + currentFeatureToIntersect
						currentTempFeature = "in_memory\\" + currentFeatureToIntersect + valueToIntersect
						if arcpy.Exists("temp"):
							arcpy.Delete_management("temp")
						if arcpy.Exists(currentTempFeature):
							arcpy.Delete_management(currentTempFeature)
						whereClause = buildWhereClause(currentFeatureToIntersectPath, mainFieldIntersects, valueToIntersect)
						arcpy.MakeFeatureLayer_management(currentFeatureToIntersectPath, "temp")
						arcpy.SelectLayerByAttribute_management("temp", "NEW_SELECTION", whereClause)
						arcpy.CopyFeatures_management("temp", currentTempFeature)
						selectCount = int(arcpy.GetCount_management(currentTempFeature).getOutput(0))
						# Remove empty feature classes, keep others
						if not selectCount == 0:
							# Regional trail might not cover the whole main value, remove if so
							if "regional_trail" in currentTempFeature:
								# Get length for current main value
								mainLength = mainValuesLengthDict.get(valueToIntersect)
								# Get length for regional trail
								currentLength = 0.0
								for row in arcpy.da.SearchCursor(currentTempFeature,"SHAPE@LENGTH"):
									currentLength = currentLength + row[0]
									#print(currentLength)
								if not currentLength < mainLength:
									tempFeaturesToIntersectList.append(currentTempFeature)
								if currentLength < mainLength:
									arcpy.Delete_management(currentTempFeature)
							if not "regional_trail" in currentTempFeature:
								tempFeaturesToIntersectList.append(currentTempFeature)
						if selectCount == 0:
							arcpy.Delete_management(currentTempFeature)
						arcpy.Delete_management("temp")
						#print(tempFeaturesToIntersectList)

					# Make final intersect and add it to list of new features
					#print(intersectFeaturePath)
					arcpy.Intersect_analysis(tempFeaturesToIntersectList, intersectFeaturePath,"NO_FID")
					newIntersectedFeaturesList.append(intersectFeaturePath)
					# Removes useless fields and renames the main one to be like in the validation table
					for field in arcpy.ListFields(intersectFeaturePath):
						# Removes duplicate of mainFieldIntersects
						if field.name == mainFieldIntersects:
								arcpy.AlterField_management(intersectFeaturePath, field.name, mainFieldValidationTableName, mainFieldValidationTableName)
						if not field.name == mainFieldIntersects:
							if field.aliasName == mainFieldIntersects:
								try:
									arcpy.DeleteField_management(intersectFeaturePath, field.name)
								except:
									print("essential field, cannot delete")
					# Deletes temporary features
					for tempFeature in tempFeaturesToIntersectList:
						if arcpy.Exists(tempFeature):
							arcpy.Delete_management(tempFeature)

			# Add or replace values from new intersections to validation table
			# Get field position for rows
			fieldPositionDict = {}
			fieldCount2 = 0
			for field in arcpy.ListFields(validationTablePath):
				name = field.name
				position = fieldCount2
				fieldPositionDict.update({position: name})
				fieldCount2 += 1
			for intersectedValue in valuesToIntersectList:
				# Update existing rows
				if intersectedValue in validationTableMainValuesList:
					mainValueField = validationTableFieldsNames[0]
					whereClause = buildWhereClause(validationTablePath, mainValueField, intersectedValue)
					updateCursor = arcpy.da.UpdateCursor(validationTablePath, validationTableFieldsNames, whereClause)
					fieldCount3 = 1
					for row in updateCursor:
						row[0] = intersectedValue
						while fieldCount3 < len(validationTableFieldsNames):
							currentField = fieldPositionDict.get(fieldCount3)
							currentEditDate = actualLastEditDatesDict.get(intersectedValue + currentField)
							row[fieldCount3] = currentEditDate
							fieldCount3 += 1
							updateCursor.updateRow(row)
				# Insert new rows
				if not intersectedValue in validationTableMainValuesList:
					insertCursor = arcpy.da.InsertCursor(validationTablePath, validationTableFieldsNames)
					insertValues = [intersectedValue]
					fieldCount4 = 1
					while fieldCount4 < len(validationTableFieldsNames):
						print(actualLastEditDatesDict)
						print(fieldPositionDict)
						print(fieldCount4)
						currentField = fieldPositionDict.get(fieldCount4)
						currentEditDate = actualLastEditDatesDict.get(intersectedValue + currentField)
						insertValues.append(currentEditDate)
						fieldCount4 += 1
					insertCursor.insertRow(insertValues)