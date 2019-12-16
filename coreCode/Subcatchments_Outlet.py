import arcpy

# Input Path
inputPath = "D:/Temp/Test_ArcPy/Outlet/PreData/"
# Process Path
processPath = "D:/Temp/Test_ArcPy/Outlet/Process/"
# Output Path
outputPath = "D:/Temp/Test_ArcPy/Outlet/Result/"
# Input Data Path
inShpPath = inputPath + "subcatchments.shp"
inNodePath = inputPath + "junctions.shp"
# Index Field
indexField = "sOrder"
# Join Node
joinField = "node"
# Process Data Path
outShpTempPath = processPath + "subcaTemp.shp"
outJoinTempPath = processPath + "joined.shp"
# Output Data Path
outShpPath = outputPath + "subcatchments.shp"
try:
    # Execute CopyFeatures
    arcpy.CopyFeatures_management(inShpPath, outShpTempPath)
    # Run the Spatial Join tool, using the defaults for the join operation and join type
    arcpy.SpatialJoin_analysis(inShpPath, inNodePath, outJoinTempPath)
    # Execute AddField
    arcpy.AddField_management(outShpTempPath, "Outlet", "TEXT", "", "", "", "outlet", "NULLABLE", "NON_REQUIRED", "")
    # Create a feature layer
    layerName = "subcaShp"
    arcpy.MakeFeatureLayer_management(outShpTempPath, layerName)
    # Join the feature layer to a table
    arcpy.AddJoin_management(layerName, indexField, outJoinTempPath, indexField)
    # Calculate Slope
    arcpy.CalculateField_management(layerName, "Outlet",  "!joined." + joinField + "!", "PYTHON")
    # Remove the join
    arcpy.RemoveJoin_management(layerName, "joined")
    # Copy the layer to a new permanent feature class
    arcpy.CopyFeatures_management(layerName, outShpPath)

    print "success"
except Exception as err:
    print err.args[0]
