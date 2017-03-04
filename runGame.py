#basic structure - print board, get user input, do move, do ai move, repeat.
#After we get user input, we test its validity. If it's valid, we do it
#if it's invalid, report back to player, print board again, and ask for input
#if it's "undo" then pop the last player and ai moves, and print the board.
import chess, random

#prints the board, showing ranks and files. Flips the board if the player is black
def printBoard(board,player):
    str_rep = str(board)
    if player:
        str_files = "\n   A B C D E F G H"
        new_board = "8| "
        num = 7
        for char in str_rep:
            if char != "\n":
                new_board += char
            else:
                new_board += "\n"+str(num)+"| "
                num -= 1
        new_board += "\n +-" + ("-"*15)
        new_board += str_files
        print new_board
    else:
        str_rep = str_rep[::-1]
        str_files = "\n   H G F E D C B A"
        new_board = "1| "
        num = 2
        for char in str_rep:
            if char != "\n":
                new_board += char
            else:
                new_board += "\n"+str(num)+"| "
                num += 1
        new_board += "\n +-" + ("-"*15)
        new_board += str_files
        print new_board

#returns a random legal Move Object
def randomLegalMove(board):
    x = []
    for i in board.legal_moves:
        x.append(i)
    return random.choice(x)

#returns true if this move will promote a pawn, false otherwise
def moveIsPromoting(board,uci_move):
    try:
        for i in board.legal_moves:
            if uci_move in str(i) and len(uci_move) != len(str(i)):
                return True
        return False
    except:
        return False

#this will need to be changed so the body is something like
#aiObject.getMove(board)
#it's in place so that the main game-playing code won't need to be changed
#when we update the ai.
def getAIMove(board):
    return randomLegalMove(board)

#performs the AI's chosen move, and prints the move made.
#returns true if the AI could make the move.
#otherwise (implies game is over) it returns false.
def doAIMove(board):
    if not board.is_game_over():
        opponentMove = str(getAIMove(board))
        print "Opponent makes move: " + opponentMove
        board.push_uci(opponentMove)
        return True
    return False

#####--------------------Main-Game-Code----------------#######
#Print instructions to play game, mostly text commands
print "Moves: Type the 'from' square, followed by the 'to' square."
print "For example, 'a3a5' (without quotes) would move whatever piece is in a3 to a5"
print "Type 'quit' (without quotes) to quit the game."
print "Type 'undo' (without quotes) to undo your last move."
print "White or Black? White goes first. Please type 'w' (no quotes) for white, 'b' (no quotes) for black."

#create the board and user variables
board = chess.Board()
user_input = ""
playerMoveCount = 0

#get the user to choose white or black
player = raw_input(">>> ").lower()
while player != "w" and player != "b":
    print "Invalid input. Please type w or b for white or black."
    player = raw_input(">>> ").lower()

if player == "w":
    player = True
else:
    #if the user chose black, the AI must make the first mvoe
    player = False
    doAIMove(board)

#as long as the game is still going, and the user hasn't entered 'quit', keep playing
while (not user_input == "quit") and not board.is_game_over():
    printBoard(board,player)
    user_input = raw_input(">>> ").lower().strip()
    try:
        if user_input == "":
            print "Incorrect move syntax"
        elif user_input == "undo":
            if playerMoveCount > 0:
                board.pop()
                board.pop()
                playerMoveCount -= 1
                print "You and your opponent's previous moves have been undone."
            else:
                print "You haven't made any moves yet!"
        elif user_input == "quit":
            break
        elif moveIsPromoting(board,user_input):
            #instructions to promote pawn
            print "Pawn is being promoted."
            print "Enter a letter based on what you want to promote your pawn to."
            print "q=Queen,r=Rook,b=Bishop,n=Knight"
            promotion = raw_input(">>> ")
            #enforces valid input.
            while promotion.lower() not in "qrbn":
                print "Please enter valid piece (q,r,b, or n)"
                promotion = raw_input(">>> ")
            #make move
            board.push_uci(user_input+promotion)
            print "You made move: " + user_input + promotion
            playerMoveCount+=1
            doAIMove(board)
        else:
            board.push_uci(user_input)
            print "You made move: " + user_input
            playerMoveCount+=1
            doAIMove(board)
            
    except ValueError as e:
        if e.message.startswith("illegal uci"):
            print "Illegal Move, did you type the correct squares?"
        else:
            print "Incorrect move syntax."
    except IndexError:
        print "No moves have been made yet, can't undo."

#if we get here, game is over. Check winner and make announcement
print "Game over!"
result = board.result().split("-")
if result[0] == "*" or result[0] == result[1]:
    print "Draw!"
elif int(result[0]) > int(result[1]):
    print "White won!"
else:
    print "Black won!"
