import time
class alphaBetaMinimaxAI:
    def __init__(self, computer, board, depth=4):
        #true if computer is white, false if black
        self.computer = computer
        self.board = board
        self.depth = depth
        self.currMove = None
        self.aggressiveness = 5
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

    #Don't know if this will actually help ai, unused right now
    def offenseDefense(self):
        if self.capturedPiece():
            #if it's the comp's turn, player captured ai's piece
            if self.board.turn == self.computer:
                return -self.defensiveness
            else:
                return self.aggressiveness
        else:
            return 0

    def piecesProtected(self):
        total = 0
        piece_values = {"p":.5,"b":2,"n":2,"r":5,"q":7,"k":0}
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
        
    def staticEval(self):
        #sums pieces on board.
        pieceTotal = self.sumPieces()
        #are we in check?
        checkTotal = self.check()
        #Checkmate? Could be really good or really bad
        checkmateTotal = self.checkmate()
        #Returns number based off if a piece was captured, and how
        #offensive/defensive we are
        #offDef = self.offenseDefense()
        openSpace = self.sumOpenSpace()
        protectionValue = self.piecesProtected()
        return pieceTotal+checkTotal+checkmateTotal+openSpace+protectionValue

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
        if len(self.board.stack) > 1:
            playerMove = self.board.pop().uci()
            pastMove = self.board.peek().uci()
            self.board.push_uci(playerMove)
            if pastMove[2:] + pastMove[:2] == move:
                return True
            else:
                return False
        else:
            return False

    def samePieceTwice(self, move):
        if len(self.board.stack) > 1:
            playerMove = self.board.pop().uci()
            pastMove = self.board.peek().uci()
            self.board.push_uci(playerMove)
            if pastMove[2:] == move[:2]:
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

    def genGoodMoves(self):
        moves = []
        for item in self.board.legal_moves:
            if self.badMove(str(item)) <= 0:
                moves.append(str(item))
        return moves
        

    def alphaBetaMinimax(self,move=None,alpha=-999999,beta=999999,depth=0,fullstart=0,timelimit=-1):
        #debugging data
        startTime = time.time()
        nodesVisited = 0 if depth == 0 else 1
        self.currMove = move
        #set up moves
        if depth != 0:
            self.board.push_uci(move)
            
        moves = self.genGoodMoves()
        
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
