import model as m, scene as s, render as r, ui

scene = s.scene()

if __name__ == "__main__":

	ui.setup()
	# camera = scene.getCamera()
	# camera.setFocalLength(18)
	# camera.translate(0, -20, 0)
	# cube = m.model.cube(size=1)
	# scene.addModel(cube)
	# cube.translate(1, 0, 1)
	r.render(scene)
	ui.start()
