from game.Board import *
from game.Stone import *
from tkinter import *

window = Tk()
window.title("Checkers")
canvas = Canvas(window, width=400, height=400)
board = Board(canvas)
canvas.bind("<Button-1>", board.onClick)
board.start()
board.draw()
canvas.pack()
window.mainloop()