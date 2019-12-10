import arcpy
from arcpy.sa import *
import json

# Input Path
inputPath = "D:/Temp/Test_ArcPy/Imperv/PreData/"
# Process Path
processPath = "D:/Temp/Test_ArcPy/Imperv/Process/"
# Output Path
outputPath = "D:/Temp/Test_ArcPy/Imperv/Result/"
# Input Data Path
inShpPath = inputPath + "subcatchments.shp"
inlandUsePath = inputPath + "landUse.shp"
# Index Field
indexField = "sOrder"
# Parameters Category + Runoff
weights = {"A": 0.9, "B": 0.6, "C": 0.4, "D": 0.15}
# Process Data Path
outShpTempPath = processPath + "subcaTemp.shp"
outLandTempPath = processPath + "landTemp.shp"
outLandRasterPath = processPath + "landUseRaster"
outTablePath = processPath + "impervTable.dbf"
# Output Data Path
outShpPath = outputPath + "subcatchments.shp"
try:
    # Execute CopyFeatures
    arcpy.CopyFeatures_management(inShpPath, outShpTempPath)
    arcpy.CopyFeatures_management(inlandUsePath, outLandTempPath)
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckExtension("Spatial")
    # Execute AddField
    arcpy.AddField_management(outLandTempPath, "Weight", "DOUBLE", "", "", "", "weight", "NULLABLE", "NON_REQUIRED", "")
    # Calculate Weight
    codeBlock = """
def getWeight(type, weights):
    return weights[type]"""
    expression = "getWeight( !category! ," + json.dumps(weights) + ")"
    arcpy.CalculateField_management(outLandTempPath, "Weight",  expression, "PYTHON", codeBlock)
    # Execute FeatureToRaster
    arcpy.FeatureToRaster_conversion(outLandTempPath, "Weight", outLandRasterPath, 5)
    # Execute ZonalStatisticsAsTable
    outImperv = ZonalStatisticsAsTable(outShpTempPath, indexField, outLandRasterPath, outTablePath, "NODATA", "MEAN")
    # Execute AddField
    arcpy.AddField_management(outShpTempPath, "Imperv", "DOUBLE", "", "", "", "imperv", "NULLABLE", "NON_REQUIRED", "")
    # Create a feature layer
    layerName = "subcaShp"
    arcpy.MakeFeatureLayer_management(outShpTempPath, layerName)
    # Join the feature layer to a table
    arcpy.AddJoin_management(layerName, indexField, outImperv, indexField)
    # Calculate Slope
    arcpy.CalculateField_management(layerName, "Imperv",  "!impervTable.MEAN!", "PYTHON")
    # Remove the join
    arcpy.RemoveJoin_management(layerName, "impervTable")
    # Copy the layer to a new permanent feature class
    arcpy.CopyFeatures_management(layerName, outShpPath)
    print "success"
except Exception as err:
    print err.args[0]
