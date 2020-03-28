import model as m

class scene:

	def __init__(self):
		self._models = []
		self._camera = m.camera()

	def getCamera(self):
		return self._camera

	def addModel(self, model):
		self._models.append(model)

	def getModels(self):
		return self._models
