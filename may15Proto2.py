import random, os, shapefile, shapely
import matplotlib.pyplot as plt

print("Initializing")

d = open("d.csv", "a+")

if(not os.path.exists("prev.txt")):
    with open("prev.txt", "w") as prev:
        prev.write("0\n0\n0")
        prev = open("prev.txt", "a+")
else:
    prev = open("prev.txt", "a+")
 
prev.seek(0)   
iStart = int(prev.readline())
jStart = int(prev.readline())
kStart = int(prev.readline())
prev.seek(0)

with open("firstNames.txt", "r") as f:
    exec("firstNames=["+f.read()+"]")
with open("middleNames.txt", "r") as f:
   exec("middleNames=["+f.read()+"]")
with open("lastNames.txt", "r") as f:
    exec("lastNames=["+f.read()+"]")
with open("maleNames.txt", "r") as f:
    exec("maleNames=["+f.read()+"]")
with open("educations.txt", "r") as f:
   exec("educations=["+f.read()+"]")
with open("streets.txt", "r") as f:
    exec("streets=["+f.read()+"]")
    
sf = shapefile.Reader("Shape Files\\ap_abl")
shapeRecs = list(sf.shapeRecords())


noSchool = 0
incomplete = 0
high = 0
ba = 0
ma = 0
do = 0
numOfPeopleAdded = 0
for line in d:
    if(not line == ""):
        numOfPeopleAdded += 1
        found = line.find("No School")
        if(not found ==  -1 and not found == 0):
            noSchool += 1
        found = line.find("Incomplete School")
        if(not found ==  -1 and not found == 0):
            incomplete += 1
        found = line.find("High School")
        if(not found ==  -1 and not found == 0):
            high += 1
        found = line.find("Bachelors")
        if(not found ==  -1 and not found == 0):
            ba += 1
        found = line.find("Masters")
        if(not found ==  -1 and not found == 0):
            ma += 1
        found = line.find("Doctorate")
        if(not found ==  -1 and not found == 0):
            do += 1
            
print(numOfPeopleAdded)
   
testList = educations
dList = []

peopleWanted = int(input("How many people do you want to add?"))

if(peopleWanted > len(firstNames) * len(middleNames) * len(lastNames) or peopleWanted < 0):
    peopleWanted = len(firstNames) * len(middleNames) * len(lastNames)

def findEducation(educations):
    total = peopleWanted
    working = False
    global noSchool
    global incomplete
    global high
    global ba
    global ma
    global do
    
    while(not working):
        test = testList[random.randint(0, len(testList)-1)]
        if(test == "No School" and ((noSchool+1)/total) < 0.3):
            noSchool += 1
            working = True
        elif(test == "Incomplete School" and ((incomplete+1)/total) < 0.3):
            incomplete += 1
            working = True
        elif(test == "High School" and ((high+1)/total) < 0.2):
            noSchool += 1
            working = True
        elif(test == "Bachelors" and ((ba+1)/total) < 0.15):
            ba += 1
            working = True
        elif(test == "Masters" and ((ma+1)/total) < 0.04):
            ma += 1
            working = True
        elif(test == "Doctorate" and ((do+1)/total) < 0.01):
            do += 1
            working = True
        else:
            testList.remove(test)
        
        return test

    
def findPos(shapeRecs):
    shapeRec = random.choice(shapeRecs)
    pos = {}
    shape = shapeRec.shape
    bbox = shape.bbox
    record = shapeRec.record
    pos["lat"] = random.uniform(bbox[1], bbox[3])
    pos["long"] = random.uniform(bbox[0], bbox[2])
    pos["village"] = record[8].title().replace(",", ".")
    pos["mandal"] = record[9].title().replace(",", ".")
    pos["district"] = record[13].title().replace(",", ".")
    pos["state"] = record[14]
    return pos    
    
    
try:            
    for i in firstNames[iStart:]:
        for j in middleNames[jStart:]:
            for k in lastNames[kStart:]:
                name = i+" "+j
                age = random.randint(0, 120)
                sex = "M" if i in maleNames else "F"
                education = findEducation(educations)
                income = round(random.uniform(1, 500), 2)
                networth = income * round(random.uniform(1, 3), 2)
                streetNum = random.randint(1, 9999)
                street = random.choice(streets)
                pos = findPos(shapeRecs)
                village = pos["village"]
                mandal = pos["mandal"]
                district = pos["district"]
                state = pos["state"]
                pin = random.randint(111111, 999999)
                lat = pos["lat"]
                long = pos["long"]
                text = name+", "+k+", "+sex+", "+str(age)+", "+education+", "+str(income)+", "+str(networth)+", "+str(streetNum)+", "+street+", "+village+", "+mandal+", "+district+", "+state+", "+str(pin)+", "+str(lat)+", "+str(long)+"\n"
                
                d.seek(0)
                if(not any(name+k in s for s in d.readlines())):
                    dList.append(text)
                numOfPeopleAdded += 1
                    
                if(numOfPeopleAdded == peopleWanted):
                    raise KeyboardInterrupt
                if(numOfPeopleAdded % 1000 == 0):
                    print(numOfPeopleAdded, "new people have been registered.")
except KeyboardInterrupt:              
    d.close()
    prev.seek(0)
    prev.truncate()
    prev.write(str(firstNames.index(i))+"\n"+str(middleNames.index(j))+"\n"+str(lastNames.index(k)))
    prev.close()    
    with open("d.csv", "a") as d:
        print("Adding registered people")
        random.shuffle(dList)
        d.writelines(dList)
    with open("d.csv", "ab") as d:
        d.seek(-2, 2)
        d.truncate()
    input("A total of " + str(numOfPeopleAdded) + " people have been added.")