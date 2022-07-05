import os
import pickle
import json
import requests
import time
import random
import base64

TOKEN = 'TOKEN HERE'
SWAPINTERVAL = 300 #seconds, how long between image swaps. Discord limits to 2 per 10 mins/600
BASEURL = "https://discord.com/api"
IMGDIR = "WHERE YOUR IMAGES ARE STORED"
IMGEXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
ALREADYPUSHED = "./ALREADYPUSHED.bin"
IMAGES = [img for img in os.listdir(IMGDIR) if any(img.endswith(ext) for ext in IMGEXTENSIONS)]

while True:
    """_summary_
        Chooses random index from [IMAGES]
        If the program can't find an extension, chooses another
        If the program pulls a used image, pulls against
        returns the image, and the extension
    """
    def getRandomBanner(postedImages):
        image = random.choice(IMAGES)
        if image not in postedImages:
            _, imageExt = os.path.splitext(image)
            
            if not imageExt:
                return getRandomBanner(postedImages)
        
            return image, imageExt
        return getRandomBanner(postedImages)   
    
    
    """_summary_
        Opens pushed images, if there is a file error, clears list.
    """
    try:
        with open(ALREADYPUSHED, "rb") as image_file:
            postedImages = pickle.load(image_file)
            if not postedImages or len(IMAGES) - 1 == len(postedImages):
                postedImages = []
    except(EOFError, FileNotFoundError):
        postedImages = []
    
    """_summary_
        sets image, imageext as a random entry from [IMAGES]
        logs it as a posted image
    """
    image, imageExt = getRandomBanner(postedImages)
    postedImages.append(image)
    with open(ALREADYPUSHED, 'wb') as o:
        pickle.dump(postedImages, o)
    
    imageType = 'jpeg' if imageExt == '.jpg' else imageExt[1:] #converts jpg to jpeg
    
    with open(f"{IMGDIR}{image}", "rb") as image_file: #encodes image into base64 to upload to discord
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