import os
import pickle
import json
import requests
import time
import random
import base64

TOKEN = 'MjQzMTU5MTk3Mzk3NjgwMTI5.GQPstm.BNbmm8z3KYOwzhjGUu7Ui7F1JfFoiBnrb6-TuU'
SWAPINTERVAL = 600
BASEURL = "https://discord.com/api"
IMGDIR = "D:/Users/brian/Desktop/pfps/banners/"
IMGEXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
ALREADYPUSHED = "D:/Users/brian/Desktop/pfps/ALREADYPUSHED.bin"
IMAGES = [img for img in os.listdir(IMGDIR) if any(img.endswith(ext) for ext in IMGEXTENSIONS)]

while True:
    def getRandomBanner(postedImages):
        print(IMAGES)
        image = random.choice(IMAGES)
        if image not in postedImages:
            _, imageExt = os.path.splitext(image)
            
            if not imageExt:
                return getRandomBanner(postedImages)
        
            return image, imageExt
        return getRandomBanner(postedImages)   

    try:
        with open(ALREADYPUSHED, "rb") as image_file:
            postedImages = pickle.load(image_file)
            if not postedImages or len(IMAGES) - 1 == len(postedImages):
                postedImages = []
    except(EOFError, FileNotFoundError):
        postedImages = []
    
    image, imageExt = getRandomBanner(postedImages)
    postedImages.append(image)
    with open(ALREADYPUSHED, 'wb') as o:
        pickle.dump(postedImages, o)
    
    imageType = 'jpeg' if imageExt == '.jpg' else imageExt[1:]
    
    with open(f"{IMGDIR}{image}", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        
    payload = {
        "banner": f"data:image/{imageType};base64,{encoded_image.decode()}"
    }
    
    headers = {
        'Accept': '*/*',
        'Authorization': f'{TOKEN}',
        'Content-Type': 'application/json'
    }
        
    r = requests.patch(f'{BASEURL}/users/@me', data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
        print ('Changed! | ', os.path.basename(image))
    else:
        print ('Error', r.status_code, os.path.basename(image))
    time.sleep(SWAPINTERVAL)