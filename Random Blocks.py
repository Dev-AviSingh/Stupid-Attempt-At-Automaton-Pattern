import random
import tkinter as tk
from threading import Thread
root = tk.Tk()

class Block(object):
	def __init__(self, initialColour = 0x000000, canvas = None, size = 50, position = (0, 0), addition = False):
		self.canvas = canvas
		self.size = size
		self.position = position
		self.colour = initialColour
		self.stringColour = "#" + str(initialColour)[2:].zfill(6)
		self.sprite = None
		self.blockMatrix = None
		self.blockAbove = None
		self.blockBelow = None
		self.blockLeft = None
		self.blockRight = None
		self.addition = addition
		self.colour = random.randint(0, 16777215)

	def draw(self, position = None):
		if position != None:
			self.position = position

		x = self.position[0] * self.size
		y = self.position[1] * self.size

		self.sprite = self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill = self.stringColour)

	def setBlockMatrix(self, blockMatrix):
		self.blockMatrix = blockMatrix
		row, column = self.position[0], self.position[1]
		if row != 0:
			self.blockAbove = self.blockMatrix[row - 1][column]

		if row != len(self.blockMatrix) - 1:
			self.blockBelow = self.blockMatrix[row + 1][column] 

		if column != 0:
			self.blockLeft = self.blockMatrix[row][column - 1]

		if column != len(self.blockMatrix[0]) - 1:
			self.blockRight = self.blockMatrix[row][column + 1] 

		
	def changeColour(self, colour = None):
		#self.colour = random.randint(0, 16777215)
		
		# Cartesian format addition
		if self.addition:
			if self.blockAbove != None:
				self.colour -= self.blockAbove.colour

			if self.blockLeft != None:
				self.colour -= self.blockLeft.colour

			# If instead of these while true block you cap the limits from 0 to 16777215, you get a checkerboard pattern because the only colours eventually left are black and white because of 1 and 16777215 respectively. 
			while True:
				if self.colour < 0:
					self.colour = 16777215 - self.colour
				else:
					break

			if self.blockBelow != None:
				self.colour += self.blockBelow.colour

			if self.blockRight != None:
				self.colour += self.blockRight.colour

			while True:
				if self.colour > 16777215:
					self.colour = self.colour - 16777215
				else:
					break
		
		'''
		# Division
		if self.blockAbove != None:
			self.colour += self.colour % max(1, self.blockAbove.colour)

		if self.blockLeft != None:
			self.colour -= self.blockLeft.colour * self.colour

		self.colour = max(0, self.colour)

		if self.blockBelow != None:
			print(type(self.blockBelow.colour), type(self.colour))
			self.colour += self.colour % max(1, self.blockBelow.colour)

		if self.blockRight != None:
			self.colour += self.blockRight.colour * self.colour

		self.colour = min(self.colour, 16777215)
		'''

		self.stringColour = "#" + str(hex(self.colour))[2:].zfill(6)

class Frame(tk.Frame):
	def __init__(self, master = None, size = 250, matrixSize = 5, interval = 166, addition = False):
		super().__init__(master = master)
		self.master = master
		self.size = (size, size)
		self.matrixSize = matrixSize
		self.blockSize = size / matrixSize
		self.blockMatrix = []
		self.interval = interval
		self.controllerWidth = 100
		self.killYourself = False
		self.addition = addition
		self['bg'] = "black"
		self.master['bg'] = "black"
		self.place(x = 0, y = 0, width = size + self.controllerWidth, height = size)
		self.master.geometry("{}x{}".format(size + self.controllerWidth, size))


		self.canvas = tk.Canvas(master = self, bg = "black", bd = 0)
		self.canvas.place(x = 0, y = 0, width = size, height = size)

		self.canvasSizeController = tk.Scale(master = self, from_=100, to = 1000, orient = tk.VERTICAL, bg="black", fg = "#eeeeee", length = (size - 50) // 2, tickinterval = 100)
		self.matrixSizeController = tk.Scale(master = self, from_=1, to = 100, orient = tk.VERTICAL, bg="black", fg = "#eeeeee", length = (size - 50) // 2, tickinterval = 10)

		self.canvasSizeController.place(x = size, y = 0, width = self.controllerWidth)
		matrixSizeControllerPosition = (size - 50) // 2
		self.matrixSizeController.place(x = size, y = matrixSizeControllerPosition, width = self.controllerWidth)

		self.canvasSizeController.set(size)
		self.matrixSizeController.set(self.matrixSize)

		self.additionCheckbox = tk.Checkbutton(master = self, text = "Addition",relief = "flat", bg = "black", fg = "red",command = self.changeAdditionState)
		self.additionCheckbox.place(x = size, y = size - 25)

		if addition:
			self.additionCheckbox.select()

		self.changeValuesButton = tk.Button(master = self, bg = "black", fg = "white", text = "Update", command = self.updateDimensions)
		self.changeValuesButton.place(x = size, y = size - 50, width = self.controllerWidth, height = 25)

		self.generateBlocks()
		self.update()

	def changeAdditionState(self):
		self.addition = not self.addition
		print("Changing addition state")

	def updateDimensions(self):
		canvasSize = self.canvasSizeController.get()
		matrixWidth = self.matrixSizeController.get()
		interval = self.interval

		root = tk.Tk()
		frame = Frame(master = root, size = canvasSize, matrixSize = matrixWidth, interval = interval, addition = self.addition)

		self.killYourself = True
		#print(self.killYourself)
		Thread(target = root.mainloop(), args = ()).start()

	def generateBlocks(self):
		for x in range(self.matrixSize):
			row = []
			for y in range(self.matrixSize):
				row.append(Block(canvas = self.canvas, position = (x, y), size = self.blockSize, addition = self.addition))
			self.blockMatrix.append(row)

		for x in range(self.matrixSize):
			for y in range(self.matrixSize):
				self.blockMatrix[y][x].setBlockMatrix(self.blockMatrix)

	def update(self):
		if self.killYourself:
			print("Killing myself")
			self.master.destroy()

		self.canvas.delete('all')
		for row in self.blockMatrix:
			for block in row:
				block.changeColour()
				block.draw()

		print("Addition :", self.addition)
		self.canvas.after(self.interval, self.update)

root = tk.Tk()
s = 500
frame = Frame(master = root, size = s, matrixSize = 5, interval = 1000)
frame.mainloop()
