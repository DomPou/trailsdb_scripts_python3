import sys, arcpy

sys.path.append("C:\\Trailsdb_Scripts\\Variables")
from Connection_to_trailsdb_ArcGIS_Pro import *

sys.path.append(functionsFolder)
from trailsdb_queries_PairwiseIntersect_Two_Feature_Classes_v1 import intersectFeatureClassesFromTrailsdb_returnName_v1


#Trailsdb
statusList = ["reg","pro"]
mainFeatureList = ["trail_code","project_trail","manager","owner"]
#mainFeatureList = ["trail_code"]
datasetsDict = {"reg":["registered_info"],"pro":["proposed_info","proposed_signage_info"]}
mainFeaturesIntersectToDict = {}


def intersectMainFeaturesToAll_v1(database_version):
	'''Intersect main features to all others in trailsdb_queries and return dictionary {main features:[intersected features]}'''

	# General Variables
	gdbVariables = trailsdb_or_tests(database_version)
	gdbPath = gdbVariables[1]
	gdbFeaturesRoot = gdbVariables[2]

	outDataset = "basic_intersects"

	# Registered or proposed
	for status in statusList:
		currentDatasetsList = datasetsDict.get(status)
		# Main feature to intersect everything to
		for currentMainFeature in mainFeatureList:
			intersectFeaturesList = []
			# Feature containing the main code for the final intersect
			mainFeatureName = "fc_" + currentMainFeature + "_" + status

			for currentDataset in currentDatasetsList:
				arcpy.env.workspace = gdbPath + currentDataset + "\\"
				# List all line features in proper dataset other than the main feature
				for featureWithRoot in arcpy.ListFeatureClasses():
					if not mainFeatureName in featureWithRoot:
						if arcpy.Describe(featureWithRoot).shapeType == "Polyline":
							pathLength = len(gdbFeaturesRoot)
							featurePath = gdbPath + featureWithRoot
							featureName = featurePath[pathLength:]
							intersectFeatureName = intersectFeatureClassesFromTrailsdb_returnName_v1(mainFeatureName, outDataset, featureName, database_version)

							#if featureName[:3] == "fc_":
							#	intersectFeatureName = "trailsdb_queries.sde.int_" + currentMainFeature + "_" + featureName[3:]
							#if featureName[:7] == "fc_act_":
							#		intersectFeatureName = "trailsdb_queries.sde.int_" + currentMainFeature + "_" + featureName[7:]

							intersectFeaturesList.append(intersectFeatureName)

			mainFeaturesIntersectToDict.update({currentMainFeature + "_" + status:intersectFeaturesList})

	#print(mainFeaturesIntersectToDict)
	return mainFeaturesIntersectToDict

#intersectMainFeaturesToAll_v1("trailsdb")