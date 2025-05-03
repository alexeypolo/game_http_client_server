import http.server
import socketserver
import urllib.parse

class Game:
    '''Active game'''
    def __init__(self, player1, player2):
        self.players = [player1, player2]
    
    def player_exists(self, player):
        return player in self.players
    
    def oponent(self, player):
        if self.players[0] == player:
            return self.players[1]
        return self.players[0]


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

def action_getmsg(game_id, player):
    try:
        global games_outbox
        response = 'OK, ' + games_outbox[game_id][player].pop(0)
    except:
        response = 'OK::NONE'
    
    return response

def action_start_game(player):

    if len(waiting_games) == 0:
        global next_game_id
        game_id = str(next_game_id)
        next_game_id += 1

        waiting_games[game_id] = player
        print(f'DBG: waiting_games={waiting_games}')
        response = f'OK, to={player}, game_id={game_id}, game_status=WAIT_FOR_OPONENT'
    else:
        game_id, oponent = waiting_games.popitem()
        print(f'DBG: popped game_id={game_id}, oponent={oponent} from the waiting list')
    
        global active_games, games_outbox

        # List a new game and create an empty game_outbox
        active_games[game_id] = Game(player, oponent)
        games_outbox[game_id] = { player: [], oponent: []}

        # Notify the player and the oponent. Same message is sent to both sides
        msg = f'game_id={game_id}, game_status=STARTED'
        push_message(game_id, oponent, f'to={oponent}, from={player}, {msg}')
        response = f'OK, to={player}, from={oponent}, {msg}'

    return response

def action_fire(game_id, player, location):
    game = active_games.get(game_id)

    if not game:
        return 'ERR::ACTION_FIRE::GAME_ID_INACTIVE'
    if game.player_exists(player):
        return 'ERR::ACTION_FIRE::PLAYER_DOES_NOT_EXIST'
    
    oponent = game.oponent(player)

    msg = f'to={oponent}, from={player}, game_id={game_id}, action=fire, location={location}'
    push_message(game_id, oponent, msg)

    return f'OK, to={player}, game_id={game_id}'

def action_fire_report(game_id, player, location, cell_state):
    game = active_games.get(game_id)

    if not game:
        return 'ERR::ACTION_FIRE_REPORT::GAME_ID_INACTIVE'
    if game.player_exists(player):
        return 'ERR::ACTION_FIRE_REPORT::PLAYER_DOES_NOT_EXIST'
    
    oponent = game.oponent(player)

    msg = f'to={oponent}, game_id={game_id}, location={location}, cell_state={cell_state}'
    push_message(game_id, oponent, msg)

    return f'OK, to={player}, game_id={game_id}'


class GameServer(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        url = self.path
        values = parse_url_qs(url)
        print(f'GET: {url}, parsed: {values}')

        action = values.get('action')
        game_id = values.get('game_id')
        player = values.get('player')
        location = values.get('location')
        cell_state = values.get('cell_state')

        if action == 'start_game':
            if not player:
                response = 'ERR::MISSING_PARAM'
            else:
                response = action_start_game(player)
        elif action == 'fire':
            if None in [game_id, player, location]:
                response = 'ERR::MISSING_PARAM'
            else:
                response = action_fire(game_id, player, location)
        elif action == 'fire-report':
            if None in [game_id, player, location, cell_state]:
                response = 'ERR::MISSING_PARAM'
            else:
                response = action_fire_report(game_id, player, location, cell_state)
        elif action == 'getmsg':
            if None in [game_id, player]:
                response = 'ERR::MISSING_PARAM'
            else:
                response = action_getmsg(game_id, player)
        else:
            response = f'ERR::UNKNOWN_ACTION'

        response = f'action={action}, status={response}'

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
