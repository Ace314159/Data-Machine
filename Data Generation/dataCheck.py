import csv


def checkData(line, configFile, lineNumber):
    errors = []
    configFile.seek(0)
    config = list(csv.reader(configFile))
    try:
        order = config[0]
        fieldNames = config[order.index("FieldName")+1]
        types = config[order.index("Type")+1]
        minNums = config[order.index("NumberMin")+1]
        maxNums = config[order.index("NumberMax")+1]
    except (ValueError, IndexError) as e:
        configFile.close()
        raise e
        errors.append("Line {lineNumber}: Config file is not set up correctly.".format(lineNumber=lineNumber))
        return errors
    
    valueCount = 0
    for valueIndex, value in enumerate(line):
        if(not str(value).strip()):
            try:
                errors.append("Line {lineNumber}: {configVal} is blank.".format(lineNumber=lineNumber, configVal=fieldNames[valueIndex].title()))
            except IndexError:
                errors.append("Line {lineNumber}: Extra values have been found.".format(lineNumber=lineNumber))
                break
            
        try:
            int(value)
            if(not types[valueIndex] == "number"):
                errors.append("Line {lineNumber}: {configVal} needs to be a number.".format(lineNumber=lineNumber, configVal=fieldNames[valueIndex].title))
            elif(not minNums[valueIndex] < int(value) < maxNums[valueIndex]):
                errors.append("Line {lineNumber}: {configVal} needs to be within the min and max paramaters.".format(lineNumber=lineNumber, configVal=fieldNames[valueIndex].title))
        except ValueError:
            if(not types[valueIndex] == "string"):
                errors.append("Line {lineNumber}: {configVal} needs to be a string.".format(lineNumber=lineNumber, configVal=fieldNames[valueIndex].title))
                
        valueCount += 1
        
    if(valueCount < len(fieldNames)):
        print(valueCount, len(fieldNames))
        errors.append("Line {lineNumber}: Not enough values".format(lineNumber=lineNumber))
    elif(valueCount > len(fieldNames)):
        errors.append("Line {lineNumber}: Extra values have been found.".format(lineNumber=lineNumber))
        
    return list(set(errors))

            
print("Opening Required Files")
with open("dwithBugs.csv", "r") as d:
    with open("config.csv", "r") as configFile:
        errors = []
        curLine = 0
        print("Finding Errors")
        for line in csv.reader(d):
            curLine += 1
            errors.extend(checkData(line, configFile, curLine))
            if(curLine % 1000 == 0):
                print(str(curLine) + " lines have been checked.")

errors = list(filter(None, errors))

numOfErrors = 0
print("\n")
if(errors):
    for error in errors:
        print(error)
        numOfErrors += 1
    print(str(numOfErrors) + " errors have been found.")
else:
    print("No errors have been found.")

input()