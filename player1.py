"""
Name: Jason Lee
UCINetID: 40445771
"""
import socket
import tkinter as tk
from gameboard import BoardClass

"""DISCLAIMER:
The code was created and tested on a Mac. The GUI looks different when ran on Windows.
"""

class Player1():
    """A class to store and handle information about player 1.
    """
    def __init__(self) -> None:
        """Function to initialize a variable for the socket connection.
        
        The socket connection can be used anywhere in Player1 class.
        """
        self.connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def createGUI(self) -> None:
        """Function to initialize the GUI window and starting widgets.
        
        Creates the widgets that prompts the user to connect to player 2. Asks user for port
        and IP address of player 2.
        """
        self.window = tk.Tk()
        self.window.title("Player 1 Tic-Tac-Toe")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        #IP address and port
        self.hostLabel = tk.Label(self.window, text="IP address") 
        self.hostLabel.pack()
        self.hostInput = tk.StringVar(self.window)
        self.hostEntry = tk.Entry(self.window, textvariable=self.hostInput)
        self.hostEntry.pack()

        self.portLabel = tk.Label(self.window, text="Port number") 
        self.portLabel.pack()
        self.portInput = tk.StringVar(self.window)
        self.portEntry = tk.Entry(self.window, textvariable=self.portInput)
        self.portEntry.pack()

        self.hostPortBtn = tk.Button(self.window, text="Enter", command=self.establishConnection)
        self.hostPortBtn.pack()

        self.connectionTextVar = tk.StringVar(self.window)
        self.connectionLabel = tk.Label(self.window, textvariable=self.connectionTextVar)
        self.connectionLabel.pack()

        self.yesBtn = tk.Button(self.window, text="Yes", command=self.tryAgain)
        self.noBtn = tk.Button(self.window, text="No", command=self.window.quit)

        self.window.mainloop()

    def establishConnection(self) -> None:
        """Establishes the socket connection to player 2.
        
        Binds the IP address and port number of player 2 and then attempts to connect.
        """
        host = self.hostInput.get()
        port = self.portInput.get()
        self.connectionTextVar.set(" ")
        try:
            self.connectionSocket.connect((host,int(port)))
            self.hostPortBtn["state"] = "disabled"
            self.hostEntry["state"] = "disabled"
            self.portEntry["state"] = "disabled"
            self.connectionTextVar.set("Connection successful!")
            self.window.update_idletasks()
            self.window.after(1000)
            self.removeHostPortWidgets()
            self.createUsernameWidgets()
            
        except:
            self.hostPortBtn["state"] = "disabled"
            self.connectionTextVar.set("Connection failed. Do you want to try again?")
            self.yesBtn.place(x=225, y=150)
            self.noBtn.place(x=320, y=150)

    def tryAgain(self) -> None:
        """Failing to connect to player 2.
        
        Asks the user if they want to attempt to connect to player 2 again.
        """
        self.hostPortBtn["state"] = "normal"
        self.connectionTextVar.set("Please try again.")
        self.yesBtn.place_forget()
        self.noBtn.place_forget()

    def removeHostPortWidgets(self) -> None:
        """Remove all widgets that prompts for IP address and port.
        """
        self.hostLabel.pack_forget()
        self.portLabel.pack_forget()
        self.hostEntry.pack_forget()
        self.portEntry.pack_forget()
        self.hostPortBtn.pack_forget()
        self.connectionLabel.pack_forget()

    def createUsernameWidgets(self) -> None:
        """Create widgets that prompts user for username.
        
        Widgets to ask player 1 to enter an alphanumeric username to send to player 2.
        """
        self.usernameLabel = tk.Label(self.window, text="Enter an alphanumeric username")
        self.usernameLabel.pack()

        self.p1username = tk.StringVar(self.window)
        self.usernameEntry = tk.Entry(self.window, textvariable=self.p1username)
        self.usernameEntry.pack()
        
        self.usernameBtn = tk.Button(self.window, text="Enter", command=self.sendUserName)
        self.usernameBtn.pack()

        self.usernameCheckVar = tk.StringVar(self.window)
        self.usernameCheck = tk.Label(self.window, textvariable=self.usernameCheckVar)

    def removeUsernameWidgets(self) -> None:
        """Remove all widgets that prompts user for username.
        """
        self.usernameLabel.pack_forget()
        self.usernameEntry.pack_forget()
        self.usernameBtn.pack_forget()
        self.usernameCheck.pack_forget()

    def sendUserName(self) -> None:
        """Sends username to player 2.

        Takes the user inputted username and checks that it is alphanumeric. Sends valid username
        to player 2. Prompts user to try again if username is invalid.
        """
        self.usernameCheckVar.set("")
        self.window.update_idletasks()

        if self.p1username.get().isalnum():
            self.connectionSocket.sendall(self.p1username.get().encode())
            player1Board.player1Name = self.p1username.get()
            self.usernameBtn["state"] = "disabled"
            self.removeUsernameWidgets()
            self.receiveUserName()

        else:
            self.usernameCheckVar.set("Invalid username. Please try again.")
            self.usernameCheck.pack()

    def receiveUserName(self) -> None:
        """Receives player 2's username via sockets.
        
        Receiving player 2's username. Once received, the game board is drawn and the game begins.
        """
        self.usernameTextVar = tk.StringVar(self.window)
        self.receiveUsernameText = tk.Label(self.window, textvariable=self.usernameTextVar)
        self.usernameTextVar.set("Waiting for player 2 to send their username...")
        self.receiveUsernameText.pack()
        self.window.update_idletasks()
        self.window.after(500)
        player1Board.player2Name = self.connectionSocket.recv(1024).decode()
        self.removeUsernameWidgets()
        self.usernameTextVar.set("You are playing against: "+ player1Board.player2Name + "\nYou are X")
        self.playerTurnVar = tk.StringVar(self.window)
        self.playerTurnLabel = tk.Label(self.window, textvariable=self.playerTurnVar)
        self.playerTurnLabel.pack()
        self.playerTurnVar.set("Your turn to make a move...")
        self.drawGameBoard()

    def drawGameBoard(self) -> None:
        """Drawing the game board.
        
        Draws the tic tac toe game board grid using lines on canvas. Positions on the board are
        created using buttons.
        """
        self.canvas = tk.Canvas(self.window, width=500, height=500, borderwidth=5, bg="white")
        self.canvas.pack()

        self.canvas.create_line(200,100,200,400, fill="black", width=5)
        self.canvas.create_line(300,100,300,400, fill="black", width=5)

        self.canvas.create_line(100,200,400,200, fill="black", width=5)
        self.canvas.create_line(100,300,400,300, fill="black", width=5)

        self.btn1 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("1"))
        self.btn1.place(x=105, y=105)
        self.btn2 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("2"))
        self.btn2.place(x=208, y=105)
        self.btn3 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("3"))
        self.btn3.place(x=310, y=105)
        
        self.btn4 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("4"))
        self.btn4.place(x=105, y=206)
        self.btn5 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("5"))
        self.btn5.place(x=208, y=206)
        self.btn6 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("6"))
        self.btn6.place(x=310, y=206)

        self.btn7 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("7"))
        self.btn7.place(x=105, y=307)
        self.btn8 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("8"))
        self.btn8.place(x=208, y=307)
        self.btn9 = tk.Button(self.canvas, borderwidth=0, width=6, height=5, command=lambda:self.sendMove("9"))
        self.btn9.place(x=310, y=307)

        self.listOfBtns = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8, self.btn9]

    def sendMove(self, position: str) -> None:
        """Sends move played to player 2.
        
        Using the buttons on the game board, player 1 plays a move and it is sent to player 2.
        The move is drawn on the game board.
        """
        player1Board.updateGameBoard(int(position), 'player1')
        self.disableGameBoard()
        self.listOfBtns[int(position)-1].place_forget()
        self.drawX(position)
        self.window.update_idletasks()
        self.window.after(100)
        self.connectionSocket.sendall(position.encode())

        if player1Board.isWinner('player1'):
            self.youWin()
        elif player1Board.boardIsFull():
            self.tieGame()
        else:
            self.receiveMove()

    def receiveMove(self) -> None:
        """Receives the move played by player 2.
        
        Once player 1 sends a move, it will wait for player 2 to send a move.
        Draws the move player 2 sent on the game board.
        """
        self.playerTurnVar.set(f"Waiting for {player1Board.player2Name} to make a move...")
        self.window.update_idletasks()
        self.window.after(100)
        position = self.connectionSocket.recv(1024).decode()
        player1Board.updateGameBoard(int(position), 'player2')
        self.listOfBtns[int(position)-1].place_forget()
        self.drawO(position)

        if player1Board.isWinner('player2'):
            self.youLose()
        elif player1Board.boardIsFull():
            self.tieGame()
        else:
            self.enableGameBoard()
            self.playerTurnVar.set("Your turn to make a move...")

    def disableGameBoard(self) -> None:
        """Disabling buttons on the game board.
        
        Disables the buttons on the game board so moves cannot be played while waiting for
        player 2 to send a move.
        """
        for btn in self.listOfBtns:
            btn['state'] = "disabled"
    
    def enableGameBoard(self) -> None:
        """Enables buttons on the game board.
        
        Re-enable the buttons on the game board once a move has been received.
        """
        for btn in self.listOfBtns:
            btn['state'] = "normal"

    def drawX(self, position: str) -> None:
        """Draw X moves on the game board.
        
        When player 1 plays a move, an X is draw on the position where the move was played.
        """
        if position == "1":
            self.canvas.create_text(150, 150, text="X", fill="black", font=('Helvetica 100 bold'))
        elif position == "2":
            self.canvas.create_text(250, 150, text="X", fill="black", font=('Helvetica 100 bold'))
        elif position == "3":
            self.canvas.create_text(350, 150, text="X", fill="black", font=('Helvetica 100 bold'))
        elif position == "4":
            self.canvas.create_text(150, 250, text="X", fill="black", font=('Helvetica 100 bold'))
        elif position == "5":
            self.canvas.create_text(250, 250, text="X", fill="black", font=('Helvetica 100 bold'))
        elif position == "6":
            self.canvas.create_text(350, 250, text="X", fill="black", font=('Helvetica 100 bold'))
        elif position == "7":
            self.canvas.create_text(150, 350, text="X", fill="black", font=('Helvetica 100 bold'))
        elif position == "8":
            self.canvas.create_text(250, 350, text="X", fill="black", font=('Helvetica 100 bold'))
        elif position == "9":
            self.canvas.create_text(350, 350, text="X", fill="black", font=('Helvetica 100 bold'))
    
    def drawO(self, position: str) -> None:
        """Draw O moves on the game board.
        
        When player 2 sends a move, an O is draw on the position where the move was played.
        """
        if position == "1":
            self.canvas.create_text(150, 150, text="O", fill="black", font=('Helvetica 100 bold'))
        elif position == "2":
            self.canvas.create_text(250, 150, text="O", fill="black", font=('Helvetica 100 bold'))
        elif position == "3":
            self.canvas.create_text(350, 150, text="O", fill="black", font=('Helvetica 100 bold'))
        elif position == "4":
            self.canvas.create_text(150, 250, text="O", fill="black", font=('Helvetica 100 bold'))
        elif position == "5":
            self.canvas.create_text(250, 250, text="O", fill="black", font=('Helvetica 100 bold'))
        elif position == "6":
            self.canvas.create_text(350, 250, text="O", fill="black", font=('Helvetica 100 bold'))
        elif position == "7":
            self.canvas.create_text(150, 350, text="O", fill="black", font=('Helvetica 100 bold'))
        elif position == "8":
            self.canvas.create_text(250, 350, text="O", fill="black", font=('Helvetica 100 bold'))
        elif position == "9":
            self.canvas.create_text(350, 350, text="O", fill="black", font=('Helvetica 100 bold'))

    def removeGameBtns(self) -> None:
        """Remove all game board buttons.
        
        When the game is over, all buttons are removed from the game board.
        """
        for i in range(9):
            self.listOfBtns[i].place_forget()

    def youWin(self) -> None:
        """Player 1 wins.
        
        Removes the canvas and all text on the window. Prompts the user to play again.
        """
        player1Board.numGames += 1
        player1Board.numWins += 1
        self.canvas.create_text(260,50, text="You Win!", fill="green", font=('Helvetica 80 bold'))
        self.removeGameBtns()
        self.window.update_idletasks()
        self.window.after(2000)
        self.promptPlayAgain()

    def youLose(self) -> None:
        """Player 1 loses.
        
        Removes the canvas and all text on the window. Prompts the user to play again.
        """
        player1Board.numGames += 1
        player1Board.numLosses += 1
        self.canvas.create_text(260,50, text="You Lose!", fill="red", font=('Helvetica 80 bold'))
        self.removeGameBtns()
        self.window.update_idletasks()
        self.window.after(2000)
        self.promptPlayAgain()

    def tieGame(self) -> None:
        """Tie game.
        
        Removes the canvas and all text on the window. Prompts the user to play again.
        """
        player1Board.numGames += 1
        player1Board.numTies += 1
        self.canvas.create_text(260,50, text="Tie Game!", fill="blue", font=('Helvetica 80 bold'))
        self.removeGameBtns()
        self.window.update_idletasks()
        self.window.after(2000)
        self.promptPlayAgain()
    
    def promptPlayAgain(self) -> None:
        """Prompts user to play again.
        
        Creates a menu that asks player 1 if they want to play again.
        """
        self.canvas.create_rectangle(150,180,350,310, fill="white", outline='black')
        self.canvas.create_text(250,200, text="Do you want to play again?", fill="black", font=('Helvetica 16'))
        self.yesPlayAgainBtn = tk.Button(self.canvas, text="Yes", highlightbackground="white", command=self.playAgain)
        self.noPlayAgainBtn = tk.Button(self.canvas, text="No", highlightbackground="white", command=self.endGame)
        self.yesPlayAgainBtn.place(x=220, y=220)
        self.noPlayAgainBtn.place(x=222, y=260)

    def playAgain(self) -> None:
        """Restarts game.
        
        Tells player 2 to play again via socket. Re-draw game board and reset moves.
        """
        self.connectionSocket.sendall('Play Again'.encode())
        player1Board.resetGameBoard()
        self.yesPlayAgainBtn.place_forget()
        self.noPlayAgainBtn.place_forget()
        self.canvas.destroy()
        self.playerTurnVar.set("Your turn to make a move...")
        self.drawGameBoard()

    def endGame(self) -> None:
        """Game ends.
        
        Tells player 2 game is over via socket. Displays the game statisics.
        """
        self.connectionSocket.sendall('Fun Times'.encode())
        self.receiveUsernameText.pack_forget()
        self.playerTurnLabel.pack_forget()
        self.canvas.destroy()
        self.endGameHeader = tk.Label(self.window, text="-----Game Statistics-----")
        self.endGameHeader.pack()
        self.statisticsText = tk.Label(self.window, text=f'Player 1 Username: {player1Board.computeStats()[0]}\nPlayer 2 Username: {player1Board.computeStats()[1]}\nTotal number of games: {player1Board.computeStats()[2]}\nNumber of wins: {player1Board.computeStats()[3]}\nNumber of losses: {player1Board.computeStats()[4]}\nNumber of ties: {player1Board.computeStats()[5]}')
        self.statisticsText.pack()

    def startGame(self) -> None:
        """Function to start game.
        """
        self.createGUI()

if __name__ == "__main__":
    player1 = Player1() 
    player1Board = BoardClass()
    player1.startGame()
