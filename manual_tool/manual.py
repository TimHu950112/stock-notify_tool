from dotenv import load_dotenv
import pymongo,certifi,os,sys 
sys.path.append("..") 
from send_email import send_email

load_dotenv()
client=pymongo.MongoClient("mongodb+srv://"+os.getenv("mongodb")+".rpebx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())

db=client.stockify
users=db.users

def insert_new(email_account):
    users.insert_one({"email":email_account,"verified":False})

def verify(email_account):
    users.update_one({"email":email_account},{"$set":{"verified":True}})

def delete(email_account):
    users.delete_one({"email":email_account})

def send_verify_code(email_account):
    send_email(email_account,os.getenv("web_link")+"/verify/"+email_account)

if __name__=="__main__":
    # insert_new("")
    # verify("")
    # delete("")
    # print(list(users.find({}))[0]['verified'])
    pass
