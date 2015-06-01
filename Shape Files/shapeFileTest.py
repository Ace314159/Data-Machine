import shapefile, random
import matplotlib.pyplot as plt

print("Initializing Shapefile")
sf = shapefile.Reader("ap_abl")
input(sf.fields)
print("Initializing Geometries and Records")
shapeRecs = list(sf.shapeRecords())

fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([76, 85])
plt.ylim([12, 21])

print("Adding Polygons")
for shapeRec in shapeRecs:
    shape = shapeRec.shape
    record = shapeRec.record
    input(record)
    points = shape.points
    
    poly = plt.Polygon(points, fill=False, edgecolor="k")
    
    if("MANGALAGIRI" in record):
        bbox = shape.bbox
        boundX = [bbox[0], bbox[2]]
        boundY = [bbox[1], bbox[3]]
                
        pointsIn = []
        for i in range(100):
            works = False
            while(not works):
                x = random.uniform(boundX[0], boundX[1])
                y = random.uniform(boundY[0], boundY[1])
                pair = [x, y]
                if(poly.contains_point(pair) and pair not in pointsIn):
                    works = True
                    plt.plot([x], [y], "ro")
                    pointsIn.append(pair)
                    print(str(y) + ", " + str(x))
    
    ax.add_patch(poly)

print("Displaying Polygons")
plt.show()