"""Timestamp formatting code (Robert)."""

from datetime import datetime


def format_timestamp(value):
    """Convert YYYY-MM-DDTHH:MM:SS to MM/DD/YYYY hh:mm AM/PM.

    Also accepts a space instead of T. Invalid input raises ValueError.
    Timestamps use the supplied clock time; no timezone conversion is done.
    """
    if not isinstance(value, str):
        raise ValueError("Timestamp must be a string in YYYY-MM-DDTHH:MM:SS format.")

    # Try the two supported input formats. strptime validates the date and time.
    for input_format in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            timestamp = datetime.strptime(value, input_format)
        except ValueError:
            continue

        # Round-tripping also requires zero-padded input fields.
        if timestamp.strftime(input_format) == value:
            return timestamp.strftime("%m/%d/%Y %I:%M %p")

    raise ValueError("Use a valid timestamp in YYYY-MM-DDTHH:MM:SS format.")
