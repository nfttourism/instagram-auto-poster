Instagram Auto Poster - Clean package for Render / Liara

Files included:
- main.py
- requirements.txt
- Procfile
- README.md

How to use:
1) Upload this zip to Render (Upload a .zip) or extract and push to GitHub then connect Render.
2) Set environment variables in your service settings:
   IG_USERNAME = your_instagram_username
   IG_PASSWORD = your_instagram_password
   IG_PROXY = (optional) socks5://user:pass@host:port
   PORT = 8000

3) Build command:
   pip install -r requirements.txt

4) Start command (Render uses Procfile, Liara use uvicorn main:app ...):
   python main.py
   or with uvicorn: uvicorn main:app --host 0.0.0.0 --port 8000

Endpoints:
GET /        -> health check
POST /post   -> JSON body: { "image_url": "...", "caption": "..." }

Notes:
- Do NOT hardcode credentials inside files; use environment variables.
- First login may trigger Instagram challenge; verify the account via mobile if needed.
