import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_app import app

if __name__ == "__main__":
    SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()
