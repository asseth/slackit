## what is Slackit?

Slackit allow you to mirror the gitter channels of the Ethereum foundation to your own slack channels.

## usage

    git clone https://github.com/asseth/slackit.git
    cd slackit
    docker build -t asseth/slackit .
    docker run -e SLACK_TOKEN=YOUR_SLACK_TOKEN -e GITTER_TOKEN=YOUR_GITTER_TOKEN --name=slackit asseth/slackit
