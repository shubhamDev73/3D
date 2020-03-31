""" Implements the display and render algorithms """

import structs, ui

# Global variables contains reference assigned by latest call (used while updating in this module)
# scene: scene to display
# triangles: list of triangles (viewport coordinates) and their corresponding model to calculate selected model
# selected: reference to the model that is currently selected

scene = None
triangles = []
selected = None

def display(_scene):

	""" Displays the scene on UI """

	if _scene is None:
		return

	global scene, triangles
	scene = _scene
	camera = scene.getCamera()

	# Window: bottom-left is (0, 0)
	min_window = structs.vector(0, 0)
	max_window = structs.vector(scene.getWorldSize(), scene.getWorldSize())
	# Viewport: top-left is (0, 0)
	min_viewport = structs.vector(0, ui.viewportSize)
	max_viewport = structs.vector(ui.viewportSize, 0)

	# Drawing
	ui.clear()
	triangles = []
	for model in scene.getModels():
		for face in model.getFaces():
			# Model coordinates -> world coordinates -> view coordinates -> projection coordinates -> viewport coordinates
			projection = (camera.project(camera.getViewCoordinates(model.getWorldCoordinates(face[i]))) for i in range(3))
			projection = tuple(map(lambda vector: getViewportCoordinates(vector, min_window, max_window, min_viewport, max_viewport), projection))
			ui.draw_line(projection[0], projection[1], selected is model)
			ui.draw_line(projection[1], projection[2], selected is model)
			triangles.append((projection[0], projection[1], projection[2], model))
	return True

def getViewportCoordinates(projectionCoordinates, min_window, max_window, min_viewport, max_viewport):

	""" Get viewport coordinates corresponding to given projection coordinates """

	# First translate to window origin, then scale, then translate to viewport origin
	# TODO: check last step
	s = structs.vector()
	for i in range(3):
		try:
			s.insert(i, (max_viewport.get(i) - min_viewport.get(i)) / (max_window.get(i) - min_window.get(i)))
		except:
			pass
	return projectionCoordinates.translate(min_window * -1).scale(s).translate(min_viewport)

def select(event):

	""" Checks if some model is selected """

	global selected
	selected = None
	clickPoint = structs.vector(event.x, event.y)
	for v0, v1, v2, model in triangles:
		# For line created by each cyclic pair v0, v1 if v2 and click point lie on same side of line, then clicked on that model
		if sameSide(v0, v1, v2, clickPoint) and sameSide(v1, v2, v0, clickPoint) and sameSide(v2, v0, v1, clickPoint):
			selected = model
			break
	ui.updateProperties(selected)
	display(scene)
	return selected

def sameSide(point1, point2, referencePoint, checkPoint):

	""" Checks whether reference point and check point are on same side of line created by point1 and point2 """

	if point2.get(0) == point1.get(0):
		# slope = infinity
		ref = referencePoint.get(0) - point2.get(0)
		check = checkPoint.get(0) - point2.get(0)
	else:
		slope = (point2.get(1) - point1.get(1)) / (point2.get(0) - point1.get(0))
		ref = (referencePoint.get(1) - point2.get(1)) - slope * (referencePoint.get(0) - point2.get(0))
		check = (checkPoint.get(1) - point2.get(1)) - slope * (checkPoint.get(0) - point2.get(0))
	return ref * check > 0

def export(file):

	""" Export selected model to file """

	model = selected
	if model is None:
		return
	print("Exporting {} to {}".format(str(model), file))

	# Interchanging y and z axes as convention is different
	t = structs.matrix.identity(4)
	t.insert(1, 1, 0)
	t.insert(1, 2, 1)
	t.insert(2, 2, 0)
	t.insert(2, 1, 1)

	# This program: (0, 0, 0) to (worldSize, worldSize, worldSize)
	min_window = structs.vector()
	max_window = structs.vector.one() * scene.getWorldSize()
	# For WebGL: (-1, -1, -1) to (1, 1, 1)
	min_viewport = structs.vector.one() * -1
	max_viewport = structs.vector.one()

	vertices = []
	indices = []
	colors = []
	index = 0
	for face in model.getFaces():
		for vertex in face:
			# Creating different vertex for each face to have constant colour across a face
			vertices += getViewportCoordinates(t * model.getWorldCoordinates(vertex), min_window, max_window, min_viewport, max_viewport).asList()
			indices.append(index)
			colors += list(model.getMaterial((int)(index / 3)))
			index += 1

	# Writing to file
	try:
		f = open(file, "w")
		f.write("var vertices = {};\n".format(str(vertices)))
		f.write("var indices = {};\n".format(str(indices)))
		f.write("var colors = {};\n".format(str(colors)))
		f.close()
		print("Exported!!")
		return True
	except:
		print("Export failed...")
		return False
