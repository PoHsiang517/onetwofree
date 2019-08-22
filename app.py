import os
import json
import re

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, JoinEvent, LeaveEvent, FollowEvent,
    TextMessage, ImageMessage, AudioMessage, TextSendMessage, ImageSendMessage, StickerMessage
)

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
SECRET = os.environ.get("SECRET")

# Channel Access Token
line_bot_api = LineBotApi(ACCESS_TOKEN)
# line_bot_api = LineBotApi('YOB5RBTArIkHRWTWlXdc+IBwbFnwRxSPzHMNHurl0+/0xJ8bKVl2lcpAp7XE2sBM7l3YD4V6VBW+A+3g/CkBnshn7tF1ImmS8jivWt/EUDiGO14crpibn5UajQJPKNjbsB+47KRbjZR8X/F53Xs44AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler(SECRET)
# handler = WebhookHandler('476c26b19e949a1f5d9721bb4cd9583d')


# re判斷輸入字串是否為數字

def is_number(num):
	pattern = re.compile(r"^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$")
	result = pattern.match(num)
	if result:
		return True
	else:
		return False
#====================================================================

@app.route("/")
def index():
    return "<p>Welcome to onetwofree LineBot Demo</p><p>請用LINE測試本功能</p>"

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    weather = re.compile(r"\w*天氣\w*") #使用re判斷輸入字串中是否含有特定字詞
    if weather.findall(event.message.text): #判斷list中是否有值，True表示有關鍵字，False表示沒有關鍵字則進到下一個判斷
        message = TextSendMessage("查詢天氣功能")
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == "人之初": #message from user #輸入必須為固定字詞
        message = TextSendMessage("性本善")
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text = "你輸入的訊息是:　" + event.message.text)
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
