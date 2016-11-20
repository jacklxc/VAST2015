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
        y1=facility["y1"]
        y2=facility["y2"]
        for x in range(x1, x2+1):
            for y in range(y1,y2+1):
                positions[x,y] = facility_id
for i in range(len(facilities)):
    facility_id = i+1
    if facility_id not in [23,35,41,43,63]:
        facility = facilities[i]
        x1=facility["x1"]
        x2=facility["x2"]
        y1=facility["y1"]
        y2=facility["y2"]
        for x in range(x1, x2+1):
            for y in range(y1,y2+1):
                positions[x,y] = facility_id

with open("positions.pkl","rb") as picklefile:
    new_positions = cPickle.load(picklefile)
print new_positions

########
import cPickle
with open("positions.pkl","wb") as picklefile:
    cPickle.dump(positions, picklefile)