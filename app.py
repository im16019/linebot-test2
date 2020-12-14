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
import pandas as pd
import codecs as co

app = Flask(__name__)

line_bot_api = LineBotApi('BW/HND4FU1efVOdN3KsTgQxucMlPz9VTmTC0B8xVZmOKAceLZQMjSvgTY5l+LXrvEpy+MJJ3mtrj+f+FRNst9499Abs8sFDZqDlyupjnoCD346QWjjrs7ksZTZrvrRodkSDNY2n3UBmnPX0F65nU0wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4567c2bd3d51462f7e0372915364c675')

@app.route("/")
def test():
    return "OK"

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

with co.open('D:/linebot-test4/searching.csv', 'r', 'Shift-JIS', 'ignore') as file:
     data = pd.read_table(file, delimiter=',')
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    word = event.message.text
    Amaterial = data['material'][data['material'].str.contains(word)]
    reply_message = f"{word}の検索結果は{Amaterial}です。"
    line_bot_api.reply_message(
        event.reply_token,
          TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()