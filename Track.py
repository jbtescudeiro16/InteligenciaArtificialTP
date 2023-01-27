from Parser import mParser
from Node import *

from colorama import Fore, Back, Style

class Track: 

    def __init__ (self, path):

        self.path = path
        self.matrix = mParser(path)

    def print_track(self):

        for line in self.matrix:
            
            for char in line:

                if (char == 'o' or char == 'P' or char == 'F'):

                   print(Fore.GREEN + char, end="")

                else:

                    print(Fore.WHITE + char, end="")

            print()

    def get_path(self):

        return self.path

    def set_position_visited(self, linha, coluna):

        list = []

        counter = 0

        for char in self.matrix[linha]:

            if (counter == coluna and char != 'P' and char != 'F'):
                    
                list.append('o')
            
            else:
                
                list.append(char)
            
            counter += 1

        self.matrix[linha] = ''.join(list)

    def getWalls(self):

        result = []

        i = 0

        for line in self.matrix:

            j = 0

            for pos in line:

                if pos == 'X':

                    result.append(Node(-1,i,j,True)) 

                j += 1

            i += 1

        return result

    def inside_track(self,x,y):

        if (x < 0 or x >= self.getNumLinhas()):
            return False
        if (y < 0 or y >= self.getNumColunas()):
            return False

        return self.matrix[x][y] != 'X'

    def is_wall(self,x,y):

        if (x < 0 or x >= self.getNumLinhas()):
            return False
        if (y < 0 or y >= self.getNumColunas()):
            return False

        return self.matrix[x][y] == 'X'

    def finished_race(self,x,y):

        if (x < 0 or x >= self.getNumLinhas()): 
            return False
        if (y < 0 or y >= self.getNumColunas()): 
            return False

        return self.matrix[x][y] == 'F'

    def get_Player_inicial_pos(self):

        x = -1

        for line in self.matrix:

            x += 1

            y = -1

            for pos in self.matrix[x]:

                y += 1

                if (pos == 'P'):

                    return [y,x]

    def get_Player_inicial_pos_two_players(self):

        result = []

        x = -1

        for line in self.matrix:

            x += 1

            y = -1

            for pos in self.matrix[x]:

                y += 1

                if (pos == 'P'):

                    result.append([y,x])

        return result

    def get_Player_final_pos(self):

        result = []

        x = -1

        for line in self.matrix:

            x += 1

            y = -1

            for pos in self.matrix[x]:

                y += 1

                if (pos == 'F'):

                    result.append([y,x])
        
        return result

    def get_middle_f(self):

        return self.get_Player_final_pos()[1]

    def getNumLinhas(self):

        counter = 0

        for line in self.matrix:

            counter += 1

        return counter

    def getNumColunas(self):

        counter = 0

        for pos in self.matrix[0]:

            counter += 1

        return counter

    def possible_pos(self):

        counter = 0

        for line in self.matrix:

            for pos in line:

                if (pos == '-' or pos == 'P' or pos == 'F'):

                    counter += 1

        return counter
