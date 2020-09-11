print("2018180029 이관민 AI Work1\nN-Queen.")

import queue

# chess board는 (i, j)로 구성 ( n > i >= 0, n >= j > 0), j = 0은 퀸인 열은 미배치
# board list는 board[i] = j 로 구성
class State:
    def __init__(self, board, goal, moves=0):
        self.board = board
        self.moves = moves
        self.goal = goal

    # moves 번째 열에 퀸을 배치한다. 
    def expand(self, moves):
        result = []
        for j in range(self.goal):
            if self.check_point(self.board, moves, j+1):
                new_board = self.board.copy()
                new_board[moves] = j + 1
                result.append(State(new_board, self.goal, moves + 1))
        return result

    def check_point(self, board, i, j):
        if self.board[i] > 0:
            return False
        index_column = i
        for _i in range(self.moves):
            _j = self.board[_i] 
            if _j == j: # 같은 행 제외
                return False
            #대각선 위 방향 제외
            uj = _j + (i - _i)
            if uj == j:
                return False
            #대각선 아래 방향 제외
            dj = _j - (i - _i)
            if dj == j:
                return False
        return True

    #해당 열에 퀸을 둘 수 있는 칸 수를 센다. 
    def check_column_hole(self, index_column):
        if self.board[index_column] > 0:
            return 0
        column = [ 0 for i in range(self.goal) ]
        for i in range(self.moves):
            j = self.board[i] - 1
            column[j] += 1 # 같은 행 제외
            #대각선 위 방향 제외
            if j + (index_column - i) < self.goal:
                column[j + (index_column - i)] += 1
            #대각선 아래 방향 제외
            if j - (index_column - i) >= 0:
                column[j - (index_column - i)] += 1
        result = 0
        for t in column:
            if t == 0:
                result += 1
        return result            

    # 상태와 상태를 비교하기 위하여 less than 연산자를 정의한다.
    # 다음 퀸을 배치해야 되는 열의 퀸을 배치 가능한 칸 수가 더 적은 쪽이 
    # 퀸을 배치할수록 배치 가능한 칸 수가 줄어듦으로 N-Queen을 성립하는 퀸 배치가 가능할 확률이 높다고 보고 비교한다.
    def __lt__(self, other):
        if self.g() != other.g():
            return self.g() > other.g()
        else:
            return self.check_column_hole(self.moves) < other.check_column_hole(self.moves)
    # f(n)을 계산하여 반환한다.
    def f(self):
        return self.h() + self.g()
    # 휴리스틱 함수 값인 h(n)을 계산하여 반환한다.
    # 아직 퀸을 배치하지 않은 열의 수를 센다. 
    def h(self):
        return self.goal - self.moves
    # 시작 노드로부터의 경로를 반환한다.
    def g(self):
        return self.moves
    # 퀸 배치 프린트
    def __str__(self):
        result = ""
        t = 0
        for p in self.board:
            if p > 0:  
                result += ("Q"+ chr(ord('a')+t) + ascii(p) + "\t")
            else:
                result += ("None\t")
            t += 1
        return result

    def is_goal(self):
        return self.moves == self.goal           

n = eval(input("N = "))

# board[i] = j (i, j)로 구성 (j > 1), 0은 퀸 미배치
start_board = [ 0 for x in range(n)]

open_queue = queue.PriorityQueue()
open_queue.put(State(start_board, n))
closed_queue = [ ]
moves = 0
while not open_queue.empty():
    current = open_queue.get()
    print(current)
    if current.is_goal():
        print("탐색 성공")
        break
    for state in current.expand(current.moves):
        if state not in closed_queue:
            open_queue.put(state)
    closed_queue.append(current)
else:
    print ('탐색 실패')
