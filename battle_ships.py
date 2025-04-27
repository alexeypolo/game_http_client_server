#!/usr/bin/env python3
import sys
import game_client
import random
from helper import *

fire='💥'
debris='🗡️'
ship="🛳️"
miss="🤪"
water='🌊'
fog='🌫️'
bomb='🧨'

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
            
print_sea(sea, oponent_sea)
url='http://localhost:9000'
player=sys.argv[1]

request = { 'action': 'start_game', 'player': player}
response = game_client.request(url, request)
my_turn = False

game_id = response['game_id']

if response['status'] == "WAIT_FOR_OPONENT":
  print("""
                          ЖДИ ИГРОКА...""")
  while True:
    request = { 'action': 'getmsg', 'player': player, "game_id":  game_id}
    response = game_client.request(url, request)
    if len(response) != 0 and response['status']=='STARTED':
      break  
  my_turn=True
elif response['status'] == 'STARTED':
  my_turn=False

print("""                         
                         НГРА НАЧЕТА!!!""")
while True:
  if my_turn:
    print("ВАШ ХОД:")
    loc = input()
    request = { 'action': 'fire', 'player': player, "game_id":  game_id, 'location': loc}
    response = game_client.request(url, request)


  else:
    print("ХОД СОПЕРНИКА")
    while True:
      request = { 'action': 'getmsg', 'player': player, "game_id":  game_id }
      response = game_client.request(url, request)
      if response != {}:
        loc=response['location']
        column=ord(loc[0].lower()) - ord('a')         
        row=ord(loc[1].lower()) - ord('1')
        cell=sea[row][column]
        if cell==water:
          status='miss'
        elif cell==ship:
          status='hit'
        elif cell == debris:
          status ='BEEN_THERE'

        request = { 'action': 'fire-report', 'player': player, "game_id": game_id, "status":status }
        response = game_client.request(url, request)

        print(response)
       
  
  my_turn=not my_turn
