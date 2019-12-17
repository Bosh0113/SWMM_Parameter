from modelservicecontext import EModelContextStatus
from modelservicecontext import ERequestResponseDataFlag
from modelservicecontext import ERequestResponseDataMIME
from modelservicecontext import ModelServiceContext
from modeldatahandler import ModelDataHandler
import xml.etree.ElementTree as ET
from zip_utils import zip_dirs
from zip_utils import unzip_dir
import Subcatchments_Slope
import sys
import os

# Begin
if len(sys.argv) < 4:
    exit()

ms = ModelServiceContext()
ms.onInitialize(sys.argv[1], sys.argv[2], sys.argv[3])
mdh = ModelDataHandler(ms)

# create instance folder
instance_dir = ms.getModelInstanceDirectory()
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)
instance_event1 = instance_dir + "event1_data"
if not os.path.exists(instance_event1):
    os.makedirs(instance_event1)
instance_event2 = instance_dir + "event2_data"
if not os.path.exists(instance_event2):
    os.makedirs(instance_event2)

# parameters
shp_file_path = ""
dem_file_path = ""
indexField = ""

# Enter State
ms.onEnterState('SubcatchmentsInput')

# Event - input data
ms.onFireEvent('subcatchment_input')

ms.onRequestData()

data_subcatchment_input = None
if ms.getRequestDataFlag() == ERequestResponseDataFlag.ERDF_OK:
    # input data is zip
    if ms.getRequestDataMIME() == ERequestResponseDataMIME.ERDM_ZIP_FILE:
        # get input data
        data_subcatchment_input = ms.getRequestDataBody()
        unzip_dir(data_subcatchment_input, instance_event1)
        for root, dirs, files in os.walk(instance_event1):
            for file in files:
                filename = os.path.splitext(file)
                if filename[len(filename) - 1] == '.shp':
                    shp_file_path = root + '\\' + file
    else:
        print("Input shapefile failed!")
        ms.onFinalize()
else:
    ms.onFinalize()
# Event - input data
ms.onFireEvent('dem_input')

ms.onRequestData()

data_dem_input = None
if ms.getRequestDataFlag() == ERequestResponseDataFlag.ERDF_OK:
    if ms.getRequestDataMIME() == ERequestResponseDataMIME.ERDM_ZIP_FILE:
        # get input data
        data_dem_input = ms.getRequestDataBody()
        unzip_dir(data_dem_input, instance_event2)
        files = os.listdir(instance_event2)
        for file in files:
            filename = os.path.splitext(file)
            if filename[len(filename) - 1] == '.xml':
                fileTitle = file.split(".")[0]
                dem_file_path = instance_event2 + '\\' + fileTitle
    else:
        print("Input DEM failed!")
        ms.onFinalize()
else:
    ms.onFinalize()

# Event - input data
ms.onFireEvent('parameter_input')

ms.onRequestData()

data_parameter_input = None
if ms.getRequestDataFlag() == ERequestResponseDataFlag.ERDF_OK:
    # input data is in UDX format
    if ms.getRequestDataMIME() == ERequestResponseDataMIME.ERDM_XML_FILE:
        # get input data
        rank_tree = ET.ElementTree()
        rank_tree.parse(ms.getRequestDataBody())
        value_node_list = rank_tree.findall("XDO")
        indexField = value_node_list[0].attrib['value']
    # input data is in other formats
    else:
        print("Input parameters failed!")
        ms.onFinalize()
else:
    ms.onFinalize()

# Leave State
ms.onLeaveState()

# Run model
os.chdir(os.path.dirname(instance_dir))
Subcatchments_Slope.getSlope(shp_file_path, dem_file_path, indexField)

# Enter State
ms.onEnterState('ResultOutput')

# Event - output
ms.onFireEvent('subcatchment_output')
result_path = os.path.join(instance_dir, "Result")
result_zip_path = os.path.join(instance_dir, "Result.zip")
if not os.path.exists(result_path):
    print("Model error!")
    ms.onFinalize()
zip_dirs([result_path], result_zip_path)


ms.setResponseDataFlag(ERequestResponseDataFlag.ERDF_OK)

# Set output format,ERequestResponseDataMIME is the enumeration class of output format
ms.setResponseDataMIME(ERequestResponseDataMIME.ERDM_RAW_FILE)

# Set output path,output_path is the path of output data
ms.setResponseDataBody(result_zip_path)

ms.onResponseData()

# Leave State
ms.onLeaveState()

ms.onFinalize()
