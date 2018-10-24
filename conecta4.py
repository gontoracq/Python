# -*- coding: utf-8 -*-
"""
    The Connect-4 game.
    
    Copyright (C) 2017  Ignacio Perez-Hurtado 
                        perezh at us dot es
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# This program follows the rules of connect-4:
# https://en.wikipedia.org/wiki/Connect_Four

# The algorithm for the AI is minimax:
# http://www.cs.us.es/cursos/ia1/temas/tema-07.pdf

import copy
import Red_Neuronal
import genetico
import numpy as np

# This class represents a board as a matrix of 6 rows x 8 columns where
# values can be: 0 if the cell is empty. 1 if the cell contains a player 1 token
# or 2 if it contains a player 2 token. The player can be 1 or 2

class State(object):
    def __init__(self, board = [[0 for x in range(8)] for y in range(6)], player = 1):
         self.__board = board
         self.__player = player
         self.__movements = []
         self.__winner = self.__compute_winner()
         for i in range(8):
             if self.__board[0][i]==0:
                 self.__movements.append(i)
    
    # Return the available movements as a list. Each movement is a number in [0 - 7] representing the
    # column to add a new token
    @property
    def movements(self):
        return self.__movements
   
   # Return the board as a matrix
    @property
    def board(self):
        return self.__board
    
    # Return the current player (1 or 2)    
    @property
    def player(self):
        return self.__player
    
    #Return the winner of this board: 1, 2 or None    
    @property
    def winner(self):
        return self.__winner
    
    #Return True if the board is a final state    
    def is_final_state(self):
        return len(self.__movements)==0 or self.__winner != None
    
    #Return True if the board is a winning board    
    def is_winning_state(self):
        return self.__winner == self.__player
    
    def __compute_winner(self):
       for i in range(6):
           for j in range(8):
               if (self.__board[i][j]==0):
                   continue
               for inc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,1)]:
                   x = i + inc[0]
                   y = j + inc[1]
                   length = 1
                   while (x>=0 and y>=0 and x<6 and y<8 and self.__board[x][y] == self.__board[i][j]):
                       length+=1
                       x += inc[0]
                       y += inc[1]
                       if (length==4):
                           return self.__board[i][j]
       return None
            
                  
    
    # Return a new state after applying a movement. If the movement can not be applied, it returns None
    def apply_movement(self,movement):
        depth = 0
        while (depth<6 and self.__board[depth][movement]==0):
            depth+=1
        if (depth==0):
            return None
        newboard = copy.deepcopy(self.__board)
        newboard[depth-1][movement] = self.__player
        newstate = State(newboard, 1 if self.__player==2 else 2)
        return newstate
         
    def __str__(self):
        newrow = '+---+---+---+---+---+---+---+---+\n'
        cad = newrow
        for i in range(6):
            cad += "|"
            for j in range(8):
                if (self.__board[i][j]==0):
                    cad+="   |"
                elif (self.__board[i][j]==1):
                    cad+=" X |"
                else:
                    cad+=" O |"
            cad +="\n"+newrow
        cad+="Player: "+str(self.__player)+"\n"
        cad+="Winner: "+str(self.__winner)
        return cad
    
    def __repr__(self):
        return self.__str__()
        
        
   # This class is an abstract strategy class for implementing different heuristics   
class Heuristic(object):
    def heuristic(self, state, player): # To implement
        raise NotImplementedError('C4Heuristic is an abstract class!')
    
    
    # This is an example of the Heuristic class by giving 100 points if the state is a winning
    # state, -100 points if it is a losing state and 0 points otherwise.
    # It is very naive, of course...
    
class HeuristicaNeuronal(Heuristic):
    
    instance = None
    
    def __init__(self,redNeuronal):
        self._redNeuro = redNeuronal
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
             cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance   
    
    def heuristic(self, state, player):
        tablero = state.board
        v = [tablero[0]+tablero[1]+tablero[2]+tablero[3]+tablero[4]+tablero[5]]
        if (state.winner==None):
            return self._redNeuro.activacion(v)
        if (state.winner==player):
            return 1000000
        return -1000000

    
class ExtremelyNaiveHeuristic(Heuristic):
        # Singleton pattern  
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
             cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance   
 
    def heuristic(self, state, player):
        if (state.winner==None):
            return 0
        if (state.winner==player):
            return 1000000
        return -1000000
  
    # This non so naive heuristic count the number of possible slots for each player
    # and return a weighted sum
    
class NonSoNaiveHeuristic(Heuristic):
    # Singleton pattern  
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance   
 
    def heuristic(self, state, player):
        if (state.winner==player):
            return 1000000
        elif (state.winner!=None):
            return -1000000
        
        values = [[0,0,0,0],[0,0,0,0]]
        line = [0]*4
        for i in range(6):
            for j in range(8):
                 for inc in [(0,1),(1,0),(1,1),(-1,1)]:
                     x = i+3*inc[0]
                     y = j+3*inc[1]
                     if x<0 or y<0 or x>=6 or y>=8:
                         continue
                     for k in range(4):
                         line[k] = state.board[i+k*inc[0]][j+k*inc[1]]
                     if 1 in line and 2 not in line:
                         value = int(sum(line))
                         values[0][value-1]+=1
                     elif 2 in line and 1 not in line:
                         value = int(sum(line)/2)
                         values[1][value-1]+=1
        if player==1:
            if (state.player==2 and values[1][2]>0):
                return -1000000
            if (state.player==1 and values[0][2]>0):
                return 1000000
            return (values[0][0] - values[1][0]) + 10*(values[0][1] - values[1][1]) +100*(values[0][2] - values[1][2])
        else:
            if (state.player==1 and values[0][2]>0):
                return -1000000
            if (state.player==2 and values[1][2]>0):
                return 1000000             
            return (values[1][0] - values[0][0]) + 10*(values[1][1] - values[0][1]) +100*(values[1][2] - values[0][2])           
  

    
class MinimaxAlgorithm(object):
   
    def __init__(self,min_value,max_value,heuristic):
        self.__min_value = min_value
        self.__max_value = max_value
        self.__heuristic = heuristic
      
        
    def test(self,depth=4):
        state = State()
        r1 = Red_Neuronal.RedNeuronal(48,5,5,1)
        print(state)
        while (state != None and not state.is_final_state()):
            state = self.minimax_decision_a_b(state,depth,state.player)
            aux = state.board[0]+state.board[1]+state.board[2]+state.board[3]+state.board[4]+state.board[5]
            aux2 = r1.activacion(aux) 
            print(aux2[0])
            print(state)
    
    
    def minimax_decision(self,current, depth,max_player):
        max_node = None
        max_val = self.__min_value
        sucessors = [current.apply_movement(movement) for movement in current.movements]
        for node in sucessors:
            current_value = self.__minimax_value(node,depth-1,max_player)            
            if (current_value >= max_val):
                max_val = current_value
                max_node = node
        return max_node
        
        
    def minimax_decision_a_b(self,current,depth,max_player):
        max_node = None            
        alpha = self.__min_value
        sucessors = [current.apply_movement(movement) for movement in current.movements]
        for node in sucessors:
            current_value = self.__minimax_value_a_b(node,depth-1,alpha,self.__max_value,max_player)            
            if (current_value > alpha):
                alpha = current_value
                max_node = node
            if (alpha >= self.__max_value):
                break
        return max_node
    
    def __minimax_value(self,node,depth, max_player):
        if node.is_final_state() or depth==0 or len(node.movements)==0:
            return self.__heuristic.heuristic(node,node.player)
        sucessors = [node.apply_movement(movement) for movement in node.movements]
        if node.player == max_player:
            return self.__max(sucessors,depth-1,max_player)
        else:
            return self.__min(sucessors,depth-1,max_player)
    
    
    def __minimax_value_a_b(self,node,depth, alpha, beta, max_player):
        if node.is_final_state() or depth==0 or len(node.movements)==0:
            return self.__heuristic.heuristic(node,node.player)
        sucessors = [node.apply_movement(movement) for movement in node.movements]
        if node.player == max_player:
            return self.__max_a_b(sucessors,depth-1,alpha, beta, max_player)
        else:
            return self.__min_a_b(sucessors,depth-1,alpha,beta,max_player)        
    
    def __max(self,sucessors,depth,max_player):
        max_val = self.__min_value
        for node in sucessors:
            current_value = self.__minimax_value(node,depth,max_player)
            if (current_value >= max_val):
                max_val = current_value
        return max_val
    
    
    
    def __max_a_b(self,sucessors,depth,alpha,beta,max_player):
        for node in sucessors:
            current_value = self.__minimax_value_a_b(node,depth,alpha,beta,max_player)
            if (current_value > alpha):
                alpha = current_value
            if alpha >= beta:
                break
        return alpha        
    
    def __min(self,sucessors,depth,max_player):
        min_val = self.__max_value
        for node in sucessors:
            current_value = self.__minimax_value(node,depth,max_player)
            if (current_value <= min_val):
                min_val = current_value
        return min_val
        
    def __min_a_b(self,sucessors,depth,alpha,beta,max_player):
        for node in sucessors:
            current_value = self.__minimax_value_a_b(node,depth,alpha,beta,max_player)
            if (current_value < beta):
                beta = current_value
            if alpha>=beta:
                break
        return beta
            
            
            
# This is a test:            
# minimax = MinimaxAlgorithm(-9999999,9999999,NonSoNaiveHeuristic())  
# minimax.test()          
            
# We can compare heuristics by playing together

# This function receives two heuristics. Player 1 plays with heuristic1 and player 2 plays with heuristic2
# The function returns 0 if draws. 1 if player 1 wins. 2 if player 2 wins.
def compareHeuristics(heuristic1, heuristic2,depth=4,verbose=False):
    algorithm1 = MinimaxAlgorithm(-10000000,10000000,heuristic1)
    algorithm2 = MinimaxAlgorithm(-10000000,10000000,heuristic2)
    state = State()
    if (verbose):
        print(state)
    while (state != None and not state.is_final_state()):
        if (state.player==1):
            state = algorithm1.minimax_decision_a_b(state,depth,state.player)
        else:
            state = algorithm2.minimax_decision_a_b(state,depth,state.player)
        if (verbose):
            print(state)
    if state==None or state.winner==None:
        return 0
    return state.winner


    
def cromosomaPesos(redNeuronal):
    lista = redNeuronal.pesosEnLista()
    return genetico.Cromosoma(lista)

def muta(lista):
    
    lista1 = []
    for l in lista:
        elem = l*2-1
        lista1.append(elem)
    lista1.reverse()
    return lista1

    
             
# Example:
# compareHeuristics(ExtremelyNaiveHeuristic(),NonSoNaiveHeuristic(),5,True)
# compareHeuristics(HeuristicaNeuronal(Red_Neuronal.RedNeuronal(48,5,5,1)),HeuristicaNeuronal(Red_Neuronal.RedNeuronal(48,5,5,1)),5,True)

