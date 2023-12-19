"""
Name: Jason Lee
UCINetID: 40445771
"""
class BoardClass():
    """A class to store and handle information about the game board.

    Attributes:
        player1Name (str): the username of player 1
        player2Name (str): the username of player 2 (will always be 'player2')
        lastUserPlayed (str): the user that last played a move (will be store either 'player1' or 'player2')
        numWins (int): the number of wins for the current player
        numLoses (int): the number of loses for the current player
        numTies (int): the number of ties for the current player
        numGames (int): the total number of games played
        gameBoard (list[[],[],[]]): a 3x3 list that stores the information of the game board (list[row][col])
    """
    def __init__(self) -> None:
        """Function to initialize variables for BoardClass.
        """
        self.player1Name = ""
        self.player2Name = ""
        self.lastUserPlayed = ""
        self.numWins = 0
        self.numLosses = 0
        self.numTies = 0
        self.numGames = 0
        self.gameBoard = [[' ' ,' ',' '],[' ' ,' ',' '],[' ',' ',' ']]

    def resetGameBoard(self) -> None:
        """Resets the game board.
        
        Set every position on the game board to an empty string.
        """
        self.gameBoard = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        
    def convertNumToIndex(self, position: int) -> tuple[int,int]:
        """Converts the user input from single integer to game board indices.
        
        Takes the integer user input (1-9) and converts it into a tuple of two integers that
        corresponds to the row and column index on the game board.
        """
        if position == 1:
            return 0,0
        elif position == 2:
            return 0,1
        elif position == 3:
            return 0,2
        elif position == 4:
            return 1,0
        elif position == 5:
            return 1,1
        elif position == 6:
            return 1,2
        elif position == 7:
            return 2,0
        elif position == 8:
            return 2,1
        elif position == 9:
            return 2,2

    def updateGameBoard(self, position: int, player: str) -> None:
        """Updates the game board with the user inputted move.

        Places an X or O on the board in the user inputted position based on whether player 1 or
        player 2 played the move.
        """
        if player == "player1":
            piece = 'X'
        elif player == "player2":
            piece = 'O'

        row,col = self.convertNumToIndex(position)
        self.gameBoard[row][col] = piece
        self.lastUserPlayed = player


    def isWinner(self, player: int) -> None:
        """Check if a player has won.
        
        Checks whether player 1 or player 2 has won by checking all three in a row possibilites.
        """
        if player == "player1":
            piece = 'X'
        elif player == "player2":
            piece = 'O'

        #rows
        if piece == self.gameBoard[0][0] and self.gameBoard[0][0] == self.gameBoard[0][1] and self.gameBoard[0][1] == self.gameBoard[0][2]:
            return True
        elif piece == self.gameBoard[1][0] and self.gameBoard[1][0] == self.gameBoard[1][1] and self.gameBoard[1][1] == self.gameBoard[1][2]:
            return True
        elif piece == self.gameBoard[2][0] and self.gameBoard[2][0] == self.gameBoard[2][1] and self.gameBoard[2][1] == self.gameBoard[2][2]:
            return True
        
        #columns
        elif piece == self.gameBoard[0][0] and self.gameBoard[0][0] == self.gameBoard[1][0] and self.gameBoard[1][0] == self.gameBoard[2][0]:
            return True
        elif piece == self.gameBoard[0][1] and self.gameBoard[0][1] == self.gameBoard[1][1] and self.gameBoard[1][1] == self.gameBoard[2][1]:
            return True
        elif piece == self.gameBoard[0][2] and self.gameBoard[0][2] == self.gameBoard[1][2] and self.gameBoard[1][2] == self.gameBoard[2][2]:
            return True
        
        #diagonals
        elif piece == self.gameBoard[0][0] and self.gameBoard[0][0] == self.gameBoard[1][1] and self.gameBoard[1][1] == self.gameBoard[2][2]:
            return True
        elif piece == self.gameBoard[0][2] and self.gameBoard[0][2] == self.gameBoard[1][1] and self.gameBoard[1][1] == self.gameBoard[2][0]:
            return True
        
    def boardIsFull(self) -> bool:
        """Checks if the game board is full.
        
        Checking each row for an empty string. If all three rows do not have any empty strings 
        then the board is full and game is a tie. (Winning on the last move is accounted for in 
        player modules)
        """
        numRowsFull = 0
        for row in self.gameBoard:
            if ' ' not in row:
                numRowsFull += 1

        if numRowsFull == 3:
            return True
        
        return False

    def computeStats(self) -> tuple:
        """Returns the game statistics.
        """
        return self.player1Name, self.player2Name, self.numGames, self.numWins, self.numLosses, self.numTies
