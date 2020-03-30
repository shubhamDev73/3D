import structs, model as m, render as r, main

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, colorchooser

viewportSize = 512
selectedColor = "red"
defaultColor = "black"

def setup():
	
	""" Setting up the UI to be used """

	# creating global variables as they are used by other functions too
	global root, canvas, optionsBar, propertiesBar

	root = Tk()

	# configuring UI style
	style = Style()
	style.configure("TButton", foreground="red", background="white")
	style.configure("TEntry", foreground="red", background="white")
	style.configure("TMenubutton", foreground="red", background="white")

	# menu
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

	# different frames
	optionsBar = Frame(root)
	optionsBar.pack(side="top")
	propertiesBar = Frame(root)
	propertiesBar.pack(side="right")
	main = Frame(root)
	main.pack(side="bottom")

	# canvas is where the model will be shown
	canvas = Canvas(main, width=viewportSize, height=viewportSize)
	canvas.bind('<Button-1>', r.select)
	canvas.pack()

	# creating options bar

	# add menu
	objects = [func for func in dir(m.model) if type(getattr(m.model, func)) is type(m.model.cube)]
	addMenubutton = Menubutton(optionsBar, text="Add")
	addMenu = Menu(addMenubutton, tearoff=0)
	for obj in objects:
		addMenu.add_command(label=obj.capitalize(), command=lambda : add(obj))
	addMenu.add_separator()
	addMenu.add_command(label="Light")
	addMenubutton['menu'] = addMenu
	addMenubutton.pack(side="left")

	# other options
	Button(optionsBar, text="Edit", command=edit).pack(side="left")
	Button(optionsBar, text="Export", command=export).pack(side="left")
	Button(optionsBar, text="Render", command=None).pack(side="left")

	# creating properties bar

	# position
	position = Frame(propertiesBar)
	position.pack(side="top")
	Label(position, text="Position").pack(side="top")
	x = Frame(position)
	x.pack(side="top")
	Label(x, text="X: ").pack(side="left")
	Entry(x).pack(side="right")
	y = Frame(position)
	y.pack(side="top")
	Label(y, text="Y: ").pack(side="left")
	Entry(y).pack(side="right")
	z = Frame(position)
	z.pack(side="top")
	Label(z, text="Z: ").pack(side="left")
	Entry(z).pack(side="right")

	# rotation
	rotation = Frame(propertiesBar)
	rotation.pack(side="top")
	Label(rotation, text="Rotation").pack(side="top")
	x = Frame(rotation)
	x.pack(side="top")
	Label(x, text="X: ").pack(side="left")
	Entry(x).pack(side="right")
	y = Frame(rotation)
	y.pack(side="top")
	Label(y, text="Y: ").pack(side="left")
	Entry(y).pack(side="right")
	z = Frame(rotation)
	z.pack(side="top")
	Label(z, text="Z: ").pack(side="left")
	Entry(z).pack(side="right")

	# scale
	scale = Frame(propertiesBar)
	scale.pack(side="top")
	Label(scale, text="Scale").pack(side="top")
	x = Frame(scale)
	x.pack(side="top")
	Label(x, text="X: ").pack(side="left")
	Entry(x).pack(side="right")
	y = Frame(scale)
	y.pack(side="top")
	Label(y, text="Y: ").pack(side="left")
	Entry(y).pack(side="right")
	z = Frame(scale)
	z.pack(side="top")
	Label(z, text="Z: ").pack(side="left")
	Entry(z).pack(side="right")

def clear():
	canvas.delete("all")

def start():
	print("Starting UI...")
	root.mainloop()

def export():
	if r.selected is None:
		return
	file = filedialog.asksaveasfilename(initialdir="./", title="Export model", initialfile="model.js", filetypes=[('Javascript files', '*.js')])
	if file:
		r.export(file if file[-3:] == ".js" else file + ".js")

# color = colorchooser.askcolor()
def draw_line(point1, point2, selected=False):
	canvas.create_line(point1.get(0), point1.get(1), point2.get(0), point2.get(1), fill=selectedColor if selected else defaultColor)

def edit():
	if r.selected is None:
		return

def add(obj):
	model = getattr(m.model, obj)()
	main.scene.addModel(model)
	r.render(main.scene)

def updateProperties(model):
	if model:
		props = [model.getPosition(), model.getRotation(), model.getScale()]
	for i, frame in enumerate(propertiesBar.winfo_children()):
		for j, prop in enumerate(frame.winfo_children()[1:]):
			entry = prop.winfo_children()[1]
			entry.delete(0, 10)
			if model:
				entry.insert(0, props[i].get(j))
