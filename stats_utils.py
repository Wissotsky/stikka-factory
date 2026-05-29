"""Statistics tracking utilities for print jobs."""

import sqlite3
import logging
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger("sticker_factory.stats_utils")

DB_FILE = "print_stats.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS print_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            printer_name TEXT NOT NULL,
            printer_model TEXT DEFAULT ''
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON print_stats(timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_printer ON print_stats(printer_name)")
    conn.commit()
    conn.close()


init_db()


def record_print(printer_name, printer_model=None):
    """Record a successful print job."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO print_stats (timestamp, printer_name, printer_model) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), printer_name, printer_model or ""),
        )
        conn.commit()
        logger.debug(f"Recorded print for printer: {printer_name}")
    except Exception as e:
        logger.error(f"Error recording print: {e}")
    finally:
        conn.close()


def get_stats_by_date(printer_name=None):
    """
    Get statistics grouped by date and printer.

    Returns:
        dict: {date: {printer_name: count}}
    """
    conn = get_connection()
    try:
        if printer_name:
            rows = conn.execute("""
                SELECT DATE(timestamp) as date, printer_name, COUNT(*) as count
                FROM print_stats WHERE printer_name = ?
                GROUP BY date, printer_name ORDER BY date
            """, (printer_name,)).fetchall()
        else:
            rows = conn.execute("""
                SELECT DATE(timestamp) as date, printer_name, COUNT(*) as count
                FROM print_stats
                GROUP BY date, printer_name ORDER BY date
            """).fetchall()

        result = defaultdict(dict)
        for row in rows:
            result[row["date"]][row["printer_name"]] = row["count"]
        return dict(result)
    finally:
        conn.close()


def get_total_stats():
    """Get total statistics per printer."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT printer_name, COUNT(*) as count FROM print_stats GROUP BY printer_name ORDER BY count DESC"
        ).fetchall()
        return {row["printer_name"]: row["count"] for row in rows}
    finally:
        conn.close()


def get_stats_summary():
    """Get summary statistics."""
    conn = get_connection()
    try:
        total = conn.execute("SELECT COUNT(*) FROM print_stats").fetchone()[0]

        printers = {
            row["printer_name"]: row["count"]
            for row in conn.execute(
                "SELECT printer_name, COUNT(*) as count FROM print_stats GROUP BY printer_name ORDER BY count DESC"
            ).fetchall()
        }

        first = conn.execute(
            "SELECT timestamp FROM print_stats ORDER BY timestamp ASC LIMIT 1"
        ).fetchone()
        last = conn.execute(
            "SELECT timestamp FROM print_stats ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()

        return {
            "total_prints": total,
            "printers": printers,
            "first_print": first["timestamp"] if first else None,
            "last_print": last["timestamp"] if last else None,
        }
    finally:
        conn.close()


def get_prints_today():
    """Get count of prints made today (resets at midnight)."""
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT COUNT(*) FROM print_stats WHERE DATE(timestamp) = DATE('now')"
        ).fetchone()[0]
    finally:
        conn.close()


def get_prints_total():
    """Get total count of all prints."""
    conn = get_connection()
    try:
        return conn.execute("SELECT COUNT(*) FROM print_stats").fetchone()[0]
    finally:
        conn.close()
