from searchPlus import *

line1 = "= = = = = = =\n"
line2 = "= x . . . v =\n"
line3 = "= . . . = . =\n"
line4 = "= . . . = . =\n"
line5 = "= = = . = . =\n"
line6 = "= . . . . . =\n"
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
                    self.initial = (i,j)
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

    def actions(self, state): #estado é a posicao do veiculo (M,N) 
        accoes = []

        #se o veiculo estiver parado, pode virar para a esquerda ou para a direita
        #check se o veiculo pode virar para a esquerda ou para a direita
        if self.vcurrent == 0:
            accoes.append('E')
            accoes.append('D')

        #check se o veiculo pode acelerar
        if self.orientacao == 'N':
            if state[0] - self.vcurrent >= 0 : #se a velocidade for menor que a posicao do veiculo nao vamos out of bounds
                if self.vcurrent < self.vmax: #se a velocidade for menor que a velocidade maxima
                    if self.LabInicial[state[0] - self.vcurrent - 1] [state[1]] != "=": #se a posicao seguinte nao for um obstaculo. subtraimos mais 1 a velocidade para ver a posicao seguinte e se nao calha num obstaculo
                            accoes.append('A')

        if self.orientacao == 'S': 
            if state[0] + self.vcurrent < self.height: 
                if self.vcurrent < self.vmax:
                    if self.LabInicial[state[0] + self.vcurrent + 1] [state[1]] != "=": #adicionamos mais 1 a velocidade para ver a posicao seguinte e se nao calha num obstaculo
                            accoes.append('A')

        if self.orientacao == 'E':
            if state[1] + self.vcurrent < self.width:
                if self.vcurrent < self.vmax:
                    if self.LabInicial[state[0]] [state[1] + self.vcurrent + 1] != "=":
                            accoes.append('A')

        if self.orientacao == 'O':
            if state[1] - self.vcurrent > 0:
                if self.vcurrent < self.vmax:
                    if self.LabInicial[state[0]] [state[1] - self.vcurrent - 1] != "=":  
                            accoes.append('A')
                        
        #check se o veiculo pode travar        
        if self.vcurrent > 0:
            accoes.append('T')
        
        #retornamos a lista de accoes ordenada alfabeticamente
        return sorted(accoes)

    def result(self, state, action):
        pass

    def goal_test(self, state):
        pass

    def display(self, state):
        pass

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
    




l = Labirinto()
print(l.LabInicial)
print (l.initial)
print (l.orientacao)
print (l.goal)
print (l.height)
print (l.width)
print(l.vcurrent)
print(l.actions(l.initial))


#condicoes de actions incorretas