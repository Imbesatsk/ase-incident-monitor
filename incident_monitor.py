import time, requests
from datetime import datetime

LOG_FILE = "app.log"
WEBHOOK_URL = "PASTE_YOUR_WEBHOOK_URL_HERE"
TEST_API = "https://httpbin.org"

def send_alert(title, details):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "discord.com" in WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": f"🚨 **INCIDENT ALERT: {title}**\n**Time:** {ts}\n**Details:** {details}"})
    with open("incidents.log", "a") as inc:
        inc.write(f"[{ts}] TICKET CREATED | {title} | {details}\n")
    print(f"\n>>> ALERT TRIGGERED: {title} <<<\n")

def check_external_api():
    try:
        r = requests.get(TEST_API, timeout=5)
        if r.status_code != 200:
            send_alert("API Health Check Failed", f"Status Code: {r.status_code}")
    except Exception as e:
        send_alert("API Unreachable", str(e))

def monitor_logs():
    print("Support Monitor Active. Watching logs & API...")
    open(LOG_FILE, "a").close()
    with open(LOG_FILE, "r") as f:
        f.seek(0, 2)
        error_count = 0
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            if "[ERROR]" in line:
                error_count += 1
                print(f"Detected error ({error_count}/3): {line.strip()}")
            if error_count >= 3:
                send_alert("High Error Rate Detected", f"Latest error: {line.strip()}")
                check_external_api()
                error_count = 0

if __name__ == "__main__":
    monitor_logs()
