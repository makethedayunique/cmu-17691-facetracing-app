"""
	This is the class to handle the returned result from the model
"""
class Mlresult:

	def __init__(self, timeslot, image, index):
		self.index = str(index)
		self.start_time = timeslot[0] # This is start time
		self.end_time = timeslot[1] # This is end time
		self.image = image # This is the screen shots urls taken from the time slot

	def set_slot(self, slot):
		self.start_time = slot[0]
		self.end_time = slot[1]

	def set_image(self, image):
		self.image = image

	def set_index(self, index):
		self.index = index

	def get_index(self):
		return self.index

	def get_slot(self):
		return self.start_time + " - " + self.end_time

	def get_image(self):
		return self.image