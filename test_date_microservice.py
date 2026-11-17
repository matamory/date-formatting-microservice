"""Start app.py in another terminal before running this test program."""

import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

URL = "http://127.0.0.1:5001/format"


def send(data, expected_status, expected_value=None):
    # Show what we are sending to the service.
    print(f"\nREQUEST:\n     POST {URL}\n     {data}\n")

    # Send an HTTP request instead of calling the service's functions.
    request = Request(URL, data=json.dumps(data).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    try:
        response = urlopen(request, timeout=5)
    except HTTPError as error:
        # Read error responses too, such as an invalid date.
        response = error

    # Read the response and turn its JSON into a Python dictionary.
    with response:
        status = response.code
        result = json.loads(response.read().decode("utf-8"))

    print(f"RESPONSE:\n     Status Code: {status}\n     {result}\n")
    # Check that the service returned the expected data.
    assert status == expected_status, "Unexpected HTTP status"
    if expected_status == 200:
        assert result["success"] is True
        assert result["formatted"] == expected_value, "Unexpected formatted value"
        print("Formatted data:", result["formatted"])
    else:
        assert result["success"] is False
        assert isinstance(result["error"], str)
    print("PASS\n")


if __name__ == "__main__":
    # ========================== USER STORY 1 ========================== Format a Date
    print("================= USER STORY 1: Format a Date =================\n")

    print("-----------------------------------------------------------")
    print("Functional Requirement 1 - Successful date formatting:\n\n"
          "Given a Fitness Tracker workout has a date of 2026-11-09,\n"
          "when the application requests that the date be formatted,\n"
          "then the microservice returns 11/09/2026.\n")
    print("Expected: 200, formatted = 11/09/2026")
    send({"type": "date", "value": "2026-11-09"}, 200, "11/09/2026")

    print("-----------------------------------------------------------")
    print("Functional Requirement 2 - Invalid date:\n\n"
          "Given an invalid date such as 2026-13-40,\n"
          "when formatting is requested, then the service returns an error\n"
          "indicating that the date is invalid.\n")
    print("Expected: 400, success = False and an error message")
    send({"type": "date", "value": "2026-13-40"}, 400)

    # ========================== USER STORY 2 ========================== Format a Timestamp
    print("================= USER STORY 2: Format a Timestamp =================\n")

    print("-----------------------------------------------------------")
    print("Functional Requirement 1 - Successful timestamp formatting:\n\n"
          "Given a Medical Journal entry has a timestamp of\n"
          "2026-11-09T09:05:00-05:00, when formatting is requested,\n"
          "then the service returns 11/09/2026 09:05 AM.\n")
    print("Expected: 200, formatted = 11/09/2026 09:05 AM")
    send({"type": "timestamp", "value": "2026-11-09T09:05:00-05:00"},
         200, "11/09/2026 09:05 AM")

    print("-----------------------------------------------------------")
    print("Functional Requirement 2 - Invalid timestamp:\n\n"
          "Given an invalid timestamp such as 2026-11-09T25:00:00,\n"
          "when formatting is requested, then the service returns an error\n"
          "indicating that the timestamp is invalid.\n")
    print("Expected: 400, success = False and an error message")
    send({"type": "timestamp", "value": "2026-11-09T25:00:00"}, 400)

    # ========================== USER STORY 3 ========================== Format Multiple Dates
    print("================= USER STORY 3: Format Multiple Dates =================\n")

    print("-----------------------------------------------------------")
    print("Functional Requirement 1 - Successfully format multiple dates:\n\n"
          "Given workout dates of 2026-11-01, 2026-11-03, and 2026-11-09,\n"
          "when the application submits all three dates for formatting,\n"
          "then the service returns 11/01/2026, 11/03/2026, and 11/09/2026\n"
          "in the same order.\n")
    print("Expected: 200, formatted = ['11/01/2026', '11/03/2026', '11/09/2026']")
    send({"type": "dates", "value": ["2026-11-01", "2026-11-03", "2026-11-09"]},
         200, ["11/01/2026", "11/03/2026", "11/09/2026"])

    print("-----------------------------------------------------------")
    print("Functional Requirement 2 - Empty date list:\n\n"
          "Given an empty list of dates, when formatting is requested,\n"
          "then the service returns an empty list without an error.\n")
    print("Expected: 200, formatted = []")
    send({"type": "dates", "value": []}, 200, [])

    print("All six functional requirement checks passed.")
