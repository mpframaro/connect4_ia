import numpy as np
import copy
import math
import time
def createboard():
    board = np.zeros((6,7))
    return board

def printboard(board):
    b =""
    for i in range(6):
        for d in range (7):
            if board[i][d] == 0:
                b = b + "_"
            elif board[i][d] == 1:
                b = b + 'X'
            else:
                b = b + 'O'
        b = b +'\n'
    b = b +'1234567\n'
    print(b)

def jogada(jog,col,board):#mudar depois,vai se inserir aqui o bot
    tabu = copy.deepcopy(board)
    n = possivel(col,tabu)
    tabu[n][col] = jog
    return tabu

def possivel(col,board):
    for i in range(6):
        if board[5-i][col] == 0:
            return 5-i
    return -1

def possimoves(board):
    possimoves = list()
    for i in range(7):
        n = possivel(i,board)
        if n != -1:
            possimoves.append(i)
    return possimoves

def empate(board):
        for i in range(7):
            if board[0][i] == 0:
                return False
        return True

def avaliacao(board,jog):
    if vencedor(board):
        return -512*jog
    elif empate(board):
        return 0

    # Evaluate all straight segments on the grid
    value = 0
    for i in range(6):
        for j in range(7):
            if j <= 3:
                # Evaluate horizontal segments
                segment = board[i][j:j + 4]
                value += evalsegment(segment)

                if i <= 2:
                    # Evaluate diagonal segments starting from upper left
                    segment = [board[i + k][j + k] for k in range(4)]
                    value += evalsegment(segment)

                if i >= 3:
                    # Evaluate diagonal segments starting from lower left
                    segment = [board[i - k][j + k] for k in range(4)]
                    value += evalsegment(segment)

            if i <= 2:
                # Evaluate vertical segments
                segment = [board[i + k][j] for k in range(4)]
                value += evalsegment(segment)

    return value

def evalsegment(segment):
    countx =0
    counto =0
    pontuacao = [0,1,10,50]
    for i in range(len(segment)):
        if segment[i] ==1:
            countx+= 1
        elif segment[i] == -1:
            counto+= 1
    if countx ==0 or counto ==0:
        if countx ==0:
            return pontuacao[counto]
        else:
            return -pontuacao[countx]
    else:
        return 0

def vencedor(board):
    for col in range(4):
        for li in range(6):
              if board[li][col] ==  board[li][col+1] == board[li][col+2] ==  board[li][col+3] and board[li][col] !=0:
                   return True
    for col in range(7):
        for li in range(3):
             if board[li][col] ==  board[li+1][col] ==  board[li+2][col] ==  board[li+3][col] and board[li][col] !=0:
                  return True
				
    for col in range(4):
        for li in range(3):
             if board[li][col] ==  board[li+1][col+1] ==  board[li+2][col+2] ==  board[li+3][col+3] and board[li][col] !=0:
                  return True
    for col in range(4):
        for li in range(3, 6):
            if board[li][col] ==  board[li-1][col+1] ==  board[li-2][col+2] ==  board[li-3][col+3] and board[li][col] !=0:
                return True

def minimax(board,jog,depth):
    tabu = copy.deepcopy(board)
    acao = maxe(tabu,jog,depth)
    print(acao[2])
    return acao[0]

def mini(board,jog,depth):
    if depth ==0 or vencedor(board) or empate(board):
        return [-1,avaliacao(board,-jog),0]
    v = 1000000
    jogar = -1
    possi = possimoves(board)
    nodes =0
    for i in possi:
        nodes = nodes+1
        pontos =maxe(jogada(jog,i,board),-jog,depth-1,)
        nodes = nodes+pontos[2]
        if pontos[1] <v:
            v = pontos[1]
            jogar = i
    return[jogar,v,nodes]

def maxe(board,jog,depth):
    if depth ==0 or vencedor(board) or empate(board):
        return [-1,avaliacao(board,-jog),1]
    v = -1000000
    jogar = -1
    possi = possimoves(board)
    nodes =0
    for i in possi:
        nodes +=1
        pontos =mini(jogada(jog,i,board),-jog,depth-1)
        nodes = nodes+pontos[2]
        if pontos[1] >v:
            v = pontos[1]
            jogar = i
    return [jogar,v,nodes]

def alphabeta(board,jog,depth,alpha,beta):
    tabu = copy.deepcopy(board)
    acao = alphamax(tabu,jog,depth,alpha,beta)
    print(acao[2])
    return acao[0]

def alphamax(board,jog,depth,alpha,beta):
    if depth ==0 or vencedor(board) or empate(board):
        return [-1,avaliacao(board,-jog),0]
    v = -1000000
    jogar = -1
    possi = possimoves(board)
    nodes=0
    for i in possi:
        nodes+=1
        pontos =alphamin(jogada(jog,i,board),-jog,depth-1,alpha,beta)
        nodes =nodes+pontos[2]
        if pontos[1] >v:
            v = pontos[1]
            jogar = i
        alpha = max(alpha,pontos[1])
        if alpha >= beta:
            break
    return [jogar,v,nodes]

def alphamin(board,jog,depth,alpha,beta):
    if depth ==0 or vencedor(board) or empate(board):
        return [-1,avaliacao(board,-jog),0]
    v = 1000000
    jogar = -1
    possi = possimoves(board)
    nodes=0
    for i in possi:
        nodes+=1
        pontos =alphamax(jogada(jog,i,board),-jog,depth-1,alpha,beta)
        nodes = nodes+pontos[2]
        if pontos[1] <v:
            v = pontos[1]
            jogar = i
        beta = min(beta,pontos[1])
        if alpha >= beta:
            break
    return[jogar,v,nodes]

class MonteCarloTreeSearchNode():
    def __init__(self, state,player, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self.q =0
        self._untried_actions = self.untried_actions()
        self.player = player
        return
    
    def untried_actions(self):
        self._untried_actions = possimoves(self.state)
        return self._untried_actions
    
    def n(self):
        return self._number_of_visits
    
    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.move(action,self.player,self.state)
        child_node = MonteCarloTreeSearchNode(
            next_state,-self.player, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node 
    
    def is_terminal_node(self):
        return self.is_game_over(self.state)
    
    def rollout(self):
        current_rollout_state = self.state
        pla = self.player
        nodes =0
        while not self.is_game_over(current_rollout_state):
            possible_moves = possimoves(current_rollout_state)
            nodes +=1
            action = self.rollout_policy(possible_moves)
            current_rollout_state = self.move(action,pla,current_rollout_state)
            pla*=-1
        return self.game_result(current_rollout_state),nodes
   
    def backpropagate(self, result):
        reward = 0 if result == self.player else 1
        while self !=None:
            self._number_of_visits+=1
            self.q+= reward
            self = self.parent
            if result==0:
                reward=0
            else:
                reward=1-reward
    
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0
    
    def best_child(self, c_param=math.sqrt(2)):
        max =0
        move=0
        for i in self.children:
            val=(i.q / i.n()) + c_param *((math.sqrt(math.log(i.parent.n()) / i.n())))
            if val>max:
                max=val
                move =i
        return move
    
    def rollout_policy(self, possible_moves):
        if len(possible_moves)==0:return None
        return possible_moves[np.random.randint(0,len(possible_moves))]
    
    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
    
    def best_action(self,time_limit):
        start_time = time.process_time()
        nodes=0
        while time.process_time() - start_time < time_limit:
            v = self._tree_policy()
            reward,n= v.rollout()
            nodes=n+nodes
            v.backpropagate(reward)
        print(nodes)
        return self.best_child(c_param=math.sqrt(2))

    def is_game_over(self,board):
        return vencedor(board) or empate(board)

    def game_result(self,board):
        jog =1
        for col in range(4):
            for li in range(6):
                if board[li][col] ==  board[li][col+1] == board[li][col+2] ==  board[li][col+3] and board[li][col] !=0:
                    if board[li][col] == jog:return 1
                    else:return -1
        for col in range(7):
            for li in range(3):
                if board[li][col] ==  board[li+1][col] ==  board[li+2][col] ==  board[li+3][col] and board[li][col] !=0:
                    if board[li][col] == jog:return 1
                    else:return -1
                    
        for col in range(4):
            for li in range(3):
                if board[li][col] ==  board[li+1][col+1] ==  board[li+2][col+2] ==  board[li+3][col+3] and board[li][col] !=0:
                    if board[li][col] == jog:return jog
                    else:return -jog
        for col in range(4):
            for li in range(3, 6):
                if board[li][col] ==  board[li-1][col+1] ==  board[li-2][col+2] ==  board[li-3][col+3] and board[li][col] !=0:
                    if board[li][col] == jog:return jog
                    else:return -jog
        return 0

    def move(self,action,jog,board):
        sta= jogada(jog,action,board)
        return sta

def bot(jog,board,flag):
    alpha = -math.inf
    beta  =  math.inf
    if flag==1:#minimax normal
        jo= minimax(board,jog,5)
    elif flag==2:#minimax com alpha-beta cuts
        jo = alphabeta(board,jog,5,alpha,beta)
    else:#mcts
        root = MonteCarloTreeSearchNode(boar,jog)
        d =root.best_action(2)
        jo= d.parent_action
    return jo    
    
boar = createboard()
jogador =1
print("escolhe o bot que vai jogar: 1-minimax, 2-minimax com alpha-beta,3-mcts")
b = int(input())
printboard(boar)
while True:
    if jogador ==1:
        colu = int(input()) -1
    else:
        start_time = time.process_time()
        colu = bot(jogador,boar,b)
        print(time.process_time() - start_time)
    boar =jogada(jogador,colu,boar)
    printboard(boar)
    if vencedor(boar):
        print(str(jogador) +' venceu ')
        break
    jogador*=-1

