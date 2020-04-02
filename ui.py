""" Creates the user interface """

import structs, model, render, main

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

# Global variables
# canvas: where the scene is drawn
# svs: string vars for property entry boxes
# prevVals: previous values of properties for rollback on invalid entry

viewportSize = 512
canvas = None
svs = []
prevVals = [0 for i in range(9)]

# Color to display model in
selectedColor = "red"
defaultColor = "black"

def setup():
	
	""" Setting up the UI to be used """

	# Creating global variables as they are used by other functions too
	global canvas, svs

	root = Tk()
	root.title("3D modelling software")

	# Configuring UI style
	style = Style()
	style.configure("TButton", foreground="red", background="white")
	style.configure("TEntry", foreground="red", background="white")
	style.configure("TMenubutton", foreground="red", background="white")

	# Main menu
	menuBar = Menu(root)

	fileMenu = Menu(menuBar, tearoff=0)
	fileMenu.add_command(label="New", command=None)
	fileMenu.add_command(label="Open", command=None)
	fileMenu.add_command(label="Save", command=None)
	fileMenu.add_command(label="Save As...", command=None)
	fileMenu.add_separator()
	fileMenu.add_command(label="Exit", command=root.quit)
	menuBar.add_cascade(label="File", menu=fileMenu)

	editMenu = Menu(menuBar, tearoff=0)
	editMenu.add_command(label="Undo", command=None)
	editMenu.add_command(label="Redo", command=None)
	editMenu.add_separator()
	editMenu.add_command(label="Cut", command=None)
	editMenu.add_command(label="Copy", command=None)
	editMenu.add_command(label="Paste", command=None)
	editMenu.add_command(label="Delete", command=None)
	menuBar.add_cascade(label="Edit", menu=editMenu)

	helpMenu = Menu(menuBar, tearoff=0)
	helpMenu.add_command(label="Help", command=None)
	helpMenu.add_command(label="About", command=None)
	menuBar.add_cascade(label="Help", menu=helpMenu)

	root.config(menu=menuBar)


	# Different frames
	optionsBar = Frame(root)
	optionsBar.pack(side="top")
	propertiesBar = Frame(root)
	propertiesBar.pack(side="right")
	mainWindow = Frame(root)
	mainWindow.pack(side="bottom")


	canvas = Canvas(mainWindow, width=viewportSize, height=viewportSize)
	canvas.bind('<Button-1>', render.select)
	canvas.pack()


	# Options bar

	# Add menu
	addMenubutton = Menubutton(optionsBar, text="Add")
	addMenu = Menu(addMenubutton, tearoff=0)

	# Adding all classmethods present in model.model (these are all pre-defined 3D models)
	for method in dir(model.model):
		if type(getattr(model.model, method)) is type(model.model.cube):
			addMenu.add_command(label=method.capitalize(), command=lambda modelType=method : add(modelType))

	# Placeholder for lights
	addMenu.add_separator()
	addMenu.add_command(label="Light")

	addMenubutton['menu'] = addMenu
	addMenubutton.pack(side="left")

	# Other options
	Button(optionsBar, text="Edit", command=None).pack(side="left")
	Button(optionsBar, text="Render", command=None).pack(side="left")
	Button(optionsBar, text="Export", command=export).pack(side="left")


	# Properties bar
	svs = [StringVar() for i in range(9)]
	for i, string in enumerate(("Position", "Rotation", "Scale")):
		# For each position, rotation, scale
		prop = Frame(propertiesBar)
		prop.pack(side="top")

		Label(prop, text=string).pack(side="top")

		x = Frame(prop)
		x.pack(side="top")
		Label(x, text="X: ").pack(side="left")
		Entry(x, textvariable=svs[i * 3 + 0], validate="focusout", validatecommand=lambda prop=i, sv=svs[i * 3 + 0] : transform(sv, prop, 0)).pack(side="right")

		y = Frame(prop)
		y.pack(side="top")
		Label(y, text="Y: ").pack(side="left")
		Entry(y, textvariable=svs[i * 3 + 1], validate="focusout", validatecommand=lambda prop=i, sv=svs[i * 3 + 1] : transform(sv, prop, 1)).pack(side="right")

		z = Frame(prop)
		z.pack(side="top")
		Label(z, text="Z: ").pack(side="left")
		Entry(z, textvariable=svs[i * 3 + 2], validate="focusout", validatecommand=lambda prop=i, sv=svs[i * 3 + 2] : transform(sv, prop, 2)).pack(side="right")

	return root

def start(root):

	""" Starts the UI """

	print("Starting UI...")
	root.mainloop()

def clear():

	""" Clears canvas to start drawing """

	canvas.delete("all")
	return canvas

def draw_line(point1, point2, selected=False):

	""" Draw line created by point1 and point2 on canvas using correct color """

	canvas.create_line(point1.get(0), point1.get(1), point2.get(0), point2.get(1), fill=selectedColor if selected else defaultColor)
	return canvas

def add(modelType):

	""" Adds a new model to the scene and selects it """

	createdModel = getattr(model.model, modelType)()
	main.scene.addModel(createdModel)
	render.selected = createdModel
	updateProperties(createdModel)
	render.display(main.scene)
	return createdModel

def setSvs():

	""" Updates svs """

	for i in range(9):
		svs[i].set(str(prevVals[i]) if render.selected else "")
	return svs

def setPrevVals():

	""" Updated previous value of svs """

	for i in range(9):
		prevVals[i] = float(svs[i].get())
	return prevVals

def updateProperties(obj):

	""" Updates displayed properties for the obj """

	if obj:
		props = (obj.getPosition(), obj.getRotation(), obj.getScale())

	# Getting correct entry box stringvar to update
	for i in range(3):
		for j in range(3):
			svs[i * 3 + j].set(str(props[i].get(j)) if obj else "")

	if obj:
		setPrevVals()

	return props if obj else None

def transform(sv, prop, axis):

	""" Transforms selected model based on updated value of sv """

	valid = True
	if render.selected is None:
		valid = False

	try:
		val = float(sv.get())
	except:
		valid = False

	if valid is False:
		# Invalid input. Revert back displayed sv
		setSvs()
		return False

	vector = [float(svs[prop * 3 + i].get()) for i in range(3)]
	vector[axis] = val
	getattr(render.selected, "set{}".format(("Position", "Rotation", "Scale")[prop]))(*vector)
	render.display(main.scene)
	setPrevVals()
	# Display in correct notation (1.0 instead of 1)
	setSvs()

	return True

def export():

	""" Opens file dialog to select file and calls render.export function """

	if render.selected is None:
		return

	file = filedialog.asksaveasfilename(initialdir="./", title="Export model", initialfile="model.js", filetypes=[('Javascript files', '*.js')])
	if file:
		# Save in js format only
		render.export(file if file[-3:] == ".js" else file + ".js")

	return file
