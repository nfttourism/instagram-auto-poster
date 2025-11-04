from fastapi import FastAPI
import uvicorn
import threading
import time

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Instagram Auto Poster is running ✅"}

def run_bot():
    print("🤖 Instagram Auto Poster is starting...")
    while True:
        print("Bot is alive and waiting for next post...")
        time.sleep(60)

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=10000)
