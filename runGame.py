#basic structure - print board, get user input, do move, do ai move, repeat.
#After we get user input, we test its validity. If it's valid, we do it
#if it's invalid, report back to player, print board again, and ask for input
#if it's "undo" then pop the last player and ai moves, and print the board.
import chess, random, ais,traceback, cPickle
debugging = True
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
            if len(uci_move) == 4 and uci_move in str(i) and len(str(i)) == 5:
                return True
        return False
    except:
        return False

#this will need to be changed so the body is something like
#aiObject.getMove(board)
#it's in place so that the main game-playing code won't need to be changed
#when we update the ai.
def getAIMove(ai):
    global debugging
    timelimit = 60 #seconds. Is NOT a guarantee that it will finish in time
    move = ai.getMove(timelimit)
    if debugging:
        print move
    return move[1]

#performs the AI's chosen move, and prints the move made.
#returns true if the AI could make the move.
#otherwise (implies game is over) it returns false.
def doAIMove(board,ai):
    if not board.is_game_over():
        print "Opponent is thinking..."
        opponentMove = str(getAIMove(ai))
        print "Opponent makes move: " + opponentMove
        board.push_uci(opponentMove)
        return True
    return False

def saveGame(board,player):
    out = open("game.data","wb")
    cPickle.dump(board,out)
    out.close()
    pout = open("player.data","wb")
    cPickle.dump(player,pout)
    pout.close()

def loadGame():
    gamein = open("game.data","rb")
    board = cPickle.load(gamein)
    gamein.close()
    pin = open("player.data","rb")
    player = cPickle.load(pin)
    pin.close()
    return board,player

#####--------------------Main-Game-Code----------------#######
#create the user variables
board = None
player = None
user_input = ""

print "Would you like to load a game, or start a new one?"
print "Please type 'l' (no quotes) to load, 'n' (no quotes) for a new game."

#this whole block gets/creates the board
user_input = raw_input(">>> ")
while not user_input.lower() == "l" and not user_input.lower() == "n":
    print "Invalid input. Please type l or n to load a game or start new."
    user_input = raw_input(">>> ")

if user_input == "l":
    try:
        board,player = loadGame()
    except:
        board = chess.Board()
        print "No game was found. Starting new game."
else:
    board = chess.Board()
    print "Starting new game."


if player == None:
    print "White or Black? White goes first. Please type 'w' (no quotes) for white, 'b' (no quotes) for black."
    #get the user to choose white or black
    player = raw_input(">>> ").lower()
    while player != "w" and player != "b":
        print "Invalid input. Please type w or b for white or black."
        player = raw_input(">>> ").lower()

if player == "w" or player == True:
    player = True
    opponent = ais.alphaBetaMinimaxAI(False,board)
else:
    #if the user chose black, the AI must make the first mvoe
    player = False
    opponent = ais.alphaBetaMinimaxAI(True,board)

#Print instructions to play game, mostly text commands
print "\n####--------------------Instructions------------------####"
print "Moves: Type the 'from' square, followed by the 'to' square."
print "For example, 'a3a5' (without quotes) would move whatever piece is in a3 to a5"
print "Type 'quit' (without quotes) to quit the game."
print "Type 'undo' (without quotes) to undo your last move."
print "Type 'save' (without quotes) to save the game."
print "####--------------------------------------------------####\n"

if player != board.turn:
     doAIMove(board,opponent)

#as long as the game is still going, and the user hasn't entered 'quit', keep playing
while (not user_input == "quit") and not board.is_game_over():
    printBoard(board,player)
    user_input = raw_input(">>> ").lower().strip()
    try:
        if user_input == "":
            print "Incorrect move syntax"
        elif user_input == "undo":
            if len(board.stack) > 1:
                board.pop()
                board.pop()
                print "You and your opponent's previous moves have been undone."
            else:
                print "You haven't made any moves yet!"
        elif user_input == "quit":
            break
        elif user_input == "save":
            saveGame(board,player)
            print "Game saved!"
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
            doAIMove(board,opponent)
        else:
            board.push_uci(user_input)
            print "You made move: " + user_input
            doAIMove(board,opponent)
            
    except Exception as e:
        if debugging:
            traceback.print_exc()
        if e.message.startswith("illegal uci"):
            print "Illegal Move, did you type the correct squares?"
        else:
            print "Incorrect move syntax."

#if we get here, game is over. Check winner and make announcement
print "Game over!"
result = board.result().split("-")
if result[0] == "*" or result[0] == result[1]:
    print "Draw!"
elif int(result[0]) > int(result[1]):
    print "White won!"
else:
    print "Black won!"
