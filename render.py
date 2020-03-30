import structs, ui

selected = None

triangles = []
scene = None

def render(_scene):
	global scene
	scene = _scene
	camera = scene.getCamera()
	min_window = structs.vector(0, 0)
	max_window = structs.vector(scene.getWorldSize(), scene.getWorldSize())
	min_viewport = structs.vector(0, ui.viewportSize)
	max_viewport = structs.vector(ui.viewportSize, 0)
	ui.clear()
	triangles.clear()
	for model in scene.getModels():
		for face in model.getFaces():
			v0 = model.getVertex(face[0])
			v1 = model.getVertex(face[1])
			v2 = model.getVertex(face[2])
			v0 = project(getViewCoordinates(getWorldCoordinates(v0, model), camera), camera)
			v1 = project(getViewCoordinates(getWorldCoordinates(v1, model), camera), camera)
			v2 = project(getViewCoordinates(getWorldCoordinates(v2, model), camera), camera)
			v0 = getViewportCoordinates(v0, min_window, max_window, min_viewport, max_viewport)
			v1 = getViewportCoordinates(v1, min_window, max_window, min_viewport, max_viewport)
			v2 = getViewportCoordinates(v2, min_window, max_window, min_viewport, max_viewport)
			ui.draw_line(v0, v1, selected is model)
			ui.draw_line(v1, v2, selected is model)
			# ui.draw_line(v2, v0, selected is model)
			triangles.append((v0, v1, v2, model))

def getWorldCoordinates(modelCoordinates, model):
	position = model.getPosition()
	# TODO: implement rotation
	rotation = model.getRotation()
	return structs.translate(modelCoordinates, position.get(0), position.get(1), position.get(2))

def getViewCoordinates(worldCoordinates, camera):
	position = camera.getPosition()
	rotation = camera.getRotation()
	# TODO: implement rotation, fill u, v, n
	u = structs.vector.direction(0) * -1
	v = structs.vector.direction(2) * -1
	n = structs.vector.direction(1)

	r = structs.matrix.identity(4)
	for i in range(3):
		r.insert(0, i, u.get(i))
		r.insert(1, i, v.get(i))
		r.insert(2, i, n.get(i))
	return r * structs.translate(worldCoordinates, -position.get(0), -position.get(1), -position.get(2))

def project(viewCoordinates, camera):
	if camera.isPerspective():
		p = structs.matrix.identity(4)
		# zv = camera.getPosition().get(2)
		# zp = camera.getPosition().get(2) - camera.getFocalLength()
		# d = zp - zv
		# p.insert(2, 2, zv / d)
		# p.insert(2, 3, -zv * (zp / d))
		# p.insert(3, 2, 1.0 / d)
		# p.insert(3, 3, -zp / d)
		p.insert(2, 2, 0)
		p.insert(3, 2, -1.0 / camera.getFocalLength())
		p.insert(3, 3, -1.0)
		v = p * viewCoordinates
		return structs.vector(v.get(0) / v.get(3), v.get(1) / v.get(3))
	else:
		return structs.vector(viewCoordinates.get(0), viewCoordinates.get(1))

def getViewportCoordinates(projectionCoordinates, min_window, max_window, min_viewport, max_viewport):
	x = (max_viewport.get(0) - min_viewport.get(0)) / (max_window.get(0) - min_window.get(0))
	y = (max_viewport.get(1) - min_viewport.get(1)) / (max_window.get(1) - min_window.get(1))
	return structs.translate(
		structs.scale(
			structs.translate(projectionCoordinates, -min_window.get(0), -min_window.get(1)), 
			x=x, y=y), 
		min_viewport.get(0), min_viewport.get(1))

def sameSide(point1, point2, referencePoint, checkPoint):
	if point2.get(0) == point1.get(0):
		ref = referencePoint.get(0) - point2.get(0)
		check = checkPoint.get(0) - point2.get(0)
	else:
		slope = (point2.get(1) - point1.get(1)) / (point2.get(0) - point1.get(0))
		ref = (referencePoint.get(1) - point2.get(1)) - slope * (referencePoint.get(0) - point2.get(0))
		check = (checkPoint.get(1) - point2.get(1)) - slope * (checkPoint.get(0) - point2.get(0))
	return ref * check > 0

def select(event):
	global selected
	selected = None
	clickPoint = structs.vector(event.x, event.y)
	for v0, v1, v2, model in triangles:
		if sameSide(v0, v1, v2, clickPoint) and sameSide(v1, v2, v0, clickPoint) and sameSide(v2, v0, v1, clickPoint):
			selected = model
			break
	render(scene)

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
			vertices += structs.translate(t * getWorldCoordinates(model.getVertex(vertex), model) / scene.getWorldSize(), -1, -1).toList()
			indices.append(index)
			colors += list(model.getMaterial((int)(index / 3)))
			index += 1
	f = open(file, "w")
	f.write("var vertices = {};\n".format(str(vertices)))
	f.write("var indices = {};\n".format(str(indices)))
	f.write("var colors = {};\n".format(str(colors)))
	f.close()
	print("Exported!!")
