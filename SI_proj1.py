from searchPlus import *

line1 = "= = = = = = =\n"
line2 = "= x . . . . =\n"
line3 = "= . . . = . =\n"
line4 = "= . . . = . =\n"
line5 = "= = = . = . =\n"
line6 = "= ^ . . . . =\n"
line7 = "= = = = = = =\n"
grelha = line1 + line2 + line3 + line4 + line5 + line6 + line7

class Labirinto(Problem):

    def __init__(self, LabInicial=grelha, vmax=3):
        #dividir a grelha em strings que sao as linhas
        LabInicial = LabInicial.split('\n')
        
        #eliminar a última linha vazia
        LabInicial.pop()

        #fazer com que lab inicial seja uma lista de listas e cada elemento das sublistas seja um caracter
        #eg: [['=','=','=','=','=','=','='], ['=','x','.','.','.','='],...]
        #remover os espacos
        for i in range(len(LabInicial)):
            LabInicial[i] = list(LabInicial[i].replace(' ','')) #replace remove os espacos

        self.LabInicial = LabInicial
        
        #set up dimensoes do labirinto
        self.height = len(self.LabInicial)
        self.width = len(self.LabInicial[0]) 
        
        #encontrar initial position e orientacao do veiculo
        for i in range(len(self.LabInicial)):
            for j in range(len(self.LabInicial[i])):
                if self.LabInicial[i][j] == '^' or self.LabInicial[i][j] == 'v' or self.LabInicial[i][j] == '<' or self.LabInicial[i][j] == '>':
                    self.coordenadas = (i,j)
                    #encontrar orientacao (N, S, E, O)
                    if self.LabInicial[i][j] == '^':
                        self.orientacao = 'N'
                    elif self.LabInicial[i][j] == 'v':
                        self.orientacao = 'S'
                    elif self.LabInicial[i][j] == '<':
                        self.orientacao = 'O'
                    else:
                        self.orientacao = 'E'
                    break
    
        #encontrar goal position
        for i in range(len(self.LabInicial)):
            for j in range(len(self.LabInicial[i])):
                if self.LabInicial[i][j] == 'x':
                    self.goal = (i,j)
                    break

        #fazer set de velocidade maxima
        self.vmax = vmax

        #fazer set da velocidade inicial. assumimos que o veiculo comeca parado
        self.vcurrent = 0 

        #estado inicial
        self.initial = (self.coordenadas, self.orientacao, self.vcurrent)

    def actions(self, state):
        """Return the actions that can be executed in the given state."""
        coordenadas, direcao, vcurrent = state
        vmax = self.vmax
        possible_actions = []

    # Check if the car can accelerate ('A')
        if vcurrent < vmax:
        # Check next position based on current direction and make sure it's not a wall
            next_pos = self.calculate_next_position(coordenadas, direcao, vcurrent + 1)
            if self.is_within_bounds(next_pos) and self.LabInicial[next_pos[0]][next_pos[1]] != '=':
                possible_actions.append('A')

    # Check if the car can brake ('T') without going below zero speed
        if vcurrent > 0:
        # Check next position based on current direction at one less speed (decelerating)
            next_pos = self.calculate_next_position(coordenadas, direcao, vcurrent - 1)
            if self.is_within_bounds(next_pos) and self.LabInicial[next_pos[0]][next_pos[1]] != '=':
                possible_actions.append('T')

    # Check if the car can turn left ('E') or right ('D'), only if the speed is 0
        if vcurrent == 0:
            possible_actions.extend(['E', 'D'])

    # Return actions sorted alphabetically
        return sorted(possible_actions)


      

    def result(self, state, action):
        (coordenadas, orientacao, vcurrent) = state
        (i,j) = coordenadas
        if action == 'E':
            if orientacao == 'N':
                orientacao = 'O'
            elif orientacao == 'S':
                orientacao = 'E'
            elif orientacao == 'E':
                orientacao = 'N'
            else:
                orientacao = 'S'
        if action == 'D':
            if orientacao == 'N':
                orientacao = 'E'
            elif orientacao == 'S':
                orientacao = 'O'
            elif orientacao == 'E':
                orientacao = 'S'
            else:
                orientacao = 'N'
        #check this part
        if action == 'A':
            if orientacao == 'N':
                coordenadas = (i - vcurrent - 1, j)
            elif orientacao == 'S':
                coordenadas = (i + vcurrent + 1, j)
            elif orientacao == 'E':
                coordenadas = (i, j + vcurrent + 1)
            else:
                coordenadas = (i, j - vcurrent - 1)
        if action == 'T':
            vcurrent -= 1
            if vcurrent > 0:
                if orientacao == 'N':
                    coordenadas = (i - vcurrent - 1, j)
                elif orientacao == 'S':
                    coordenadas = (i + vcurrent + 1, j)
                elif orientacao == 'E':
                    coordenadas = (i, j + vcurrent + 1)
                else:
                    coordenadas = (i, j - vcurrent - 1)
        if action == 'A':
            vcurrent += 1

        return (coordenadas, orientacao, vcurrent)

    def goal_test(self, state):
        if state[0] == self.goal:
            return True
        return False

    def display(self, state):
        """Primeiramente limpa o estado do labirinto para que não exista nenhum veiculo e introduz a posicao do veiculo e a orientacao do mesmo no labirinto"""
        temp = self.LabInicial.copy()
        temp = [list(row) for row in temp]
        for x in range(len(temp)):
            for y in range(len(temp[x])):
                if temp[x][y] == '^' or temp[x][y] == 'v' or temp[x][y] == '<' or temp[x][y] == '>':
                    temp[x][y] = '.' #limpar o veiculo
        (coordenadas, orientacao, vcurrent) = state
        for x in range(len(temp)):
            for y in range(len(temp[x])):
                if (x,y) == coordenadas:
                    if orientacao == 'N':
                        temp[x][y] = '^'
                    elif orientacao == 'S':
                        temp[x][y] = 'v'
                    elif orientacao == 'E':
                        temp[x][y] = '>'
                    else:
                        temp[x][y] = '<'
        return '\n'.join([' '.join(row) for row in temp])
                    

    def executa(self, state, actions_list, verbose=False):
        """Executa uma sequência de acções a partir do estado devolvendo o triplo formado pelo estado, 
            pelo custo acumulado e pelo booleano que indica se o objectivo foi ou não atingido. Se o objectivo 
            for atingido antes da sequência ser atingida, devolve-se o estado e o custo corrente.
            Há o modo verboso e o não verboso, por defeito."""
        cost = 0
        for a in actions_list:
            seg = self.result(state,a)
            cost = self.path_cost(cost,state,a,seg)
            state = seg
            obj = self.goal_test(state)
            if verbose:
                print('Ação:', a)
                print(self.display(state),end='')
                print('Custo Total:',cost)
                print('Atingido o objectivo?', obj)
                print()
            if obj:
                break
        return (state, cost, obj)
    
    def calculate_next_position(self, current_position, direction, speed):
    # Map direction to coordinate changes (assuming N, S, E, W directions)
        direction_deltas = {
            'N': (-speed, 0),  # Move up
            'S': (speed, 0),   # Move down
            'E': (0, speed),   # Move right
            'O': (0, -speed)   # Move left
                            }
        delta = direction_deltas[direction]
        return (current_position[0] + delta[0], current_position[1] + delta[1])
    
    
    def is_within_bounds(self, position):
    # Check if position is within the maze boundaries
        return 0 <= position[0] < len(self.LabInicial) and 0 <= position[1] < len(self.LabInicial[0])







line1 = "= = = = = = = = = =\n"
line2 = "= x . . . . . . . =\n"
line3 = "= . . . = . . . . =\n"
line4 = "= . . . = . = . . =\n"
line5 = "= = = . = . = . . =\n"
line6 = "= > . . . . . . = =\n"
line7 = "= = = = = = = = = =\n"
grelha2 = line1 + line2 + line3 + line4 + line5 + line6 + line7
p = Labirinto(grelha2)
resultado = breadth_first_graph_search(p)
if resultado:
    print("Solução Larg-prim (grafo) com custo", str(resultado.path_cost)+":")
    print(resultado.solution())
else:
    print("Sem solução!")