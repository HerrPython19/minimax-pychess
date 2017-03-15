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
    elif fen == "r2qk1n1/1p3pBr/2nPb2p/3p4/pp6/5N2/P1P1PPPP/R2QKBR1 w Qq - 1 13":
        fitnesses = {'f3d2': -5.18, 'f3d4': -4.37,
                     'a1b1': -4.08, 'g7c3': -3.46,
                     'g7e5': -.23, 'c2c3': -3.34,
                     'c2c4': -1.85, 'd1d5': -11.74,
                     'd1d4': -7.19, 'd1b1': -4.3,
                     'd1d3': -4.21, 'd1d2': -3.8,
                     'g7h8': -4.08, 'g7h6': -3.55,
                     'a2a3': -4.11, 'f3e5': -4.18,
                     'e2e3': -3.93, 'a1c1': -3.95,
                     'e1d2': -5.16, 'd6d7': -.15,
                     'g7f6': -4.93, 'h2h3': -4.51,
                     'g7d4': -.09, 'g1h1': -4.59,
                     'g7b2': -.12, 'g7f8': -4.65,
                     'f3g5': -5.17, 'g2g3': -4.16,
                     'e2e4': -2.76, 'g2g4': -4.33,
                     'd1c1': -4.22, 'h2h4': -4.6,
                     'f3h4': -5.29}
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
    mymove = myai.getMove()[1]
    return fitnesses[mymove]

def cumulativeFitness(chromo):
    board = chess.Board("r2qk1nr/1p3pp1/2nPb2p/3p4/pp6/5N2/PBP1PPPP/R2QKBR1 w Qkq - 0 12")
    added = fitness(chromo,board.fen())
    print added
    total = added
    board.set_fen("r2qk1n1/1p3pBr/2nPb2p/3p4/pp6/5N2/P1P1PPPP/R2QKBR1 w Qq - 1 13")
    added = fitness(chromo,board.fen())
    print added
    total += added
    board.set_fen("1r1q1kn1/1p5r/2nPb2p/3p1p2/pp6/P3PN2/1BP2PPP/R2QKBR1 w Q - 1 16")
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
                chromo[1] = cumulativeFitness(chromo[0])
                #sort based on fitness
                mychromos = sorted(mychromos,key=lambda fit_level:chromo[1])
                #compare to saved chromos and update
                bestchromo = mychromos[0]
                worstchromo = mychromos[len(mychromos)-1]
                bestloaded = getBestLoaded()
                worstloaded = getWorstLoaded()
                if bestchromo[1] > bestloaded[1]:
                    writeBest(bestchromo)
                    print "Saved new best chromo!"
                if worstchromo[1] < worstloaded[1]:
                    writeWorst(worstchromo)
                    print "Saved new worst chromo!"
                print "Final fitness is: " + str(chromo[1])
            
            mychromos = newPopulation(amount,mychromos,mutation_rate)
            saveable_chromos = mychromos[:]
            
    except:
        traceback.print_exc()
        f = open("all_chromos.ga","wb")
        cPickle.dump(saveable_chromos,f)
        f.close()
