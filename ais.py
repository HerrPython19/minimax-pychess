import time, chess, random
#TODO: Need to rewrite static eval and all subfunctions so they always return
#positive nums for white advantage, and neg for black advantage.
#Right now there are too many if statements when we can just if at a higher lvl
class alphaBetaMinimaxAI:
    def __init__(self, computer, board, depth=4):
        #true if computer is white, false if black
        self.computer = computer
        self.board = board
        self.depth = depth
        self.currMove = None
        self.is_endgame = None
        self.pieces = []
        #weights
        #these weights were alright for opening, favored player a little but
        #generally didn't make crappy moves until middlegame
        self.weights = [0.6031664325329334, 0.26609602512060027,
                        0.7950953033824536, 0.7536484927819189,
                        0.9124607897749692, 0.5791552462974463,
                        0.5999260632967787, 0.30848729751605497,
                        0.4207970707496148]
        #self.weights = [1,.5,.4,.8,.5,.1,1,.5,1]
        self.setWeights(self.weights)

    def setWeights(self, weights):
        self.materialWeight = weights[0]
        self.spaceWeight = weights[1]
        self.vulnWeight = weights[2]
        self.protectionWeight = weights[3]
        self.advancementWeight = weights[4]
        self.attackWeight = weights[5]
        self.controlWeight = weights[6]
        self.kingSafetyWeight = weights[7]
        self.doubleMoveWeight = weights[8]

    def randWeights(self):
        return [random.random(),random.random(),random.random(),
		random.random(),random.random(),random.random(),
		random.random(),random.random(),random.random()]

    def kingSafety(self):
        total = 0
        computerKing = None
        playerKing = None
        #define the comp/player kings
        for piece in self.pieces:
            if str(piece[0]) == "k":
                if self.computer:
                    playerKing = piece
                else:
                    computerKing = piece
            elif str(piece[0]) == "K":
                if self.computer:
                    computerKing = piece
                else:
                    playerKing = piece

        if computerKing[0].color:
            if computerKing[1] > 7:
                total -= 1
            if playerKing[1] < 56:
                total += 1
                
        elif not computerKing[0].color:
            if computerKing[1] < 56:
                total -= 1
            if playerKing[1] > 7:
                total += 1
                
        return total

    def sumPieces(self):
        total = 0
        piece_values = {"p":1,"b":3,"n":200,"r":5,"q":9,"k":0}
        for item in self.pieces:
            piece = item[0]
            #if piece is black
            if not piece.color:
                #if computer is white, subtract, otherwise add
                if self.computer:
                    total -= piece_values[str(piece).lower()]
                else:
                    total += piece_values[str(piece).lower()]
            else:
                #white and white, add, black and black, subtract
                if self.computer:
                    total += piece_values[str(piece).lower()]
                else:
                    total -= piece_values[str(piece).lower()]

        return total

    def checkmate(self):
        if self.board.is_checkmate():
            if self.board.turn == self.computer:
                return -1
            else:
                return 1
        else:
            return 0

    def check(self):
        if self.board.is_check():
            if self.board.turn == self.computer:
                return -1
            else:
                return 0
        else:
            return 0

    def sumOpenSpace(self):
        computerValue = 0
        playerValue = 0
        compqueen = "null"
        playerqueen = "null"
        cturn = False
        
        for piece in self.pieces:
            if str(piece) == "Q":
                if self.computer:
                    compqueen = str(piece[1])
                else:
                    playerqueen = str(piece[1])
            if str(piece) == "q":
                if self.computer:
                    playerqueen = str(piece[1])
                else:
                    compqueen = str(piece[1])
        if self.board.turn != self.computer:
            self.board.turn = not self.board.turn
            cturn = False
            
        if self.board.turn == self.computer:
            for move in self.board.pseudo_legal_moves:
                if not str(move)[:2] == compqueen[:2]:
                    computerValue += 1
            self.board.turn = not self.board.turn
            for move in self.board.pseudo_legal_moves:
                if not str(move)[:2] == playerqueen[:2]:
                    playerValue += 1

            if cturn:
                self.board.turn = not self.board.turn

        if playerValue == 0:
            playerValue = 1
        return float(computerValue)/playerValue

    def vulnerablePieces(self):
        compVulns = 1
        playerVulns = 1
        piece_values = {"p":1,"b":3,"n":3,"r":5,"q":9,"k":0}
        for item in self.pieces:
            piece = item[0]
            square = item[1]
            if piece.color == self.computer:
                if self.board.is_attacked_by(not self.computer,square)\
                   and not self.board.is_attacked_by(self.computer,square):
                    compVulns += piece_values[str(piece).lower()]
            else:
                if self.board.is_attacked_by(self.computer,square) and not\
                   self.board.is_attacked_by(not self.computer, square):
                    playerVulns -= piece_values[str(piece).lower()]

        return playerVulns/float(compVulns)

    def capturedPiece(self):
        if len(self.board.stack) > 1:
            pastMove = self.board.pop()
            if self.board.is_capture(pastMove):
                self.board.push(pastMove)
                return True
            else:
                self.board.push(pastMove)
                return False
        else:
            return False

    def piecesProtected(self):
        total = 0
        piece_values = {"p":.1,"b":.3,"n":.3,"r":.5,"q":.9,"k":0}
        for item in self.pieces:
            piece = item[0]
            square = item[1]
            if piece.color == self.computer:
                #if there is protection on ai piece
                if self.board.is_attacked_by(self.computer,square):
                    total += piece_values[str(piece).lower()]
                else:
                    total -= piece_values[str(piece).lower()]
            else:
                #if there is protection on player piece
                if self.board.is_attacked_by(piece.color,square):
                    total -= piece_values[str(piece).lower()]
                else:
                    total += piece_values[str(piece).lower()]

        return total

    def advancingPieces(self):
        total = 0
        piece_values = {"p":.1,"b":.3,"n":.3,"r":.2,"q":.2,"k":.0}
        for item in self.pieces:
            piece = item[0]
            square = item[1]
            rank = int(chess.SQUARE_NAMES[square][1])
            pName = str(piece).lower()
            if piece.color == self.computer:
                if self.computer:
                    total += piece_values[pName]*rank
                else:
                    total += piece_values[pName]*(9-rank)
            else:
                if self.computer:
                    total -= piece_values[pName]*(9-rank)
                else:
                    total -= piece_values[pName]*rank

        return total

    def centerControl(self):
        total = 0
        coreCenter = [chess.E4,chess.D4,chess.E5,chess.D5]
        outerCenter = [chess.C4,chess.C5,chess.D3,chess.D6,
                       chess.E3,chess.E6,chess.F4,chess.F5]

        for item in self.pieces:
            piece = item[0]
            square = item[1]
            if square in coreCenter:
                if piece.color == self.computer:
                    total += 1
                else:
                    total -= 1
            if square in outerCenter:
                if piece.color == self.computer:
                    total += .5
                else:
                    total -= .5
                    
        return total

    def genAttackingSquares(self,attackers):
        count = 63
        squares = []
        ranks = str(attackers).split("\n")
        for i in ranks:
            for j in i[::-1]:
                if j == "1":
		    squares.append(count)
		if j != " " and j != "\n":
		    count -= 1

        return squares

    def pawnsAttackingPiece(self, squares):
        pawnSpots = []
        for i in squares:
            piece = self.board.piece_at(i)
            if str(piece).lower() == "p":
                pawnSpots.append(i)
                
        return pawnSpots

    def totalAttacks(self):
        total = 0
        piece_values = {"p":.1,"b":.3,"n":.3,"r":.5,"q":.9,"k":0}
        for item in self.pieces:
            piece = item[0]
            square = item[1]
            if piece.color == self.computer:
                attacks = self.board.attackers(not self.computer, square)
                #we need to adjust for pieces that are being attacked by lesser/greater pieces
                squares = self.genAttackingSquares(attacks)
                attackingPawns = self.pawnsAttackingPiece(squares)
                if str(piece).lower() != "p" and attackingPawns != []:
                    total -= 2*len(attackingPawns)
                total -= len(attacks)*piece_values[str(piece).lower()]
            else:
                attacks = self.board.attackers(self.computer, square)
                #we need to adjust for pieces that are being attacked by lesser/greater pieces
                squares = self.genAttackingSquares(attacks)
                attackingPawns = self.pawnsAttackingPiece(squares)
                if str(piece).lower() != "p" and attackingPawns != []:
                    total += 2*len(attackingPawns)
                total += len(attacks)*piece_values[str(piece).lower()]

        return total

    def doubleMove(self):
        #only a penalty for the computer for right now
        if self.computer:
            if self.samePieceTwice(self.board.move_stack[len(self.board.move_stack)-1].uci()):
                    return -1
        return 0

    def isEndgame(self):
        if len(self.board.stack) >= 70:
            return True
        return False

    def endgameMultiplier(self):
        if self.isEndgame():
            return 2
        return 1

    def setPieces(self):
        self.pieces = []
        for square in range(64):
            piece = self.board.piece_at(square)
            if piece != None:
                self.pieces.append((piece,square))
                    
    def staticEval(self):
        checkWeight = 5
        checkmateWeight = 9999
        
        self.setPieces()
        #sums pieces on board.
        pieceTotal = self.sumPieces()*self.materialWeight
        #are we in check?
        checkTotal = self.check()*checkWeight
        #Checkmate? Could be really good or really bad
        checkmateTotal = self.checkmate()*checkmateWeight
        #how much open space do we have available
        openSpace = self.sumOpenSpace()*self.spaceWeight
        vulns = self.vulnerablePieces()*self.vulnWeight
        #are pieces protected?
        protectionValue = self.piecesProtected()*self.protectionWeight
        #how advanced are the pieces?
        pieceAdvancement = self.advancingPieces()*self.advancementWeight
        #where are the attacks happening, and how many?
        attacks = self.totalAttacks()*self.attackWeight
        #control of the center, very important
        control = self.centerControl()*self.controlWeight
        kingSafety = self.kingSafety()*self.kingSafetyWeight
 #       doubleMoved = self.doubleMove()*self.doubleMoveWeight
        
        return [pieceTotal,openSpace,vulns,protectionValue,
                pieceAdvancement,attacks,control,kingSafety,
                checkTotal,checkmateTotal,self.board.fen()]

    #requires move as a uci string, not a move object
    def badMove(self, move):
        #use different sub-functions to determine if this is a bad move
        #the greater total is, the worse the move.
        total = 0
        if self.backAndForth(move):
            total += 5
        return total

    def backAndForth(self,move):
        stackLen = len(self.board.move_stack)
        if stackLen > 1:
            pastMove = self.board.move_stack[stackLen-2].uci()
            if pastMove[2:] + pastMove[:2] == move:
                return True
            else:
                return False
        else:
            return False

    def samePieceTwice(self, move):
        stackLen = len(self.board.move_stack)
        if stackLen > 1:
            if self.board.move_stack[stackLen-2].uci()[2:] == move[:2]:
                return True
            else:
                return False
        else:
            return False

    def getTimeSpent(self,startTime,fullstart):
        if fullstart == 0:
            mytime = time.time()-startTime
        else:
            mytime = time.time()-fullstart
        return mytime

    def sortMoves(self,moves):
        sortedMoves = []
        afterCapture = []
        afterForward = []
        for move in moves:
            if self.board.is_capture(chess.Move.from_uci(move)):
                sortedMoves.append(move)
            elif move[3] > move[1]:
                afterCapture.append(move)
            else:
                afterForward.append(move)

        return sortedMoves + afterCapture + afterForward

    def numPieces(self):
        #returns [numWhite,numBlack]
        totalWhite = 0
        totalBlack = 0
        for square in range(64):
            piece = self.board.piece_at(square)
            if piece != None:
                if piece.color:
                    totalWhite += 1
                else:
                    totalBlack += 1

        return [totalWhite,totalBlack]

    def genGoodMoves(self,depth=0):
        moves = []
        badmoves = []
        for item in self.board.legal_moves:
            if self.badMove(str(item)) <= 0:
                moves.append(str(item))
            else:
                badmoves.append(str(item))

        #if there are no good moves, but still legal moves, return all moves
        if len(moves) == 0 and len(self.board.legal_moves) != 0:
            return badmoves

        #if there aren't many pieces on the board, allow bad moves
        num_pieces = self.numPieces()
        if self.board.turn:
            if num_pieces[0] < 7:
                return moves + badmoves
        else:
            if num_pieces[1] < 7:
                return moves + badmoves

        #only sort the moves at a low depth, it gets less important as we descend
        if depth < 3:
            return self.sortMoves(moves)
        else:
            return moves

    def getSum(self,result):
        if result == [-999999] or result == [999999]:
            return result[0]
        total = sum(result[:len(result)-1])
        return total

    def alphaBetaMinimax(self,move=None,alpha=-999999,beta=999999,depth=0,fullstart=0,timelimit=-1):
        if alpha == -999999:
            alpha = [-999999]
        if beta == 999999:
            beta = [999999]
        #debugging data
        startTime = time.time()
        nodesVisited = 0 if depth == 0 else 1
        self.currMove = move
        #set up moves
        if depth != 0:
            self.board.push_uci(move)
            
        moves = self.genGoodMoves(depth)
        
        if depth == 0 and len(moves) == 0:
                return ["",""]

        if depth == self.depth or len(moves) == 0:
            result = self.staticEval()
            return result, str(self.board.pop()), nodesVisited, self.getTimeSpent(startTime,fullstart)

        if len(moves) != 0:
            bestMove = moves[0]
            #maximizer
            if self.board.turn == self.computer:
                for item in moves:
                    result, future_move,x,y = self.alphaBetaMinimax(item,alpha,beta,depth+1,fullstart,timelimit)
                    nodesVisited += x
                    if self.getSum(result) > self.getSum(alpha):
                        alpha = result
                        bestMove = item
                    if (timelimit > 0 and y > timelimit) or alpha >= beta:
                        if depth != 0:
                            self.board.pop()
                        return alpha, bestMove, nodesVisited, self.getTimeSpent(startTime,fullstart)
                if depth != 0:
                    self.board.pop()
                return alpha, bestMove, nodesVisited, self.getTimeSpent(startTime,fullstart)

            #minimizer
            if self.board.turn != self.computer:
                for item in moves:
                    result, future_move,x,y = self.alphaBetaMinimax(item,alpha,beta,depth+1,fullstart,timelimit)
                    nodesVisited += x
                    if self.getSum(result) < self.getSum(beta):
                        beta = result
                        bestMove = item
                    if (timelimit > 0 and y > timelimit) or beta <= alpha:
                        self.board.pop()
                        return beta, bestMove, nodesVisited, self.getTimeSpent(startTime,fullstart)
                self.board.pop()
                return beta, bestMove, nodesVisited, self.getTimeSpent(startTime,fullstart)

    def getMove(self, t_limit=0):
        if t_limit > 0:
            move = self.alphaBetaMinimax(fullstart=time.time(),timelimit=t_limit)
        else:
            move = self.alphaBetaMinimax()
        self.currMove = move
        return move
