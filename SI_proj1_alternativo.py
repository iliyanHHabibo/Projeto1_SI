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
        actions = []
        coordenadas, direcao, vcurrent = state
        
        # Check if we can accelerate, decelerate, or maintain speed without hitting a wall
        # Ensure that we stay within the bounds of the maze
        if vcurrent > 0:  # Moving forward
            if coordenadas[0] + vcurrent + 1 < len(self.LabInicial) and \
               self.LabInicial[coordenadas[0] + vcurrent + 1][coordenadas[1]] != "=":
                actions.append('A')  # Accelerate
            if 0 <= coordenadas[0] - vcurrent - 1 and \
               self.LabInicial[coordenadas[0] - vcurrent - 1][coordenadas[1]] != "=":
                actions.append('D')  # Decelerate
        elif vcurrent == 0:  # If not moving, can start moving or stay
            actions.extend(['A', 'D'])  # Can either accelerate or decelerate (which would still be staying still)
    
        # Check if turning is possible without going out of bounds or hitting a wall
        # This requires checking different conditions based on the current direction
        # For simplicity, I'm assuming the car can always turn unless specified in your problem's logic
    
        actions.extend(['L', 'R'])  # Left and Right turn actions
    
        # Note: You may need to adapt turning conditions based on your maze's logic and vehicle dynamics.
        
        return actions

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
    