# AI Firewall

## Overview

**AI Firewall** is a smart, AI-driven security system designed to detect anomalies and potential threats in real-time. It leverages **machine learning models** to monitor network traffic, system logs, and user activity, providing proactive defense against attacks such as:

- Brute-force login attempts
- Malicious API requests
- Abnormal system behavior
- Suspicious network traffic patterns

This tool combines predictive models with a web-based dashboard for **real-time monitoring, logging, and response actions**.

---

## Features

- **Real-Time Monitoring:** Logs incoming events and predicts anomalies instantly.
- **Machine Learning Models:**  
  - **RandomForest:** Classifies normal vs suspicious events.  
  - **IsolationForest:** Detects anomalies in feature patterns.
- **Dashboard:** Visualizes logs, feature data, and predictions in real-time.
- **Proactive Security Actions:** Alerts admins, blocks malicious IPs, throttles suspicious requests.
- **REST API Endpoint:** `/sample_data` for submitting features to get predictions.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ne4tron/AI-Firewall.git
   cd AI-Firewall
Create a Python virtual environment and activate it:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install required dependencies:

bash
Copy code
pip install -r requirements.txt
Ensure you have SSL certificates:

certs/cert.pem

certs/key.pem

Usage
Start the dashboard with:

bash
Copy code
uvicorn dashboard.app:app --reload --host 0.0.0.0 --port 8443 \
    --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem
Access the Dashboard
Open a browser and navigate to:
https://127.0.0.1:8443 or https://<your-server-ip>:8443

The dashboard displays logs, features, and predictions in real-time.

Sample POST Request to /sample_data
bash
Copy code
curl -k -X POST https://127.0.0.1:8443/sample_data \
-H "Content-Type: application/json" \
-d '{"feature1":0.45,"feature2":0.07,"feature3":0.53,"feature4":0.85,"feature5":0.05}'
Sample response:

json
Copy code
{
  "feature1": 0.45,
  "feature2": 0.07,
  "feature3": 0.53,
  "feature4": 0.85,
  "feature5": 0.05,
  "RandomForest_prediction": 0,
  "IsolationForest_prediction": "Anomaly"
}
Real-World Use Cases
Brute-Force Attack Prevention

Detect multiple failed logins from one IP.

Block IP or trigger CAPTCHA automatically.

Malicious API Requests

Identify abnormal payloads or frequency.

Alert admins and block requests before server compromise.

System Behavior Monitoring

Monitor CPU, memory, or API patterns.

Detect unusual spikes or abnormal activities in real-time.

Benefits
Proactive defense instead of reactive blocking

Real-time visibility into system and network activity

AI-driven anomaly detection reduces false positives

Easy integration into existing networks or cloud setups

Contributing
Fork the repository

Create a feature branch (git checkout -b feature-name)

Commit your changes (git commit -m "Description")

Push to the branch (git push origin feature-name)

Open a Pull Request

License
This project is licensed under the MIT License.

pgsql
Copy code

---

If you want, I can also **write the git commands to commit this in one branch and push it to GitHub** without requiring a password (using a Personal Access Token), so your updates go live immediately.  

Do you want me to do that next?





