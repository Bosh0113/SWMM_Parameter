import arcpy
import math
import os


def getWidth(inShpPath, indexField):
    # Process Path
    if not os.path.exists('Process'):
        os.makedirs('Process')
    processPath = "./Process/"
    # Process Data Path
    outShpTempPath = processPath + "temp.shp"
    outputBoundary = processPath + "boundary.shp"
    # Output Path
    if not os.path.exists('Result'):
        os.makedirs('Result')
    # Output Data Path
    outShpPath = "./Result/subcatchments.shp"
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
    return outShpPath


if __name__ == '__main__':
    getWidth("./Data/subcatchments.shp", "sOrder")
