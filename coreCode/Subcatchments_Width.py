import arcpy
import math

# Input Path
inputPath = "D:/Temp/Test_ArcPy/Width/PreData/"
# Process Path
processPath = "D:/Temp/Test_ArcPy/Width/Process/"
# Output Path
outputPath = "D:/Temp/Test_ArcPy/Width/Result/"
# Input Data Path
inShpPath = inputPath + "subcatchments.shp"
# Index Field
indexField = "sOrder"
# Process Data Path
outShpTempPath = processPath + "temp.shp"
outputBoundary = processPath + "boundary.shp"
# Output Data Path
outShpPath = outputPath + "subcatchments.shp"
try:
    # Execute CopyFeatures
    arcpy.CopyFeatures_management(inShpPath, outShpTempPath)
    # Use MinimumBoundingGeometry function to get a convex hull area
    arcpy.MinimumBoundingGeometry_management(outShpTempPath, outputBoundary, "RECTANGLE_BY_AREA", "NONE")
    # Execute AddField
    arcpy.AddField_management(outputBoundary, "MaxEdge", "DOUBLE", "", "", "", "maxEdge", "NULLABLE", "NON_REQUIRED"
                              , "")
    # Calculate Max Edge
    expression = "(!shape.geodesicLength@METERS! + math.sqrt(math.pow(!shape.geodesicLength@METERS!, 2) - 16 *" \
                 " !shape.geodesicArea@METERS!))/4"
    arcpy.CalculateField_management(outputBoundary, "MaxEdge",  expression, "PYTHON")
    # Execute AddField
    arcpy.AddField_management(outShpTempPath, "Width", "DOUBLE", "", "", "", "slope", "NULLABLE", "NON_REQUIRED", "")
    # Create a feature layer
    layerName = "tempShp"
    arcpy.MakeFeatureLayer_management(outShpTempPath, layerName)
    # Join the feature layer to a table
    arcpy.AddJoin_management(layerName, indexField, outputBoundary, indexField)
    # Calculate Width
    arcpy.CalculateField_management(layerName, "Width",  "!shape.geodesicArea@METERS!/!boundary.MaxEdge!", "PYTHON")
    # Remove the join
    arcpy.RemoveJoin_management(layerName, "boundary")
    # Copy the layer to a new permanent feature class
    arcpy.CopyFeatures_management(layerName, outShpPath)

    print "success"
except Exception as err:
    print err.args[0]
