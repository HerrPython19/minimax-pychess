"""
Program design.
Will be centered around genetic algorithms.
chromo example:
each number float from 0 to 3
[material,space,protection,advancement,attack,control]
"""
import random,cPickle,os,ais,chess,chess.uci,traceback,subprocess
from subprocess import PIPE

def newEngine():
    return subprocess.Popen(args="",executable="stockfish/src/./stockfish",
                            stdin=PIPE,
                            stdout=PIPE,
                            stderr=PIPE)
def getEval(fen):
    myinput = ""
    myinput += "position fen " + fen + "\n"
    myinput += "go movetime 5000"
    return newEngine().communicate(input=myinput)

def createPopulation(amount):
    chromos = []
    for i in range(amount):
        chromo = []
        for weight in range(9):
            chromo.append(random.random())
        chromos.append([chromo,0])
    return chromos
#gets fitness for given fen and move
def fitness(chromo, fen):
    board = chess.Board()
    board.set_fen(fen)
    myai = ais.alphaBetaMinimaxAI(True, board)
    myai.setWeights(chromo)
    #set up game
    if fen == "r2qk1nr/1p3pp1/2nPb2p/3p4/pp6/5N2/PBP1PPPP/R2QKBR1 w Qkq - 0 12":
        fitnesses = {'f3d2': -2.12, 'f3d4': -1.56,
                     'a1b1': -1.15, 'c2c3': -2.95,
                     'c2c4': -1.57, 'd1d5': -11.52,
                     'd1d4': -8.6, 'd1b1': -1.49,
                     'd1d3': -1.22, 'd1d2': -1.11,
                     'b2d4': -1.57, 'b2f6': -6.68,
                     'a2a3': -.76, 'f3e5': -1.27,
                     'e2e3': -1.33, 'a1c1': -1.61,
                     'e1d2': -2.15, 'd6d7': -.52,
                     'h2h4': -1.47, 'h2h3': -1.3,
                     'g1h1': -1.52, 'f3g5': -5.27,
                     'b2a3': -5.5, 'g2g3': -1.7,
                     'b2g7': -.04, 'e2e4': -1.54,
                     'g2g4': -1.35, 'b2c1': -2.14,
                     'd1c1': -1.37, 'b2c3': -5.57,
                     'f3h4': -4.74, 'b2e5': -2.06}
    elif fen == "r1bq1rk1/pppp1ppp/2n2n2/1B2p3/1b2P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 8 6":
        fitnesses = {'f3d4': -4.47, 'a1b1': -.1,
                     'd2d4': .2, 'd2d3': 0,
                     'c3d5': .11, 'b5d3': -.27,
                     'f3h4': -1.08, 'b2b3': -.46,
                     'f1e1': .04, 'c3e2': -.22,
                     'c3a4': -.57, 'a2a3': -.09,
                     'f3e5': -1.92, 'a2a4': -.08,
                     'f3e1': -.91, 'h2h4': -.61,
                     'h2h3': -.11, 'g1h1': -.35,
                     'f3g5': -.67, 'd1e2': -.25,
                     'g2g3': -.89, 'b5e2': -1,
                     'd1e1': -.42, 'g2g4': -1.42,
                     'c3b1': -.7, 'b5a4': -.22,
                     'b5a6': -3.68, 'b5c6': 0,
                     'b5c4': -.16}
        
    elif fen == "1r1q1kn1/1p5r/2nPb2p/3p1p2/pp6/P3PN2/1BP2PPP/R2QKBR1 w Q - 1 16":
        fitnesses = {'f3d2': .45, 'f3d4': 1.39,
                     'a3b4': 1.58, 'a1b1': 1.08,
                     'e1e2': .81, 'f1d3': 1.58,
                     'e3e4': -.25, 'c2c4': .74,
                     'd1d5': -9.78, 'd1d4': -5.77,
                     'd1b1': 1.21, 'd1d3': 1.77,
                     'd1d2': 1.54, 'f1e2': 1.71,
                     'a1a2': .91, 'b2d4': 1.39,
                     'b2f6': -3.94, 'a1c1': .17,
                     'b2h8': -2.52, 'f3e5': 2.09,
                     'c2c3': .16, 'f1a6': -1.91,
                     'e1d2': 1.08, 'd6d7': 1.79,
                     'f1c4': -1.75, 'h2h4': 1.2,
                     'h2h3': 1.51, 'g1h1': 1.18,
                     'f3g5': -3.57, 'd1e2': 1.27,
                     'g2g3': 1.52, 'b2g7': -3.37,
                     'g2g4': 1.62, 'b2c1': .45,
                     'd1c1': .93, 'b2c3': -3.31,
                     'f1b5': .73, 'f3h4': -2.54,
                     'b2e5': 1.3}

    elif fen == "rnbqk1nr/pppp1ppp/8/8/Nb2p3/5N2/PPPPPPPP/R1BQKB1R w KQkq - 0 4":
        fitnesses = {'h1g1': -2.4, 'c2c3': -.66,
                     'f3e5': -1.23, 'f3d4': -.66,
                     'c2c4': -2.27, 'a4b6': -4.34,
                     'a1b1': -2.95, 'g2g3': -2.71,
                     'h2h4': -2.81, 'b2b3': -2.6,
                     'e2e3': -2.41, 'f3h4': -3.38,
                     'a2a3': -.62, 'a4c5': -3.94,
                     'h2h3': -2.73, 'g2g4': -2.56,
                     'f3g1': -1.28, 'f3g5': -3.29,
                     'a4c3': -2.79}

    mymove = myai.getMove()[1]
    return fitnesses[mymove]

def cumulativeFitness(chromo):
    board = chess.Board("r2qk1nr/1p3pp1/2nPb2p/3p4/pp6/5N2/PBP1PPPP/R2QKBR1 w Qkq - 0 12")
    added = fitness(chromo,board.fen())
    print added
    total = added
    board.set_fen("r1bq1rk1/pppp1ppp/2n2n2/1B2p3/1b2P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 8 6")
    added = fitness(chromo,board.fen())
    print added
    total += added
    board.set_fen("1r1q1kn1/1p5r/2nPb2p/3p1p2/pp6/P3PN2/1BP2PPP/R2QKBR1 w Q - 1 16")
    added = fitness(chromo,board.fen())
    print added
    total += added
    board.set_fen("rnbqk1nr/pppp1ppp/8/8/Nb2p3/5N2/PPPPPPPP/R1BQKB1R w KQkq - 0 4")
    added = fitness(chromo,board.fen())
    print added
    total += added
    return total
    
#make sure chromos are first sorted in descending order by fitness
def newPopulation(amount,old_chromos,mutation_rate):
    new_pop = []
    while len(new_pop) < amount:
        parent1,parent2 = selection(old_chromos)
        child = crossover(parent1,parent2)
        mutate(child,mutation_rate)
        new_pop.append([child,0])
    return new_pop
    
def selection(pool):
    return (random.choice(pool[:5])[0],random.choice(pool[:5])[0])

def crossover(chromo1,chromo2):
    cutoff = random.randint(0,len(chromo1))
    return chromo1[:cutoff]+chromo2[cutoff:]

def mutate(chromo,rate):
    myrange = int(1/float(rate))
    do_mutate = random.randint(0,myrange)
    if do_mutate == 0:
        spot = random.randint(0,len(chromo)-1)
        chromo[spot] = random.random()

def randomGame():
    allfiles = os.listdir(os.getcwd()+"/uci_games")
    ucifiles = []
    for filename in allfiles:
        if filename.endswith(".uci"):
            ucifiles.append(filename)

    rfile = random.choice(ucifiles)
    f = open(os.getcwd()+"/uci_games/"+rfile,"rb")
    gamedata = cPickle.load(f)
    f.close()
    return gamedata

def getBestLoaded():
    f = open("best.chromo","rb")
    data = cPickle.load(f)
    f.close()
    return data

def getWorstLoaded():
    f = open("worst.chromo","rb")
    data = cPickle.load(f)
    f.close()
    return data

def writeBest(chromo):
    f = open("best.chromo","wb")
    cPickle.dump(chromo,f)
    f.close()

def writeWorst(chromo):
    f = open("worst.chromo","wb")
    cPickle.dump(chromo,f)
    f.close()

def do_ga():
    amount = 15
    f = open("all_chromos.ga","rb")
    mychromos = cPickle.load(f)
    f.close()
    mychromos = createPopulation(amount)
    saveable_chromos = mychromos[:]
    mutation_rate = .25
    bestchromo = None
    worstchromo = None
    #mac
    #engine = chess.uci.popen_engine("stockfish/src/./stockfish")
    #windows
    #engine = chess.uci.popen_engine("stockfish-8-win/windows/stockfish_8_x64.exe")
    try:
        while True:
            for chromo in mychromos:
                if chromo[1] == 0:
                    chromo[1] = cumulativeFitness(chromo[0])
                    #compare to saved chromos and update
                    bestloaded = getBestLoaded()
                    worstloaded = getWorstLoaded()
                    if chromo[1] > bestloaded[1]:
                        writeBest(chromo)
                        print "Saved new best chromo!"
                    if chromo[1] < worstloaded[1]:
                        writeWorst(chromo)
                        print "Saved new worst chromo!"
                    print "Final fitness is: " + str(chromo[1]) + " for " + str(chromo[0])

            #sort based on fitness
            mychromos = sorted(mychromos,key=lambda x:x[1])
            mychromos.reverse()
            print "Final chromos before new pop:"
            print mychromos
            mychromos = newPopulation(amount,mychromos,mutation_rate)
            saveable_chromos = mychromos[:]
            
    except:
        traceback.print_exc()
        f = open("all_chromos.ga","wb")
        cPickle.dump(saveable_chromos,f)
        f.close()
