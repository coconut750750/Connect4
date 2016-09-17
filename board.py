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
        if self.area < 20:
            self.amount = 3
        elif self.area < 60:
            self.amount = 4
        else:
            self.amount = int(int((self.columns+self.rows)/2)*1/3)+3
        self.board = []
        self.reset()
    
    def printboard(self):
        os.system('clear')
        h = (5*self.columns+2)
        h = '-' * h
        print(h)
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                print('||'+self.board[self.columns*r+c], end="")
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

    #CHECKING RECURSIVELY#
    def checkh(self, cc, amount, success, time):
        if time == amount-1:
            return (cc-amount+1)
        if time == 0:
            for r in range(0,self.area):
                if r%self.columns >= self.columns-amount+1 or r<cc:
                    continue
                if self.board[r] != '   ':
                    cc = r
                    if self.board[cc] == self.board[cc+1]:
                        success = self.checkh(cc+1, amount, success, time+1)
                        if success:
                            return success
        else:
            if self.board[cc] == self.board[cc+1]:
                success = self.checkh(cc+1, amount, success, time+1)
                return success              
        return None

    def checkv(self, cc, amount, success, time):
        if time == amount-1:
            return (cc-(amount)*self.columns)
        if time == 0:
            for r in range(0,self.area-(amount-1)*self.columns):
                if r<cc:
                    continue
                if self.board[r] != '   ':
                    cc = r
                    if self.board[cc] == self.board[cc+self.columns]:
                        success = self.checkv(cc+self.columns, amount, success, time+1)
                        return success
        else:
            if self.board[cc] == self.board[cc+self.columns]:
                success = self.checkv(cc+self.columns, amount, success, time+1)
                return success
        return None

    def checkdup(self, cc, amount, success, time):
        if time == amount-1:
            return (cc+amount)
        if time == 0:
            for r in range(0,self.area-(amount-1)*self.columns):
                if r%self.columns < amount-1 or r<cc:
                    continue
                if self.board[r] != '   ':
                    cc = r
                    if self.board[cc] == self.board[cc-1+self.columns]:
                        success = self.checkdup(cc-1+self.columns, amount, success, time+1)
                        return success
        else:
            if self.board[cc] == self.board[cc-1+self.columns]:
                success = self.checkdup(cc-1+self.columns, amount, success, time+1)
                return success
        return None

    def checkddown(self, cc, amount, success, time):
        if time == amount-1:
            return (cc-amount+2)
        if time == 0:
            for r in range(0,self.area-(amount-1)*self.columns):
                if r%self.columns >= self.columns-amount+1 or r<cc:
                    continue
                if self.board[r] != '   ':
                    cc = r
                    if self.board[cc] == self.board[cc+1+self.columns]:
                        success = self.checkddown(cc+1+self.columns, amount, success, time+1)
                        return success
        else:
            if self.board[cc] == self.board[cc+1+self.columns]:
                        success = self.checkddown(cc+1+self.columns, amount, success, time+1)
                        return success
        return None
    
    def check(self, amount):
        if self.checkh(0, amount, None, 0) or self.checkv(0, amount, None, 0) or self.checkdup(0, amount, None, 0) or self.checkddown(0, amount, None, 0):
            return True
        return False

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

    #CHECKING RECURSSIVELY#
    #AMOUNT = NUMBER IN A ROW
    
    

    #CHECKING TRAPS#

#    def checkhtrap(self):
#        for r in range(0,self.area-self.columns):
#            if r%self.columns > self.columns-2:
#                continue

#connect = Board([8,8])
#connect.put(62, 36)
#connect.put(61, 36)
#connect.put(60, 36)
#connect.put(1, 36)
#connect.put(0, 32)
#connect.put(11, 36)
#print(connect.checkh(0, 3, None, 0)+3-1)
