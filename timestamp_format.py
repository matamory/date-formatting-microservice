"""Timestamp formatting code (Robert)."""

from datetime import datetime


def format_timestamp(value):
    """Convert an ISO timestamp to MM/DD/YYYY hh:mm AM/PM.

    Accepts timezone offsets and a space instead of T.
    Invalid input raises ValueError.
    Timestamps use the supplied clock time; no timezone conversion is done.
    """
    if not isinstance(value, str):
        raise ValueError("Timestamp must be an ISO date and time string.")

    # Require a time as well as a date; fromisoformat also accepts dates alone.
    if len(value) < 16 or value[10] not in ("T", " "):
        raise ValueError("Timestamp must include a date and time.")

    # Parse the supplied offset without converting to another timezone.
    try:
        timestamp = datetime.fromisoformat(value)
    except ValueError:
        raise ValueError("Use a valid ISO timestamp, such as 2026-11-09T09:05:00-05:00.") from None

    return timestamp.strftime("%m/%d/%Y %I:%M %p")
