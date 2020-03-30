class matrix:

	@classmethod
	def identity(cls, n=4):
		result = matrix(n, n)
		for i in range(n):
			result.insert(i, i, 1)
		return result

	def __init__(self, rows=4, coloumns=4):
		self._rows = rows
		self._coloumns = coloumns
		self._matrix = [[0 for i in range(coloumns)] for i in range(rows)]

	def getSize(self):
		return (self._rows, self._coloumns)

	def get(self, row, coloumn):
		return self._matrix[row][coloumn]

	def insert(self, row, coloumn, element):
		self._matrix[row][coloumn] = element

	def __mul__(self, other):
		if isinstance(other, vector):
			result = vector()
			for i in range(4):
				value = 0.0
				for k in range(4):
					value += self.get(i, k) * other.get(k)
				result.insert(i, value)
			return result
		else:
			sizes = (self.getSize(), other.getSize())
			if sizes[0][1] != sizes[1][0]:
				raise TypeError

			r = sizes[0][0]
			c = sizes[1][1]
			iter = sizes[0][1]

			result = matrix(r, c)
			for i in range(r):
				for j in range(c):
					value = 0.0
					for k in range(iter):
						value += self.get(i, k) * other.get(k, j)
					result.insert(i, j, value)
			return result

	def __str__(self):
		string = ""
		for i in range(self._rows):
			for j in range(self._coloumns):
				string += str(self.get(i, j)) + "\t"
			string += "\n"
		return string

class vector:

	@classmethod
	def direction(cls, n):
		result = vector()
		result.insert(n, 1)
		return result

	def __init__(self, x=0.0, y=0.0, z=0.0):
		self._vector = matrix(4, 1)
		self._vector.insert(0, 0, x)
		self._vector.insert(1, 0, y)
		self._vector.insert(2, 0, z)
		self._vector.insert(3, 0, 1.0)

	def get(self, index):
		return self._vector.get(index, 0)

	def insert(self, index, element):
		return self._vector.insert(index, 0, element)

	def translate(self, x=0.0, y=0.0, z=0.0):
		self._vector = translate(self._vector, x, y, z)
		return self._vector

	def rotate(self, angle, axis):
		self._vector = rotate(self._vector, angle, axis)
		return self._vector

	def scale(self, x=1.0, y=1.0, z=1.0):
		self._vector = scale(self._vector, x, y, z)
		return self._vector

	def toList(self):
		return [self.get(0), self.get(1), self.get(2)]

	def __mul__(self, num):
		v = vector()
		for i in range(3):
			v.insert(i, self.get(i) * num)
		return v

	def __truediv__(self, num):
		v = vector()
		for i in range(3):
			v.insert(i, self.get(i) / num)
		return v

	def __str__(self):
		return "({}, {}, {})".format(self.get(0), self.get(1), self.get(2))

def translate(vector, x=0.0, y=0.0, z=0.0):
	t = matrix.identity(4)
	t.insert(0, 3, x)
	t.insert(1, 3, y)
	t.insert(2, 3, z)
	return t * vector

def rotate(vector, angle, axis):
	# TODO
	return vector

def scale(vector, x=1.0, y=1.0, z=1.0):
	s = matrix.identity(4)
	s.insert(0, 0, x)
	s.insert(1, 1, y)
	s.insert(2, 2, z)
	return s * vector
