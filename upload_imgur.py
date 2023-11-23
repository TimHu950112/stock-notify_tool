#上傳圖片
import pyimgur,os
from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.getenv("client_id")
PATH = "stock.jpg" #A Filepath to an image on your computer"

def img_upload():
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.type)
    return uploaded_image.link