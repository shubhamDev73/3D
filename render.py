import structs, ui

selected = None

triangles = []
scene = None

def render(_scene):
	global scene, triangles
	scene = _scene
	camera = scene.getCamera()
	min_window = structs.vector(0, 0)
	max_window = structs.vector(scene.getWorldSize(), scene.getWorldSize())
	min_viewport = structs.vector(0, ui.viewportSize)
	max_viewport = structs.vector(ui.viewportSize, 0)
	ui.clear()
	triangles = []
	for model in scene.getModels():
		for face in model.getFaces():
			projection = (camera.project(camera.getViewCoordinates(model.getWorldCoordinates(face[i]))) for i in range(3))
			projection = tuple(map(lambda vector: getViewportCoordinates(vector, min_window, max_window, min_viewport, max_viewport), projection))
			ui.draw_line(projection[0], projection[1], selected is model)
			ui.draw_line(projection[1], projection[2], selected is model)
			# ui.draw_line(projection[2], projection[0], selected is model)
			triangles.append((projection[0], projection[1], projection[2], model))

def getViewportCoordinates(projectionCoordinates, min_window, max_window, min_viewport, max_viewport):
	x = (max_viewport.get(0) - min_viewport.get(0)) / (max_window.get(0) - min_window.get(0))
	y = (max_viewport.get(1) - min_viewport.get(1)) / (max_window.get(1) - min_window.get(1))
	s = structs.vector(x, y)
	return projectionCoordinates.translate(min_window * -1).scale(s).translate(min_viewport)

def select(event):
	global selected
	selected = None
	clickPoint = structs.vector(event.x, event.y)
	for v0, v1, v2, model in triangles:
		if sameSide(v0, v1, v2, clickPoint) and sameSide(v1, v2, v0, clickPoint) and sameSide(v2, v0, v1, clickPoint):
			selected = model
			break
	ui.updateProperties(selected)
	render(scene)

def sameSide(point1, point2, referencePoint, checkPoint):
	if point2.get(0) == point1.get(0):
		ref = referencePoint.get(0) - point2.get(0)
		check = checkPoint.get(0) - point2.get(0)
	else:
		slope = (point2.get(1) - point1.get(1)) / (point2.get(0) - point1.get(0))
		ref = (referencePoint.get(1) - point2.get(1)) - slope * (referencePoint.get(0) - point2.get(0))
		check = (checkPoint.get(1) - point2.get(1)) - slope * (checkPoint.get(0) - point2.get(0))
	return ref * check > 0

def export(file):
	model = selected
	if model is None:
		return
	print("Exporting {} to {}".format(str(model), file))
	t = structs.matrix.identity(4)
	t.insert(1, 1, 0)
	t.insert(1, 2, 1)
	t.insert(2, 2, 0)
	t.insert(2, 1, 1)
	vertices = []
	indices = []
	colors = []
	index = 0
	for face in model.getFaces():
		for vertex in face:
			vertices += (t * model.getWorldCoordinates(vertex) / scene.getWorldSize()).translate(structs.vector(-1, -1)).asList()
			indices.append(index)
			colors += list(model.getMaterial((int)(index / 3)))
			index += 1
	f = open(file, "w")
	f.write("var vertices = {};\n".format(str(vertices)))
	f.write("var indices = {};\n".format(str(indices)))
	f.write("var colors = {};\n".format(str(colors)))
	f.close()
	print("Exported!!")
