"""
This file contains all kinds of code snippets.
"""

from person import Person
import numpy as np
import cPickle
import csv

def mapFacility(fileName):
    facilities = []
    with open(fileName,'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row.keys():
                row[key] = int(row[key])
            facilities.append(row)
    return facilities

def getMAP(facilities):
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
    return positions

def load_pkl(fileName):
    with open(fileName,"rb") as picklefile:
        new_positions = cPickle.load(picklefile)
    return new_positions

def dump_pkl(fileName, Object):
    with open(fileName,"wb") as picklefile:
        cPickle.dump(Object, picklefile)

def printRoute(visitor,MAP):
    for i in range(visitor.time.shape[0]):
        print "At time %d: %d: %d, coordinate %d,%d, facility #%d" % (visitor.time[i,0],visitor.time[i,1],visitor.time[i,2],visitor.position[i,0],visitor.position[i,1],
        MAP[visitor.position[i,0],visitor.position[i,1]])
def getAreaMAP(areaMAP):
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
    return areamap

def crawl_visitors(fileName):
    visitors = {}
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0
        for row in reader:
            ID = row["id"]
            time = row['Timestamp']
            if ID in visitors:
                visitors[ID].add(row)
            else:
                visitors[ID] = Person(row)
            counter += 1
            if counter%100000==0:
                print counter
                print "The number of visitors is %d" % (len(visitors),)
    return visitors

def extract_visitors_features(visitors, MAP, areaMAP):
    count = 0
    for ID in visitors.keys():
        count+=1
        visitor = visitors[ID]
        visitor.extract_features(MAP,areaMAP)
        if count % 500 == 0:
            print count

def aggregate_visitors_data(visitors):
    toPCA = np.zeros((0,78))
    IDlist = []
    for ID in visitors.keys():
        visitor = visitors[ID]
        aggregated = visitor.aggregate_data()
        toPCA = np.append(toPCA, aggregated, axis=0)
        IDlist.append(int(ID))
    return toPCA, IDlist

def np2csv(fileName, array):
    np.savetxt(fileName, array, delimiter=",")

def output_features(toPCA):
    features = toPCA[:,-4:]
    np2csv("features.csv",features)
def plot_PCA(X_r):
    plt.figure()
    for i in range(X_r.shape[0]):
        plt.scatter(X_r[i,0],X_r[i,1])
    plt.title('PCA')
    plt.show()

def list2csv(fileName, list):
    with open(fileName, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list)
def doPCA(toPCA):
    pca = PCA(n_components=2, whiten=True)
    X_r = pca.fit_transform(toPCA)
    kmeans = KMeans(n_clusters=5).fit_predict(X_r)