""" Implements basic structures used throughout """

import math

class matrix:

	""" Class implementing all matrix functionality """

	# Commonly used matrices as classmethods

	@classmethod
	def identity(cls, n=4):
		# Identity matrix of degree n
		result = matrix(n, n)
		for i in range(n):
			result.insert(i, i, 1)
		return result

	def __init__(self, rows=4, coloumns=4):
		# Matrix is internally stored as an array of size rows (first index) x coloumns (second index)
		self._rows = rows
		self._coloumns = coloumns
		self._matrix = [[0 for i in range(coloumns)] for i in range(rows)]

	def getSize(self):
		return (self._rows, self._coloumns)

	def get(self, row, coloumn):
		return self._matrix[row][coloumn]

	def insert(self, row, coloumn, element):
		self._matrix[row][coloumn] = element
		return self

	def __mul__(self, other):
		if isinstance(other, vector):
			# matrix * vector, returns vector
			result = vector()
			for i in range(4):
				value = 0.0
				for k in range(4):
					value += self.get(i, k) *  other.get(k)
				result.insert(i, value)
			return result
		else:
			# matrix * matrix, returns matrix
			sizes = (self.getSize(), other.getSize())
			if sizes[0][1] != sizes[1][0]:
				raise TypeError

			r = sizes[0][0]
			c = sizes[1][1]
			iterations = sizes[0][1]

			result = matrix(r, c)
			for i in range(r):
				for j in range(c):
					value = 0.0
					for k in range(iterations):
						value += self.get(i, k) * other.get(k, j)
					result.insert(i, j, value)
			return result

	def __str__(self):
		# Pretty formatting
		string = ""
		for i in range(self._rows):
			for j in range(self._coloumns):
				string += str(self.get(i, j)) + "\t"
			string += "\n"
		return string

class vector:

	""" Class implementing all vector functionality """

	# Commonly used vectors as classmethods

	@classmethod
	def direction(cls, n):
		# Vector pointing along a particular axis (0 for x-axis, 1 for y-axis, 2 for z-axis)
		result = vector()
		result.insert(n, 1)
		return result

	@classmethod
	def one(cls):
		# Vector with all components as 1.0
		return vector(1.0, 1.0, 1.0)

	def __init__(self, x=0.0, y=0.0, z=0.0):
		# Vector is internally stored as a 4x1 matrix (but does not inherit from it)
		self._vector = matrix(4, 1)
		self._vector.insert(0, 0, x)
		self._vector.insert(1, 0, y)
		self._vector.insert(2, 0, z)
		self._vector.insert(3, 0, 1.0)

	def get(self, index):
		return self._vector.get(index, 0)

	def getMagnitude(self):
		return math.sqrt(sum(math.pow(self._vector.get(i), 2) for i in range(3)))

	def normalized(self):
		return self / self.getMagnitude()

	def insert(self, index, element):
		self._vector.insert(index, 0, element)
		return self

	# Vector transformations (commit is used to commit the change to self)

	def translate(self, positionVector, commit=True):
		result = self + positionVector
		if commit:
			self._vector = result.asMatrix()
			return self
		else:
			return result

	def rotate(self, rotationVector, commit=True):
		result = self
		for i in range(3):
			# Separately for x, y, z axes
			r = matrix.identity(4)
			r.insert((i + 1) % 3, (i + 1) % 3, math.cos(math.radians(rotationVector.get(i))))
			r.insert((i + 1) % 3, (i + 2) % 3, - math.sin(math.radians(rotationVector.get(i))))
			r.insert((i + 2) % 3, (i + 1) % 3, math.sin(math.radians(rotationVector.get(i))))
			r.insert((i + 2) % 3, (i + 2) % 3, math.cos(math.radians(rotationVector.get(i))))
			result = r * result
		if commit:
			self._vector = result.asMatrix()
			return self
		else:
			return result

	def scale(self, scaleVector, commit=True):
		s = matrix.identity(4)
		s.insert(0, 0, scaleVector.get(0))
		s.insert(1, 1, scaleVector.get(1))
		s.insert(2, 2, scaleVector.get(2))
		if commit:
			self._vector = (s * self).asMatrix()
			return self
		else:
			return s * self

	# Converting vector in another form

	def asMatrix(self):
		m = matrix(4, 1)
		for i in range(4):
			m.insert(i, 0, self.get(i))
		return m

	def asList(self):
		return [self.get(0), self.get(1), self.get(2)]

	def __add__(self, other):
		# Vector addition
		result = vector()
		for i in range(3):
			result.insert(i, self.get(i) + other.get(i))
		return result

	def __mul__(self, num):
		# Scalar multiplication
		result = vector()
		for i in range(3):
			result.insert(i, self.get(i) * num)
		return result

	def __truediv__(self, num):
		# Scalar division
		result = vector()
		for i in range(3):
			result.insert(i, self.get(i) / num)
		return result

	def __str__(self):
		# Pretty formatting
		return "({}, {}, {})".format(self.get(0), self.get(1), self.get(2))
