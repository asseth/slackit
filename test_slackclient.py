from slackclient import SlackClient

def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )


if __name__ == '__main__':
    with open('slack_token', 'r') as tokenfile:
        token=tokenfile.read().strip()
        slack_client = SlackClient(token)
        channels = list_channels()

        if channels:
            print("Channels: ")
            for c in channels:
                print(c['name'], c['id'])
                if c['name']=='test_bot':
                    send_message(c['id'], 'coucou je teste')

        else:
            print("Unable to authenticate.")
