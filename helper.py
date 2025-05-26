#!/usr/bin/env python3
def code_to_emoji(code):
    if code == ord('💥'): return '💥'
    if code == 0x1F5E1: return '🗡️'
    if code == 0x1F6F3: return '🛳️'
    if code == ord('🌊'): return '🌊'
    if code == 0x1F32B: return '🌫️'
    if code == ord('🧨'): return '🧨'

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







