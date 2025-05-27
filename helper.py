#!/usr/bin/env python3
def code_to_emoji(code):
    if code == ord('💥'): return '💥'
    if code == 0x1F5E1: return '🗡️'
    if code == 0x1F6F3: return '🛳️'
    if code == ord('🌊'): return '🌊'
    if code == 0x1F32B: return '🌫️'
    if code == ord('🧨'): return '🧨'
    if code == 0x2B55: return '⭕️'
    
    return ' '

def print_sea(sea, oponent_sea):
    print('  A  B  C  D  E  F  G  H', end='')
    print(' ' * 10, '  A  B  C  D  E  F  G  H')
    for i in range(8):
        print(i+1, '', end='')
        for j in range(8):
            print(code_to_emoji(sea[i][j]) + ' ', end='')
        print(' ' * 9, end='')
        print(i+1, '', end='')
        for j in range(8):
            print(code_to_emoji(oponent_sea[i][j]) + ' ', end='')
        print()


def count_cells(sea, x):
    n=0
    for row in range(8):
        for column in range(8):
            if sea[row][column] == x:
                n=n+1
    return n 

def mark_circles(oponent_sea,row,column):
    sea2=oponent_sea
    if row > 0:
        r=row-1
        cl=column
        cr=column
        if column > 0:
            cl=cl-1        
        if column < 7:
            cr=cr+1
        for c in range(cl,cr+1):
            sea2[r][c]=0x2B55

    if row < 7:
        r=row+1
        cl=column
        cr=column
        if column > 0:
            cl=cl-1        
        if column < 7:
            cr=cr+1
        for c in range(cl,cr+1):
            sea2[r][c]=0x2B55


    if column > 0:
        sea2[row][column-1]=0x2B55

    if column <7:
        sea2[row][column+1]=0x2B55

def is_legal(sea):
    for i in range(8):
        for j in range(8):
            if sea[i][j] == 1:
                # row above
                if i > 0:
                    if (j > 0) and sea[i-1][j-1] == 1:
                        return False
                    if sea[i-1][j] == 1:
                        return False
                    if j < 8 - 1 and sea[i-1][j+1] == 1:
                        return False
                # this row
                if (j > 0) and sea[i][j-1] == 1:
                    return False
                if j < 8 - 1 and sea[i][j+1] == 1:
                    return False
                # row below
                if i < 8 - 1:
                    if (j > 0) and sea[i+1][j-1] == 1:
                        return False
                    if sea[i+1][j] == 1:
                        return False
                    if j < 8 - 1 and sea[i+1][j+1] == 1:
                        return False

    return True







