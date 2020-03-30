import model as m, scene as s, render as r, ui

scene = s.scene()

if __name__ == "__main__":

	ui.setup()
	r.render(scene)
	ui.start()
