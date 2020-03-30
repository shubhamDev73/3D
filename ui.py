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
	global root, canvas, menuBar, propertiesBar

	root = Tk()

	# configuring UI style
	style = Style()
	style.configure("TButton", foreground="red", background="white")
	style.configure("TEntry", foreground="red", background="white")

	# different frames
	menuBar = Frame(root)
	menuBar.pack(side="top")
	propertiesBar = Frame(root)
	propertiesBar.pack(side="right")
	main = Frame(root)
	main.pack(side="bottom")

	# canvas is where the model will be shown
	canvas = Canvas(main, width=viewportSize, height=viewportSize)
	canvas.bind('<Button-1>', r.select)
	canvas.pack()

	# creating menu bar
	Button(menuBar, text="Add", command=add).pack(side="left")
	Button(menuBar, text="Edit", command=edit).pack(side="left")
	Button(menuBar, text="Export", command=export).pack(side="left")
	Button(menuBar, text="Render", command=None).pack(side="left")

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
	lis = Listbox(menuBar)
	lis.insert(0, "Cube")
	lis.insert(1, "Cube")
	lis.insert(2, "Sphere")
	lis.insert(3, "Cylinder")
	lis.pack()

def edit():
	if r.selected is None:
		return
