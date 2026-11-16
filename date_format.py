from datetime import datetime

INPUT_FORMAT = "%Y-%m-%d"       #2026-11-16
OUTPUT_FORMAT = "%m/%d/%Y"      #11/16/2026


def format_date(value):
    """Return MM/DD/YYYY, or raise ValueError for invalid input."""
    if not isinstance(value, str):
        raise ValueError("Date value must be string")

    try:
         parsed = datetime.strptime(value, INPUT_FORMAT) # turn text into datetime object
    except ValueError:
         raise ValueError(f"{value} is not a valid date. Must use YYYY-MM-DD formatting")

    return parsed.strftime(OUTPUT_FORMAT) # turn datetime object into text

def format_dates(values):
    """Return formatted dates in the same order, or raise ValueError."""
    if not isinstance(values, list):
        raise ValueError("Date values must be in a list")
    
    dates_list = []
    for value in values:
         dates_list.append(format_date(value))
    return dates_list