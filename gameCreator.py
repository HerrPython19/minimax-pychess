#creates uci games from pgn files.
#basically just a sequence of uci moves.
import os, subprocess,sys,cPickle

for pgn in os.listdir(os.getcwd()+"/pgns"):
    if pgn.endswith(".pgn"):
        fullpath = os.getcwd()+"/pgns/"+pgn
        process = subprocess.Popen(["pgn-extract/./pgn-extract","-Wuci","-M",
                                    fullpath],stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout,stderror = process.communicate()
        #parse data
        pgndata = stdout.split("\n\n")
        index = 1
        for i in range(1,len(pgndata),2):
            parsed = pgndata[i].lower().split(" ")
            parsed = parsed[:len(parsed)-1]
            f = open("uci_games/"+pgn[:len(pgn)-4]+"_"+str(index)+".uci","wb")
            cPickle.dump(parsed,f)
            f.close()
            index += 1
