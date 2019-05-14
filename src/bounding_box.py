from .serializer import Serializable
import json


class BoundingBox():
	def __init__(self, object_id, bounding_box,frame_no):
		self.object_id = object_id
		self.bounding_box = bounding_box
		self.frame_no = frame_no	


	def __repr__(self):
		return json.dumps(self.__dict__)
