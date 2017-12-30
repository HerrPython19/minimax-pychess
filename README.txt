Justin Alcorn
Robert Judkins
COS 470

Welcome to our chess engine!
A quick rundown of the files and folders here.

-README.md
	Was used for the github account. Not really sure what’s in there.
-runGame.py
	Pretty much what it says. Run this file and you’ll pick some game options in the console. Then it’ll start up a graphical chess game with our AI as the opponent.
-ais.py
	Contains AI. Has things like getMove(), the minimax algorithm, and the static evaluation function.
-weightFinder.py
	Runs genetic algorithms on ai in ais.py to find optimal weights.
-game.data
	Holds saved game data.
-player.data
	Holds saved player data. (Whether the human was white or black in the saved game)
-all_chromos.ga
	Holds all saved chromosomes used in weightFinder.py if it was halted mid-run.
-worst.chromo
	Holds worst current chromosome
-best.chromo
	Holds best current chromosome.
-goodWeights.pickle
	Saved the current good weights for the ai.
-spriteSheet.png
	Was downloaded from a free-use site. Used to create images for chess game.

To play the game yourself, simply run runGame.py
It will ask you instructions in the console. Such as, do you want to load a game or start a new one?
Do you want to be white or black?
What is the time limit for the AI, in seconds?
You will then be presented with a virtual chessboard where you can play your game.
You select a piece, then the space you want to move it to.
To undo, press z.
To save, press s.
The game will halt once someone has won, or if there was a draw.