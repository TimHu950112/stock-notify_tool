from dotenv import load_dotenv
from send_email import send_email
import pymongo,certifi,os


load_dotenv()
client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())

db=client.stockify
users=db.users

def email_function(email_account,mode):
    result=list(users.find({"email":email_account}))
    if len(result)!=0:
        if result[0]["verified"]==True:
            return '您已經驗證過了'
        if mode=='verify':
            users.update_one({"email":email_account},{"$set":{"verified":True}})
            return '驗證成功'
    users.insert_one({"email":email_account,"verified":False})    
    send_email(email_account,os.getenv("weblink")+"/"+email_account)
    return '已發送驗證訊息至您的信箱'
