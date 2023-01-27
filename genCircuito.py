from random import random

from random import  *
from Graph import *

#Function that generates array of random integeres in a range.
def generateRList (l,col):
    randomlist = []

    for i in range(0, l - 1):
        n = randint(1, col - 2)
        randomlist.append(n)
    return randomlist

#Functions that generates all the track , given the size and the file you want to print on
def generateCircuito(l,col,file):
        map= [["X" for _ in range(col)] for _ in range(l)]
        i=1
        j=1
        c=-1
        for p in map:
            c+=1
            if c==0 or c==l-1:
                print ("")
            else:
                i=1
                while i < col-1:
                    p[i] = "-"
                    i+=1
        k = randint(1, l-4)
        m = k + 3
        while k < m:
            map[k][col-1] = "F"
            k += 1

        counter = 0
        while counter < col:
            list = generateRList(l, col)
            k=1
            while k < l - 1:
                for pos in list:
                    map[k][pos] = "X"
                    k += 1
            counter += 10

        posPlayerl= randint(1,l-2)
        posPlayerc=randint(1,int((col-2)/2))

        map[posPlayerl][posPlayerc] = "P"

        fil=open(file,"w")
        for p in map:
            fil.write(convert(p) +"\n")
        fil.close()

        return map

def generateCircuito_two_players(l,col,file):
        map= [["X" for _ in range(col)] for _ in range(l)]
        i=1
        j=1
        c=-1
        for p in map:
            c+=1
            if c==0 or c==l-1:
                print ("")
            else:
                i=1
                while i < col-1:
                    p[i] = "-"
                    i+=1
        k = randint(1, l-4)
        m = k + 3
        while k < m:
            map[k][col-1] = "F"
            k += 1

        counter = 0
        while counter < col:
            list = generateRList(l, col)
            k=1
            while k < l - 1:
                for pos in list:
                    map[k][pos] = "X"
                    k += 1
            counter += 10

        posPlayerl= randint(1,l-2)
        posPlayerc=randint(1,int((col-2)/2))

        map[posPlayerl][posPlayerc] = "P"

        posPlayerl_two = randint(1,l-2)
        posPlayerc_two = posPlayerc 

        while (posPlayerl_two == posPlayerl):

            posPlayerl_two = randint(1,l-2)

        map[posPlayerl_two][posPlayerc_two] = "P"

        fil=open(file,"w")
        for p in map:
            fil.write(convert(p) +"\n")
        fil.close()

        return map

#Function to convert arraylist of char to string
def convert(s):

        # initialization of string to ""
        new = ""

        # traverse in the string
        for x in s:
            new += x

        # return string
        return new

def isValid(file):

    g = Graph(file)

    g.cria_grafo()

    map = g.getTrack()

    for node in g.getNodes():

        if map.finished_race(node.getPl(),node.getPc()):

            return True

    return False

def generateValidCircuito(l,col,file):

    map = generateCircuito(l,col,file)

    valid = isValid(file)

    while(not valid):

        map = generateCircuito(l,col)

        valid = isValid(file)

    return map
