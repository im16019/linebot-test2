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

line_bot_api = LineBotApi('6+mGTbab9xfjZ0sTzyNWmT8JuLwAeJnwrY3P3h6l2LqH66cgkCMNn1E9vrhpfc5TEpy+MJJ3mtrj+f+FRNst9499Abs8sFDZqDlyupjnoCAZUpGLdglQAu4mexOyVsSsQQT75DdIXQ2qYyIoY1ibRgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('879cd17815e58e70cc15cf61d8779d55')

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

with co.open('https://github.com/im16019/linebot-test2/blob/main/searching.csv', 'r', 'Shift-JIS', 'ignore') as file:
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