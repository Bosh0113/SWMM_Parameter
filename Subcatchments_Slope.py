import arcpy
from arcpy.sa import *

# Input Path
inputPath = "D:/Temp/Test_ArcPy/Slope/PreData/"
# Process Path
processPath = "D:/Temp/Test_ArcPy/Slope/Process/"
# Output Path
outputPath = "D:/Temp/Test_ArcPy/Slope/Result/"
# Input Data Path
inShpPath = inputPath + "subcatchments.shp"
inDEMPath = inputPath + "resareadem"
# Index Field
indexField = "sOrder"
# Process Data Path
outShpTempPath = processPath + "temp.shp"
outSlopePath = processPath + "slope"
outTablePath = processPath + "slopeMean.dbf"
# Output Data Path
outShpPath = outputPath + "subcatchments.shp"
try:
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
    arcpy.AddField_management(inShpPath, "Slope", "DOUBLE", "", "", "", "slope", "NULLABLE", "NON_REQUIRED", "")
    # Create a feature layer
    layerName = "subcatchmentShp"
    arcpy.MakeFeatureLayer_management(inShpPath, layerName)
    # Join the feature layer to a table
    arcpy.AddJoin_management(layerName, indexField, outSMean, indexField)
    # Calculate Slope
    arcpy.CalculateField_management(layerName, "Slope",  "!slopeMean.MEAN!", "PYTHON")
    # Remove the join
    arcpy.RemoveJoin_management(layerName, "slopeMean")
    # Copy the layer to a new permanent feature class
    arcpy.CopyFeatures_management(layerName, outShpPath)

    print "success"
except Exception as err:
    print err.args[0]
