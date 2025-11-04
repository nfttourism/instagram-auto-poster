import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from instagrapi import Client
import requests, tempfile

app = FastAPI()

IG_USER = os.getenv("IG_USERNAME")
IG_PASS = os.getenv("IG_PASSWORD")
IG_PROXY = os.getenv("IG_PROXY")  # optional, e.g., socks5://user:pass@host:port

class PostPayload(BaseModel):
    image_url: str
    caption: str

def get_client():
    if not IG_USER or not IG_PASS:
        raise RuntimeError("Instagram username/password not set in environment variables")
    cl = Client()
    if IG_PROXY:
        cl.set_proxy(IG_PROXY)
    cl.login(IG_USER, IG_PASS)
    return cl

@app.get("/")
def root():
    return {"message": "Instagram Auto Poster is running ✅"}

@app.post("/post")
def post_to_instagram(payload: PostPayload):
    try:
        cl = get_client()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {e}")

    try:
        r = requests.get(payload.image_url, timeout=30)
        if r.status_code != 200:
            raise HTTPException(status_code=400, detail="Image download failed")
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.write(r.content)
        tmp.flush()
        media = cl.photo_upload(tmp.name, payload.caption)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
    return {"status": "success", "media_id": getattr(media, 'pk', None)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
