from Node import *
from Track import *

import math
from queue import Queue

import networkx as nx  # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # idem

# adiconar as paredes à lista de vizinhos na fst A*, snd A*, fst Greedy, snd Greedy

class Graph:

    def __init__ (self, path, directed=True):

        self.nodes = []
        self.graph = {}
        self.h = {}
        self.track = Track(path)
        self.directed = directed

        playerInitPos = self.track.get_Player_inicial_pos()

        fst_node = Node(0, playerInitPos[0], playerInitPos[1])

        self.nodes.append(fst_node)

        self.graph[fst_node.getId()] = list()

        self.calcula_heuristica(None,0)

        self.walls = self.track.getWalls()
    
    def __str__ (self):
        
        out = ""
        for key in self.graph.keys():
            out += "node" + str(key) + ": " + str(self.graph[key]) + "\n"
            return out

    def getTrack(self):

        return self.track

    def getWalls(self):

        return self.walls
        
    def get_node_by_id(self, node_id):

        for node in self.nodes:
            if node.getId() == node_id:
                return node
            
        return None

    def get_node_by_pos(self,Pl,Pc):

        for node in self.nodes:

            if node.getPl() == Pl and node.getPc() == Pc:

                return node 
        
        return None

    def node_exists(self, node_id):

        for node in self.nodes:
            if node.getId() == node_id:
                return True
            
        return False

    def edge_exists(self, node1, node2, weight):

        if ( (not self.node_exists(node1.getId())) or (not self.node_exists(node2.getId()))):

            return False

        if ((node2,weight) in self.graph[node1.getId()]):

            return True

        if ((node1,weight) in self.graph[node2.getId()]):

            return True

        return False

    def add_edge(self, node1, node2, weight):

        if (self.edge_exists(node1,node2,weight)):

            return

        n1 = node1.clone()
        n2 = node2.clone()

        if (n1 not in self.nodes):
            self.nodes.append(n1)
            self.graph[node1.getId()] = list()
            self.h[node1.getId()] = list()
        else:
            n1 = self.get_node_by_id(node1.getId())

        if (n2 not in self.nodes):
            self.nodes.append(n2)
            self.graph[node2.getId()] = list()
            self.h[node2.getId()] = list()
        else:
            n2 = self.get_node_by_id(node2.getId())

        self.graph[node1.getId()].append((node2, weight))

        if not self.directed:
            self.graph[node2.getId()].append((node1, weight))

    def getNodes(self):
        return self.nodes

    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.graph[node1.getId()] 
        for (nodo, custo) in a:
            if nodo == node2:
                custoT = custo

        return custoT

    def calcula_custo(self, caminho):
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            
            i = i + 1
        return custo

    def calcula_heuristica(self, nodo_pai_id, nodo_atual_id):

        # Heuristica (Vel Pc, Vel Pl, Valor numérico da heuristica)

        # o primeiro nodo tem heuristica 0
        if (nodo_pai_id == None or nodo_pai_id == -1):

            self.h[nodo_atual_id] = list()

            self.h[nodo_atual_id].append((0,0,0))

            return

        if (nodo_atual_id == -1):

            self.h[nodo_atual_id] = list()

            self.h[nodo_atual_id].append((0,0,0))

            return

        # calcular o centro da meta
        f_pos = self.track.get_middle_f()

        f_pos_Pc = f_pos[0]
        f_pos_Pl = f_pos[1]

        # calcular posição do nodo pai
        nodo_pai = self.get_node_by_id(nodo_pai_id)

        nodo_pai_Pc = nodo_pai.getPc()
        nodo_pai_Pl = nodo_pai.getPl()

        # calcular posição do nodo atual
        
        nodo_atual = self.get_node_by_id(nodo_atual_id)

        nodo_atual_Pc = nodo_atual.getPc()
        nodo_atual_Pl = nodo_atual.getPl()

        # calcular incremento do velocidade
        vel_Pc_inc = nodo_atual_Pc - nodo_pai_Pc
        vel_Pl_inc = nodo_atual_Pl - nodo_pai_Pl

        # adicionar o incremento de velocidade e calcular o valor numérico da heuristica
        heuristica_do_pai = self.h[nodo_pai_id][0]

        atual_vel_pc = heuristica_do_pai[1] + vel_Pc_inc
        atual_vel_pl = heuristica_do_pai[2] + vel_Pl_inc

        pc_dist_dif = f_pos_Pc - nodo_atual_Pc
        pl_dist_dif = f_pos_Pl - nodo_atual_Pl

        valor_numerico = 0

        valor_numerico = 0

        # precisa de aumentar a pos coluna
        if (f_pos_Pc - nodo_atual_Pc < 0):

            valor_numerico -= atual_vel_pc

        # precisa de dimunir a pos coluna
        elif (f_pos_Pc - nodo_atual_Pc > 0):

            valor_numerico += atual_vel_pc

        # precisa de aumentar a pos linha
        if (f_pos_Pl - nodo_atual_Pl < 0):

            valor_numerico -= atual_vel_pl

        # precisa de diminuir a pos linha
        elif (f_pos_Pl - nodo_atual_Pl > 0):

            valor_numerico += atual_vel_pl

        heuristica_do_atual = (atual_vel_pc, atual_vel_pl, -valor_numerico)

        if (len(self.h[nodo_atual_id]) != 0):

            self.h[nodo_atual_id] = list()
            
        self.h[nodo_atual_id].append(heuristica_do_atual)

    def print_heuristicas(self):

        for node in self.nodes:

            node_id = node.getId()

            print(str(node_id) + " HEURISTICAS ")

            for h in self.h[node_id]:

                print(str(h))

            print()


    def expande(self, id):

        nodo = self.get_node_by_id(id)

        Pc = nodo.getPc()
        Pl = nodo.getPl()

        # superior esquerdo
        
        if (self.track.inside_track(Pl-1,Pc-1)):

            novo_nodo = Node(len(self.nodes), Pc-1, Pl-1) 

            for node in self.nodes:

                if novo_nodo.is_equal(node):

                    novo_nodo.setId(node.getId())
            
            self.add_edge(nodo,novo_nodo,1)
                
            self.calcula_heuristica(id, novo_nodo.getId())

        # esquerda

        if (self.track.inside_track(Pl,Pc-1)):

            novo_nodo = Node(len(self.nodes), Pc-1, Pl)

            for node in self.nodes:

                if novo_nodo.is_equal(node):

                    novo_nodo.setId(node.getId())

            self.add_edge(nodo,novo_nodo,1)

            self.calcula_heuristica(id, novo_nodo.getId())

        # superior direito
        
        if (self.track.inside_track(Pl-1,Pc+1)):

            novo_nodo = Node(len(self.nodes), Pc+1, Pl-1)

            for node in self.nodes:

                if novo_nodo.is_equal(node):

                    novo_nodo.setId(node.getId())

            self.add_edge(nodo,novo_nodo,1)

            self.calcula_heuristica(id, novo_nodo.getId())
        
        # direita

        if (self.track.inside_track(Pl,Pc+1)):

            novo_nodo = Node(len(self.nodes), Pc+1, Pl)

            for node in self.nodes:

                if novo_nodo.is_equal(node):

                    novo_nodo.setId(node.getId())

            self.add_edge(nodo,novo_nodo,1)

            self.calcula_heuristica(id, novo_nodo.getId())

        # inferior direito

        if (self.track.inside_track(Pl+1,Pc+1)):

            novo_nodo = Node(len(self.nodes), Pc+1, Pl+1)

            for node in self.nodes:

                if novo_nodo.is_equal(node):

                    novo_nodo.setId(node.getId())

            self.add_edge(nodo,novo_nodo,1)

            self.calcula_heuristica(id, novo_nodo.getId())

        # cima

        if (self.track.inside_track(Pl-1,Pc)):

            novo_nodo = Node(len(self.nodes), Pc, Pl-1)

            for node in self.nodes:

                if novo_nodo.is_equal(node):

                    novo_nodo.setId(node.getId())

            self.add_edge(nodo,novo_nodo,1)

            self.calcula_heuristica(id, novo_nodo.getId())

        # inferior esquerdo

        if (self.track.inside_track(Pl+1,Pc-1)):

            novo_nodo = Node(len(self.nodes), Pc-1, Pl+1)

            for node in self.nodes:

                if novo_nodo.is_equal(node):

                    novo_nodo.setId(node.getId())

            self.add_edge(nodo,novo_nodo,1)

            self.calcula_heuristica(id, novo_nodo.getId())

        # baixo

        if (self.track.inside_track(Pl+1,Pc)):

            novo_nodo = Node(len(self.nodes), Pc, Pl+1)

            for node in self.nodes:

                if novo_nodo.is_equal(node):

                    novo_nodo.setId(node.getId())

            self.add_edge(nodo,novo_nodo,1)

            self.calcula_heuristica(id, novo_nodo.getId())

    
    def cria_grafo(self):
    
        counter = 0

        while (len(self.nodes) > counter):

            self.expande(counter)

            counter += 1
    
    def desenha(self):
        
        G = nx.DiGraph()
        
        for node in self.nodes:

            G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()))

            for (nodeADJ, weight) in self.graph[node.getId()]:

                G.add_node(nodeADJ.getId(),pos=(nodeADJ.getPc(),self.track.getNumLinhas() - nodeADJ.getPl()))
                G.add_edge(node.getId(),nodeADJ.getId())

        pos = nx.get_node_attributes(G,'pos')
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='silver')
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='slategray')
        nx.draw_networkx_labels(G, pos)

        plt.text(0.2, 0.8, "Green and Orange: Player Path", fontsize = 10)

        plt.show()

    def is_connected(self,path,node1,node2):

        index1 = path.index(node1)
        index2 = path.index(node2)

        return abs(index1-index2) == 1

    def procura_DFS(self, start, end, path=[], visited=set()):

        if path == None:

            path = []
            visited = set()
        
        path.append(start)
        visited.add(start)

        if start in end:
            # calcular o custo do caminho funçao calcula custo.
            custoT = self.calcula_custo(path)
            return (path, custoT)
        for (adjacente, peso) in self.graph[start.getId()]:
            if adjacente not in visited:
                
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()  # se nao encontra remover o que está no caminho......
        return None
    
    def procura_DFS_snd_player(self, start, end, player_one_path, path=[], visited=set()):

        if path == None:

            path = []
            visited = set()

        path.append(start)
        visited.add(start)

        if start in end:
            # calcular o custo do caminho funçao calcula custo.
            custoT = self.calcula_custo(path)
            return (path, custoT)
        for (adjacente, peso) in self.graph[start.getId()]:
            if len(player_one_path) == 0:
                player_one_path.append(None)
            if (adjacente not in visited) and (not adjacente.is_equal(player_one_path[0])):
                resultado = self.procura_DFS_snd_player(adjacente, end, player_one_path[1:], path, visited)
                if resultado is not None:
                    return resultado
        path.pop()  # se nao encontra remover o que está no caminho......
        return None
    
    def desenha_DFS(self):

        track_to_print = Track(self.track.get_path())

        start_pos = self.track.get_Player_inicial_pos()
        end_pos = self.track.get_Player_final_pos()

        start = self.get_node_by_pos(start_pos[1],start_pos[0])

        end_list = []

        for pos in end_pos:

            end_list.append(self.get_node_by_pos(pos[1],pos[0]))

        res = self.procura_DFS(start,end_list)
        
        path = res[0]

        G = nx.DiGraph()
        
        for node in self.nodes:

            if (node in path):

                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='springgreen')
                track_to_print.set_position_visited(node.getPl(),node.getPc())

            else:
                
                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='silver')

            for (nodeADJ, weight) in self.graph[node.getId()]:

                if (node in path and nodeADJ in path and self.is_connected(path,node,nodeADJ)):
                    
                    G.add_edge(node.getId(),nodeADJ.getId(), color='darkorange')

                else:

                    G.add_edge(node.getId(),nodeADJ.getId(), color='slategray')

        track_to_print.print_track()
        print("Custo: " + str(res[1]))

        colors = nx.get_node_attributes(G, 'color').values()
        colorsEDGE = nx.get_edge_attributes(G, 'color').values()
        pos = nx.get_node_attributes(G,'pos')
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=colors)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=colorsEDGE)
        nx.draw_networkx_labels(G, pos)

        plt.text(0.2, 0.8, "Green and Orange: Player Path", fontsize = 10)

        plt.show()

    def procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()

        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        nodo_final = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual in end:
                path_found = True
                nodo_final = nodo_atual
            else:
                for (adjacente, peso) in self.graph[nodo_atual.getId()]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)



        # Reconstruir o caminho

        path = []
        if path_found:
            path.append(nodo_final)
            while parent[nodo_final] is not None:
                path.append(parent[nodo_final])
                nodo_final = parent[nodo_final]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path)
        return (path, custo)

    def procura_BFS_snd_player(self, start, end, player_one_path):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()

        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        nodo_final = None

        # TODO
        # criar uma variavel depth e testar com o index igual a depth 
        # na lista das posiçoes do player one path

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual in end:
                path_found = True
                nodo_final = nodo_atual
            else:
                for (adjacente, peso) in self.graph[nodo_atual.getId()]:
                    if adjacente not in visited:

                        depth = 0

                        n = nodo_atual

                        while n != None:

                            n = parent[n]
                            depth += 1

                        if depth >= len(player_one_path) or adjacente != player_one_path[depth]:

                            fila.put(adjacente)
                            parent[adjacente] = nodo_atual

                            visited.add(adjacente)

        # Reconstruir o caminho

        path = []
        if path_found:
            path.append(nodo_final)
            while parent[nodo_final] is not None:
                path.append(parent[nodo_final])
                nodo_final = parent[nodo_final]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path)
        return (path, custo)

    def desenha_BFS(self):

        track_to_print = Track(self.track.get_path())

        start_pos = self.track.get_Player_inicial_pos()
        end_pos = self.track.get_Player_final_pos()

        start = self.get_node_by_pos(start_pos[1],start_pos[0])

        end_list = []

        for pos in end_pos:

            end_list.append(self.get_node_by_pos(pos[1],pos[0]))

        res = self.procura_BFS(start,end_list)
        
        path = res[0]

        G = nx.DiGraph()
        
        for node in self.nodes:

            if (node in path):

                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='springgreen')
                track_to_print.set_position_visited(node.getPl(),node.getPc())

            else:
                
                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='silver')

            for (nodeADJ, weight) in self.graph[node.getId()]:

                if (node in path and nodeADJ in path and self.is_connected(path,node,nodeADJ)):
                    
                    G.add_edge(node.getId(),nodeADJ.getId(), color='darkorange')

                else:

                    G.add_edge(node.getId(),nodeADJ.getId(), color='slategray')

        track_to_print.print_track()
        print("Custo: " + str(res[1]))

        colors = nx.get_node_attributes(G, 'color').values()
        colorsEDGE = nx.get_edge_attributes(G, 'color').values()
        pos = nx.get_node_attributes(G,'pos')
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=colors)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=colorsEDGE)
        nx.draw_networkx_labels(G, pos)

        plt.text(0.2, 0.8, "Green and Orange: Player Path", fontsize = 10)

        plt.show()

    def isADJ(self, nodo1, nodo2):

        nodo1_pl = nodo1.getPl()
        nodo1_pc = nodo1.getPc()
        nodo2_pl = nodo2.getPl()
        nodo2_pc = nodo2.getPc()

        dif_pl = nodo1_pl - nodo2_pl
        dif_pc = nodo1_pc - nodo2_pc

        if dif_pl == 0 and dif_pc == 0:

            return False

        if dif_pl != -1 and dif_pl != 0 and dif_pl != 1:

            return False

        if dif_pc != -1 and dif_pc != 0 and dif_pc != 1:

            return False

        return True

    def getNeighboursWalls(self, nodo):

        walls = self.getWalls()

        nodo_pl = nodo.getPl()
        nodo_pc = nodo.getPc()

        result = []

        for wall in walls:

            if self.isADJ(nodo, wall):

                result.append((wall,1))

        return result

    def getNeighbours(self, nodo):
        lista = []
        for (adjacente, peso) in self.graph[nodo.getId()]:
            lista.append((adjacente, peso))

        for wall in self.walls:

            lista.append((wall,25))

        return lista

    def greedy(self, start, end):
        
        open_list = set([start])
        closed_list = set([])

        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None
            
            for v in open_list:

                if n == None: 
                    n = v

                else:

                    # recalcular heuristicas

                    self.calcula_heuristica(parents[v].getId(), v.getId())
                    self.calcula_heuristica(parents[n].getId(), n.getId())

                    if self.h[v.getId()][0][2] < self.h[n.getId()][0][2]:

                        n = v

            if n == None:
                print('Path does not exist!')
                return None

            print(n)

            if (n.isWall()):

                open_list.remove(n)
                closed_list.add(n)

                continue
            
            if n in end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.getNeighbours(n):
                
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def greedy_snd_player(self, start, end, player_one_path):
        
        open_list = set([start])
        closed_list = set([])

        parents = {}
        parents[start] = start

        while len(open_list) > 0:

            n = None
            
            for v in open_list:

                if n == None: 
                    n = v

                else:

                    # recalcular heuristicas

                    self.calcula_heuristica(parents[v].getId(), v.getId())
                    self.calcula_heuristica(parents[n].getId(), n.getId())

                    if self.h[v.getId()][0][2] < self.h[n.getId()][0][2]:

                        n = v

            if n == None:
                print('Path does not exist!')
                return None

            print(n)

            if (n.isWall()):

                open_list.remove(n)
                closed_list.add(n)

                continue
            
            if n in end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.getNeighbours(n):
                
                if m not in open_list and m not in closed_list:

                    depth = 1

                    node = n

                    while node != start:

                        depth += 1
                        node = parents[node]

                    if depth >= len(player_one_path) or m != player_one_path[depth]:    

                        open_list.add(m)
                        parents[m] = n

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def desenha_Greedy(self):

        track_to_print = Track(self.track.get_path())

        start_pos = self.track.get_Player_inicial_pos()
        end_pos = self.track.get_Player_final_pos()

        start = self.get_node_by_pos(start_pos[1],start_pos[0])

        end_list = []

        for pos in end_pos:

            end_list.append(self.get_node_by_pos(pos[1],pos[0]))

        res = self.greedy(start,end_list)
        
        path = res[0]

        G = nx.DiGraph()
        
        for node in self.nodes:

            if (node in path):

                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='springgreen')
                track_to_print.set_position_visited(node.getPl(),node.getPc())

            else:
                
                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='silver')

            for (nodeADJ, weight) in self.graph[node.getId()]:

                if (node in path and nodeADJ in path and self.is_connected(path,node,nodeADJ)):
                    
                    G.add_edge(node.getId(),nodeADJ.getId(), color='darkorange')

                else:

                    G.add_edge(node.getId(),nodeADJ.getId(), color='slategray')

        track_to_print.print_track()
        print("Custo: " + str(res[1]))

        colors = nx.get_node_attributes(G, 'color').values()
        colorsEDGE = nx.get_edge_attributes(G, 'color').values()
        pos = nx.get_node_attributes(G,'pos')
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=colors)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=colorsEDGE)
        nx.draw_networkx_labels(G, pos)

        plt.text(0.2, 0.8, "Green and Orange: Player Path", fontsize = 10)

        plt.show()

    def calcula_est(self, estima):
        l = list(estima.keys())
        min_estima = estima[l[0]]
        node = l[0]
        for k, v in estima.items():
            if v < min_estima:
                min_estima = v
                node = k
        return node

    def procura_aStar(self, start, end):
        
        open_list = {start}
        closed_list = set([])

        g = {} 

        g[start] = 0

        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
           
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else:
                    flag = 1
                    # recalcular heuritica
                    self.calcula_heuristica(parents[v].getId(), v.getId())
                    calc_heurist[v] = g[v] + self.h[v.getId()][0][2]
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)
                n = min_estima
            if n == None:
                print('Path does not exist!')
                return None

            print(n)

            if (n.isWall()):

                open_list.remove(n)
                closed_list.add(n)

                continue

            if n in end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.getNeighbours(n): 
              
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def procura_aStar_snd_player(self, start, end, player_one_path):
        
        open_list = {start}
        closed_list = set([])

        g = {} 

        g[start] = 0

        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
           
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else:
                    flag = 1
                    # recalcular heuritica
                    self.calcula_heuristica(parents[v].getId(), v.getId())
                    calc_heurist[v] = g[v] + self.h[v.getId()][0][2]
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)
                n = min_estima
            if n == None:
                print('Path does not exist!')
                return None

            print(n)

            if (n.isWall()):

                open_list.remove(n)
                closed_list.add(n)

                continue

            if n in end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            for (m, weight) in self.getNeighbours(n): 
              
                if m not in open_list and m not in closed_list:

                    depth = 1

                    node = n

                    while node != start:

                        depth += 1
                        node = parents[node]

                    if depth >= len(player_one_path) or m != player_one_path[depth]:

                        open_list.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight

                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
        

    def desenha_a_star(self):

        track_to_print = Track(self.track.get_path())

        start_pos = self.track.get_Player_inicial_pos()
        end_pos = self.track.get_Player_final_pos()

        start = self.get_node_by_pos(start_pos[1],start_pos[0])

        end_list = []

        for pos in end_pos:

            end_list.append(self.get_node_by_pos(pos[1],pos[0]))

        res = self.procura_aStar(start,end_list)
        
        path = res[0]

        G = nx.DiGraph()
        
        for node in self.nodes:

            if (node in path):

                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='springgreen')
                track_to_print.set_position_visited(node.getPl(),node.getPc())

            else:
                
                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='silver')

            for (nodeADJ, weight) in self.graph[node.getId()]:

                if (node in path and nodeADJ in path and self.is_connected(path,node,nodeADJ)):
                    
                    G.add_edge(node.getId(),nodeADJ.getId(), color='darkorange')

                else:

                    G.add_edge(node.getId(),nodeADJ.getId(), color='slategray')

        track_to_print.print_track()
        print("Custo: " + str(res[1]))

        colors = nx.get_node_attributes(G, 'color').values()
        colorsEDGE = nx.get_edge_attributes(G, 'color').values()
        pos = nx.get_node_attributes(G,'pos')
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=colors)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=colorsEDGE)
        nx.draw_networkx_labels(G, pos)

        plt.text(0.2, 0.8, "Green and Orange: Player Path", fontsize = 10)

        plt.show()
    
    def generate_two_player_path(self, player_1_travessia_tag, player_2_travessia_tag):

        # tags
        # 0 profundidade
        # 1 largura
        # 2 greedy
        # 3 a*

        result = []

        players_pos = self.track.get_Player_inicial_pos_two_players()

        player_one_pos = players_pos[0]
        player_two_pos = players_pos[1]

        end_pos = self.track.get_Player_final_pos()

        end_list = []

        for pos in end_pos:

            end_list.append(self.get_node_by_pos(pos[1],pos[0]))

        # travessia do Player One
        start_player_one = self.get_node_by_pos(player_one_pos[1],player_one_pos[0])

        if player_1_travessia_tag == 0:

            result.append(self.procura_DFS(start_player_one, end_list, None))

        elif player_1_travessia_tag == 1:

            result.append(self.procura_BFS(start_player_one, end_list))

        elif player_1_travessia_tag == 2:

            result.append(self.greedy(start_player_one, end_list))

        elif player_1_travessia_tag == 3:

            result.append(self.procura_aStar(start_player_one, end_list))

        # travessia do Player Two
        start_player_two = self.get_node_by_pos(player_two_pos[1],player_two_pos[0])

        if player_2_travessia_tag == 0:

            result.append(self.procura_DFS_snd_player(start_player_two, end_list, result[0][0][1:], None))

        elif player_2_travessia_tag == 1:

            result.append(self.procura_BFS_snd_player(start_player_two, end_list, result[0][0]))

        elif player_2_travessia_tag == 2:

            result.append(self.greedy_snd_player(start_player_two, end_list, result[0][0]))

        elif player_2_travessia_tag == 3:

            result.append(self.procura_aStar_snd_player(start_player_two, end_list, result[0][0]))

        return result

    def desenha_player_one(self, path_player_one, custo_player_one, travessia):

        plt.figure(1)

        track_to_print = Track(self.track.get_path())

        G = nx.DiGraph()
        
        for node in self.nodes:

            if (node in path_player_one):

                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='springgreen')
                track_to_print.set_position_visited(node.getPl(),node.getPc())

            else:
                
                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='silver')

            for (nodeADJ, weight) in self.graph[node.getId()]:

                if (node in path_player_one and nodeADJ in path_player_one and self.is_connected(path_player_one,node,nodeADJ)):
                    
                    G.add_edge(node.getId(),nodeADJ.getId(), color='darkorange')

                else:

                    G.add_edge(node.getId(),nodeADJ.getId(), color='slategray')

        track_to_print.print_track()
        print("Custo Player One: " + str(custo_player_one))

        colors = nx.get_node_attributes(G, 'color').values()
        colorsEDGE = nx.get_edge_attributes(G, 'color').values()
        pos = nx.get_node_attributes(G,'pos')
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=colors)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=colorsEDGE)
        nx.draw_networkx_labels(G, pos)

        plt.gca().set_title("Player One - Travessia " + travessia)

        plt.text(0.2, 0.8, "Green and Orange: Player Path", fontsize = 10)

    def desenha_player_two(self, path_player_two, custo_player_two, travessia):

        plt.figure(2)

        track_to_print = Track(self.track.get_path())

        G = nx.DiGraph()
        
        for node in self.nodes:

            if (node in path_player_two):

                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='springgreen')
                track_to_print.set_position_visited(node.getPl(),node.getPc())

            else:
                
                G.add_node(node.getId(),pos=(node.getPc(),self.track.getNumLinhas() - node.getPl()), color='silver')

            for (nodeADJ, weight) in self.graph[node.getId()]:

                if (node in path_player_two and nodeADJ in path_player_two and self.is_connected(path_player_two,node,nodeADJ)):
                    
                    G.add_edge(node.getId(),nodeADJ.getId(), color='darkorange')

                else:

                    G.add_edge(node.getId(),nodeADJ.getId(), color='slategray')

        track_to_print.print_track()
        print("Custo Player Two: " + str(custo_player_two))

        colors = nx.get_node_attributes(G, 'color').values()
        colorsEDGE = nx.get_edge_attributes(G, 'color').values()
        pos = nx.get_node_attributes(G,'pos')
        
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=colors)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=colorsEDGE)
        nx.draw_networkx_labels(G, pos)

        plt.gca().set_title("Player Two - Travessia " + travessia)

        plt.text(0.2, 0.8, "Green and Orange: Player Path", fontsize = 10)

    def tag_to_travessia(self, tag):

        if (tag == 0):

            return "em profundidade"

        elif (tag == 1):

            return "em largura"

        elif (tag == 2):

            return "Greedy"

        elif (tag == 3):

            return "A*"

        return None

    def print_winner(self, player):

        print("---------------------------------------------------------------")
        print("\nWinner: " + player + "\n")
        print("---------------------------------------------------------------")

    def print_draw(self):

        print("---------------------------------------------------------------")
        print("\nDraw\n")
        print("---------------------------------------------------------------")

    def desenha_two_players(self, tag_1, tag_2):

        paths = self.generate_two_player_path(tag_1, tag_2)

        path_player_one = paths[0][0]
        path_player_two = paths[1][0]

        custo_player_one = paths[0][1]
        custo_player_two = paths[1][1]

        self.desenha_player_one(path_player_one, custo_player_one, self.tag_to_travessia(tag_1))
        self.desenha_player_two(path_player_two, custo_player_two, self.tag_to_travessia(tag_2))

        if (custo_player_one == custo_player_two):

            self.print_draw()

        else:

            if (custo_player_one < custo_player_two):

                self.print_winner("Player One")

            else:

                self.print_winner("Player Two")

        plt.show()

