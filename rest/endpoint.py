# -*- coding:utf-8 -*-
import json
import os

from flask import Flask, request

from message import pr_msg
from wechat_sdk import WeChat

app = Flask(__name__)

we = WeChat(
    url=os.environ.get('WECHAT_BASE_URL'),
    corp_id=os.environ.get('WECHAT_CORP_ID'),
    corp_secret=os.environ.get('WECHAT_CORP_SECRET'),
    agent_id=os.environ.get('WECHAT_AGENT_ID')
)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/wechat', methods=['POST'])
def wechat():

    if request.method != 'POST':
        return 'Error'

    payload = json.loads(request.data)

    repo = {
        'full_name': payload['repository']['full_name'],
        'owner': payload['repository']['owner']['login']
    }

    if 'pull_request' in payload:
        we.auto_send_text_card_message(
            pr_msg(repo, payload)
        )
        return 'yoyoyo'
    elif 'issue' in payload:
        return
    else:
        return 'not support'

if __name__ == '__main__':
    app.run()
