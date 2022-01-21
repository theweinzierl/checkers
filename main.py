from turtle import width
from game.Board import *
from game.Stone import *
from tkinter import *





window = Tk()
window.title("Checkers")

canvas = Canvas(window, width=400, height=400)



test = Board(canvas)
canvas.bind("<Button-1>", test.onClick)

test.start()
test.draw()
canvas.pack()
window.mainloop()