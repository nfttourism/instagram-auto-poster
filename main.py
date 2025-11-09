import os
from fastapi import FastAPI, HTTPException, UploadFile, Form
from pydantic import BaseModel
from instagrapi import Client
import uvicorn
import tempfile

app = FastAPI()

# Login once at startup
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
cl = None

@app.on_event("startup")
def login_instagram():
    global cl
    try:
        cl = Client()
        cl.login(USERNAME, PASSWORD)
        print("✅ Instagram login successful.")
    except Exception as e:
        print(f"❌ Instagram login failed: {e}")

@app.get("/")
def home():
    return {"message": "Bot is alive and waiting for next post..."}

class PostData(BaseModel):
    caption: str
    image_url: str

@app.post("/post")
async def post_to_instagram(data: PostData):
    global cl
    if not cl:
        raise HTTPException(status_code=503, detail="Instagram client not logged in")

    try:
        # Download image to temporary file
        import requests
        img_data = requests.get(data.image_url).content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(img_data)
            tmp_path = tmp.name

        # Upload to Instagram
        cl.photo_upload(tmp_path, data.caption)
        return {"status": "success", "message": "Post uploaded to Instagram!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
