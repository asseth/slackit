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
    slack_channels = slack_channels(slack_client, 'zgitter')

    # gitter: slack
    mirror = [
        ['ethereum/welcome', 'zgitter_welcome'],
        ['ethereum/go-ethereum', 'zgitter_go-ethereum'],
        ['ethereum/solidity','zgitter_solidity'],
        ['ethereum/web3.js','zgitter_web3js'],
        ['ethereum/mist', 'zgitter_mist'],
        ['ethereum/cpp-ethereum', 'zgitter_cpp-ethereum'],
        ['ethereum/research', 'zgitter_research'],
        ['ethereum/ethereumj', 'zgitter_ethereumj'],
        ['ethereum/tutorials', 'zgitter_tutorials'],
        ['ethereum/light-client', 'zgitter_light-client'],
        ['ethereum/swarm', 'zgitter_swarm'],
        ['ethereum/mix', 'zgitter_mix'],
        ['ethereum/homestead-guide', 'zgitter_homestead-gui'],
        ['ethereum/pyethereum', 'zgitter_pyethereum'],
        ['ethereum/EIPs', 'zgitter_eips'],
        ['ethereum/governance', 'zgitter_governance'],
        ['ethereum/ethereumjs-lib', 'zgitter_ethereumjslib'],
        ['ethereum/devcon2social', 'zgitter_devcon2social'],
        ['ethereum/general', 'zgitter_general'],
        ['ethereum/whisper', 'zgitter_whisper'],
        ['ethereum/frontier-guide', 'zgitter_frontier-gui'],
        ['ethereum/go-ethereum/name-registry', 'zgitter_gethnameregis'],
        ['ethereum/minercommunitysupport', 'zgitter_miner-support'],
        ['ethereum/evm2.0-design', 'zgitter_evm-2-design'],
        ['ethereum/formal-methods', 'zgitter_formal-method'],
        ['ethereum/cpp-ethereum-development', 'zgitter_cppeth-dev'],
        ['ethereum/devp2p', 'zgitter_devp2p'],
        ['ethereum/AllCoreDevs', 'zgitter_all-core-devs'],
        ['ethereum/remix', 'zgitter_remix'],
        ['ethereum/porting', 'zgitter_porting'],
        ['ethereum/serpent', 'zgitter_serpent'],
        ['ethereum/casper-scaling-and-protocol-economics', 'zgitter_casper'],
        ['ethereum/yellowpaper', 'zgitter_yellowpaper'],
        ['ethereum/state-channels', 'zgitter_state-channel'],
        ['ethereum/ecosystem-standards', 'zgitter_ecosystem'],
        ['ethereum/privacy-tech', 'zgitter_privacy-tech'],
        ['ethereum/BerlinMeetup', 'zgitter_berlin-meetup'],
        ['ethereum/evmjit', 'zgitter_evm-jit'],
        ['ethereum/pydevp2p', 'zgitter_pydevp2p'],
        ['ethereum/ethereum.js', 'zgitter_ethereum-js'],
        ['ethereum/swatch', 'zgitter_swatch'],
        ['ethereum/ethereum-org', 'zgitter_ethereum-org'],
        ['ethereum/tests', 'zgitter_tests'],
        ['ethereum/documentation', 'zgitter_documentation'],
        ['ethereum/homesteadtest', 'zgitter_homesteadtest'],
        ['ethereum/solidity-development', 'zgitter_solidity-dev'],
        ['ethereum/OSMiningPool', 'zgitter_os-miningpool'],
        ['ethereum/native-dapp-subscriptions', 'zgitter_dapp-subscrip'],
        ['ethereum/common', 'zgitter_common'],
        ['ethereum/ethereum-es', 'zgitter_ethereum-es'],
        ['ethereum/MIT-Media-Lab-Hack', 'zgitter_mit-media-lab'],
        ['ethereum/test-tools', 'zgitter_test-tools'],
    ]

    for gitter_room, slack_channel in mirror:
        thread = Thread(target=slackit, args=(token_gitter, slack_client,  gitter_rooms[gitter_room],  slack_channels[slack_channel]))
        thread.start()
