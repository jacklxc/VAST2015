facilities = []
with open('data.csv','rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for key in row.keys():
            row[key] = int(row[key])
        facilities.append(row)

positions=np.zeros((100,100),dtype=np.int)

for i in range(len(facilities)):
    facility_id = i+1
    if facility_id in [23,35,41,43,63]:
        facility = facilities[i]
        x1=facility["x1"]
        x2=facility["x2"]
        y2=100-facility["y1"]
        y1=100-facility["y2"]
        for x in range(x1, x2+1):
            for y in range(y1-1,y2):
                positions[x,y] = facility_id
for i in range(len(facilities)):
    facility_id = i+1
    if facility_id not in [23,35,41,43,63]:
        facility = facilities[i]
        x1=facility["x1"]
        x2=facility["x2"]
        y2=100-facility["y1"]
        y1=100-facility["y2"]
        for x in range(x1, x2+1):
            for y in range(y1-1,y2):
                positions[x,y] = facility_id

#########

with open("positions.pkl","rb") as picklefile:
    new_positions = cPickle.load(picklefile)
print new_positions

########
import cPickle
with open("positions.pkl","wb") as picklefile:
    cPickle.dump(positions, picklefile)

##########
for i in range(visitor.time.shape[0]):
    print "At time %d: %d: %d, coordinate %d,%d, facility #%d" % (visitor.time[i,0],visitor.time[i,1],visitor.time[i,2],visitor.position[i,0],visitor.position[i,1],
    MAP[visitor.position[i,0],visitor.position[i,1]])
########
areamap = []
for i in range(100):
    areamap.append([])
    for j in range(100):
        if areaMAP[i,j]==1:
            areamap[i].append("blue")
        elif areaMAP[i,j]==2:
            areamap[i].append("pink")
        elif areaMAP[i,j]==3 or areaMAP[i,j]==4:
            areamap[i].append("yellow")
        elif areaMAP[i,j]==5 or areaMAP[i,j]==6 or areaMAP[i,j]==7:
            areamap[i].append("red")
        elif areaMAP[i,j]==8 or areaMAP[i,j]==9:
            areamap[i].append("green")
        else:
            areamap[i].append("out")
print areamap