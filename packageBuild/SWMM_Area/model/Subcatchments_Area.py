import arcpy
import os


def getArea(input_data):
    # Output Path
    if not os.path.exists('Result'):
        os.makedirs('Result')
    # Output Data Path
    output = "./Result/subcatchments.shp"
    # Execute CopyFeatures
    arcpy.CopyFeatures_management(input_data, output)
    # Execute AddField
    arcpy.AddField_management(output, "Area", "DOUBLE", "", "", "", "area", "NULLABLE", "NON_REQUIRED", "")
    # Calculate Area
    arcpy.CalculateField_management(output, "Area",  "!shape.geodesicArea@HECTARES!", "PYTHON")
    return output


if __name__ == '__main__':
    getArea("./Data/subcatchments.shp")
