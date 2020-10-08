import math
import time
import numpy as np
from guppy import hpy
import samplePegs as sample
import heapq

astarDict = {} # keep track of expanded state

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.count = 0
    def isEmpty(self):
        return len(self.heap) == 0
    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1
    def pop(self):
        try:
            (_, _, item) = heapq.heappop(self.heap)
            return item
        except:
            return None

def indexBoard(graph): # graph is array, mark symbol with index
    board = []
    count = 0
    for index in range(0,7): # '--000--'
        line = graph[index]
        row = []
        for i in range(0, len(line)):
            if line[i] == '-':
                row.append([line[i],' '])
            else:
                row.append([line[i],str(count)])
                count+=1
        board.append(row)
    return board

def getSuccessors(board):
    output = []
    for i in range(0, len(board)):
        row = board[i]
        for j in range(0, len(row)): # ['X','4']
            elem = row[j]
            if elem[0]=='-' or elem[0]=='0':
                continue
            r,l,u,d = True, True, True, True
            if j-2<0:# cannot move left
                l = False
            if j+2>=7:# cannot move right
                r = False
            if i-2<0: # cannot move up
                u = False
            if i+2>=7: # cannot move down
                d = False
            if l and row[j-2][0]=='0' and row[j-1][0]=='X':
                boardcp = copyBoard(board)
                step = (board[i][j][1], board[i][j-2][1])
                boardcp[i][j-2][0] = 'X'
                boardcp[i][j-1][0] = '0'
                boardcp[i][j][0] = '0'
               # print(step)
                output.append((step, boardcp))
            if r and row[j+2][0]=='0' and row[j+1][0]=='X':
                boardcp = copyBoard(board)
                step = (board[i][j][1], board[i][j+2][1])
                boardcp[i][j+2][0] = 'X'
                boardcp[i][j+1][0] = '0'
                boardcp[i][j][0] = '0'
                #print(step)
                output.append((step, boardcp))
            if u and board[i-2][j][0]=='0' and board[i-1][j][0]=='X':
                boardcp = copyBoard(board)
                step = (board[i][j][1], board[i-2][j][1])
                boardcp[i-2][j][0] = 'X'
                boardcp[i-1][j][0] = '0'
                boardcp[i][j][0] = '0'
                #print(step)
                output.append((step, boardcp))
            if d and board[i+2][j][0]=='0' and board[i+1][j][0]=='X':
                boardcp = copyBoard(board)
                step = (board[i][j][1], board[i+2][j][1])
                boardcp[i+2][j][0] = 'X'
                boardcp[i+1][j][0] = '0'
                boardcp[i][j][0] = '0'
                #print(step)
                output.append((step, boardcp))
    return output

def copyBoard(board):
    output = []
    for row in board:
        i = []
        for elem in row:
            j= []
            for peg in elem:
                j.append(peg)
            i.append(j)
        output.append(i)
    return output

def isGoal(board):
    if getNumFilled(board)!=1:
        return False
    for row in board:
        for elem in row: # ['X', '16']
            if(elem[0]=='X' and elem[1]=='16'):
                return True
    return False

def getNumFilled(board):
    count = 0
    for row in board:
        for elem in row:
            if elem[0]=='X':
                count+=1
    return count

def aStarSearch(board, heuristic):
    pqueue = PriorityQueue()
    expandCount = 0
    if(isGoal(board)):
        aStarSearch[str(board)] = [[],0,True]
        return [], 0, True
    pqueue.push(([],board), 0)
    i = 0
    while i<2**(getNumFilled(board)-1):
        i+=1
        oldPath = pqueue.pop() # oldpath=([], board)
        if oldPath==None:
            break
        if prune and str(oldPath[1]) in astarDict:
            toLoop = astarDict[str(oldPath)]
        else:
            toLoop = getSuccessors(oldPath[1])
            astarDict[str(oldPath)] = toLoop
        for successor in toLoop:
            if prune and str(oldPath[1]) not in astarDict:
                expandCount+=1
            newPath = list(oldPath[0])
            newPath.append(successor[0]) # newpath = [(9,7)]
            pqueue.push((newPath, successor[1]), (getNumFilled(board)-len(newPath))+heuristic(successor[1], successor[0]))
            if isGoal(successor[1]):
                return newPath, expandCount, True
    return [], expandCount, False

def manhattanHeuristic(board, move): # ('9','7'), closer to center smaller value
    x,y = getCoordinates(board, move[1]) # '7' = 2, 1
    centerx, centery = 3, 3
    return abs(centery - y) + abs(centerx - x)

def lessNodeHeuristic(board, move):
    return getNumFilled(board)

def euclideanHeuristic(board, move):
    x,y = getCoordinates(board, move[1])
    centerx, centery = 3,3
    return ((centery-y)**2 + (centerx-x)**2)**0.5

def getCoordinates(board, marker): # '7'
    x = 0
    for row in board:
        y = 0
        for elem in row:
            if elem[1]==marker:
                return x,y
            y+=1
        x+=1
    return -1,-1

userInput = input("Enter 0-Manhattan Heuristic or 1-Less Node Heuristic or 2-Euclidean Heuristic: ")
if(userInput=='0'):
    heuristic = manhattanHeuristic
elif(userInput=='1'):
    heuristic = lessNodeHeuristic
elif(userInput=='2'):
    heuristic = euclideanHeuristic
pruneInput = input("Run with prune method? 1-Yes 0-No : ")
prune = False
if(pruneInput=='1'):
    prune = True
elif(pruneInput=='0'):
    prune = False
i = 0
for graph in sample.inputs:
    i+=1
    print()
    print("Test case#", i)
    board = indexBoard(graph)
    t0 = time.time()
    path, expanded, sol = aStarSearch(board, heuristic)
    t1 = time.time()
    if heuristic==manhattanHeuristic:
        print("Using Manhattan Heuristic")
    elif heuristic==lessNodeHeuristic:
        print("Using Less Node Heuristic")
    elif heuristic==euclideanHeuristic:
        print("Using Euclidean Heuristic")
    if sol:
        print("There is solution")
    else:
        print("There is no solution")
    print('Path', end =': ')
    print(path)
    print('Nodes expanded: ',expanded)
    print('Memory usage:', hpy().heap().size, 'bytes')
    print('Running time: {0:.2f} seconds'.format(t1 - t0))

