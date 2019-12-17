import arcpy
from arcpy.sa import *
import os


def getSlope(inShpPath, inDEMPath, indexField):
    servicePath = os.path.abspath(os.path.join(inDEMPath, "../.."))
    # Process Path
    if not os.path.exists('Process'):
        os.makedirs('Process')
    processPath = servicePath + "\\Process\\"
    # Process Data Path
    outShpTempPath = processPath + "temp.shp"
    outSlopePath = processPath + "slope"
    outTablePath = processPath + "slopeMean.dbf"
    # Output Path
    if not os.path.exists('Result'):
        os.makedirs('Result')
    # Output Data Path
    outShpPath = servicePath + "\\Result\\subcatchments.shp"
    # Execute CopyFeatures
    arcpy.CopyFeatures_management(inShpPath, outShpTempPath)
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckExtension("Spatial")
    # Fill
    fillDEM = Fill(inDEMPath)
    # Slope
    outSlope = Slope(fillDEM, "DEGREE")
    outSlope.save(outSlopePath)
    # Set local variables
    zoneField = indexField
    # Execute ZonalStatisticsAsTable
    outSMean = ZonalStatisticsAsTable(outShpTempPath, zoneField, outSlope, outTablePath, "NODATA", "MEAN")
    # Execute AddField
    arcpy.AddField_management(outShpTempPath, "Slope", "DOUBLE", "", "", "", "slope", "NULLABLE", "NON_REQUIRED", "")
    # Create a feature layer
    layerName = "subcatchmentShp"
    arcpy.MakeFeatureLayer_management(outShpTempPath, layerName)
    # Join the feature layer to a table
    arcpy.AddJoin_management(layerName, indexField, outSMean, indexField)
    # Calculate Slope
    arcpy.CalculateField_management(layerName, "Slope",  "!slopeMean.MEAN!", "PYTHON")
    # Remove the join
    arcpy.RemoveJoin_management(layerName, "slopeMean")
    # Copy the layer to a new permanent feature class
    arcpy.CopyFeatures_management(layerName, outShpPath)
    return outShpPath


if __name__ == '__main__':
    getSlope("./Data/subcatchments.shp", "./Data/resareadem", "sOrder")
