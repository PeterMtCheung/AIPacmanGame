# reactiveAgents.py
# ---------------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC
# Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class NaiveAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        sense = state.getPacmanSensor()
        if sense[7]:
            action = Directions.STOP
        else:
            action = Directions.WEST
        return action

class PSAgent(Agent):
    "An agent that follows the boundary using production system."
    def getAction(self, state):
        sense = state.getPacmanSensor()
        x = [sense[1] or sense[2] , sense[3] or sense[4] ,
        sense[5] or sense[6] , sense[7] or sense[0]]
        if x[0] and not x[1]:
            action = Directions.EAST
        elif x[1] and not x[2]:
            action = Directions.SOUTH
        elif x[2] and not x[3]:
            action = Directions.WEST
        elif x[3] and not x[0]:
            action = Directions.NORTH
        else:
            action = Directions.NORTH
        return action

class ECAgent(Agent):
    "An agent that follows the boundary using error-correction."

    def getAction(self, state):
        sense = state.getPacmanSensor() + [1]
        weight_north = [1, -2, -2, 0, 0, 0, 0, 1, -1]
        weight_east = [0, 1, 1, -2, -2, 0, 0, 0, -1]
        weight_south = [0, 0, 0, 1, 1, -2, -2, 0, -1]
        weight_west = [-1, 0, 0, 0, 0, 1, 1, -2, -1]
        def dot(sense, weight):
            return sum(i * j for i, j in zip(sense, weight))

        if dot(sense, weight_north)>=0:
            return Directions.NORTH
        elif dot(sense, weight_east)>=0:
            return Directions.EAST
        elif dot(sense, weight_south)>=0:
            return Directions.SOUTH
        elif dot(sense, weight_west)>=0:
            return Directions.WEST
        else:
            return Directions.NORTH

class SMAgent(Agent):
    "An sensory-impaired agent that follows the boundary using state machine."
    def registerInitialState(self,state):
        "The agent receives the initial GameState (defined in pacman.py)."
        sense = state.getPacmanImpairedSensor() 
        self.prevAction = Directions.STOP
        self.prevSense = sense

    def getAction(self, state):
        sense = state.getPacmanImpairedSensor()
        prevSense = self.prevSense
        prevAction = self.prevAction
        occupy = [1, sense[0], 1, sense[1], 1, sense[2], 1, sense[3]]
        occupy[0] = 1 if prevSense[0] and Directions.EAST == prevAction else 0
        occupy[2] = 1 if prevSense[1] and Directions.SOUTH == prevAction else 0
        occupy[4] = 1 if prevSense[2] and Directions.WEST == prevAction else 0
        occupy[6] = 1 if prevSense[3] and Directions.NORTH == prevAction else 0
        if(occupy[1] and not occupy[3]):
            action = Directions.EAST
        elif (occupy[3] and not occupy[5]):
            action = Directions.SOUTH
        elif (occupy[5] and not occupy[7]):
            action = Directions.WEST
        elif(occupy[7] and not occupy[1]):
            action = Directions.NORTH
        elif(occupy[0]):
            action = Directions.NORTH
        elif(occupy[2]):
            action = Directions.EAST
        elif(occupy[4]):
            action = Directions.SOUTH
        elif(occupy[6]):
            action = Directions.WEST
        else: action = Directions.NORTH
        self.prevAction = action
        self.prevSense = sense
        return action
