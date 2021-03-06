from piece import *
from board import Board
from player import Player

"""
RUNS BY CYCLES
>Each cycle is when both White and Black make a move.
>Stars the game by a White Move.
>Every move, checks if the game is finished, prints board, and
prints the last move of the game.

>For each move:
>1. Ask the position of the piece to move
>2. Shows all possible move for that piece
>3. User chose one move the his or her turn is over
>4. The same with the next player
"""

class Game():
    def __init__(self):
        self.howToPlay = """
> This is the chess board, the black pieces are shown
at the top and the white pieces, at the bottom.

> Also, you have a legend of the pieces at the right

> To play, the player on turn will have to choose the
piece he or she wants to move by typing its cords.
> The cords are given by a letter and a number that are
both at the left and bottom of the board. Ex: G3

> Then, the possible moves for the chosen piece will be
displayed. They are shown by ( ) instead of [ ].
> You only have to choose one of the shown cord the same
way as before. Then it's the rival's turn

> Now you guys are all good to start playing!

>>> Press ENTER to go back to the main menu
        """
        self.menu = """
++++++++++++++++++++++++++++++++++++
            CHESS GAME

            1. Start Game
            2. How to Play

            3. Exit

                            by Jem
++++++++++++++++++++++++++++++++++++
Choose an option:"""
        self.board = Board() #creates the board for the game
        #get players names
        self.wPl = Player("w", wki) #white player
        self.bPl = Player("b", bki) #black player

    #--------------------------------------
    #displays menu and waits for the user's choice
    def displayMenu(self):
        print(self.menu) #display menu options

        while True:
            choice = input() #ask the user his or her choice from the main menu

            if choice != "" and choice.isnumeric():
                choice = int(choice)
                
                if choice == 1:
                    print("\n>>> GAME STARTED!\nGood luck, " + self.wPl.name + " and " + self.bPl.name + "!")
                    self.startGame(self.wPl, self.bPl) #starts the game
                elif choice == 2:
                    self.printHowToPlay()
                elif choice == 3:
                    print(">>> THANKS FOR PLAYING, COME BACK SOON!")
                    exit() #ends the program
                else:
                    print("Your choice must be a number between 1 and 3")
            else:
                print("Your choice must be a number [1-3]")

    #-------------------------------------------------
    #runs while the game is not over
    #parameter are the name of the players
    def startGame(self, wPl, bPl):
        lastTurn = "b" #to start the game with a white's turn
        while True: #set turn info
            if lastTurn == "b":
                lastTurn = "w" 
                currentPl = self.wPl #current player
            else:
                lastTurn = "b"
                currentPl = self.bPl #current player

            (self.board).print(None) #prints actual state of the board

            #check if game finish in tied
            if self.gameIsTied() != False:
                print(self.gameIsTied()) #print tie message
                exit() #end the program

            #if king is on check, player must protect it
            if (currentPl.king).isOnCheck():      
                if (self.gameIsOver(currentPl) != False):
                    print(self.gameIsOver(currentPl)) #print end message
                    exit() #end program
                else:
                    print(currentPl.teamName + " KING IS ON CHECK, PROTECT IT")
                    #run protect king to take him out of the check position
                    (currentPl.king).protect()
            else:
                #if king is not on check, them rus a regular turn
                print(">>> " + currentPl.teamName + "'S TURN (" + currentPl.name + ")")
                self.runTurn(currentPl)

    #----------------------------------
    #runs a turn for the current player's team
    def runTurn(self, currentPl):
        piece = self.getPieceToMove(currentPl.team) #get piece to move
        to = self.getPositionTo(piece, currentPl.team, currentPl) #get the possito to move to
        try:
            print(piece.moveTo(to[0], to[1])) #move the piece and prints a state
        except:
            pass

    #-----------------------------------
    #print how to play messages
    def printHowToPlay(self):
        print(">>> HOW TO PLAY\nThis is how the board looks like:") #header
        (self.board).print(None) #print board for example
        print(self.howToPlay) #display how to play message
        input() #wait to quit menu
        self.displayMenu() #go back to main menu

    #-------------------------------------------------
    #Ask the user to insert the position of the piece to move.
    #And checks that it is possible to move that piece.
    def getPieceToMove(self, team):
        while True:
            print("\nInsert the position of the piece to move:")
            piecePosition = input() #the only user interaction for this function

            #make sure input is not only one character or digit
            if len(piecePosition) == 0 or len(piecePosition) == 1:
                print("The input should be one letter and one digit, try again")
            else:
                if self.isValidPos(piecePosition):
                    if toSys(piecePosition, False):
                        #the position in this variable is ok
                        piecePosition = toSys(piecePosition, True)

                        #check that there are possible moves,
                        #otherwive, asks again for position
                        if self.validateForPiece(piecePosition, team):
                            #set piece position [x][y]
                            x = piecePosition[0]
                            y = piecePosition[1]
                            #return the specific piece
                            piece = getPieceAtPosition(x, y)
                            
                            #get all possible moves to check if there are moves indeed
                            allPossibleMoves = piece.getMoves()
                            #if piece is a king, discard check moves
                            if piece.__class__ == king:
                                allPossibleMoves = piece.discardCheckMoves(allPossibleMoves)

                            if len(allPossibleMoves) == 0:
                                print("No possible moves for " + piece.name + ", try another one")
                            else:
                                #return the piece
                                return piece
                        else:
                            print("Empty spot, try another one")
                    else:
                        print("Invaid position, try another one")
                else:
                    print("Not a valid position, try another one.")
    
    #---------------------------------------------
    #Ask the user to choose one of the possible moves to the piece chose before
    def getPositionTo(self, piece, team, currentPl):
        #get all possible moves to check if there are moves indeed
        allPossibleMoves = piece.getMoves()
        #if piece is a king, discard check moves
        if piece.__class__ == king:
            allPossibleMoves = piece.discardCheckMoves(allPossibleMoves)

        (self.board).print(allPossibleMoves) #print board with possible moves

        piece.printPossibleMoves() #print the possible moves

        print('\nInsert "0" if you want to choose a different piece.')

        while True:
            positionTo = input() #the only user interaction for this function

            #make sure input is not only one character or digit
            if len(positionTo) == 0 or (positionTo != "0" and len(positionTo) == 1):
                print("The input should be one letter and one digit, try again")
            else:
                #if users wants to change piece, go back
                if positionTo == "0":
                    (self.board).print(None)
                    self.runTurn(currentPl) #run again to change piece
                    break

                if self.isValidPos(positionTo):
                    if toSys(positionTo, False):
                        positionTo = toSys(positionTo, True)
                        if [positionTo[0], positionTo[1]] in allPossibleMoves:
                            return positionTo #return item
                        else:
                            print("That move is not possible, check the list and try again")
                    else:
                        print("Invaid position, try another one")
                else:
                    print("Not a valid position, try another one.")

    #--------------------------------------------------------------
    #return true is the pos const of a letter and a number
    def isValidPos(self, pos):
        if pos[0].isnumeric() and not pos[1].isnumeric():
            return True
        elif not pos[0].isnumeric() and pos[1].isnumeric():
            return True
        return False

    #--------------------------------------------------------------
    #return True if the choosen piece to move is able to move
    #takes in consideration if there is a piece is that pos and
    #if the piece is the same team of the player in turn
    def validateForPiece(self, piecePosition, team):
        x = piecePosition[0]
        y = piecePosition[1]
        if not checkForPiece(x, y):
            return False
        else:
            if getPieceAtPosition(x, y).team != team:
                return False
        return True

    #-------------------------------
    #returns tie message is the game is a tie, False otherwise
    def gameIsTied(self):
        #if only the two kings are remainig, the game is a tie
        if (all_black_pieces == [bki]) and (all_white_pieces == [wki]):
            tieMessage = """
        +++++++++++++++++++++++++++++++++++++
                        GAME OVER   
            TIE BETWEEN BLACKS AND WHITES
        
        Congratulations, {pl1} and {pl2}!
        +++++++++++++++++++++++++++++++++++++
            """.format(pl1=self.wPl.name, pl2=self.bPl.name)
            return tieMessage
        
        return False
    
    #-----------------------------------------
    #return gameover message is game is over, false otherwise
    def gameIsOver(self, currentPl):
        #if there are no saving moves, its a check mate and game is over
        savingMoves = (currentPl.king).getSavingMoves()

        if len(savingMoves) == 0:
            endMessage = """
        +++++++++++++++++++++++++++++++++++++
                    GAME OVER
            {winnerTeam}'S ARE THE WINNERS
            CHECK MAKE ON {teamName}'S KING
        
        Congratulations!
        +++++++++++++++++++++++++++++++++++++
            """.format(winnerTeam=currentPl.opTeamName, teamName=currentPl.teamName)
            return endMessage
        
        return False