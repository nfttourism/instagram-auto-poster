# diagnostic_main.py — برای تشخیص سریع
import os, time
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "diagnostic server running", "env": dict(list(os.environ.items())[:10])}

if __name__ == "__main__":
    print("Starting diagnostic uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
