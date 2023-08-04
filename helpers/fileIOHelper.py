import os
import json
import shutil

srcPath = "ReactIE_PDF_Conversion"

def outputDirtyJsonFile(xmlPath, output):
    outputFileName = xmlPath.split("/")[-1][:-4] + ".json"
    result_directory = srcPath + "/result/"
    if not os.path.exists(result_directory):
        os.mkdir(result_directory)
    outputFilePath = result_directory + outputFileName
    with open(outputFilePath, "w") as outfile:
        json.dump(output, outfile, indent=4, ensure_ascii=False)
    print("Step 2: Parsed PDF to JSON, written to:", outputFilePath)
    return outputFilePath

def outputCleanJsonFile(jsonPath, output):
    outputFileName = jsonPath.split("/")[-1][:-5] + ".json"
    result_directory = srcPath + "/../json/"
    if not os.path.exists(result_directory):
        os.mkdir(result_directory)
    outputFilePath = result_directory + outputFileName
    with open(outputFilePath, "w") as outfile:
        json.dump(output, outfile, indent=4, ensure_ascii=False)
    print("Step 3: Cleaned JSON file, written to:", outputFilePath)
    return outputFilePath

# given a path, make sure the path is valid (rename if needed)
# valid path is returned
def validateFilename(inputfile: str):
    newFilename = inputfile.replace(" ", "_").replace("(", "_").replace(")", "_")
    os.rename(inputfile, newFilename)
    return newFilename

# clear everything in the xml and result folder
def cleanFolders():
    
    xml_directory = srcPath + "/xmlFiles/"
    result_directory = srcPath + "/result/"
    final_result_directory = srcPath + "/filtered_result/"
    if os.path.exists(xml_directory):
        shutil.rmtree(xml_directory)
    if os.path.exists(result_directory):
        shutil.rmtree(result_directory)
    if os.path.exists(final_result_directory):
        shutil.rmtree(final_result_directory)
