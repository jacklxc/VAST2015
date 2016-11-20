import numpy as np
class Person(object):
	"""A class describing the person"""
	def __init__(self, args):
		self.time = np.zeros((0,3))
		self.position = np.zeros((0,2))
		self.id = args.pop('id', "Error")
		self.add_time(args.pop('Timestamp', 'Error'))
		x = int(args.pop('X', '-1'))
		y = int(args.pop('Y', '-1'))
		position = np.array([[x,y]])
		np.append(self.position,position, axis=0)

	def add(self, args):
		if args.pop('id','Error') == self.id:
			self.add_time(args.pop('Timestamp', 'Error'))
			x = int(args.pop('X', '-1'))
			y = int(args.pop('Y', '-1'))
			position = np.array([[x,y]])
			np.append(self.position,position, axis=0)

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
		np.append(self.time, TIME, axis=0)





