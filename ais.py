import time, chess
class alphaBetaMinimaxAI:
    def __init__(self, computer, board, depth=4):
        #true if computer is white, false if black
        self.computer = computer
        self.board = board
        self.depth = depth
        self.currMove = None
        #Keep aggro/defense between 0 and 1
        #High aggression - likes boards that attack player
        self.aggressiveness = 0
        #High defense - likes boards that aren't attacking computer
        self.defensiveness = 0
        self.timer_leeway = 5 #seconds. used to give program time to return
                                #after actual time limit runs out.

    def sumPieces(self):
        total = 0
        piece_values = {"p":1,"b":4,"n":4,"r":7,"q":10,"k":0}
        for square in str(self.board):
            if square.lower() in "rnbqkp":
                #if the piece is black
                if square.islower():
                    #if the computer is white, subtract score of piece
                    if self.computer:
                        total -= piece_values[square.lower()]
                    #if computer is black, add score
                    else:
                        total += piece_values[square.lower()]
                #same here. white and white, add. white and black, subtract.
                else:
                    if self.computer:
                        total += piece_values[square.lower()]
                    else:
                        total -= piece_values[square.lower()]
        return total

    def checkmate(self):
        if self.board.is_checkmate():
            if self.board.turn == self.computer:
                return -99999
            else:
                return 99999
        else:
            return 0

    def check(self):
        if self.board.is_check():
            if self.board.turn == self.computer:
                return -15
            else:
                return 15
        else:
            return 0

    def sumOpenSpace(self):
        total = 0
        if self.board.turn == self.computer:
            total += len(self.board.legal_moves)/10.0
            self.board.turn = not self.board.turn
            total -= len(self.board.legal_moves)/10.0
            self.board.turn = not self.board.turn
        else:
            total -= len(self.board.legal_moves)/10.0
            self.board.turn = not self.board.turn
            total += len(self.board.legal_moves)/10.0
            self.board.turn = not self.board.turn
        return total

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
        piece_values = {"p":.5,"b":1.5,"n":1.5,"r":2.5,"q":3,"k":0}
        for square in range(64):
            piece = self.board.piece_at(square)
            if piece != None:
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
        piece_values = {"p":.4,"b":.5,"n":.5,"r":.4,"q":.4,"k":.1}
        for square in range(64):
            piece = self.board.piece_at(square)
            rank = int(chess.SQUARE_NAMES[square][1])
            if piece != None:
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

    def totalAttacks(self):
        total = 0
        piece_values = {"p":1,"b":1.2,"n":1.2,"r":1.4,"q":2,"k":.1}
        for square in range(64):
            piece = self.board.piece_at(square)
            if piece != None:
                if piece.color == self.computer:
                    total -= len(self.board.attackers(not self.computer,
                                                      square))*piece_values[str(piece).lower()]+self.defensiveness
                else:
                    total += len(self.board.attackers(self.computer,
                                                      square))*piece_values[str(piece).lower()]+self.aggressiveness
        return total
                    
    def staticEval(self):
        #sums pieces on board.
        pieceTotal = self.sumPieces()
        #are we in check?
        checkTotal = self.check()
        #Checkmate? Could be really good or really bad
        checkmateTotal = self.checkmate()
        #how much open space do we have available
        openSpace = self.sumOpenSpace()
        #are pieces protected?
        protectionValue = self.piecesProtected()
        #how advanced are the pieces?
        pieceAdvancement = self.advancingPieces()
        #where are the attacks happening, and how many?
        attacks = self.totalAttacks()
        return round(pieceTotal+checkTotal+checkmateTotal+openSpace+protectionValue+pieceAdvancement+attacks,3)

    #requires move as a uci string, not a move object
    def badMove(self, move):
        #use different sub-functions to determine if this is a bad move
        #the greater total is, the worse the move.
        total = 0
        if self.backAndForth(move):
            total += 5
        if self.samePieceTwice(move):
            total += 2
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
        

    def alphaBetaMinimax(self,move=None,alpha=-999999,beta=999999,depth=0,fullstart=0,timelimit=-1):
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
                    if result > alpha:
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
                    if result < beta:
                        beta = result
                        bestMove = item
                    if (timelimit > 0 and y > timelimit) or beta <= alpha:
                        self.board.pop()
                        return beta, bestMove, nodesVisited, self.getTimeSpent(startTime,fullstart)
                self.board.pop()
                return beta, bestMove, nodesVisited, self.getTimeSpent(startTime,fullstart)

    def getMove(self, t_limit=0):
        if t_limit > 0:
            if t_limit < self.timer_leeway:
                t_limit = self.timer_leeway + 1
            move = self.alphaBetaMinimax(fullstart=time.time(),timelimit=t_limit-self.timer_leeway)
        else:
            move = self.alphaBetaMinimax()
        self.currMove = move
        return move
