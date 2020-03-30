import structs

class object:

	def __init__(self, name="", position=structs.vector(), rotation=structs.vector(), scale=structs.vector(1.0, 1.0, 1.0)):
		self._name = name
		self._position = position
		self._rotation = rotation
		self._scale = scale

	def getPosition(self):
		return self._position

	def getRotation(self):
		return self._rotation

	def getScale(self):
		return self._scale

	def setPosition(self, x=0.0, y=0.0, z=0.0):
		self._position = structs.vector(x, y, z)

	def setRotation(self, x=0.0, y=0.0, z=0.0):
		self._rotation = structs.vector(x, y, z)

	def setScale(self, x=1.0, y=1.0, z=1.0):
		self._scale = structs.vector(x, y, z)

	def __str__(self):
		return self._name

class model(object):

	@classmethod
	def cube(cls, name="Cube", position=structs.vector(), rotation=structs.vector(), scale=structs.vector(1.0, 1.0, 1.0), material=(0.5, 0.5, 0.5, 1.0), size=1.0):
		cube = cls(name, position, rotation, material)

		cube.createVertex(structs.vector(-size/2, -size/2, -size/2))
		cube.createVertex(structs.vector(size/2, -size/2, -size/2))
		cube.createVertex(structs.vector(size/2, size/2, -size/2))
		cube.createVertex(structs.vector(-size/2, size/2, -size/2))
		cube.createVertex(structs.vector(-size/2, -size/2, size/2))
		cube.createVertex(structs.vector(size/2, -size/2, size/2))
		cube.createVertex(structs.vector(size/2, size/2, size/2))
		cube.createVertex(structs.vector(-size/2, size/2, size/2))

		cube.createFace(3, 2, 1, 0)
		cube.createFace(0, 1, 5, 4)
		cube.createFace(1, 2, 6, 5)
		cube.createFace(2, 3, 7, 6)
		cube.createFace(3, 0, 4, 7)
		cube.createFace(4, 5, 6, 7)

		return cube

	def __init__(self, name="", position=structs.vector(), rotation=structs.vector(), scale=structs.vector(1.0, 1.0, 1.0), material=(0.5, 0.5, 0.5, 1.0)):
		object.__init__(self, name, position, rotation)
		self._vertices = []
		self._faces = []
		self._materials = []
		self._numVertices = 0
		self._numFaces = 0
		self._material = material

	def getVertex(self, vertex):
		if vertex < self._numVertices:
			return self._vertices[vertex]
		else:
			raise ValueError

	def getFace(self, face):
		if face < self._numFaces:
			return self._faces[face]
		else:
			raise ValueError

	def getMaterial(self, material):
		if material < self._numFaces:
			return self._materials[material]
		else:
			raise ValueError

	def getVertices(self):
		return self._vertices

	def getFaces(self):
		return self._faces

	def createVertex(self, position):
		self._vertices.append(position)
		self._numVertices += 1

	def createFace(self, vertex1, vertex2, vertex3, vertex4=None, material=None):
		if vertex1 < self._numVertices and vertex2 < self._numVertices and vertex3 < self._numVertices:
			if vertex4 is None:
				self._faces.append((vertex1, vertex2, vertex3))
				self._materials.append(self._material if material is None else material)
				self._numFaces += 1
			elif vertex4 < self._numVertices:
				self._faces.append((vertex1, vertex2, vertex3))
				self._faces.append((vertex3, vertex4, vertex1))
				self._materials.append(self._material if material is None else material)
				self._materials.append(self._material if material is None else material)
				self._numFaces += 2
			else:
				raise ValueError
		else:
			raise ValueError

class camera(object):

	def __init__(self, position=structs.vector(), rotation=structs.vector(), scale=structs.vector(1.0, 1.0, 1.0), perspective=True, focalLength=60, nearPlane=1.0, farPlane=2000.0):
		object.__init__(self, "Camera", position, rotation)
		self._perspective = perspective
		self._focalLength = focalLength
		self._nearPlane = nearPlane
		self._farPlane = farPlane

	def isPerspective(self):
		return self._perspective

	def getFocalLength(self):
		return self._focalLength

	def getNearPlane(self):
		return self._nearPlane

	def getFarPlane(self):
		return self._farPlane

	def setPerspective(self, perspective):
		self._perspective = perspective

	def setFocalLength(self, focalLength):
		self._focalLength = focalLength

	def setNearPlane(self, value):
		self._nearPlane = value

	def setFarPlane(self, value):
		self._farPlane = value
