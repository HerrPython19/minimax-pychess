#basic structure - print board, get user input, do move, do ai move, repeat.
#After we get user input, we test its validity. If it's valid, we do it
#if it's invalid, report back to player, print board again, and ask for input
#if it's "undo" then pop the last player and ai moves, and print the board.
import chess, random, ais,traceback, cPickle, pygame,time,threading
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
    timelimit = 120 #seconds. Is NOT a guarantee that it will finish in time
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

def genSprites(sheet):
    SPR_WIDTH = SPR_HEIGHT = OFFSET = 60
    sprites = {}
    sprites["Q"] = sheet.subsurface(
            pygame.Rect(OFFSET*1,OFFSET*0,SPR_WIDTH,SPR_HEIGHT))
    sprites["K"] = sheet.subsurface(
            pygame.Rect(OFFSET*0,OFFSET*1,SPR_WIDTH,SPR_HEIGHT))
    sprites["R"] = sheet.subsurface(
            pygame.Rect(OFFSET*0,OFFSET*0,SPR_WIDTH,SPR_HEIGHT))
    sprites["N"] = sheet.subsurface(
            pygame.Rect(OFFSET*3,OFFSET*0,SPR_WIDTH,SPR_HEIGHT))
    sprites["B"] = sheet.subsurface(
            pygame.Rect(OFFSET*1,OFFSET*1,SPR_WIDTH,SPR_HEIGHT))
    sprites["P"] = sheet.subsurface(
            pygame.Rect(OFFSET*2,OFFSET*0,SPR_WIDTH,SPR_HEIGHT))
    sprites["q"] = sheet.subsurface(
            pygame.Rect(OFFSET*3,OFFSET*1,SPR_WIDTH,SPR_HEIGHT))
    sprites["k"] = sheet.subsurface(
            pygame.Rect(OFFSET*2,OFFSET*2,SPR_WIDTH,SPR_HEIGHT))
    sprites["r"] = sheet.subsurface(
            pygame.Rect(OFFSET*2,OFFSET*1,SPR_WIDTH,SPR_HEIGHT))
    sprites["n"] = sheet.subsurface(
            pygame.Rect(OFFSET*1,OFFSET*2,SPR_WIDTH,SPR_HEIGHT))
    sprites["b"] = sheet.subsurface(
            pygame.Rect(OFFSET*3,OFFSET*2,SPR_WIDTH,SPR_HEIGHT))
    sprites["p"] = sheet.subsurface(
            pygame.Rect(OFFSET*0,OFFSET*2,SPR_WIDTH,SPR_HEIGHT))

    return sprites

def strToSquare(pos):
    squares = {'B8': 57, 'C7': 50, 'E8': 60, 'G8': 62, 'G7': 54,
               'G6': 46, 'G5': 38, 'G4': 30, 'G3': 22, 'G2': 14,
               'G1': 6, 'A8': 56, 'B7': 49, 'A1': 0, 'A3': 16,
               'A2': 8, 'A5': 32, 'A4': 24, 'A7': 48, 'A6': 40,
               'C3': 18, 'C2': 10, 'C1': 2, 'E6': 44, 'E1': 4,
               'C6': 42, 'E3': 20, 'E2': 12, 'D8': 59, 'C8': 58,
               'H8': 63, 'D5': 35, 'E5': 36, 'E4': 28, 'F8': 61,
               'E7': 52, 'F1': 5, 'F2': 13, 'F3': 21, 'F4': 29,
               'F5': 37, 'F6': 45, 'F7': 53, 'H2': 15, 'H3': 23,
               'H1': 7, 'H6': 47, 'H7': 55, 'H4': 31, 'H5': 39,
               'B4': 25, 'B5': 33, 'B6': 41, 'C5': 34, 'B1': 1,
               'B2': 9, 'B3': 17, 'D6': 43, 'D7': 51, 'D4': 27,
               'C4': 26, 'D2': 11, 'D3': 19, 'D1': 3}
    
    return squares[pos]

def getSquare(pos, player):
    posx = pos[0]
    posy = pos[1]

    if player:
        if posx < 64*1:
            myfile = "A"
        elif posx < 64*2:
            myfile = "B"
        elif posx < 64*3:
            myfile = "C"
        elif posx < 64*4:
            myfile = "D"
        elif posx < 64*5:
            myfile = "E"
        elif posx < 64*6:
            myfile = "F"
        elif posx < 64*7:
            myfile = "G"
        else:
            myfile = "H"

        if posy < 64*1:
            myrank = "8"
        elif posy < 64*2:
            myrank = "7"
        elif posy < 64*3:
            myrank = "6"
        elif posy < 64*4:
            myrank = "5"
        elif posy < 64*5:
            myrank = "4"
        elif posy < 64*6:
            myrank = "3"
        elif posy < 64*7:
            myrank = "2"
        else:
            myrank = "1"
    else:
        if posx < 64*1:
            myfile = "H"
        elif posx < 64*2:
            myfile = "G"
        elif posx < 64*3:
            myfile = "F"
        elif posx < 64*4:
            myfile = "E"
        elif posx < 64*5:
            myfile = "D"
        elif posx < 64*6:
            myfile = "C"
        elif posx < 64*7:
            myfile = "B"
        else:
            myfile = "A"

        if posy < 64*1:
            myrank = "1"
        elif posy < 64*2:
            myrank = "2"
        elif posy < 64*3:
            myrank = "3"
        elif posy < 64*4:
            myrank = "4"
        elif posy < 64*5:
            myrank = "5"
        elif posy < 64*6:
            myrank = "6"
        elif posy < 64*7:
            myrank = "7"
        else:
            myrank = "8"
            
    return str(myfile+myrank).lower()

def drawScreen(myscreen,myboard,sheet,sprites,player,selectedSquare):
    myfont = pygame.font.SysFont("calibri",30)
    lbl_white = myfont.render("White",1,(255,206,158))
    lbl_black = myfont.render("Black",1,(209,139,71))
    
    myscreen.fill((0,0,0))
    screen.blit(lbl_white,(155,530))
    screen.blit(lbl_black,(285,530))

    if myboard.turn:
        pygame.draw.rect(myscreen,(210,210,210),(147,523,90,40),3)
    else:
        pygame.draw.rect(myscreen,(210,210,210),(277,523,80,40),3)
    
    light = True
    count = 0
    #fills from left to right, bottom to top, white's perspective
    for i in range(8):
        for j in range(8):
            if player:
                x = j*64
                y = (7-i)*64
            else:
                x = (7-j)*64
                y = i*64

            bg = (209,139,71) if (i+j) % 2 == 0 else (255,206,158)
            pygame.draw.rect(myscreen,bg,(x,y,64,64))
            if len(myboard.move_stack) > 0:
                from_sq = strToSquare(myboard.move_stack[-1].uci()[:2].upper())
                to_sq = strToSquare(myboard.move_stack[-1].uci()[2:4].upper())
                if count == from_sq or count == to_sq:
                    pygame.draw.rect(myscreen,(165,229,91),(x+4,y+4,56,56))

            piece = myboard.piece_at(count)
            if piece != None:
                sprite = sprites[str(piece)]
                rect = pygame.Rect(x,y,64,64)
                myscreen.blit(sprite,rect)

                #if user has selected a square and we're on that square,
                #draw a border around it to show selection
                if selectedSquare != None:
                    if count == strToSquare(selectedSquare.upper()):
                        pygame.draw.rect(myscreen,(0,0,255),
                                     (x+1,y+1,62,62),4)
            
            count += 1

def drawPromotion(screen,sprites,player):
    if player:
        q = sprites["Q"]
        r = sprites["R"]
        n = sprites["N"]
        b = sprites["B"]
        pygame.draw.rect(screen,(0,0,0),(140,200,270,70))
    else:
        q = sprites["q"]
        r = sprites["r"]
        n = sprites["n"]
        b = sprites["b"]
        pygame.draw.rect(screen,(255,255,255),(140,200,270,70))

    qrect = pygame.Rect(140,205,64,64)
    rrect = pygame.Rect(210,205,64,64)
    nrect = pygame.Rect(280,205,64,64)
    brect = pygame.Rect(350,205,64,64)
    screen.blit(q,qrect)
    screen.blit(r,rrect)
    screen.blit(n,nrect)
    screen.blit(b,brect)
    
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
print "White is CAPITAL letters, black is lowercase letters."
print "Moves: Type the 'from' square, followed by the 'to' square."
print "For example, 'a3a5' (without quotes) would move whatever piece is in a3 to a5"
print "Type 'quit' (without quotes) to quit the game."
print "Type 'undo' (without quotes) to undo your last move."
print "Type 'save' (without quotes) to save the game."
print "####--------------------------------------------------####\n"
#initialize pygame
pygame.init()
screen = pygame.display.set_mode((512,612))
pygame.display.set_caption("Minimax-Pychess")
clock = pygame.time.Clock()
sheet = pygame.image.load("spriteSheet.png")
all_sprites = genSprites(sheet)

selectedSquare = None
promoting = False
promotionMove = ""

makeAIMove = False
AIMoving = False
user_input = ""
board_copy = board.copy()

def runAI():
    global makeAIMove, AIMoving, board, board_copy
    while user_input != "quit":
        time.sleep(.25)
        if makeAIMove:
            AIMoving = True
            print "Opponent is thinking..."
            move = getAIMove(opponent)
            print "Opponent makes move: " + str(move)
            board.push_uci(str(move))
            printBoard(board,player)
            board_copy = board.copy()
            AIMoving = False
            makeAIMove = False

t = threading.Thread(target=runAI,args=())
t.start()

if player != board.turn:
    drawScreen(screen,board_copy,sheet,all_sprites,player,selectedSquare)
    pygame.display.flip()
    makeAIMove = True

#as long as the game is still going, and the user hasn't entered 'quit', keep playing
while (not user_input == "quit"):
    drawScreen(screen,board_copy,sheet,all_sprites,player,selectedSquare)
    if promoting:
        drawPromotion(screen,all_sprites,player)
    pygame.display.flip()
        
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            user_input == "quit"
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP and not makeAIMove:
            pos = pygame.mouse.get_pos()
            if promoting:
                qrect = pygame.Rect(140,205,64,64)
                rrect = pygame.Rect(210,205,64,64)
                nrect = pygame.Rect(280,205,64,64)
                brect = pygame.Rect(350,205,64,64)
                if qrect.collidepoint(pos):
                    user_input = promotionMove+"q"
                    promoting = False
                    promotionMove = ""
                elif rrect.collidepoint(pos):
                    user_input = promotionMove+"r"
                    promoting = False
                    promotionMove = ""
                elif nrect.collidepoint(pos):
                    user_input = promotionMove+"n"
                    promoting = False
                    promotionMove = ""
                elif brect.collidepoint(pos):
                    user_input = promotionMove+"b"
                    promoting = False
                    promotionMove = ""
            else:
                #check for collisions
                square = getSquare(pos,player)
                piece = board.piece_at(strToSquare(square.upper()))

                #if player hasn't yet picked an attacking piece, highlight the
                #piece they clicked on (if it's theirs and their turn)
                if selectedSquare == None:
                    if piece != None and piece.color == player:
                        selectedSquare = square
                    else:
                        selectedSquare = None
                #if the player had selected a piece, but just picked another of
                #their own pieces, just highlight the new one
                elif piece != None and piece.color == player:
                    if square == selectedSquare:
                        selectedSquare = None
                    else:
                        selectedSquare = square
                #otherwise, attack the opponent piece
                else:
                    user_input = selectedSquare+square
                    selectedSquare = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and not makeAIMove:
                user_input = "save"
            if event.key == pygame.K_z and not makeAIMove:
                user_input = "undo"

    if moveIsPromoting(board,user_input):
        promoting = True
        promotionMove = user_input
        user_input = ""
        
    #user_input = raw_input(">>> ").lower().strip()
    try:
        if user_input == "":
            pass
        elif user_input == "undo":
            if len(board.stack) > 1:
                board.pop()
                board.pop()
                board_copy = board.copy()
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
            #promotion = raw_input(">>> ")
            #enforces valid input.
            while promotion.lower() not in "qrbn":
                print "Please enter valid piece (q,r,b, or n)"
                #promotion = raw_input(">>> ")
            #make move
            board.push_uci(user_input+promotion)
            print "You made move: " + user_input + promotion
            makeAIMove = True
        else:
            board.push_uci(user_input)
            board_copy = board.copy()
            print "You made move: " + user_input
            makeAIMove = True
            
    except Exception as e:
        if debugging:
            traceback.print_exc()
        if e.message.startswith("illegal uci"):
            print "Illegal Move, did you type the correct squares?"
        else:
            print "Incorrect move syntax."

    user_input = ""

#if we get here, game is over. Check winner and make announcement
print "Game over!"
result = board.result().split("-")
if result[0] == "*" or result[0] == result[1]:
    print "Draw!"
elif int(result[0]) > int(result[1]):
    print "White won!"
else:
    print "Black won!"

print "\n#####Final board#####"
printBoard(board,player)
raw_input("\nPress enter to quit.\n")
