from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta
import json, os, subprocess


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
BAN_FILE = 'firewall/banlist.json'


app = FastAPI(title="AI Firewall Dashboard")


def create_access_token(data: dict):
to_encode = data.copy()
expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
to_encode.update({"exp": expire})
return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
if form_data.username != "admin" or form_data.password != "password":
raise HTTPException(status_code=400, detail="Incorrect credentials")
access_token = create_access_token({"sub": form_data.username})
return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
try:
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
username = payload.get("sub")
if username != "admin":
raise HTTPException(status_code=401, detail="Invalid user")
return username
except JWTError:
raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/", response_class=HTMLResponse)
def index(user: str = Depends(get_current_user)):
html = "<html><body><h1>AI Firewall Dashboard</h1>"
html += "<p>Visit /api/banlist for JSON banlist</p></body></html>"
return HTMLResponse(content=html)


@app.get("/api/banlist")
def banlist(user: str = Depends(get_current_user)):
if not os.path.exists(BAN_FILE):
return {}
with open(BAN_FILE, 'r') as f:
data = json.load(f)
now = datetime.utcnow().timestamp()
active = {ip: info for ip, info in data.items() if info.get('expires',0) > now}
return active


@app.post("/api/unblock/{ip}")
def unblock(ip: str, user: str = Depends(get_current_user)):
if not os.path.exists(BAN_FILE):
raise HTTPException(status_code=404, detail="Banlist not found")
with open(BAN_FILE, 'r') as f:
data = json.load(f)
if ip not in data:
raise HTTPException(status_code=404, detail="IP not in banlist")
subprocess.run(['iptables','-D','INPUT','-s',ip,'-j','DROP'], check=False)
del data[ip]
with open(BAN_FILE, 'w') as f:
json.dump(data, f, indent=2)
return {"status":"unblocked","ip":ip}
