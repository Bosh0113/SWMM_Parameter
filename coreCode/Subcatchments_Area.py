import arcpy

# Input Path
inputPath = "D:/Temp/Test_ArcPy/Area/PreData/"
# Output Path
outputPath = "D:/Temp/Test_ArcPy/Area/Result/"
# Input Data Path
inPath = inputPath + "subcatchments.shp"
# Output Data Path
outPath = outputPath + "subcatchments.shp"
try:
    # Execute CopyFeatures
    arcpy.CopyFeatures_management(inPath, outPath)
    # Execute AddField
    arcpy.AddField_management(outPath, "Area", "DOUBLE", "", "", "", "area", "NULLABLE", "NON_REQUIRED", "")
    # Calculate Area
    arcpy.CalculateField_management(outPath, "Area",  "!shape.geodesicArea@HECTARES!", "PYTHON")

    print "success"
except Exception as err:
    print err.args[0]
