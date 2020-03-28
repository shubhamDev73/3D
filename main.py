import model as m, scene as s, render as r, ui

ui.setup()

scene = s.scene()
camera = scene.getCamera()
camera.setFocalLength(18)
camera.translate(0, -2, 0)
cube = m.model.cube(size=1)
scene.addModel(cube)
cube.translate(1, 0, 1)
r.render(scene, ui.canvas)

ui.start()
