#!/usr/bin/python3
import os
import sys
import time
from random import randrange
from random import shuffle
import argparse
from board import Board

parser = argparse.ArgumentParser(description = 'play a fun little game')
parser.add_argument("mode", type = str, choices=['s','d','z'], help='s = singleplayer, d = doubleplayer')
mode = parser.parse_args().mode

os.system('clear')
if mode == 's':
    print('singleplayer mode activated')
elif mode == 'd':
    print('doubleplayer mode activated')
available = []
for i in range(4, 31):
    available.append(str(i))
cc = 0
connect = None

def reset():
    global turn,powerupenable,p1p,p2p,enable,connect
    enable = ''
    powerupenable = False
    turn = 0
    length = 0
    width = 0
    os.system('clear')
    print("choose a board size. minimum: 4, maximum 30")
    while length not in available:
        length = input("board length?  ")
    while width not in available:
        width = input("board width?  ")
    print("creating board size {} x {}".format(length, width))
    size = [int(length),int(width)]
    connect = Board(size)
    time.sleep(.75)
    connect.reset()
    p1p = int(connect.area/10)
    p2p = int(connect.area/10)
reset()

connect.printboard()


possiblecolumns = []
for i in range(1,connect.columns+1):
    possiblecolumns.append(str(i))
columnsforcomp = possiblecolumns
possiblerows = []
for i in range(1,connect.rows+1):
    possiblerows.append(str(i))
powers = ['flip','bomb','random']
column = '111'
cc = 0
totalturns = connect.area
poweryn = False
yesno = ['y','n']

def ask(z):
    global column, cc,a,b,c,d,e,f,g,poweryn,totalturns,p1p,p2p
    power = '0'
    pp = 5
    poweryn = False
    if powerupenable:
        while not(power in yesno):
            power = input("powerup? (y/n):  ")
        if turn%2 == 1 and power == 'y':
            p1p -= 1
            pp = p1p
            print("you have {} powerups left".format(p1p))
        elif power == 'y':
            p2p -= 1
            pp = p2p
            print("you have {} powerups left".format(p2p))        
    while power == 'y' and pp > 0:
        poweryn = True
        powerup = ''
        while not(powerup in powers):
            powerup = input("which powerup? (flip, bomb, random)  ")
        if powerup == 'flip':
            revrow = 0
            while not(revrow in possiblerows):
                revrow = input("which row shall be flipped?  ")
            revrow = int(revrow)
            tmp1 = (connect.rows-revrow)*connect.columns
            tmp2 = (tmp1+connect.columns)
            preflip = connect.board[tmp1:tmp2]
            postflip = []
            for i in range(1,len(preflip)+1):
                postflip.append(preflip[len(preflip)-i])
            for i in range(tmp1,tmp2):
                connect.board[i] = postflip[i-tmp1]
            connect.checkdrop()
            z = '1'
            break
        if powerup == 'bomb':
            r = 0
            c = 0
            while not(r in possiblerows):
                r = input("which row?  ")
            while not(c in possiblecolumns):
                c = input("which column?  ")
            r = connect.rows-int(r)
            c = int(c)
            connect.board[connect.columns*r+c-1] = '   '
            connect.checkdrop()
            z = '1'
            break
        if powerup == 'random':
            randrow = 0
            while not(randrow in possiblerows):
                randrow = input("which row shall be randomized?  ")
            randrow = int(randrow)
            tmp1 = (connect.rows-randrow)*connect.columns
            tmp2 = (tmp1+connect.columns)
            postrand = connect.board[tmp1:tmp2]
            shuffle(postrand)
            for i in range(tmp1,tmp2):
                connect.board[i] = postrand[i-tmp1]
            connect.checkdrop()
            z = '1'
            break
    while not(z in possiblecolumns):
        z = input("what column? ")
    cc = int(z)
    while not(z in possiblecolumns) or connect.board[cc-1] != '   ':
        z = input("what column?s")
        try:
            cc = int(z)
        except ValueError:
            pass
            
def askcomp():
    if (turn == 2) and  connect.amount > 3:
        return
    column = randrange(1,connect.columns+1)
    while connect.board[column-1] != '   ':
        column = randrange(1,connect.columns+1)
    global cc, poweryn
    poweryn = False
    random = False
    if connect.checkv(0, connect.amount-1, None, 0) != None and connect.board[connect.checkv(0, connect.amount-1, None, 0)] == '   ': 
        cc = connect.checkv(0, connect.amount-1, None, 0)%connect.columns+1
        return
    try:
        if connect.checkh(0, connect.amount-1, None, 0) != None and (connect.board[connect.checkh(0, connect.amount-1, None, 0)-1] == '   ' or connect.board[connect.checkh(0 ,  connect.amount-1, None, 0)+ connect.amount-1] == '   '):
            if connect.board[connect.checkh(0, connect.amount-1, None, 0)-1] == '   ':
                cc = (connect.checkh(0, connect.amount-1, None, 0))%connect.columns
            elif connect.board[connect.checkh(0 ,  connect.amount-1, None, 0)+ connect.amount-1] == '   ':
                cc = (connect.checkh(0 ,  connect.amount-1, None, 0)+ connect.amount)%connect.columns
            else:
                random = True
            if not random and cc == 0:
                cc = connect.columns
            if not random:
                return
        elif connect.checkh(0, connect.amount-2, None, 0) != None and (connect.board[connect.checkh(0, connect.amount-2, None, 0)-1] == '   ' or connect.board[connect.checkh(0 , connect.amount-2, None, 0)+ connect.amount-2] == '   '):
            if connect.board[connect.checkh(0, connect.amount-2, None, 0)-1] == '   ':
                cc = (connect.checkh(0, connect.amount-2, None, 0))%connect.columns
                print(cc)
            elif connect.board[connect.checkh(0 ,  connect.amount-2, None, 0)+ connect.amount-2] == '   ':
                cc = (connect.checkh(0 ,  connect.amount-2, None, 0)+ connect.amount-2)%connect.columns+1
            else:
                random = True
            if not random and cc == 0:
                cc = connect.columns
            if not random:
                return
    except IndexError:
        random = True
    random = True
    if random:
        cc = column
        
while turn<totalturns and mode != 'z':
    while not(enable in yesno):
        print("you need to connect {} to win".format(connect.amount))
        enable = input("enable powerups? (y/n):  ")
        if enable in yesno and enable == yesno[0]:
            print("  each player gets {} powerups".format(int(connect.area/10)))
            confirm=''
            while not(confirm in yesno):
                confirm = input("continue? (y/n):  ")
            if confirm == yesno[0]:
                powerupenable = True
                totalturns += 100
        
    connect.printboard()
    
    turn += 1
    print('turn {}/{}'.format(turn,totalturns))
    #PRINT PLAYER TURN#
    if turn %2 ==1:
        print("blue guy's turn")
    elif mode == 'd':
        print("red guy's turn")
    #ASK COLUMN#
    if not(mode == 's' and turn%2==0):
        ask(column)
    else:
        askcomp()
    #GET COLOR#
    if turn%2==1:
        col = 34
    else:
        col = 31
    #DROP#
    if not poweryn:
        connect.drop(cc,col)
    else:
        connect.printboard()
        
    if connect.check(connect.amount) or turn == totalturns:
        if connect.check(connect.amount) and turn%2==1 and enable == 'n':
            print("blue guy wins!!!")
        elif connect.check(connect.amount) and enable == 'n':
            print("red guy wins!!!")
        elif enable == 'y' and connect.check(connect.amount) == '\033[034m o \033[00m':
            print("blue guy wins!!!")
        elif enable == 'y' and connect.check(connect.amount) == '\033[031m o \033[00m':
            print("red guy wins!!!")
        else:
            print("blue and red guy win and lose")
        tt = ''
        while not(tt in yesno):
            try:
                tt = input("play again? (y/n):  ")
            except KeyboardInterrupt:
                print()
                break
        if tt == 'y':
           reset()
           connect.printboard()
        else:
            break
    
print("good bye. see you later.")


#SECRET AREA

if mode == 'z':
    print('secret liar of mr. coconut infiltrated...')
    time.sleep(.5)
    reset()

    def rain(cc,a):
        for i in range(0,7):
            connect.drop(cc, a)
            
                                        
    def makeitrain():
        t = [1,3,5,7,9,11,13,15]
        for i in t:
            rain(i, randrange(29,38))
                
    connect.printboard()
    
    turn = 0
    while turn != 56:    
        while not(column in possible):
            column = input("what column mr.?   ")
            if column == 'rain':
                makeitrain()
                break
        try:
            cc = int(column)*2-1
        except ValueError:
            break
        while g[cc] != '   ':
            while not(column in possible):
                column = input("what column mr.?   ")
                if column == 'rain':
                    makeitrain()
                    break
        cc = int(column)*2-1

        connect.drop(cc, randrange(29,39))
        turn += 1
        column = '111'
