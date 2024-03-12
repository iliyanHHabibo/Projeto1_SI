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
        """Construtor do problema do labirinto. O estado inicial é uma string com o labirinto e a velocidade máxima"""
        LabInicial = LabInicial.split('\n')
        LabInicial.pop() 
        for i in range(len(LabInicial)):
            LabInicial[i] = list(LabInicial[i].replace(' ', ''))  
        self.LabInicial = LabInicial
        self.height = len(self.LabInicial)
        self.width = len(self.LabInicial[0])
        self.vmax = vmax


        #estado inicial
        self.set_initial_and_goal_states()
        
    def set_initial_and_goal_states(self):
        """Define o estado inicial e o estado objectivo. O estado inicial é uma tripla com a posição, a orientação e a velocidade do veículo. O estado objectivo é a posição onde se encontra o objectivo."""
        symbol_to_orientation = {'^': 'N', '>': 'E', 'v': 'S', '<': 'O'}  
        for i, row in enumerate(self.LabInicial):
            for j, val in enumerate(row):
                if val in '^v<>':  #Verifica se o valor é um dos símbolos dos veículos
                    self.initial = ((i, j), symbol_to_orientation[val], 0)  #Estado inicial com a posição, orientação e velocidade
                    self.LabInicial[i][j] = '.'  # Substitui o símbolo do veículo por um ponto
                    
                elif val == 'x':  # Verifica se o valor é o símbolo do objectivo
                    self.goal = (i, j)

    def actions(self, state):
        coordenadas, orientacao, vcurrent = state
        possible_actions = []

        #Verifica se é possível acelerar ou travar
        if vcurrent == 0:
            possible_actions.extend(['E', 'D'])


        if vcurrent < self.vmax:
            next_pos = self.calculate_next_position(coordenadas, orientacao, vcurrent + 1)
            if self.is_within_bounds(next_pos) and self.LabInicial[next_pos[0]][next_pos[1]] != '=':
                possible_actions.append('A')
        if vcurrent > 0:
            next_pos = self.calculate_next_position(coordenadas, orientacao, vcurrent - 1)
            if self.is_within_bounds(next_pos) and self.LabInicial[next_pos[0]][next_pos[1]] != '=':
                possible_actions.append('T')

        return sorted(possible_actions)

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
                    

    def result(self, state, action):
        """Retorna o estado seguinte após a execução da ação"""
        coordenadas, orientacao, vcurrent = state 

        #Criar novas variáveis para o novo estado
        new_coordenadas, new_orientacao, new_vcurrent = coordenadas, orientacao, vcurrent

        if action == 'A':  
            new_vcurrent = min(vcurrent + 1, self.vmax)
        elif action == 'T':  
            new_vcurrent = max(vcurrent - 1, 0)
        elif action == 'E':  
            new_orientacao = {'N': 'O', 'O': 'S', 'S': 'E', 'E': 'N'}[orientacao]
        elif action == 'D': 
            new_orientacao = {'N': 'E', 'E': 'S', 'S': 'O', 'O': 'N'}[orientacao]

     
        if new_vcurrent > 0:
            new_coordenadas = self.calculate_next_position(coordenadas, new_orientacao, new_vcurrent)

        
        return (new_coordenadas, new_orientacao, new_vcurrent)
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

    def goal_test(self, state):
         position, _, speed = state
         return position == self.goal and speed == 0

    def calculate_next_position(self, current_position, direction, speed):
        direction_deltas = {'N': (-speed, 0), 'S': (speed, 0), 'E': (0, speed), 'O': (0, -speed)}
        delta = direction_deltas[direction]
        return (current_position[0] + delta[0], current_position[1] + delta[1])
    
    def is_within_bounds(self, position):
        return 0 <= position[0] < self.height and 0 <= position[1] < self.width



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

actions_list = ['A', 'T', 'A', 'T', 'E', 'A', 'T', 'A', 'T', 'A', 'T', 'A', 'T', 'E', 'A', 'T', 'A', 'T']

# Call the executa method with verbose=True
initial_state = p.initial
final_state, total_cost, goal_reached = p.executa(initial_state, actions_list, verbose=True)

# Display the final state and other information
print("Final State:")
print(p.display(final_state))
print("Total Cost:", total_cost)
print("Goal Reached:", goal_reached)


    #fazer testes 
    #se nao ha açoes possiveis: se vamos bater mesmo que travemos, devolvemos lista de actions vazia
    #testar executa com o verboso a true e conseguimos validar se cada uma das açoes esta correta ou nao
    #pensar em situações em que o carro nao pode fazer nada e ver como podemos corrigir
    #vel 0 vel 1 vel 2. testar o codigo. qual e a lista de açoes quando isto acontece
