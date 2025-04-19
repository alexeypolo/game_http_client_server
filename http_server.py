import http.server
import socketserver
import urllib.parse

next_game_id = 1
next_msg_id = 1

waiting_games = {}
active_games = {}

# An outbox of messages
games_outbox = {}

def parse_url_qs(url):
    parsed_url = urllib.parse.urlparse(url)
    parsed_qs = urllib.parse.parse_qs(parsed_url.query)
    kv = {}
    for key in parsed_qs:
        kv[key] = parsed_qs[key][0]
    return kv

def push_message(game_id, player, msg):
    global games_outbox, next_msg_id

    msg_id = str(next_msg_id)
    next_msg_id += 1

    msg = f'msg_id={msg_id}, {msg}'
    games_outbox[game_id][player].append(msg)
    print(f'push_message: games_outbox={games_outbox}')

def pop_message(game_id, player):
    try:
        global games_outbox
        msg = games_outbox[game_id][player].pop(0)
    except:
        msg = ""
    print(f'pop_message: games_outbox={games_outbox}, msg="{msg}"')
    return msg

def action_start_game(player):

    if len(waiting_games) == 0:
        global next_game_id
        game_id = str(next_game_id)
        next_game_id += 1

        waiting_games[game_id] = player
        print(f'DBG: waiting_games={waiting_games}')
        response = f'to={player}, game_id={game_id}, status=WAIT_FOR_OPONENT'
    else:
        game_id, oponent = waiting_games.popitem()
        print(f'DBG: popped game_id={game_id}, oponent={oponent} from the waiting list')
    
        global active_games, games_outbox

        # List a new game and create an empty game_outbox
        active_games[game_id] = [player, oponent]
        games_outbox[game_id] = { player: [], oponent: []}

        # Notify the player and the oponent. Same message is sent to both sides
        msg = f'game_id={game_id}, status=STARTED'
        push_message(game_id, oponent, f'to={oponent}, from={player}, {msg}')
        response = f'to={player}, from={oponent}, {msg}'

    return response

def action_fire(game_id, player, location):
    game = active_games.get(game_id)

    if not game:
        response = 'ERR_GAME_ID_INACTIVE'
    elif player not in game:
        response = 'ERR_BAD_PLAYER'
    else:
        if game[0] == player:
            oponent = game[1]
        else:
            oponent = game[0]

        msg = f'to={oponent}, from={player}, game_id={game_id}, action=fire, location={location}'
        push_message(game_id, oponent, msg)
        response = f'to={player}, game_id={game_id}, status=FIRE_OK'

    return response

def action_getmsg(game_id, player):
    return pop_message(game_id, player)

class GameServer(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        url = self.path
        values = parse_url_qs(url)
        print(f'GET: {url}, parsed: {values}')

        action = values.get('action')
        game_id = values.get('game_id')
        player = values.get('player')
        location = values.get('location')

        if action == 'start_game':
            if player:
                response = action_start_game(player)
            else:
                response = 'ERR_MISSING_PLAYER'            
        elif action == 'fire':
            if not player:
                response = 'ERR_MISSING_PLAYER'
            elif not game_id:
                response = 'ERR_MISSING_GAME_ID'
            elif not location:
                response = 'ERR_MISSING_LOCATION'
            else:
                response = action_fire(game_id, player, location)
        elif action == 'getmsg':
            if not player:
                response = 'ERR_MISSING_PLAYER'
            elif not game_id:
                response = 'ERR_MISSING_GAME_ID'
            else:
                response = action_getmsg(game_id, player)
        else:
            response = f'ERR_BAD_ARGS'

        if response.startswith('ERR_'):
            response = f'status={response}'

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = "<html><body>"
        output += f"<response>{response}</response>"
        output += "</body></html>"
        self.wfile.write(bytes(output, "utf8"))


PORT = 9000
with socketserver.TCPServer(("", PORT), GameServer) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
