import samplePegs as sample
import time
import numpy as np
from guppy import hpy

idsdict = {} # {str graph: [successor graphs]}, avoid revisit expanded node

def idsearch(board):
    limit = 0
    totalExpanded = 0
    while limit<getNumFilled(board): # change
        limit+=1
        path, expanded, isSol= dlsearch(board, limit, 0)
        totalExpanded+=expanded
        if(isSol): # first solution
            finalPath = []
            reverse = reversed(path)
            for step in reverse:
                finalPath.append(step)
            return finalPath, totalExpanded, True
    return [], totalExpanded, False

def dlsearch(board, limit, depth):
    return recursiveDLS(board, limit, depth)

def recursiveDLS(board,limit, depth):
    if isGoal(board):
        if str(board) not in idsdict:
            idsdict[str(board)] = [[], 0, True]
        return [], 0, True
    if depth==limit: 
        return [], 0, False
    expandCount = 0
    for successor in getSuccessors(board):
        newboard = successor[1]
        if prune and str(newboard) in idsdict:
            path = idsdict[str(newboard)][0]
            newExpanded = idsdict[str(newboard)][1]
            sol = idsdict[str(newboard)][2]
            expandCount += newExpanded
        else:
            path, newExpanded, sol= recursiveDLS(newboard, limit, depth+1)
            expandCount += 1
            expandCount += newExpanded
        if(sol):
            path.append(successor[0]) # successor[0] = ('9','7')
            if prune and str(newboard) not in idsdict:
                idsdict[str(newboard)] = [path, expandCount, True]
                expandCount -=1
            return path, expandCount, True
    #if str(board) not in idsdict:
       # idsdict[str(board)] = [[], expandCount, False]
    return [], expandCount, False

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

def getNumFilled(board): # [[[],[]],[[],[]]]
    count=0
    for row in board:
        for elem in row:
            if elem[0]=='X':
                
                count+=1
    return count

def isGoal(board):
    if getNumFilled(board)!=1:
        return False
    for row in board:
        for elem in row: # ['X', '16']
            if(elem[0]=='X' and elem[1]=='16'):
                return True
    return False

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

i = 1
userInput = input("Run with prune method? 1-Yes 0-No : ")
prune = False
if userInput=='1':
    prune = True
elif userInput=='0':
    prune = False
for graph in sample.inputs:
    print('Test case# ', i)
    i+=1
    board = indexBoard(graph)
    t0 = time.time()
    path, expanded, sol =idsearch(board)
    t1 = time.time()
    # print("length:",len(idsdict))
    # for ele in idsdict:
    #     print(idsdict[ele])
    if sol:
        print("There is solution")
    else:
        print("There is no solution")
    print('Path', end =': ')
    print(path)
    print('Nodes expanded: ',expanded)
    print('Memory usage:', hpy().heap().size, 'bytes')
    print('Running time: {0:.2f} seconds'.format(t1 - t0))
    print()