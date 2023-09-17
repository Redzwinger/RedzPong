'''
********************************************************

Program by Achintya Kamath / Redzwinger (September 2022)

********************************************************
'''

'''
References/Resources:
https://neat-python.readthedocs.io/en/latest/index.html - The Official NEAT documents
https://github.com/CodeReclaimers/neat-python - The NEAT resources (config.txt, etc.)

https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf - The original NEAT papers for understanding the tech

https://youtu.be/2f6TmKm7yx0 - Tutorial
https://github.com/techwithtim/NEAT-Pong-Python - Original Code (including the ping pong game files)
'''

'''
This program uses a pre-existing Ping Pong game for python and adds an AI made using the NeuroEvolution of Augmenting Topologies or NEAT Algorithm for python.

NEAT is an AI training and creating algorithm that creates a set of "genomes" and then trains them against each in various ways, from which we then select the best trained "gene" from a "genome" as the AI for whatever we require it for.

In this particular instance we are creating a Neural Network that will train the genomes with one another and then set a "fitness" value to each gene within it, the genome/gene with the highest fitness rating will continue on to train with the next genome, and so on until the number of set generations are runned.

From this training spree we select the "best" one and set it as the AI to control the Right Paddle of the ping pong game.

For purposes of this program:
The user controls the left paddle with "W" for "Up" and "S" for "Down"

This is a less trained version of the orignal. The threshold set to 250 for this version :)
'''

import pygame
from pong import Game
import neat
import os
import pickle
import sys
                        #creating a class for the AI commands
class pongAI:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

                      #The code snippet that actually runs the pong game
    def play_with_the_ai(self, genome, config): #remove genome and config to train the AI

        net = neat.nn.FeedForwardNetwork.create(genome, config) #letting the AI control just the right paddle

        width, height = 800, 600   #size of the game window (fixed because it intereferes with the AI cannot be changed)
        window = pygame.display.set_mode((width,height)) #initializing the window

        game = Game(window, width, height) #game widow initialization

        run = True

        clock = pygame.time.Clock() #The speed the game runs at

        while run: #display loop for thw game window
            clock.tick(120) #Frames per second
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run == False

            keys = pygame.key.get_pressed() #setting up the controls (The left paddle)

            if keys[pygame.K_w]: #paddle goes up
                self.game.move_paddle(left=True, up=True)

            if keys[pygame.K_s]: #paddle goes down
                self.game.move_paddle(left=True, up=False)
                
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                
            if keys[pygame.K_r]:
                self.game.reset()

            output = net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decison = output.index(max(output)) #finding max value

            #The AI controls from the testing module get rid of this to train the AI
            
            if decison == 0: #standing still
                pass
            elif decison == 1: #moving up
                self.game.move_paddle(left=False, up=True)
            else: #moving down
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop() #loop for the ball
            #print(game_info.left_score, game_info.right_score)
            self.game.draw(True, False) #score and other stuff
            pygame.display.update()
            
        pygame.quit()
        
        #End of code snippet that runs the pong game :)
    
 #now as pong is a multiplayer game, for the AI to be trained sufficiently enough to be good against any and all opponents the AI is going to be trained with every other instance of the AI in the neural network. This way it will learn in a step by step manner, in other words, with an opponent that is always better/different than the previous one, thereby eliminating the possibility of getting a false result of the AI being good which will be possible if the Ai is trained with another AI or with a hard coded opponent.

    def training_the_ai(self, genome1, genome2, config):

        #CREATING THE ACTUAL NEURAL NETWORKS

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        #running the game for the AI
        while run:
            for event in pygame.event.get(): #same as above
                if event.type == pygame.QUIT:
                    quit()

            #now the next bit is telling the AI how to control the paddles this is done by incorporating the stuff from the paddles file which is a part of the game file

            output1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decison1 = output1.index(max(output1)) #finding max value
            
            output2 = net2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decison2 = output2.index(max(output2)) #finding max value

            if decison1 == 0: #standing still
                pass
            elif decison1 == 1: #moving up
                self.game.move_paddle(left=True, up=True)
            else: #moving down
                self.game.move_paddle(left=True, up=False)

            if decison2 == 0: #standing still
                pass
            elif decison2 == 1: #moving up
                self.game.move_paddle(left=False, up=True)
            else: #moving down
                self.game.move_paddle(left=False, up=False)

            #print(output1, output2)

            game_info = self.game.loop() #initialising the game

            self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            if game_info.left_score >=1 or game_info.right_score >= 1 or game_info.left_hits > 50:
                self.calculate_fitness(genome1, genome2, game_info)
                #here if one paddle it immediately quits the game. this makes sure the AI doesn't continuously miss the ball. This reduces the time for training the AI
                break

            #setting the fitness info for each genome based on the training
    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits

        #setting up the two genomes to play against one another
def training_grind(genomes, config):
    width, height = 800, 600
    window = pygame.display.set_mode((width,height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1: #to break the training loop
            break
        #making sure the same genomes don't play against each other multiple times
        genome1.fitness = 0 #intial fitness
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness #preventing repeated 0 fitness
            game = pongAI(window, width, height)
            game.training_the_ai(genome1, genome2, config) #simulating the two AI and set their fitness


    #initialising the neat network to produce population to train
def run_neat(config):
    p =neat.Checkpointer.restore_checkpoint('neat-checkpoint-7') #(use this to restore a checkpoint)

    #p =neat.Population(config) #population/used for new training
    p.add_reporter(neat.StdOutReporter(True)) #reporting the info of the AI (threshold, etc.)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    #saving the progress of the training process of AI after every 1 generation of AI trained

    winner = p.run(training_grind, 1) #can change the number of genomes to set the number of generations
    #passing the number of genomes to determine the number of generations it will run for
    #The "winner" is the best gene of all of the genomes

    #now saving the best neural network/genome using the pickle module which saves a whole python object

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f) #the pickle file

def best_of_the_best(config): #testing the best AI
    width, height = 800, 600
    window = pygame.display.set_mode((width,height))

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f) #loading the saved best AI

    game = pongAI(window, width, height)
    game.play_with_the_ai(winner, config) #running the test AI

     #loading the config file/ running the AI training module through main
if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

        #loading the properties from the config file

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    #run_neat(config) #running the NEAT AI algorithm to train generations by using the config file.
    best_of_the_best(config) #using the best AI

