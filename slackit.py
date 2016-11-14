import json
import os
import requests
from slackclient import SlackClient
from threading import Thread


def slack_channels(slack_client, filtr):
    channels_call = slack_client.api_call("channels.list")
    channels_to_filter = {}
    if channels_call.get('ok'):
        channels = channels_call['channels']
        for channel in channels:
            channel_name = channel["name"]
            if channel_name.startswith(filtr):
                channels_to_filter[channel["name"]] = channel["id"]
    return channels_to_filter


def send_slack_message(slack_client, channel_id, user, message, avatar):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username=user,
        icon_emoji=':robot_face:'
    )


def gitter_rooms(token, filtr):
    r = requests.get('https://api.gitter.im/v1/rooms?access_token={}'.format(token))
    rooms = json.loads(r.text)
    rooms_to_mirror = {}
    for room in rooms:
        room_name = room["name"]
        if room_name.startswith(filtr):
            rooms_to_mirror[room["name"]] = room["id"]
    return rooms_to_mirror


def mirror_to_slack(slack_channel_id, data, slack_client):
    # urls, sent, unread, html, mentions, issues, id, meta, readBy, fromUser, v, text
    msg = data['text']
    name = data['fromUser']['displayName']
    avatar =  data['fromUser']['avatarUrl']
    send_slack_message(slack_client, slack_channel_id, name, msg, avatar)


def listen_gitter_post_slack(token, slack_client, gitter_room_id, slack_channel_id):
    url = 'https://stream.gitter.im/v1/rooms/{}/chatMessages'.format(gitter_room_id)
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, headers=headers, stream=True)
    for line in r.iter_lines():
        if line.strip():
            data = json.loads(line.decode('utf8'))
            mirror_to_slack(slack_channel_id, data, slack_client)


if __name__ == '__main__':

    def slackit(token_gitter, slack_client, room, channel):
        print("THREAD {room} {channel}".format(room=room, channel=channel))
        listen_gitter_post_slack(token_gitter, slack_client, room, channel)

    token_gitter = os.environ['GITTER_TOKEN']
    token_slack = os.environ['SLACK_TOKEN']

    slack_client = SlackClient(token_slack)

    gitter_rooms = gitter_rooms(token_gitter, 'ethereum')
    slack_channels = slack_channels(slack_client, 'gitter')

    # gitter: slack
    mirror = [
        ['ethereum/solidity','gitter_solidity'],
        ['ethereum/web3.js', 'gitter_web3js'],
        ['ethereum/cpp-ethereum', 'gitter_cpp-ethereum'],
        ['ethereum/light-client', 'gitter_light-client'],
        ['ethereum/go-ethereum', 'gitter_go-ethereum'],
        ['ethereum/tutorials', 'gitter_tutorials'],
        ['ethereum/yellowpaper', 'gitter_yellowpaper'],
        ['ethereum/ethereumj', 'gitter_ethereumj'],
        ['ethereum/mist', 'gitter_mist'],
        ['ethereum/research', 'gitter_research'],
        ['ethereum/welcome', 'gitter_welcome'],
    ]

    for gitter_room, slack_channel in mirror:
        thread = Thread(target=slackit, args=(token_gitter, slack_client,  gitter_rooms[gitter_room],  slack_channels[slack_channel]))
        thread.start()
