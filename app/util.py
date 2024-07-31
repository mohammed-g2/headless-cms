from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return a naive datetime object, a date without timezone"""
    return datetime.now(timezone.utc)
