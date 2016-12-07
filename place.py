import numpy as np
class Place(object):
	"""A class describing the person"""
	def __init__(self, name):
		#self.check_in_count = np.zeros((60*16,),dtype=np.int)
		self.population = np.zeros((60*16,),dtype=np.int)
		self.name = name

	def count_check_in(self, time):
		if time!="Error":
			hour = int(time[10:12])
			minute = int(time[13:15])
			second = int(time[16:18])
		else:
			hour = np.nan
			minute = np.nan
			second = np.nan
		time_in_minute = (hour-8)*60 + minute
		self.check_in_count[time_in_minute] += 1

	def add_person(self,time, interval):
		"""
		Inputs
		- time: numpy int array of shape (3,)
		- interval: int (time interval in minutes)
		"""
		start = (time[0]-8)*60 + time[1]
		end = start + interval
		self.population[start:end+1] += 1

	def population_per_unit_time(self,unit_time):
		index = np.arange(60*16)%unit_time==0
		return self.population[index]

	def _time_interval(self):
		time_interval = self.time[1:,:] - self.time[:-1,:]
		time_interval = self._format_time(time_interval)
		interval_in_seconds = np.sum(time_interval,axis=1)
		interval_in_seconds = np.append(np.zeros((1,),dtype=np.int),interval_in_seconds)
		return interval_in_seconds
	

	def _time2seconds(self, time):
		if len(time.shape)>1:
			N = time.shape[0]
		else:
			N = 1
			time = np.expand_dims(time,axis=0)
		seconds = np.zeros((1,N),dtype = np.int)
		seconds[0,:] = time[:,0]*3600 + time[:,1]*60 + time[:,2]
		return seconds

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







