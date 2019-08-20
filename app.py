from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('swpST/tCuk/g6laDEpAN4GY4Nk6BqHtLIPInJXNTAEVN/zNbjUf4S2cEmuBsCysN7l3YD4V6VBW+A+3g/CkBnshn7tF1ImmS8jivWt/EUDinU3Cag2A/emS6p3UfwbLonmzbRTMFcq9IoyzVBo9LZAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('476c26b19e949a1f5d9721bb4cd9583d')


@app.route("/")
def home():
    return 'home OK'

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="這是自動回覆訊息： " + event.message.text))


if __name__ == "__main__":
    app.run()
    