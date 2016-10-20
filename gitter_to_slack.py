import json
import requests

def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

def send_slack_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )


def mirror_gitter_to_slack(data):
    # urls, sent, unread, html, mentions, issues, id, meta, readBy, fromUser, v, text
    print(data['text'])

def gitter_rooms(token, filtr):
    r = requests.get('https://api.gitter.im/v1/rooms?access_token={}'.format(token))
    rooms = json.loads(r.text)
    rooms_to_mirror = {}
    for room in rooms:
        room_name = room["name"]
        if room_name.startswith(filtr):
            rooms_to_mirror[room["id"]] = room["name"]
    return rooms_to_mirror

def listen_from_gitter(token):
    r = requests.get('https://api.gitter.im/v1/rooms?access_token={}'.format(token))
    rooms = json.loads(r.text)

    rooms_to_mirror = {}
    for room in rooms:
        room_name = room["name"]
        if room_name.startswith('gloubi'):
            rooms_to_mirror[room["id"]] = room["name"]
    print(rooms_to_mirror)
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



    with open('token_gitter', 'r') as tokenfile_gitter:
        with open('token_slack', 'r') as tokenfile_slack:
            token_gitter = tokenfile_gitter.read().strip()
            token_slack = tokenfile_slack.read().strip()


            gitter_rooms = gitter_rooms(token_gitter, 'ethereum')
            print(gitter_rooms)
