#!/usr/bin/env python3
import os
import sys
import game_client
import random
from helper import *

fire = ord('💥')
debris = 0x1F5E1 # 🗡️
ship = 0x1F6F3 # 🛳️
water = ord('🌊')
fog = 0x1F32B # 🌫️
bomb = ord('🧨')

sea=[
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]
oponent_sea = [
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0],
    ]

ships = ([1] * 8) + ([0] * 56)

while True:
    random.shuffle(ships)

    for i in range(8):
        for j in range(8):
            sea[i][j] = ships[i*8 + j]

    ok = is_legal(sea)
    if ok:
       break

for i in range(8):
        for j in range(8):
            if sea[i][j] == 0:
              sea [i][j] = water
            if sea[i][j] == 1:
              sea[i][j] = ship
            oponent_sea[i][j] = fog
            
os.system('clear')
print_sea(sea, oponent_sea)

player = sys.argv[1]
if len(sys.argv) > 2:
   url=sys.argv[2]
else:
   url='http://localhost:9000'

request = { 'action': 'start_game', 'player': player}
response = game_client.request(url, request)
my_turn = False


game_id = response['game_id']

if response['game_status'] == "WAIT_FOR_OPONENT":
  print("""
                          ЖДИ ИГРОКА...""")
  while True:
    request = { 'action': 'getmsg', 'player': player, "game_id":  game_id}
    response = game_client.request(url, request)
    if response['status'] == 'OK' and response['game_status']=='STARTED':
      break  
  my_turn=True
elif response['game_status'] == 'STARTED':
  my_turn=False

print("""                         
                         ИГРА НАЧАТА!!!""")
while True:
  os.system('clear')
  print_sea(sea, oponent_sea)

  if my_turn == True:
    my_turn=False
    print("ВАШ ХОД:")
    loc = input()
    request = { 'action': 'fire', 'player': player, "game_id":  game_id, 'location': loc}
    response = game_client.request(url, request)
    while True:
      request = { 'action': 'getmsg', 'player': player, "game_id":  game_id }
      response = game_client.request(url, request)
      if response['status'] == 'OK':
         if response['action']=='fire-report':
            loc=response['location']
            cell_state=int(response['cell_state'])

            column = ord(loc[0].lower()) - ord('a')         
            row = ord(loc[1].lower()) - ord('1')
            oponent_sea[row][column] = cell_state

            n = count_cells(oponent_sea, debris)
            if n==8:
               print('ПОБЕДА!!')
               input()

            break

  else:
    my_turn=True
    print("                    ХОД СОПЕРНИКА:")
    while True:
      request = { 'action': 'getmsg', 'player': player, "game_id":  game_id }
      response = game_client.request(url, request)
      if response['status'] == 'OK':
        loc = response['location']
        print(f'Стреляют по {loc}')

        column = ord(loc[0].lower()) - ord('a')         
        row = ord(loc[1].lower()) - ord('1')
        cell = sea[row][column]

        if cell == water:
          sea[row][column] = fire
        elif cell == ship:
          sea[row][column] = debris 

        request = { 'action': 'fire-report', 'player': player, "game_id": game_id, 'location':loc,"cell_state":sea[row][column]}
        response = game_client.request(url, request)

        n = count_cells(sea, debris)
        if n==8:
          print('                   ПОРАЖЕНИЕ☠️ ☠️')
          input()

        break