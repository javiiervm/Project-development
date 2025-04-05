from copy import deepcopy

import ChessGame as game
import Board as brd
import Player as plr
import Position as pos
import Square as sq
import os

def castlingChecker(kingPiece, playerSquares):
    if not kingPiece.getPiece().getCastling():
        return []
    rooks = []
    for square in playerSquares[:]:
        if square.getPiece().getName() == "Rook" and square.getPiece().getCastling():
            rooks.append(square)
    return rooks

def getDestinyList(chosenSquare, danger):
    availableSquares = chosenSquare.getPiece().possibleMoves(chessGame.getBoard(), chosenSquare.getPosition())
    if chosenSquare.getPiece().getName() == "King":
        return checkKingMoves(availableSquares, danger)
    return availableSquares

def pieceMovement(currentPlayer, playerSquares, danger):
    for square in playerSquares:
        print(f"{square.getPosition().printPos()} -> {square.getPiece().printData()}")

    while True:
        pieceIsValid, chosenSquare = squareSelectionChecker(playerSquares, pos.Position(int(input("Select a piece to move:\nRow\n>> ")), int(input("Column\n>> "))))
        if pieceIsValid:
            break

    king = (chosenSquare.getPiece().getName() == "King")
    availableSquares = getDestinyList(chosenSquare, danger)
    if king and chosenSquare.getPiece().getCastling():
        rooksToCastling = castlingChecker(chosenSquare, playerSquares)  # List of the possible rooks to castling with
        if len(rooksToCastling) > 0:
            for rook in rooksToCastling:
                rookMoves = getDestinyList(rook, danger)    # List of the possible moves of the rook to look for coincidences
                for destiny in rookMoves:
                    if destiny.getPosition().getX() == chosenSquare.getPosition().getX() and (destiny.getPosition().getY() + 1 == chosenSquare.getPosition().getY() or destiny.getPosition().getY() - 1 == chosenSquare.getPosition().getY()):
                        availableSquares.append(rook)
                        break

    if king and len(availableSquares) == 0:
        return True
    # Filter the movements that can led to a check situation
    for square in availableSquares[:]:  # Create a shallow copy of the list
        testGame = game.ChessGame(chessGame.getBoard(), "1", "2")
        testGame.board.movePiece(chosenSquare, square)
        newCheck, _, _ = testGame.checkForCheck(currentPlayer.isWhite())
        if newCheck:
            print(f"Menace found! Removing {square.getPosition().printPos()} from the list...")
            availableSquares.remove(square)
    for square in availableSquares:
        print(f"{square.getPosition().printPos()}")
    if len(availableSquares) > 0:
        while True:
            selectedSquareIsValid, destinySquare = squareSelectionChecker(availableSquares, pos.Position(int(input("Select a square to move your piece to:\nRow\n>> ")), int(input("Column\n>> "))))
            if selectedSquareIsValid:
                break
        if king and destinySquare.hasPiece() and (destinySquare.getPiece().isWhite() == currentPlayer.isWhite()) and (destinySquare.getPiece().getName() == "Rook"):
            print("You decided to perform a castling!")
            rookMoving = deepcopy(destinySquare)
            if rookMoving.getPosition().getY() == 0:
               chessGame.board.movePiece(chosenSquare, sq.Square(pos.Position(destinySquare.getPosition().getX(), destinySquare.getPosition().getY() + 1), None))
               chessGame.board.movePiece(rookMoving, sq.Square(pos.Position(destinySquare.getPosition().getX(), destinySquare.getPosition().getY() + 2), None))
            elif rookMoving.getPosition().getY() == 7:
               chessGame.board.movePiece(chosenSquare, sq.Square(pos.Position(destinySquare.getPosition().getX(), destinySquare.getPosition().getY() - 1), None))
               chessGame.board.movePiece(rookMoving, sq.Square(pos.Position(destinySquare.getPosition().getX(), destinySquare.getPosition().getY() - 2), None))
        else:
            print(f"You decided to move piece {chosenSquare.getPosition().printPos()} to square {destinySquare.getPosition().printPos()}")
            chessGame.board.movePiece(chosenSquare, destinySquare)
    return False

def checkKingMoves(kingmoves, bannedMoves):
    newList = []
    # Filter king moves against banned moves
    for kingMove in kingmoves:
        is_banned = False
        king_pos = kingMove.getPosition()
        for bannedMove in bannedMoves:
            if king_pos.getX() == bannedMove.getX() and king_pos.getY() == bannedMove.getY():
                is_banned = True
                break
        if not is_banned:
            newList.append(kingMove)
    return newList

# Function to check if player selected a valid square
def squareSelectionChecker(squareList, selected):
    for square in squareList:
        if square.getPosition().getX() == selected.getX() and square.getPosition().getY() == selected.getY():
            return True, square
    return False, None

# Function that executes every round
def roundFunc():
    currentPlayer = chessGame.getPlayerTurn()

    print(f"\nROUND {chessGame.getRound()}! {currentPlayer.turnMessage()}\n")    # Message at the beginning of each round
    chessGame.getBoard().printBoard()   # Print board state at the beginning of each round

    ischeck, danger, _ = chessGame.checkForCheck(currentPlayer.isWhite())  # Returns True and a list of pieces (positions) that are doing check in case of danger
    #print(f"JAQUE AL REY ACTUAL: {ischeck}")

    if not ischeck:
        playerSquares = chessGame.getBoard().getPlayerSquares(currentPlayer.isWhite())
        checkMate = pieceMovement(currentPlayer, playerSquares, danger)

    else:
        print(f"DANGER! CHECK TO THE CURRENT KING!")
        playerSquares = []
        for square in chessGame.getBoard().getPlayerSquares(currentPlayer.isWhite())[:]:  # Create a shallow copy of the list
            testGame = game.ChessGame(chessGame.getBoard(), "1", "2")
            moveList = getDestinyList(square, danger)
            for move in moveList:
                testGame.board.movePiece(square, move)
                newCheck, _, _ = testGame.checkForCheck(currentPlayer.isWhite())
                if not newCheck:
                    print(f"One move of the piece {square.getPiece().printData()} can save the king!")
                    playerSquares.append(square)
                    break
        if len(playerSquares) == 0:
            playerSquares.append(chessGame.findKing(currentPlayer.isWhite()))
        checkMate = pieceMovement(currentPlayer, playerSquares, danger)

    if checkMate:
        chessGame.setCheckMate(currentPlayer.isWhite())

    chessGame.addRound()    # Update the round counter


# Main function that manages the game
if __name__ == '__main__':
    os.system("clear")
    print("========================== [PYCHESS - By @Constructogamer and @iikerm] ==========================")

    # Create a new ChessGame
    chessGame = game.ChessGame(brd.Board(), plr.Player(input("Who will play with the WHITE king?\n>> "), True), plr.Player(input("Who will play with the BLACK king?\n>> "), False))

    # Play the game
    while not (chessGame.getCheckMate()):
        roundFunc()

    # Print result
    print("\n========================== [ END OF THE GAME! ] ==========================")
    if chessGame.getWhiteKing().isCheckMate():
        chessGame.getBlackKing().winMessage()
    else:
        chessGame.getWhiteKing().winMessage()
