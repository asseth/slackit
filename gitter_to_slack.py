import json
import requests


def mirror_to_slack(data):
    # urls, sent, unread, html, mentions, issues, id, meta, readBy, fromUser, v, text
    print(data['text'])

def listen_from_gitter(token):
    r = requests.get('https://api.gitter.im/v1/rooms?access_token={}'.format(token))
    rooms = json.loads(r.text)

    rooms_to_mirror = {}
    for room in rooms:
        room_name = room["name"]
        if room_name.startswith('gloubi'):
            rooms_to_mirror[room["id"]] = room["name"]

    room_ids = [room_id for room_id in rooms_to_mirror]

    # draft with only one room
    room_id = room_ids[0]
    url = 'https://stream.gitter.im/v1/rooms/{}/chatMessages'.format(room_id)
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, headers=headers, stream=True)
    for line in r.iter_lines():
        if line.strip():
            data = json.loads(line.decode('utf8'))
            # print(data)
            mirror_to_slack(data)


if __name__ == '__main__':

    with open('gitter_token', 'r') as tokenfile:
        token=tokenfile.read().strip()
        listen_from_gitter(token)
