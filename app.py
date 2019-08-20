import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
SECRET = os.environ.get("SECRET")

# Channel Access Token
line_bot_api = LineBotApi(ACCESS_TOKEN)
# line_bot_api = LineBotApi('YOB5RBTArIkHRWTWlXdc+IBwbFnwRxSPzHMNHurl0+/0xJ8bKVl2lcpAp7XE2sBM7l3YD4V6VBW+A+3g/CkBnshn7tF1ImmS8jivWt/EUDiGO14crpibn5UajQJPKNjbsB+47KRbjZR8X/F53Xs44AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler(SECRET)
# handler = WebhookHandler('476c26b19e949a1f5d9721bb4cd9583d')

@app.route("/")
def index():
    return "<p>Welcome to onetwofree LineBot Demo</p>"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# ================= 客製區 Start =================
def is_alphabet(uchar):
    if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
        print('English')
        return "en"
    elif '\u4e00' <= uchar<='\u9fff':
        #print('Chinese')
        print('Chinese')
        return "zh-tw"
    else:
        return "en"
# ================= 客製區 End =================

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == "TEST":
        line_bot_api.reply_message(event.reply_token, "你輸入了TEST!!")
    else:
        message = TextSendMessage(text = "你輸入的訊息是:　" + event.message.text)
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
