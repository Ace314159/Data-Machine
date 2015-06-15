inputFile = open("input.txt", "r")
values = list(inputFile.readlines())
numOfValues = 0

for i in range(len(values)):
   values[i] = '"'+values[i].strip().title()+'"'
   
outputFile = open("output.txt", "w")
values = list(set(values))
values.sort()

for j in values:
    if(j == values[0]):
        outputFile.write(j)
        numOfValues += 1
    else:
        outputFile.write(", " + j)
        numOfValues += 1
    
print(numOfValues)
inputFile.close()
outputFile.close()
input("")