"""
This file contains all kinds of code snippets.
"""

from person import Person
from place import Place
import numpy as np
import matplotlib.pyplot as plt
import cPickle
import csv

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


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

def crawl_places():
    places = []
    for i in range(68):
        places.append(Places(i))

    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0
        for row in reader:

            counter += 1
            if counter%100000==0:
                print counter
                print "The number of visitors is %d" % (len(visitors),)

def make_places():
    places = []
    for i in range(69):
        places.append(Place(i))
    areas = []
    for i in range(5):
        areas.append(Place(i))
    return places, areas

def make_positions():
    positions = []
    for i in range(100):
        for j in range(100):
            positions.append(Place((i,j)))
    return positions

def positionMAP():
    positionMAP = np.zeros((100,100),dtype=np.int)
    for i in range(100):
        for j in range(100):
            positionMAP[i,j] += 100*i+j
    return  positionMAP

def count_populations(visitors,MAP,places):
    for ID in visitors.keys():
        visitor = visitors[ID]
        visitor.time_period_on_places(MAP,places)

def aggregate_places_data(places,unit_time):
    population_record = np.zeros((int(60*16/unit_time),0),dtype=np.int)
    for i in range(len(places)):
        if i%500==0:
            print i
        population = np.expand_dims(places[i].population_per_unit_time(unit_time),axis=1)
        population_record = np.append(population_record,population,axis=1)
    return population_record

def extract_visitors_features(visitors, MAP, areaMAP):
    count = 0
    for ID in visitors.keys():
        count+=1
        visitor = visitors[ID]
        visitor.extract_features(MAP,areaMAP)
        if count % 500 == 0:
            print count

def aggregate_visitors_data(visitors,names=None):
    toPCA = np.zeros((0,78))
    IDlist = []
    if names is None:
    	names = visitors.keys()
    for ID in names:
        visitor = visitors[ID]
        aggregated = visitor.aggregate_data()
        toPCA = np.append(toPCA, aggregated, axis=0)
        IDlist.append(int(ID))
    return toPCA, IDlist

def np2csv(fileName, array):
    np.savetxt(fileName, array, delimiter=",",fmt="%1.1d")

def output_features(toPCA):
    features = toPCA[:,-4:]
    np.savetxt("features.csv", features, delimiter=",",fmt="%1.1d")

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
    return X_r, kmeans

def aggregate_routes(IDs):
	routes = np.zeros((0,7),dtype=np.int)
	counter = 0
	for ID in IDs:
	    counter += 1
	    if counter%100==0:
	        print counter
	    route = visitors[ID].route()
	    routes = np.append(routes,route,axis=0)
	return routes

def select_ID_PCA(X_r,IDlist):
	IDs = []
	for i in range(len(IDs)):
	    if X_r[i,0]>1 or X_r[i,0]<-1.2 or X_r[i,1]>2.4 or X_r[i,1]<-2:
	        IDs.append(str(IDlist[i]))
	return IDs

def reduce_PCA_data(X_r, IDlist):
	dx = 0.1
	width = 8
	height = 7
	slot = np.zeros((int(width/dx),int(height/dx)),dtype=np.int)
	for i in range(len(IDlist)):
	    X = X_r[i,0]
	    Y = X_r[i,1]
	    x = int((X+2)/dx)
	    y = int((Y+3)/dx)
	    if slot[x,y]==0:
	        slot[x,y] = IDlist[i]
	reduced_IDlist = []
	for i in range(slot.shape[0]):
	    for j in range(slot.shape[1]):
	        if slot[i,j]!=0:
	            reduced_IDlist.append(str(slot[i,j]))
	return reduced_IDlist