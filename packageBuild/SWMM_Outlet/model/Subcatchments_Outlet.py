import arcpy
import os


def getOutlet(inShpPath, inNodePath, indexField, joinField):
    # Process Path
    if not os.path.exists('Process'):
        os.makedirs('Process')
    processPath = "./Process/"
    # Process Data Path
    outShpTempPath = processPath + "subcaTemp.shp"
    outJoinTempPath = processPath + "joined.shp"
    # Output Path
    if not os.path.exists('Result'):
        os.makedirs('Result')
    # Output Data Path
    outShpPath = "./Result/subcatchments.shp"
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
    return outShpPath


if __name__ == '__main__':
    getOutlet("./Data/subcatchments.shp", "./Data/junctions.shp", "sOrder", "node")
