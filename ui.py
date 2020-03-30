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
