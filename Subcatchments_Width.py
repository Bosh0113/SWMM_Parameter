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
    arcpy.AddField_management(outputBoundary, "Area", "DOUBLE", "", "", "", "area", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(outputBoundary, "Perimeter", "DOUBLE", "", "", "", "perimeter", "NULLABLE", "NON_REQUIRED"
                              , "")
    arcpy.AddField_management(outputBoundary, "MaxEdge", "DOUBLE", "", "", "", "maxEdge", "NULLABLE", "NON_REQUIRED"
                              , "")
    # Calculate Area and Perimeter
    arcpy.CalculateField_management(outputBoundary, "Area",  "!shape.geodesicArea@METERS!", "PYTHON")
    arcpy.CalculateField_management(outputBoundary, "Perimeter",  "!shape.geodesicLength@METERS!", "PYTHON")
    # Calculate max edge
    expression = "(!Perimeter! + math.sqrt(math.pow(!Perimeter!, 2) - 16 * !Area!))/4"
    arcpy.CalculateField_management(outputBoundary, "MaxEdge",  expression, "PYTHON")
    # Execute AddField
    arcpy.AddField_management(outShpTempPath, "Width", "DOUBLE", "", "", "", "slope", "NULLABLE", "NON_REQUIRED", "")
    # Create a feature layer
    layerName = "tempShp"
    arcpy.MakeFeatureLayer_management(outShpTempPath, layerName)
    # Join the feature layer to a table
    arcpy.AddJoin_management(layerName, indexField, outputBoundary, indexField)
    # Calculate Area
    arcpy.CalculateField_management(layerName, "Width",  "!shape.geodesicArea@METERS!/!boundary.MaxEdge!", "PYTHON")
    # Remove the join
    arcpy.RemoveJoin_management(layerName, "boundary")
    # Copy the layer to a new permanent feature class
    arcpy.CopyFeatures_management(layerName, outShpPath)

    print "success"
except Exception as err:
    print err.args[0]
