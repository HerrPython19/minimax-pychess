"""
Program design.
Will be centered around genetic algorithms.
chromo example:
each number float from 0 to 3
[material,space,protection,advancement,attack,control]
"""
import random,cPickle,os,ais,chess,chess.uci
bestchromo = None
worstchromo = None

def createPopulation(amount):
    chromos = []
    for i in range(amount):
        chromo = []
        for weight in range(6):
            chromo.append(random.random()*3)
        chromos.append((chromo,0))
    return chromos

#reads through a random game.
#for each move, these weights try to guess the best move.
#for each correct best move +1 to subtotal.
#after every move has been analyzed, return the fitness as correct/total moves
def fitness(chromo, game):
    board = chess.Board()
    
    randstart = random.randint(0,len(game)-15)
    randend=randstart+15
    #set up game
    moveindex = 0
    while moveindex != randstart:
        board.push_uci(game[moveindex])
        moveindex += 1
    
    game = game[randstart:randend]
    
    myai = ais.alphaBetaMinimaxAI(board.turn,board)
    myai.materialWeight = chromo[0]
    myai.spaceWeight = chromo[1]
    myai.protectionWeight = chromo[2]
    myai.advancementWeight = chromo[3]
    myai.attackWeight = chromo[4]
    myai.controlWeight = chromo[5]
    
    correct = 0
    index = 0
    end = len(game)
    engine = chess.uci.popen_engine("stockfish/src/./stockfish")
    for move in game:
        engine.position(board)
        my_best = myai.getMove(60)[1]
        sf_best = engine.go(movetime=2000)[0].uci()
        if my_best == sf_best:
            correct += 1
        if my_best[:2] == sf_best[:2]:
            correct += .5
        board.push_uci(move)
        myai.computer = not myai.computer
        index += 1
        print "Move " + str(index) + " out of " + str(end) + ":"
        print "\t" + "AI: " + my_best
        print "\t" + "SF: " + sf_best

    print "Fitness total for chromo " +str(chromo) +": " + str(float(correct)/end)
    return float(correct)/end

#make sure chromos are first sorted in descending order by fitness
def newPopulation(old_chromos,mutation_rate):
    new_pop = []
    while len(new_pop) < 100:
        parent1,parent2 = selection(old_chromos)
        child = crossover(parent1,parent2)
        mutate(child,mutation_rate)
        new_pop.append(child)
    return new_pop
    
def selection(pool):
    return (random.choice(pool[:10])[0],random,choice(pool[:10])[0])

def crossover(chromo1,chromo2):
    cutoff = random.randint(0,len(chromo1))
    return chromo1[:cutoff]+chromo2[cutoff:]

def mutate(chromo,rate):
    myrange = int(1/float(rate))
    do_mutate = random.randint(0,myrange)
    if do_mutate == 0:
        spot = random.randint(0,len(chromo))
        chromo[spot] = random.random()*3

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

def do_ga():
    mychromos = createPopulation(50)
    saveable_chromos = mychromos[:]
    mutation_rate = .25
    try:
        while True:
            for chromo in mychromos:
                chromo[1] = fitness(chromo[0],randomGame())

            #sort based on fitness
            mychromos = sorted(mychromos,key=lambda fit_level:chromo[1])
            mychromos = newPopulation(mychromos)
            saveable_chromos = mychromos[:]
            
    except:
        f = open("all_chromos.ga","wb")
        cPickle.dump(saveable_chromos,f)
        f.close()
do_ga()
