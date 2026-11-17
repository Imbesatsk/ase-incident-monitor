import time, random
from datetime import datetime

LOG_FILE = "app.log"
events = [
    ("INFO", "200 OK - Payment processed successfully"),
    ("INFO", "200 OK - User authentication verified"),
    ("WARN", "429 Too Many Requests - Rate limit approaching"),
    ("ERROR", "500 Internal Server Error - Database connection timeout"),
    ("ERROR", "503 Service Unavailable - Payment gateway unreachable")
]

print("Starting mock production server... Press CTRL+C to stop.")
while True:
    level, message = random.choice(events)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)
    print(entry.strip())
    time.sleep(2)
