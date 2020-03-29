import model as m

class scene:

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

	def addModel(self, model):
		self._models.append(model)

	def setWorldSize(self, worldSize):
		self._worldSize = worldSize
