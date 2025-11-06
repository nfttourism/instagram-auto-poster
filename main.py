from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from instagrapi import Client
import requests, tempfile, os

app = FastAPI(title="Instagram Auto Poster")

USERNAME = os.getenv("IG_USERNAME", "visabaz")
PASSWORD = os.getenv("IG_PASSWORD", "hubir7211")

@app.get("/")
def home():
    return {"message": "✅ Instagram Auto Poster is running and ready!", "username": USERNAME}

class MediaPost(BaseModel):
    media_url: str
    caption: str

@app.post("/post")
def post_to_instagram(data: MediaPost):
    try:
        # دانلود عکس یا ویدئو
        r = requests.get(data.media_url, timeout=20)
        if r.status_code != 200:
            raise HTTPException(status_code=400, detail="Cannot download media")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.write(r.content)
        tmp.close()

        # ورود به حساب اینستاگرام
        cl = Client()
        cl.login(USERNAME, PASSWORD)

        # پست کردن
        media = cl.photo_upload(tmp.name, data.caption)
        return {"status": "✅ Uploaded successfully", "media_id": media.pk}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
