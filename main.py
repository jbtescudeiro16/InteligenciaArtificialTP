from Parser import mParser
from Track import *
from genCircuito import *
from Graph import *
from Node import *

def menu_one_player():

    print("--------------------------ONE PLAYER---------------------------")
    print("|Insira a opção que pretende realizar:                        |")
    print("|1->Gerar mapa                                                |")
    print("|2->Representar pista em forma de grafo                       |")
    print("|3->Aplicar travessia em profundidade                         |")
    print("|4->Aplicar travessia em largura                              |")
    print("|5->Aplicar travessia greedy                                  |")
    print("|6->Aplicar travessia A*                                      |")
    print("|7->Sair                                                      |")
    print("---------------------------------------------------------------")
    opcao1=int(input())

    if opcao1==1 :

        print("Insira o número de linhas do mapa:")
        l = input()
        print("Insira o número de colunas do mapa:")
        col = input()
        print("Insira o nome do ficheiro em que pretende guardar o mapa: ")
        file=input()
        x = generateValidCircuito(int(l), int(col),str(file.strip("\n") + ".txt"))
        for line in x:
            print(convert(line))

        menu_one_player()

    elif (opcao1==2):

        print("Grafo direcionado? [S/n]")

        d = input()

        direcionado = d == "S" or d == "s"

        print("Insira o nome do ficheiro de onde pretende carregar o mapa:")

        l = input()

        g = Graph(l + ".txt", direcionado)

        g.cria_grafo()

        g.desenha()

        menu_one_player()
        
    elif(opcao1==3):

        print("Grafo direcionado? [S/n]")

        d = input()

        direcionado = d == "S" or d == "s"
        
        print("Insira o nome do ficheiro de onde pretende carregar o mapa:")

        l = input()

        g = Graph(l + ".txt", direcionado)

        g.cria_grafo()

        g.desenha_DFS()

        menu_one_player()

    elif(opcao1==4):

        print("Grafo direcionado? [S/n]")

        d = input()

        direcionado = d == "S" or d == "s"
        
        print("Insira o nome do ficheiro de onde pretende carregar o mapa:")

        l = input()

        g = Graph(l + ".txt", direcionado)

        g.cria_grafo()

        g.desenha_BFS()

        menu_one_player()

    elif(opcao1==5):

        print("Grafo direcionado? [S/n]")

        d = input()

        direcionado = d == "S" or d == "s"
        
        print("Insira o nome do ficheiro de onde pretende carregar o mapa:")

        l = input()

        g = Graph(l + ".txt", direcionado)

        g.cria_grafo()

        g.desenha_Greedy()

        menu_one_player()

    elif(opcao1==6):

        print("Grafo direcionado? [S/n]")

        d = input()

        direcionado = d == "S" or d == "s"
        
        print("Insira o nome do ficheiro de onde pretende carregar o mapa:")

        l = input()

        g = Graph(l + ".txt", direcionado)

        g.cria_grafo()

        g.desenha_a_star()

        menu_one_player()

    elif(opcao1 == 7):

        menu()

def menu_two_players():

    print("--------------------------TWO PLAYERS--------------------------")
    print("|Insira a opção que pretende realizar:                        |")
    print("|1->Gerar mapa                                                |")
    print("|2->Representar pista em forma de grafo                       |")
    print("|3->Aplicar travessias                                        |")
    print("|4->Sair                                                      |")
    print("---------------------------------------------------------------")
    
    opcao1=int(input())

    if opcao1==1:

        print("Insira o número de linhas do mapa:")
        l = input()
        print("Insira o número de colunas do mapa:")
        col = input()
        print("Insira o nome do ficheiro em que pretende guardar o mapa: ")
        file=input()
        x = generateCircuito_two_players(int(l), int(col),str(file.strip("\n") + ".txt"))
        for line in x:
            print(convert(line))

        menu_two_players()

    elif (opcao1==2):

        print("Insira o nome do ficheiro de onde pretende carregar o mapa:")

        l = input()

        g = Graph(l + ".txt", False)

        g.cria_grafo()

        g.desenha()

        menu_two_players()

    elif opcao1 == 3:

        print("Insira o nome do ficheiro de onde pretende carregar o mapa:")

        mapa = input()

        print("--------------------Travessia do Player One--------------------")
        print("|1->Travesia em profundidade                                  |")
        print("|2->Travessia em largura                                      |")
        print("|3->Travessia Greedy                                          |")
        print("|4->Travessia A*                                              |")
        print("---------------------------------------------------------------")

        opcao2 = int(input())

        print("--------------------Travessia do Player Two--------------------")
        print("|1->Travesia em profundidade                                  |")
        print("|2->Travessia em largura                                      |")
        print("|3->Travessia Greedy                                          |")
        print("|4->Travessia A*                                              |")
        print("---------------------------------------------------------------")

        opcao3 = int(input())
        
        g = Graph(mapa + ".txt", False)

        g.cria_grafo()

        g.desenha_two_players(opcao2-1,opcao3-1)

        menu_two_players()

    elif opcao1 == 4:

        menu()

def menu():

    print("------------------IA-TP-GRUPO_Nº38--2022/2023------------------")
    print("|Escolha o número de jogadores no mapa:                       |")
    print("|1->One Player                                                |")
    print("|2->Two Players                                               |")
    print("|3->Sair                                                      |")
    print("---------------------------------------------------------------")

    opcao1=int(input())

    if opcao1 == 1:

        menu_one_player()

    elif opcao1 == 2:

        menu_two_players()

    elif opcao1 == 3:

        return

menu()