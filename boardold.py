#!/usr/bin/python3
import os
import time
class Board():
    def reset(self):
        self.board = []
        for i in range(0, self.area):
            self.board.append('   ')
    def __init__(self, size):
        self.columns = size[0]
        self.rows = size[1]
        self.area = self.columns * self.rows
        self.board = []
        self.reset()
    
    def printboard(self):
        os.system('clear')
        h = (5*self.columns+2)
        h = '-' * h
        print(h)
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                print('||'+self.board[self.columns*r+c], end = '')
            print('||', self.rows-r)
            print(h)
        for i in range(0, self.columns):
            if i == 0 or i > 9:
                print('   {}'.format(i+1), end='')
            else:
                print('    {}'.format(i+1), end='')
        print()

    #DROPPING CIRCLES#
    def checkdrop(self):
        self.printboard()
        for i in range(0,self.area-self.columns):
            if self.board[self.area-1-i] == '   ' and self.board[self.area-1-i-self.columns] != '   ':
                time.sleep(.07)
                self.board[self.area-1-i] = self.board[self.area-1-i-self.columns]
                self.board[self.area-1-i-self.columns] = '   '
                self.printboard()
    def put(self, cc, col):
        self.board[cc] = '\033[0{}m o \033[00m'.format(col)
        self.printboard()
        time.sleep(.07)
    def drop(self, colm, col):
        cc = colm-1
        mult = 0
        while True:
            self.put(cc+self.columns*mult, col)
            mult += 1
            if mult == self.rows or self.board[cc+self.columns*mult] != '   ':
                break
            self.board[cc+self.columns*(mult-1)] = '   '

    #CHECKING WINS#
    
    def checkwinv(self):
        for r in range(0,self.area-3*self.columns):
            if self.board[r] != '   ' and self.board[r] == self.board[r+self.columns] == self.board[r+2*self.columns] == self.board[r+3*self.columns]:
                return self.board[r]
    def checkwinh(self):
        for r in range(0,self.area):
            if r%self.columns >= self.columns-3:
                continue
            elif self.board[r] != '   ' and self.board[r] == self.board[r+1] == self.board[r+2] == self.board[r+3]:
                return self.board[r]
    def checkwindup(self):
        for r in range(0,self.area-3*self.columns):
            if r%self.columns <= 2:
                continue
            elif self.board[r] != '   ' and self.board[r] == self.board[r-1+self.columns] == self.board[r-2+2*self.columns] == self.board[r-3+3*self.columns]:
                return self.board[r]
    def checkwinddown(self):
        for r in range(0,self.area-3*self.columns):
            if r%self.columns >= self.columns-3:
                continue
            elif self.board[r] != '   ' and self.board[r] == self.board[r+1+self.columns] == self.board[r+2+2*self.columns] == self.board[r+3+3*self.columns]:
                return self.board[r]
    def checkwin(self):
        return self.checkwinv() or self.checkwinh() or self.checkwindup() or self.checkwinddown()

    #CHECKING TWOS#

    def checktwo(self):
        for r in range(0,self.area):
            if r%self.columns == self.columns-1:
                continue
            elif r%self.columns == self.columns-2:
                if self.board[r] != '   ' and self.board[r] == self.board[r+1] and self.board[r-1] == '   ':
                    return r-1
            elif r%self.columns == self.columns-2:
                continue
            elif self.board[r] != '   ' and self.board[r] == self.board[r+1] and self.board[r+2] == '   ':
                return r+2
            elif self.board[r] != '   ' and self.board[r] == self.board[r+2] and self.board[r+1] == '   ':
                try:
                    if self.board[r+8] != '   ':
                        return r+1
                except IndexError:
                    return r+1
    #CHECKING THREES#

    def checkthreev(self):
        for r in range(self.columns,self.area-2*self.columns):
            if self.board[r] != '   ' and self.board[r] == self.board[r+self.columns] == self.board[r+2*self.columns] and self.board[r-self.columns] == '   ':
                return r%self.columns
    def checkthreeh(self):
        for r in range(0,self.area):
            if r%self.columns >= self.columns-2:
                continue
            elif self.board[r] != '   ' and self.board[r] == self.board[r+1] == self.board[r+2]:
                return r-1

    #CHECKING TRAPS#

#    def checkhtrap(self):
#        for r in range(0,self.area-self.columns):
#            if r%self.columns > self.columns-2:
#                continue
 
