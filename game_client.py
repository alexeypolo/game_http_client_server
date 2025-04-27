import argparse
import requests
import sys

def get_xml_value(s, tag):
    start = s.find(f'<{tag}>')
    end = s.find(f'</{tag}>')

    if start < 0 or end < 0:
        return None
    
    start += len(f'<{tag}>')
    if end < start:
        return None
    
    return s[start:end]

def parse_response(rsp):
    res = {}
    if len(rsp) != 0:
        for pair in rsp.split(','):
            key, value = pair.strip().split('=')
            res[key.strip()] = value.strip()
    return res

def request(url, name_value_dict):
    try:
        req = f'{url}?'
        for key in name_value_dict:
            req += f'{key}={name_value_dict[key]}&'
        req=req[:-1]
    
        response = requests.get(req)
        response.raise_for_status()

        rsp = get_xml_value(response.text, 'response')
    
        rsp = parse_response(rsp)
        return rsp
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='The game of battle ships.')
    parser.add_argument('--url', required=True, help='url')
    parser.add_argument('--action', required=True, help='action')
    parser.add_argument('--player', required=True, help='player')
    parser.add_argument('--game_id', required=False, help='game_id')
    parser.add_argument('--location', required=False, help='location')
    args = parser.parse_args()

    name_value_dict = { 'action': args.action, 'player': args.player }
    if args.game_id:
        name_value_dict['game_id'] = args.game_id
    if args.location:
        name_value_dict['location'] = args.location

    rsp = request(args.url, name_value_dict)
    print(f'response: {rsp}')
    
    return 0

if __name__ == "__main__":
    sys.exit(main())