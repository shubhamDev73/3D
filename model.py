""" Implements all the physical objects used """

import structs

class object:

	""" The object class which is base class for every object(3D model, camera, light, etc.) """

	def __init__(self, name="", position=structs.vector(), rotation=structs.vector(), scale=structs.vector.one()):
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
		return self

	def setRotation(self, x=0.0, y=0.0, z=0.0):
		self._rotation = structs.vector(x, y, z)
		return self

	def setScale(self, x=1.0, y=1.0, z=1.0):
		self._scale = structs.vector(x, y, z)
		return self

	def __str__(self):
		return self._name

class model(object):

	""" The class defining 3D models """

	# Pre-defined 3D models as classmethods

	@classmethod
	def cube(cls, name="Cube", position=structs.vector(), rotation=structs.vector(), scale=structs.vector.one(), material=(0.5, 0.5, 0.5, 1.0), size=1.0):
		cube = cls(name, position, rotation, material)

		# bottom vertices
		cube.createVertex(structs.vector(-size/2, -size/2, -size/2))
		cube.createVertex(structs.vector(size/2, -size/2, -size/2))
		cube.createVertex(structs.vector(size/2, size/2, -size/2))
		cube.createVertex(structs.vector(-size/2, size/2, -size/2))

		# top vertices
		cube.createVertex(structs.vector(-size/2, -size/2, size/2))
		cube.createVertex(structs.vector(size/2, -size/2, size/2))
		cube.createVertex(structs.vector(size/2, size/2, size/2))
		cube.createVertex(structs.vector(-size/2, size/2, size/2))


		# bottom face
		cube.createFace(3, 2, 1, 0)

		# side faces
		cube.createFace(0, 1, 5, 4)
		cube.createFace(1, 2, 6, 5)
		cube.createFace(2, 3, 7, 6)
		cube.createFace(3, 0, 4, 7)

		# top face
		cube.createFace(4, 5, 6, 7)

		return cube

	def __init__(self, name="", position=structs.vector(), rotation=structs.vector(), scale=structs.vector.one(), material=(0.5, 0.5, 0.5, 1.0)):
		object.__init__(self, name, position, rotation)
		self._vertices = []
		self._faces = []
		self._materials = []
		self._material = material

	def getVertex(self, vertex):
		return self._vertices[vertex]

	def getFace(self, face):
		return self._faces[face]

	def getMaterial(self, material):
		return self._materials[material]

	def getVertices(self):
		return self._vertices

	def getFaces(self):
		return self._faces

	def createVertex(self, position):
		self._vertices.append(position)
		return self

	def createFace(self, vertex1, vertex2, vertex3, vertex4=None, material=None):
		numVertices = len(self._vertices)
		if vertex1 < numVertices and vertex2 < numVertices and vertex3 < numVertices:
			if vertex4 is None:
				self._faces.append((vertex1, vertex2, vertex3))
				self._materials.append(self._material if material is None else material)
			elif vertex4 < numVertices:
				self._faces.append((vertex1, vertex2, vertex3))
				self._faces.append((vertex3, vertex4, vertex1))
				self._materials.append(self._material if material is None else material)
				self._materials.append(self._material if material is None else material)
			else:
				raise ValueError
		else:
			raise ValueError
		return self

	def getWorldCoordinates(self, vertex):
		# First rotate, then scale, then translate
		return self._vertices[vertex].rotate(self._rotation, False).scale(self._scale, False).translate(self._position, False)

class camera(object):

	""" The class defining the camera which renders scene """

	def __init__(self, position=structs.vector(), rotation=structs.vector(), scale=structs.vector.one(), perspective=True, focalLength=60, nearPlane=1.0, farPlane=2000.0):
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
		return self

	def setFocalLength(self, focalLength):
		self._focalLength = focalLength
		return self

	def setNearPlane(self, value):
		self._nearPlane = value
		return self

	def setFarPlane(self, value):
		self._farPlane = value
		return self

	# Viewing transformations

	def getViewCoordinates(self, worldCoordinates):
		# First translate, then rotate
		# TODO: implement rotation, fill u, v, n
		u = structs.vector.direction(0) * -1
		v = structs.vector.direction(2) * -1
		n = structs.vector.direction(1)

		r = structs.matrix.identity(4)
		for i in range(3):
			r.insert(0, i, u.get(i))
			r.insert(1, i, v.get(i))
			r.insert(2, i, n.get(i))
		return r * worldCoordinates.translate(self._position * -1)

	def project(self, viewCoordinates):
		# Projecting from 3D world to 2D window
		if self._perspective:
			# Perspective projection
			# TODO: confirm this (specially self._focalLength)
			p = structs.matrix.identity(4)
			# zv = self._position().get(2)
			# zp = self._position().get(2) - self._focalLength
			# d = zp - zv
			# p.insert(2, 2, zv / d)
			# p.insert(2, 3, -zv * (zp / d))
			# p.insert(3, 2, 1.0 / d)
			# p.insert(3, 3, -zp / d)
			p.insert(2, 2, 0)
			p.insert(3, 2, -1.0 / self._focalLength)
			p.insert(3, 3, -1.0)
			v = p * viewCoordinates
			return structs.vector(v.get(0) / v.get(3), v.get(1) / v.get(3))
		else:
			# Orthogonal projection
			return structs.vector(viewCoordinates.get(0), viewCoordinates.get(1))
