import render as r
import tkinter as tk
from tkinter import filedialog, colorchooser

master = tk.Tk()
canvas = None

def keyPress(event):
	print(event.char)

def setup():
	global canvas
	canvas = tk.Canvas(master, width=r.viewportSize, height=r.viewportSize)
	canvas.bind('<Key>', keyPress)
	canvas.bind('<Button-1>', r.select)
	canvas.pack()
	exportButton = tk.Button(master, width=10, height=1, text="Export", command=export)
	exportButton.pack()

def start():
	master.mainloop()

def export():
	file = filedialog.asksaveasfilename(initialdir="./", title="Export model", initialfile="model.js", filetypes=[('Javascript files', '*.js')])
	if file:
		r.export(file if file[-3:] == ".js" else file + ".js")

# color = colorchooser.askcolor()
