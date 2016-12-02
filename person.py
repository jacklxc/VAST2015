import numpy as np
class Person(object):
	"""A class describing the person"""
	def __init__(self, args):
		self.total_facility = 68
		self.total_area = 5
		self.time = np.zeros((0,3),dtype=np.int)
		self.position = np.zeros((0,2),dtype=np.int)
		self.type = np.zeros((0,1),dtype = np.bool)
		self.id = args.pop('id', "Error")
		self.add_type(args.pop('type',"Error"))
		self.add_time(args.pop('Timestamp', 'Error'))
		x = int(args.pop('X', '-1'))
		y = int(args.pop('Y', '-1'))
		position = np.array([[x,y]])
		self.position = np.append(self.position,position, axis=0)

	def add(self, args):
		if args.pop('id','Error') == self.id:
			self.add_time(args.pop('Timestamp', 'Error'))
			self.add_type(args.pop('type',"Error"))
			x = int(args.pop('X', '-1'))
			y = int(args.pop('Y', '-1'))
			position = np.array([[x,y]])
			self.position = np.append(self.position,position, axis=0)

	def add_type(self, TYPE):
		type = True if TYPE=="check-in" else False
		self.type = np.append(self.type,np.array([[type]]), axis=0)

	def add_time(self, time):
		if time!="Error":
			hour = int(time[10:12])
			minute = int(time[13:15])
			second = int(time[16:18])
		else:
			hour = np.nan
			minute = np.nan
			second = np.nan
		TIME = np.array([[hour, minute, second]])
		self.time = np.append(self.time, TIME, axis=0)

	def extract_features(self, MAP, areaMAP):
		"""
		MAP is the mapping between coordinate (x,y) and the facilities.
		"""
		self.time_on_each_facility = self._time_on_each_facility(MAP)
		self.time_on_each_area = self._time_on_each_area(areaMAP)
		self.time_enter = self.time[0,:]
		self.time_exit = self.time[-1,:]
		self.num_facility_visited = self._num_facility_visited()
		self.num_check_in = np.sum(self.type)
		self.time_interval = self._time_interval_minutes()

	def _time_interval_minutes(self):
		time_interval = self.time[1:,:] - self.time[:-1,:]
		time_interval = self._format_time(time_interval)
		interval_in_minutes = time_interval[:,0]*60 + time_interval[:,1]
		interval_in_minutes = np.append(interval_in_minutes,np.ones((1,),dtype=np.int))
		return interval_in_minutes
	
	def route(self):
		self.time_interval = self._time_interval()
		time_interval = np.expand_dims(self.time_interval, axis=1)
		route = np.concatenate((self.time,time_interval,self.position), axis=1)
		return route


	def aggregate_data(self):
		dimension = 78 # Total data dimensions to aggregate

		data = np.zeros((1,dimension))
		prev_dim = 0

		dim = prev_dim + self.time_on_each_facility.shape[0]
		seconds = self._time2seconds(self.time_on_each_facility)
		data[0,prev_dim:dim] = seconds
		prev_dim = dim

		dim = prev_dim + self.time_on_each_area.shape[0]
		seconds = self._time2seconds(self.time_on_each_area)
		data[0,prev_dim:dim] = seconds

		seconds = self._time2seconds(self.time_enter)
		data[0,dim] = seconds
		dim +=1

		seconds = self._time2seconds(self.time_exit)
		data[0,dim] = seconds
		dim +=1

		seconds = self.num_facility_visited
		data[0,dim] = seconds
		dim +=1

		seconds = self.num_check_in
		data[0,dim] = seconds

		return data

	def _time2seconds(self, time):
		if len(time.shape)>1:
			N = time.shape[0]
		else:
			N = 1
			time = np.expand_dims(time,axis=0)
		seconds = np.zeros((1,N),dtype = np.int)
		seconds[0,:] = time[:,0]*3600 + time[:,1]*60 + time[:,2]
		return seconds

	def _time_on_each_facility(self, MAP):
		time_on_places = np.zeros((self.total_facility+1,3), dtype = np.int)
		prev_time = self.time[0,:]
		x = self.position[0,0]
		y = self.position[0,1]
		facility = MAP[x, y]
		for i in range(1, self.time.shape[0]):
			time_spent = self.time[i,:] - prev_time
			time_on_places[facility,:] += time_spent
			prev_time = self.time[i,:]
			x = self.position[i,0]
			y = self.position[i,1]
			facility = MAP[x, y]
		time_on_places = self._format_time(time_on_places)
		return time_on_places

	def _time_on_each_area(self, areaMAP):
		time_on_places = np.zeros((self.total_area,3), dtype = np.int)
		prev_time = self.time[0,:]
		x = self.position[0,0]
		y = self.position[0,1]
		area = areaMAP[x, y]
		for i in range(1, self.time.shape[0]):
			time_spent = self.time[i,:] - prev_time
			time_on_places[area,:] += time_spent
			prev_time = self.time[i,:]
			x = self.position[i,0]
			y = self.position[i,1]
			area = areaMAP[x, y]
		time_on_places = self._format_time(time_on_places)
		return time_on_places

	def _num_facility_visited(self):
		time_sum = np.sum(self.time_on_each_facility, axis=1)
		visited = time_sum > 0
		count = np.sum(visited)
		return count - 1 # Exclude facility No.0

	def _format_time(self, time):
		"""Takes a numpy array (N,3) of time and format it"""
		for n in range(time.shape[0]):
			hour, minute, second = time[n,0], time[n,1], time[n,2]
			if second is not np.nan:
				while second >=60:
					second -= 60
					minute += 1
				while second <0:
					minute -= 1
					second += 60
				while minute >= 60:
					minute -= 60
					hour += 1
				while minute <0:
					hour -= 1
					minute += 60
				time[n,0], time[n,1], time[n,2] = hour, minute, second
		return time

	def time_period_on_places(self,MAP,places):
		for n in range(self.time.shape[0]):
			place = MAP[self.position[n,0], self.position[n,1]]
			places[place].add_person(self.time[n,:],self.time_interval[n])







