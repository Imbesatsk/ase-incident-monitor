import sqlite3
from datetime import datetime

DB_NAME = "transactions.db"

def setup_mock_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS ledger")
    cur.execute("""
        CREATE TABLE ledger (
            txn_id TEXT PRIMARY KEY,
            amount REAL,
            status TEXT,
            updated_at TEXT
        )
    """)
    records = [
        ("TXN1001", 4500.00, "SUCCESS", "2026-11-18 10:00:01"),
        ("TXN1002", 1200.00, "PENDING", "2026-11-18 10:02:15"),
        ("TXN1003", 8900.00, "FAILED",  "2026-11-18 10:05:40"),
    ]
    cur.executemany("INSERT INTO ledger VALUES (?, ?, ?, ?)", records)
    conn.commit()
    conn.close()

def reconcile():
    gateway_feed = [
        {"txn_id": "TXN1001", "amount": 4500.00, "status": "SUCCESS"},
        {"txn_id": "TXN1002", "amount": 1200.00, "status": "SUCCESS"},
        {"txn_id": "TXN1003", "amount": 8900.00, "status": "FAILED"},
        {"txn_id": "TXN1004", "amount": 2500.00, "status": "SUCCESS"},
    ]

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    discrepancies = []
    for item in gateway_feed:
        cur.execute("SELECT amount, status FROM ledger WHERE txn_id = ?", (item["txn_id"],))
        row = cur.fetchone()
        if not row:
            discrepancies.append(f"[CRITICAL] {item['txn_id']}: Present in Gateway ({item['status']}), MISSING in DB.")
        elif row[1] != item["status"]:
            discrepancies.append(f"[WARN] {item['txn_id']}: Status mismatch -> DB={row[1]} | Gateway={item['status']}")

    conn.close()

    report_name = f"reconcile_report_{datetime.now().strftime('%Y%m%d')}.log"
    with open(report_name, "w") as f:
        f.write("=== EOD TRANSACTION RECONCILIATION REPORT ===\n")
        for d in discrepancies:
            f.write(d + "\n")

    print(f"Reconciliation complete. {len(discrepancies)} issues logged to {report_name}.")

if __name__ == "__main__":
    setup_mock_db()
    reconcile()
