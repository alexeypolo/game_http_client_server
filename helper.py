#!/usr/bin/env python3
def print_sea(sea, oponent_sea):
    print('  A  B  C  D  E  F  G  H', end='')
    print(' ' * 10, '  A  B  C  D  E  F  G  H')
    for i in range(8):
        print(i+1, '', end='')
        for j in range(8):
            print(sea[i][j] + ' ', end='')
        print(' ' * 9, end='')
        print(i+1, '', end='')
        for j in range(8):
            print(oponent_sea[i][j] + ' ', end='')
        print()


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







