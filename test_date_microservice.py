"""Start app.py in another terminal before running this test program."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URL = "http://127.0.0.1:5001/format"


def test_request(name, data, expected_status, expected_value=None):
    # Show what we are sending to the service.
    print("\n" + name)
    print("Sending POST to", URL)
    print("Request JSON:", json.dumps(data))

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

    print("Received HTTP status:", status)
    print("Response JSON:", json.dumps(result))
    # Check that the service returned the expected data.
    assert status == expected_status, "Unexpected HTTP status"
    if expected_status == 200:
        assert result["success"] is True
        assert result["formatted"] == expected_value, "Unexpected formatted value"
        print("Formatted data:", result["formatted"])
    else:
        assert result["success"] is False
        assert isinstance(result["error"], str)
    print("PASS")


if __name__ == "__main__":
    # Try each formatting option and one invalid date.
    try:
        test_request("Single date", {"type": "date", "value": "2026-11-09"},
                     200, "11/09/2026")
        test_request("Timestamp", {"type": "timestamp", "value": "2026-11-09T09:05:00-05:00"},
                     200, "11/09/2026 09:05 AM")
        test_request("Multiple dates", {"type": "dates", "value": ["2026-11-01", "2026-11-09"]},
                     200, ["11/01/2026", "11/09/2026"])
        test_request("Invalid date", {"type": "date", "value": "2026-13-40"}, 400)
    except URLError as error:
        raise SystemExit("Could not reach the service. Start app.py in another terminal. " + str(error))

    print("\nAll four HTTP demonstration checks passed.")
