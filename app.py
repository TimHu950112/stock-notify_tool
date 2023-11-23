from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage ,ImageSendMessage
from flask import *
from flask_restful import Api,Resource
from dotenv import load_dotenv
from get_stock import *
from upload_imgur import *
import pymongo,certifi,os

from send_email import send_email
from data_base import *

load_dotenv()
client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())

#初始化 flask 伺服器
app=Flask(
    __name__,
    static_folder="assets",
    static_url_path="/assets"
)
app.secret_key=os.getenv("secret_key")



# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(os.getenv('line_access'))
handler = WebhookHandler(os.getenv('line_secret'))

class Verify_Email(Resource):
    def get(self,email_account):
        result=email_function(email_account,'verify')
        if result != None:
            return result
        return '出現錯誤，請重新驗證',403

# 加載API
api = Api(app)
api.add_resource(Verify_Email, '/verify/<string:email_account>')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#LINEBOT
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if '@' in event.message.text:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(email_function(event.message.text,'line')))
            # line_bot_api.broadcast(TextMessage(text='【系統維護通知】\n 目前系統維護中，將暫時關閉送達通知功能，但您仍可以利用下方貨態查詢按鍵查詢。造成您的不便，敬請見諒'))
        if '上市' in event.message.text:
            print(event.message.text.replace('上市', '').split(' ')[1:])
            get_stock(event.message.text.replace('上市', '').split(' ')[1:], '上市')
            imgae_url=img_upload()
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=imgae_url,preview_image_url=imgae_url))
        if '上櫃' in event.message.text:
            get_stock(event.message.text.replace('上櫃', '').split(' ')[1:], '上櫃')
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=imgae_url,preview_image_url=imgae_url))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage('很抱歉，您的回覆超出了我的能力範圍'))
    return 200


if __name__=="__main__":
    app.run(debug=True,port=5500)