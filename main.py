import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from instagrapi import Client
import requests
import tempfile
from pathlib import Path
import uvicorn

app = FastAPI()

USERNAME = os.getenv("IG_USERNAME", "visabaz")
PASSWORD = os.getenv("IG_PASSWORD", "hubir7211")
PROXY = os.getenv("IG_PROXY")

SESSION_DIR = Path("/tmp")
SESSION_DIR.mkdir(parents=True, exist_ok=True)
SESSION_FILE = SESSION_DIR / "session.json"


def get_client():
    cl = Client()
    if PROXY:
        cl.set_proxy(PROXY)
    if SESSION_FILE.exists():
        cl.load_settings(str(SESSION_FILE))
    cl.login(USERNAME, PASSWORD)
    try:
        cl.dump_settings(str(SESSION_FILE))
    except Exception:
        pass
    return cl


class PostData(BaseModel):
    media_url: str
    caption: str


@app.get("/")
def root():
    return {"message": "✅ Instagram Auto Poster is running!", "username": USERNAME}


@app.post("/post")
def post_to_instagram(data: PostData):
    cl = get_client()

    response = requests.get(data.media_url, timeout=30)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error downloading media file")

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    tmp_file.write(response.content)
    tmp_file.flush()

    try:
        media = cl.photo_upload(tmp_file.name, data.caption)
        return {"status": "ok", "media_id": media.pk}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
