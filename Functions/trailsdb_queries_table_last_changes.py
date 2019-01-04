import sys, arcpy

sys.path.append("C:\\Trailsdb_Scripts\\Variables")
from Connection_to_trailsdb_ArcGIS_Pro import *

sys.path.append(functionsFolder)
from trailsdb_queries_intersect_main_features_to_all_v1 import intersectMainFeaturesToAll_v1
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
intersectedFeaturesDict = intersectMainFeaturesToAll_v1(database_version)


#intersectedFeaturesDict = {'trail_code_reg': ['int_trail_code_snowshoeing_reg', 'int_trail_code_horseback_riding_reg', 'int_trail_code_environment_reg', 'int_trail_code_network_reg', 'int_trail_code_paddling_reg', 'int_trail_code_mountain_biking_reg', 'int_trail_code_regional_trail_reg', 'int_trail_code_signage_trail_reg', 'int_trail_code_dog_sledding_reg', 'int_trail_code_snowmobiling_reg', 'int_trail_code_fat_biking_reg', 'int_trail_code_local_trail_reg', 'int_trail_code_owner_reg', 'int_trail_code_operational_date_reg', 'int_trail_code_walking_reg', 'int_trail_code_rollerblading_reg', 'int_trail_code_gis_data_reg', 'int_trail_code_road_cycling_reg', 'int_trail_code_project_trail_reg', 'int_trail_code_atv_reg', 'int_trail_code_cross_country_skiing_reg', 'int_trail_code_category_reg', 'int_trail_code_trail_type_reg', 'int_trail_code_manager_reg'], 'project_trail_reg': ['int_project_trail_snowshoeing_reg', 'int_project_trail_horseback_riding_reg', 'int_project_trail_environment_reg', 'int_project_trail_network_reg', 'int_project_trail_paddling_reg', 'int_project_trail_mountain_biking_reg', 'int_project_trail_regional_trail_reg', 'int_project_trail_signage_trail_reg', 'int_project_trail_dog_sledding_reg', 'int_project_trail_snowmobiling_reg', 'int_project_trail_fat_biking_reg', 'int_project_trail_local_trail_reg', 'int_project_trail_owner_reg', 'int_project_trail_operational_date_reg', 'int_project_trail_walking_reg', 'int_project_trail_rollerblading_reg', 'int_project_trail_trail_code_reg', 'int_project_trail_gis_data_reg', 'int_project_trail_road_cycling_reg', 'int_project_trail_atv_reg', 'int_project_trail_cross_country_skiing_reg', 'int_project_trail_category_reg', 'int_project_trail_trail_type_reg', 'int_project_trail_manager_reg'], 'manager_reg': ['int_manager_snowshoeing_reg', 'int_manager_horseback_riding_reg', 'int_manager_environment_reg', 'int_manager_network_reg', 'int_manager_paddling_reg', 'int_manager_mountain_biking_reg', 'int_manager_regional_trail_reg', 'int_manager_signage_trail_reg', 'int_manager_dog_sledding_reg', 'int_manager_snowmobiling_reg', 'int_manager_fat_biking_reg', 'int_manager_local_trail_reg', 'int_manager_owner_reg', 'int_manager_operational_date_reg', 'int_manager_walking_reg', 'int_manager_rollerblading_reg', 'int_manager_trail_code_reg', 'int_manager_gis_data_reg', 'int_manager_road_cycling_reg', 'int_manager_project_trail_reg', 'int_manager_atv_reg', 'int_manager_cross_country_skiing_reg', 'int_manager_category_reg', 'int_manager_trail_type_reg'], 'owner_reg': ['int_owner_snowshoeing_reg', 'int_owner_horseback_riding_reg', 'int_owner_environment_reg', 'int_owner_network_reg', 'int_owner_paddling_reg', 'int_owner_mountain_biking_reg', 'int_owner_regional_trail_reg', 'int_owner_signage_trail_reg', 'int_owner_dog_sledding_reg', 'int_owner_snowmobiling_reg', 'int_owner_fat_biking_reg', 'int_owner_local_trail_reg', 'int_owner_operational_date_reg', 'int_owner_walking_reg', 'int_owner_rollerblading_reg', 'int_owner_trail_code_reg', 'int_owner_gis_data_reg', 'int_owner_road_cycling_reg', 'int_owner_project_trail_reg', 'int_owner_atv_reg', 'int_owner_cross_country_skiing_reg', 'int_owner_category_reg', 'int_owner_trail_type_reg', 'int_owner_manager_reg'], 'trail_code_pro': ['int_trail_code_atv_pro', 'int_trail_code_paddling_pro', 'int_trail_code_regional_trail_pro', 'int_trail_code_network_pro', 'int_trail_code_road_cycling_pro', 'int_trail_code_cross_country_skiing_pro', 'int_trail_code_walking_pro', 'int_trail_code_rollerblading_pro', 'int_trail_code_environment_pro', 'int_trail_code_local_trail_pro', 'int_trail_code_gis_data_pro', 'int_trail_code_project_trail_pro', 'int_trail_code_dog_sledding_pro', 'int_trail_code_mountain_biking_pro', 'int_trail_code_category_pro', 'int_trail_code_snowshoeing_pro', 'int_trail_code_manager_pro', 'int_trail_code_trail_type_pro', 'int_trail_code_owner_pro', 'int_trail_code_snowmobiling_pro', 'int_trail_code_fat_biking_pro', 'int_trail_code_horseback_riding_pro'], 'project_trail_pro': ['int_project_trail_atv_pro', 'int_project_trail_paddling_pro', 'int_project_trail_regional_trail_pro', 'int_project_trail_network_pro', 'int_project_trail_road_cycling_pro', 'int_project_trail_cross_country_skiing_pro', 'int_project_trail_walking_pro', 'int_project_trail_rollerblading_pro', 'int_project_trail_environment_pro', 'int_project_trail_local_trail_pro', 'int_project_trail_gis_data_pro', 'int_project_trail_dog_sledding_pro', 'int_project_trail_mountain_biking_pro', 'int_project_trail_category_pro', 'int_project_trail_snowshoeing_pro', 'int_project_trail_manager_pro', 'int_project_trail_trail_type_pro', 'int_project_trail_owner_pro', 'int_project_trail_trail_code_pro', 'int_project_trail_snowmobiling_pro', 'int_project_trail_fat_biking_pro', 'int_project_trail_horseback_riding_pro'], 'manager_pro': ['int_manager_atv_pro', 'int_manager_paddling_pro', 'int_manager_regional_trail_pro', 'int_manager_network_pro', 'int_manager_road_cycling_pro', 'int_manager_cross_country_skiing_pro', 'int_manager_walking_pro', 'int_manager_rollerblading_pro', 'int_manager_environment_pro', 'int_manager_local_trail_pro', 'int_manager_gis_data_pro', 'int_manager_project_trail_pro', 'int_manager_dog_sledding_pro', 'int_manager_mountain_biking_pro', 'int_manager_category_pro', 'int_manager_snowshoeing_pro', 'int_manager_trail_type_pro', 'int_manager_owner_pro', 'int_manager_trail_code_pro', 'int_manager_snowmobiling_pro', 'int_manager_fat_biking_pro', 'int_manager_horseback_riding_pro'], 'owner_pro': ['int_owner_atv_pro', 'int_owner_paddling_pro', 'int_owner_regional_trail_pro', 'int_owner_network_pro', 'int_owner_road_cycling_pro', 'int_owner_cross_country_skiing_pro', 'int_owner_walking_pro', 'int_owner_rollerblading_pro', 'int_owner_environment_pro', 'int_owner_local_trail_pro', 'int_owner_gis_data_pro', 'int_owner_project_trail_pro', 'int_owner_dog_sledding_pro', 'int_owner_mountain_biking_pro', 'int_owner_category_pro', 'int_owner_snowshoeing_pro', 'int_owner_manager_pro', 'int_owner_trail_type_pro', 'int_owner_trail_code_pro', 'int_owner_snowmobiling_pro', 'int_owner_fat_biking_pro', 'int_owner_horseback_riding_pro']}

def intersectionsTrailsDB_queries_v1():
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
				featurePath = gdbFeaturesRoot_queries + currentFeature
				if arcpy.Exists(featurePath):
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
					mainValuesLengthDict.update({row[0]: row[2]})
				if row[0] in mainValuesList:
					currentMaxDate = actualLastEditDatesDict.get(row[0])
					currentLength = mainValuesLengthDict.get(row[0])
					currentLength = currentLength + row[2]
					mainValuesLengthDict.update({row[0]: currentLength})
					if row[1] > currentMaxDate:
						actualLastEditDatesDict.update({row[0]: row[1]})

			# Get last edit dates from corresponding intersects from trailsdb_queries
			arcpy.env.workspace = gdbPath_queries + gdbName_queries + ".sde.basic_intersects"
			intersectFeatures = arcpy.ListFeatureClasses()

			for currentFeatureName in intersectFeatures:
				currentFeaturePath = gdbPath_queries + currentFeatureName
				if "int_" + currentMainFeature in currentFeatureName:
					if currentFeatureName[-3:] == status:
						for currentField in arcpy.ListFields(currentFeaturePath):
							if currentField.name in validationTableFieldsNames:
								intersectLastEditDateField = currentField.name
								for row in arcpy.da.SearchCursor(currentFeaturePath, [mainFieldIntersects, intersectLastEditDateField]):
									mainValue = row[0]
									lastEditDate = row[1]
									actualLastEditDatesDictKey = row[0] + intersectLastEditDateField
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

			# Intersection of needed feature classes
			for valueToIntersect in valuesToIntersectList:
				tempFeaturesToIntersectList = []
				intersectFeatureName = "int_" + valueToIntersect + "_" + status
				intersectFeaturePath = gdbPath_queries + currentOutputDataset + gdbName_queries + ".sde." + intersectFeatureName
				if arcpy.Exists(intersectFeaturePath):
					arcpy.Delete_management(intersectFeaturePath)
				# Create temporary features for intersect
				for currentFeatureToIntersect in intersectFeaturesList:
					currentFeatureToIntersectPath = gdbPath_queries + currentFeatureToIntersect
					currentTempFeature = tempEditingGdbPath + "\\" + currentFeatureToIntersect + valueToIntersect
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
							for row in arcpy.da.SearchCursor(currentTempFeature,"shape_Length"):
								currentLength = currentLength + row[0]
							if not currentLength < mainLength:
								tempFeaturesToIntersectList.append(currentTempFeature)
							if currentLength < mainLength:
								arcpy.Delete_management(currentTempFeature)
						if not "regional_trail" in currentTempFeature:
							tempFeaturesToIntersectList.append(currentTempFeature)
					if selectCount == 0:
						arcpy.Delete_management(currentTempFeature)
					arcpy.Delete_management("temp")
				# Make final intersect and add it to list of new features
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
			for intersectedValue in valuesToIntersectList:
				# Update existing rows
				if intersectedValue in validationTableMainValuesList:
					fieldCount2 = 1
					mainValueField = validationTableFieldsNames[0]
					whereClause = buildWhereClause(validationTablePath, mainValueField, intersectedValue)
					for row in arcpy.da.UpdateCursor(validationTablePath, validationTableFieldsNames, whereClause):
						row[0] = intersectedValue
						while fieldCount2 < len(validationTableFieldsNames):
							currentField = validationTableFieldsNames[fieldCount2]
							currentEditDate = actualLastEditDatesDict.get(intersectedValue + currentField)
							row[fieldCount2] = currentEditDate
							fieldCount2 += 1
						cursor.updateRow(row)
				# Insert new rows
				if not intersectedValue in validationTableMainValuesList:
					insertCursor = arcpy.da.InsertCursor(validationTablePath, validationTableFieldsNames)
					insertValues = [intersectedValue]
					fieldCount3 = 1
					while fieldCount3 < len(validationTableFieldsNames):
						currentField = validationTableFieldsNames[fieldCount3]
						currentEditDate = actualLastEditDatesDict.get(intersectedValue + currentField)
						insertValues.append(currentEditDate)
						fieldCount3 += 1
					insertCursor.insertRow(insertValues)