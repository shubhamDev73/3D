""" Creates the user interface """

import structs, model as m, render as r, main

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

# Global variables

viewportSize = 512
svs = []
prevVals = [0 for i in range(9)]
canvas = None

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
	fileMenu.add_command(label="Save as...", command=None)
	fileMenu.add_command(label="Close", command=None)
	fileMenu.add_separator()
	fileMenu.add_command(label="Exit", command=root.quit)
	menuBar.add_cascade(label="File", menu=fileMenu)

	editMenu = Menu(menuBar, tearoff=0)
	editMenu.add_command(label="Undo", command=None)
	editMenu.add_separator()
	editMenu.add_command(label="Cut", command=None)
	editMenu.add_command(label="Copy", command=None)
	editMenu.add_command(label="Paste", command=None)
	editMenu.add_command(label="Delete", command=None)
	editMenu.add_command(label="Select All", command=None)
	menuBar.add_cascade(label="Edit", menu=editMenu)

	helpMenu = Menu(menuBar, tearoff=0)
	helpMenu.add_command(label="Help Index", command=None)
	helpMenu.add_command(label="About...", command=None)
	menuBar.add_cascade(label="Help", menu=helpMenu)

	root.config(menu=menuBar)


	# Different frames
	optionsBar = Frame(root)
	optionsBar.pack(side="top")
	propertiesBar = Frame(root)
	propertiesBar.pack(side="right")
	mainWindow = Frame(root)
	mainWindow.pack(side="bottom")


	# canvas is where the model will be shown
	canvas = Canvas(mainWindow, width=viewportSize, height=viewportSize)
	canvas.bind('<Button-1>', r.select)
	canvas.pack()


	# Options bar

	# Add menu
	addMenubutton = Menubutton(optionsBar, text="Add")
	addMenu = Menu(addMenubutton, tearoff=0)

	# List of all classmethods in model.model (these are all pre-defined 3D models)
	objects = [method for method in dir(m.model) if type(getattr(m.model, method)) is type(m.model.cube)]
	for obj in objects:
		addMenu.add_command(label=obj.capitalize(), command=lambda obj=obj : add(obj))

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

def add(model):

	""" Adds a new model to the scene and selects it """

	createdModel = getattr(m.model, model)()
	main.scene.addModel(createdModel)
	r.selected = createdModel
	updateProperties(createdModel)
	r.display(main.scene)
	return createdModel

def setSvs():

	""" Updates svs """

	for i in range(9):
		svs[i].set(str(prevVals[i]) if r.selected else "")
	return svs

def setPrevVals():

	""" Updated previous value of svs """

	for i in range(9):
		prevVals[i] = float(svs[i].get())
	return prevVals

def updateProperties(model):

	""" Updates displayed properties for the model """

	if model:
		props = [model.getPosition(), model.getRotation(), model.getScale()]

	# Getting correct entry box stringvar to update
	for i in range(3):
		for j in range(3):
			svs[i * 3 + j].set(str(props[i].get(j)) if model else "")

	if model:
		setPrevVals()

	return props if model else None

def transform(sv, prop, axis):

	""" Transforms selected model based on updated value of sv """

	valid = True
	if r.selected is None:
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
	getattr(r.selected, "set{}".format(("Position", "Rotation", "Scale")[prop]))(*vector)
	r.display(main.scene)
	setPrevVals()
	# Display in correct notation (1.0 instead of 1)
	setSvs()

	return True

def export():

	""" Opens file dialog to select file and calls render.export function """

	if r.selected is None:
		return

	file = filedialog.asksaveasfilename(initialdir="./", title="Export model", initialfile="model.js", filetypes=[('Javascript files', '*.js')])
	if file:
		# Save in js format only
		r.export(file if file[-3:] == ".js" else file + ".js")

	return file
