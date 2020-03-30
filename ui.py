import structs, model as m, render as r

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

	# creating menu bar
	Button(optionsBar, text="Add", command=add).pack(side="left")
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

def add():
	lis = Listbox(optionsBar)
	lis.insert(0, "Cube")
	lis.insert(1, "Cube")
	lis.insert(2, "Sphere")
	lis.insert(3, "Cylinder")
	lis.pack()

def edit():
	if r.selected is None:
		return
