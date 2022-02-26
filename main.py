# Dient als Einstiegspunkt. Zeigt das Hauptfenster an und startet die Mainloop von Tkinter.

from game.Board import *
from game.Stone import *
from tkinter import *

window = Tk()
window.title("Simple Checkers")
canvasMenu = None
canvasScore = None
canvasBoard = None
board = None


def showMenu() -> None:
    global canvasMenu, canvasBoard, canvasScore, board

    if canvasMenu is None:
        canvasMenu = Canvas(window, width=400, height=400)

        title = Label(canvasMenu, text="Simple-Checkers", font=("bold", 30))
        
        btnBotGame = Button(canvasMenu, text="Starte KI gegen KI", width=40,
                    height=3, bd="3", command=lambda: showGame(Board.Mode.BotGame))
        btn1on1 = Button(canvasMenu, text="Starte Mensch gegen KI", width=40,
                    height=3, bd="3", command=lambda: showGame(Board.Mode.OneOnOne))
  
        title.pack()
        btnBotGame.pack()
        btn1on1.pack()
    
    if not canvasBoard is None:
        canvasBoard.pack_forget()
        del board
        board = None

    if not canvasScore is None:
        canvasScore.pack_forget()

    canvasMenu.pack()

def showGame(mode: Board.Mode) -> None:
    global canvasMenu, canvasBoard, canvasScore, board

    if canvasBoard is None:
        
        canvasScore = Canvas(window, width=400, height=200)

        btnCancel = Button(canvasScore, text="Zurück", width=40,
                    height=3, bd="3", command=showMenu)

        # btnCancel.pack() > Zurück-Funktion macht leider Probleme > erzeugt "Geister-Spieler"
        

    if not canvasMenu is None:
        canvasMenu.pack_forget()

    canvasBoard = Canvas(window, width=400, height=400)
    board = Board(canvasBoard, mode, window)
    canvasBoard.bind("<Button-1>", board.onClick)
    board.start()
    
    #canvasScore.pack()
    canvasBoard.pack()

showMenu()
window.mainloop()
