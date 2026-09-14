from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "shipments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS shipments (
    tracking_id TEXT PRIMARY KEY,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    status TEXT NOT NULL,
    eta TEXT NOT NULL,
    delay_hours REAL NOT NULL,
    carrier TEXT NOT NULL
)
"""


def connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def seed_shipments(count: int = 300) -> None:
    conn = connection()
    existing = conn.execute("SELECT COUNT(*) FROM shipments").fetchone()[0]
    if existing:
        conn.close()
        return
    rows = []
    cities = [("Chennai", "Bengaluru"), ("Hyderabad", "Pune"), ("Mumbai", "Delhi"), ("Kolkata", "Bengaluru")]
    for i in range(1, count + 1):
        origin, destination = cities[i % len(cities)]
        delay = round((i % 8) * 0.7, 1)
        status = "Delayed" if delay >= 3 else ("In Transit" if i % 5 else "Out for Delivery")
        rows.append((f"RT-{i:05d}", origin, destination, status, f"2026-09-{(i % 27) + 1:02d}", delay, f"Carrier-{(i % 7) + 1}"))
    conn.executemany("INSERT INTO shipments VALUES (?,?,?,?,?,?,?)", rows)
    conn.commit()
    conn.close()


def get_shipment(tracking_id: str):
    conn = connection()
    row = conn.execute("SELECT * FROM shipments WHERE tracking_id = ?", (tracking_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def search_shipments(query: str, limit: int = 5):
    conn = connection()
    rows = conn.execute("SELECT * FROM shipments WHERE tracking_id LIKE ? OR origin LIKE ? OR destination LIKE ? LIMIT ?", (f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
    conn.close()
    return [dict(row) for row in rows]
