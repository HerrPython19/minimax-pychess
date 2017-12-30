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
            chromo.append(round(random.random(),2))
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
        
    elif fen == "r3k2r/pppq2pp/2np1n2/2b1p1Q1/4P3/2NP1P1b/PPP4P/R3KB1R w KQkq - 1 12":
        fitnesses = {'g5g1': -16.51, 'h1g1': -11.10,
                     'g5g3': -9.97, 'a1d1': -11.59,
                     'g5g4': -18.4, 'g5g7': -19.72,
                     'g5g6': -20.91, 'a1b1': -10.57,
                     'g5f5': -18.8, 'c3d1': -12.47,
                     'c3d5': -9.6, 'g5g2': -15.32,
                     'f1h3': -8.56, 'g5e3': -21.83,
                     'd3d4': -10.38, 'g5c1': -12.02,
                     'g5e5': -19.53, 'f3f4': -9.43,
                     'b2b4': -14.55, 'b2b3': -12.18,
                     'f1e2': -9.41, 'e1c1': -8.83,
                     'c3e2': -9.16, 'f1g2': -9.04,
                     'c3a4': -9.18, 'g5f6': -15.3,
                     'a2a3': -9.03, 'g5f4': -20.9,
                     'e1e2': -12.14, 'a2a4': -9.6,
                     'g5h4': -9.41, 'g5h5': -21.12,
                     'a1c1': -10.29, 'e1d2': -9.91,
                     'e1d1': -10.23, 'g5h6': -20.45,
                     'g5d2': -9.46, 'c3b1': -11.3,
                     'c3b5': -9.45}

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
    board.set_fen("r3k2r/pppq2pp/2np1n2/2b1p1Q1/4P3/2NP1P1b/PPP4P/R3KB1R w KQkq - 1 12")
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
        chromo[spot] = round(random.random(),2)

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

def clearSavedChromos():
    f = open("best.chromo","wb")
    cPickle.dump([[0,0,0,0,0,0,0,0,0],-999],f)
    f.close()

    f = open("worst.chromo","wb")
    cPickle.dump([[0,0,0,0,0,0,0,0,0],999],f)
    f.close()

def do_ga():
    amount = 15
    f = open("all_chromos.ga","rb")
    mychromos = cPickle.load(f)
    f.close()
    #mychromos = createPopulation(amount)
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
                    print "Is " + str(-9.02-chromo[1]) + " below max of -9.02"

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
