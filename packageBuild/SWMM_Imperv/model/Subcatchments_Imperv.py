import arcpy
from arcpy.sa import *
import json
import os


def getImperv(inShpPath, inlandUsePath, indexField, weights):
    # Process Path
    if not os.path.exists('Process'):
        os.makedirs('Process')
    processPath = "./Process/"
    # Process Data Path
    outShpTempPath = processPath + "subcaTemp.shp"
    outLandTempPath = processPath + "landTemp.shp"
    outLandRasterPath = processPath + "landUseRaster"
    outTablePath = processPath + "impervTable.dbf"
    # Output Path
    if not os.path.exists('Result'):
        os.makedirs('Result')
    # Output Data Path
    outShpPath = "./Result/subcatchments.shp"
    # Execute CopyFeatures
    arcpy.CopyFeatures_management(inShpPath, outShpTempPath)
    arcpy.CopyFeatures_management(inlandUsePath, outLandTempPath)
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckExtension("Spatial")
    arcpy.CheckOutExtension("Spatial")
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
    return outShpPath


if __name__ == '__main__':
    weights = {"A": 0.9, "B": 0.6, "C": 0.4, "D": 0.15}
    getImperv("./Data/subcatchments.shp", "./Data/landUse.shp", "sOrder", weights)
