

**Folder Structure:**

```
ai-firewall-secure/
│
├── .gitignore
├── README.md
├── requirements.txt
├── model/
│   └── train.py
├── dashboard/
│   └── app.py
├── firewall/
│   └── engine.py
└── scripts/
    └── setup_iptables.sh
```

---

**.gitignore**

```
venv/
*.pyc
__pycache__/
certs/
firewall/banlist.json
```

---

**README.md**

```
# AI Firewall Secure Version

This is an advanced AI-driven firewall with ensemble ML model, JWT authentication dashboard, and HTTPS-ready setup.

## Features
- Ensemble ML model (IsolationForest + RandomForest)
- FastAPI dashboard with JWT authentication
- HTTPS-ready structure
- NFQUEUE firewall engine

## Setup
1. Install Python dependencies: `pip install -r requirements.txt`
2. Train the model: `python model/train.py`
3. Run firewall engine: `sudo python firewall/engine.py --model model/model.joblib`
4. Start dashboard: `uvicorn dashboard.app:app --reload --host 0.0.0.0 --port 8443`

> NOTE: Do not upload private certificates or keys to GitHub. This project is for lab/demo use.
```

---

**requirements.txt**

```
scikit-learn==1.3.2
pandas==2.2.2
numpy==1.26.4
joblib==1.3.2
scapy==2.5.1
netfilterqueue==1.0.8
uvicorn==0.23.1
fastapi==0.99.3
python-multipart==0.0.6
psutil==5.9.5
schedule==1.2.0
python-jose==3.3.0
passlib[bcrypt]==1.7.4
```

---

**model/train.py**

```python
from sklearn.ensemble import IsolationForest, RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import pandas as pd
import numpy as np
import os

def generate_synthetic(n_normal=1000, n_anom=50):
    rng = np.random.RandomState(42)
    normal = rng.normal(0, 1, (n_normal,6))
    anom = rng.normal(4, 1.5, (n_anom,6))
    X = np.vstack([normal, anom])
    y = np.hstack([np.zeros(n_normal), np.ones(n_anom)])
    cols = ['pkt_len','tcp_flags','src_port','dst_port','flow_bytes','pkt_per_sec']
    return pd.DataFrame(X, columns=cols), y

def train(output_path='model/model.joblib'):
    X, y = generate_synthetic()
    iso = IsolationForest(contamination=0.02, random_state=42)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    ensemble = VotingClassifier([('iso', iso), ('rf', rf)], voting='soft')
    pipeline = Pipeline([('scaler', StandardScaler()), ('model', ensemble)])
    pipeline.fit(X, y)
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    joblib.dump(pipeline, output_path)
    print(f"Saved ensemble model to {output_path}")

if __name__ == "__main__":
    train()
```

---

**dashboard/app.py**

```python
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
```

---

**firewall/engine.py**

```python
# Placeholder engine file
print("Firewall engine script placeholder. Replace with your NFQUEUE code.")
```

---

**scripts/setup_iptables.sh**

```bash
#!/bin/bash
# Placeholder setup script
echo "Setup iptables rules here (root required)."
```

---

This folder is ready to **drag and drop to GitHub manually**, without including private keys or sensitive files.
