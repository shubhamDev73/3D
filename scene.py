""" Implements the 3D scene """

import model as m

class scene:

	""" Class implementing the 3D scene. It can contain only 1 camera and multiple 3D models """

	def __init__(self, worldSize=5):
		self._models = []
		self._camera = m.camera()
		self._worldSize = worldSize

	def getCamera(self):
		return self._camera

	def getModels(self):
		return self._models

	def getWorldSize(self):
		return self._worldSize

	def setWorldSize(self, worldSize):
		self._worldSize = worldSize
		return self

	def addModel(self, model):
		self._models.append(model)
		return self
