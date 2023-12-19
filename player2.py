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

class Player2():
    """A class to store and handle information about player 2.
    """
    def __init__(self) -> None:
        """Function to initialize a variable for the socket connection.
        
        The socket connection can be used anywhere in Player2 class. p1Socket
        is used in the other functions to send and receive data.
        """
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p1Socket = ""

    def createGUI(self) -> None:
        """Function to initialize the GUI window and starting widgets.
        
        Creates the widgets that prompts the  user for their port and IP 
        address to send to player 1..
        """
        self.window = tk.Tk()
        self.window.title("Player 2 Tic-Tac-Toe")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        self.hostLabel = tk.Label(self.window, text="Your IP address") 
        self.hostLabel.pack()
        self.hostInput = tk.StringVar(self.window)
        self.hostEntry = tk.Entry(self.window, textvariable=self.hostInput)
        self.hostEntry.pack()

        self.portLabel = tk.Label(self.window, text="Your port number") 
        self.portLabel.pack()
        self.portInput = tk.StringVar(self.window)
        self.portEntry = tk.Entry(self.window, textvariable=self.portInput)
        self.portEntry.pack()

        self.hostPortBtn = tk.Button(self.window, text="Enter", command=self.establishConnection)
        self.hostPortBtn.pack()

        self.connectionVar = tk.StringVar(self.window)
        self.connectionText = tk.Label(self.window, textvariable=self.connectionVar)
        self.connectionText.pack()

        self.window.mainloop()

    def establishConnection(self) -> None:
        """Establishes the socket connection to player 1.
        
        Listens to the connection sent by player 1.
        """
        host = self.hostInput.get()
        port = self.portInput.get()
        self.connectionVar.set("")
        try:
            self.serverSocket.bind((host,int(port)))
            self.connectionVar.set("Waiting for connection...")
            self.window.update_idletasks()
            self.serverSocket.listen(1024)
            self.p1Socket,p1Address = self.serverSocket.accept()
            self.hostPortBtn["state"] = "disabled"
            self.hostEntry["state"] = "disabled"
            self.portEntry["state"] = "disabled"
            self.connectionVar.set("Connection successful!")
            self.window.update_idletasks()
            self.removeHostPortWidgets()

        except:
            self.connectionVar.set("Connection failed. Please try again.")

    def removeHostPortWidgets(self) -> None:
        """Remove all widgets that prompts for IP address and port.
        """
        self.hostLabel.pack_forget()
        self.portLabel.pack_forget()
        self.hostEntry.pack_forget()
        self.portEntry.pack_forget()
        self.hostPortBtn.pack_forget()
        self.connectionText.pack_forget()
        self.window.update_idletasks()
        self.window.after(1000)
        self.receiveUserName()
        

    def receiveUserName(self) -> None:
        """Receives player 1's username via sockets.
        
        Receiving player 1's username. Once received, prompt player 2 to send their username.
        """
        self.usernameTextVar = tk.StringVar(self.window)
        self.receiveUsernameText = tk.Label(self.window, textvariable=self.usernameTextVar)
        self.usernameTextVar.set("Waiting for player 1 to send their username...")
        self.receiveUsernameText.pack()
        self.window.update_idletasks()

        player2Board.player1Name = self.p1Socket.recv(1024).decode()
        self.receiveUsernameText.pack_forget()
        self.createUsernameWidgets()

    def createUsernameWidgets(self) -> None:
        """Create widgets that prompts user for username.
        
        Widgets to ask player 2 to enter an alphanumeric username to send to player 1.
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
        """Sends username to player 1.

        Takes the user inputted username and checks that it is alphanumeric. Sends valid username
        to player 1. Prompts user to try again if username is invalid.
        """
        self.usernameCheckVar.set("")
        self.window.update_idletasks()

        if self.p1username.get().isalnum():
            self.p1Socket.sendall(self.p1username.get().encode())
            player2Board.player2Name = self.p1username.get()
            self.usernameBtn["state"] = "disabled"
            self.removeUsernameWidgets()
            self.usernameTextVar.set("You are playing against: "+ player2Board.player1Name + "\nYou are O")
            self.receiveUsernameText.pack()
            self.playerTurnVar = tk.StringVar(self.window)
            self.playerTurnLabel = tk.Label(self.window, textvariable=self.playerTurnVar)
            self.playerTurnLabel.pack()
            self.playerTurnVar.set(f"Waiting for {player2Board.player1Name} to make a move...")
            self.drawGameBoard()
            self.receiveMove()

        else:
            self.usernameCheckVar.set("Invalid username. Please try again.")
            self.usernameCheck.pack()

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

    def receiveMove(self) -> None:
        """Receives the move played by player 1.
        
        Once player 2 sends a move, it will wait for player 1 to send a move.
        Draws the move player 1 sent on the game board.
        """
        self.disableGameBoard()
        self.playerTurnVar.set(f"Waiting for {player2Board.player1Name} to make a move...")
        self.window.update_idletasks()
        self.window.after(100)
        position = self.p1Socket.recv(1024).decode()
        player2Board.updateGameBoard(int(position), 'player1')
        self.listOfBtns[int(position)-1].place_forget()
        self.drawX(position)

        if player2Board.isWinner('player1'):
            self.youLose()
        elif player2Board.boardIsFull():
            self.tieGame()
        else:
            self.enableGameBoard()
            self.playerTurnVar.set("Your turn to make a move...")

    def sendMove(self, position: int) -> None:
        """Sends move played to player 1.
        
        Using the buttons on the game board, player 2 plays a move and it is sent to player 1.
        The move is drawn on the game board.
        """
        player2Board.updateGameBoard(int(position), 'player2')
        self.listOfBtns[int(position)-1].place_forget()
        self.drawO(position)
        self.disableGameBoard()
        self.window.update_idletasks()
        self.window.after(100)
        self.p1Socket.sendall(position.encode())

        if player2Board.isWinner('player2'):
            self.youWin()
        elif player2Board.boardIsFull():
            self.tieGame()
        else:
            self.receiveMove()

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

    def youLose(self) -> None:
        """Player 2 loses.
        
        Removes the canvas and all text on the window. Prompts the user to play again.
        """
        player2Board.numGames += 1
        player2Board.numLosses += 1
        self.canvas.create_text(260,50, text="You Lose!", fill="red", font=('Helvetica 80 bold'))
        self.removeGameBtns()
        self.window.update_idletasks()
        self.window.after(100)
        self.receivePlayAgain()

    def youWin(self) -> None:
        """Player 2 wins.
        
        Removes the canvas and all text on the window. Prompts the user to play again.
        """
        player2Board.numGames += 1
        player2Board.numWins += 1
        self.canvas.create_text(260,50, text="You Win!", fill="green", font=('Helvetica 80 bold'))
        self.removeGameBtns()
        self.window.update_idletasks()
        self.window.after(100)
        self.receivePlayAgain()

    def tieGame(self) -> None:
        """Tie game.
        
        Removes the canvas and all text on the window. Prompts the user to play again.
        """
        player2Board.numGames += 1
        player2Board.numTies += 1
        self.canvas.create_text(260,50, text="Tie Game!", fill="blue", font=('Helvetica 80 bold'))
        self.removeGameBtns()
        self.window.update_idletasks()
        self.window.after(100)
        self.receivePlayAgain()
    
    def receivePlayAgain(self) -> None:
        """Receives play again.
        
        Waits for player 1 to send confirmation to play again. If player 1 wants to play again,
        game board is re-drawn and reset moves. If player 1 does not want to play again, game
        statisitcs are displayed.
        """
        playAgainString = self.p1Socket.recv(1024).decode()
        if playAgainString == 'Fun Times':
            self.receiveUsernameText.pack_forget()
            self.playerTurnLabel.pack_forget()
            self.canvas.destroy()
            self.endGameHeader = tk.Label(self.window, text="---Game Statistics---")
            self.endGameHeader.pack()
            self.statisticsText = tk.Label(self.window, text=f'Player 1 Username: {player2Board.computeStats()[0]}\nPlayer 2 Username: {player2Board.computeStats()[1]}\nTotal number of games: {player2Board.computeStats()[2]}\nNumber of wins: {player2Board.computeStats()[3]}\nNumber of losses: {player2Board.computeStats()[4]}\nNumber of ties: {player2Board.computeStats()[5]}')
            self.statisticsText.pack()

        elif playAgainString == 'Play Again':
            player2Board.resetGameBoard()
            self.canvas.destroy()
            self.drawGameBoard()
            self.receiveMove()

    def startGame(self) -> None:
        """Function to start game.
        """
        self.createGUI()


if __name__ == "__main__":
    player2 = Player2()
    player2Board = BoardClass()
    player2.startGame()
