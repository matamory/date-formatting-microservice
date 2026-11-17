# Date Formatting Microservice

## Description

The Date Formatting Microservice converts dates and timestamps into a consistent,
readable format.

It uses a REST API and runs on port 5001.

The microservice supports:

- `date` to format a single date
- `timestamp` to format a date and time
- `dates` to format a list of dates in the same order

## How to Request Data from the Microservice

Other programs request data by sending an HTTP POST request to:

```text
http://127.0.0.1:5001/format
```

Send a JSON body with `Content-Type: application/json` and these required fields:

- `type`: `date`, `timestamp`, or `dates`
- `value`: the date, timestamp, or list of dates to format

Dates use `YYYY-MM-DD`. Timestamps include a date and time and may include a
timezone offset. The service keeps the supplied clock time without converting
timezones.

## Example Call for Requesting Data

Run these examples in order while the service is running. They use Python's
standard library, like the test program.

```python
import json
from urllib.request import Request, urlopen

url = "http://127.0.0.1:5001/format"


def send(data):
    # Send JSON over HTTP.
    request = Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    return urlopen(request, timeout=5)
```

### Format a Date

```python
date_response = send({
    "type": "date",
    "value": "2026-11-09"
})
```

### Format a Timestamp

```python
time_response = send({
    "type": "timestamp",
    "value": "2026-11-09T09:05:00-05:00"
})
```

### Format Multiple Dates

```python
list_response = send({
    "type": "dates",
    "value": ["2026-11-01", "2026-11-03", "2026-11-09"]
})
```

## How to Receive Data from the Microservice

The Date Formatting Microservice returns data in JSON format.

Successful requests return HTTP 200 with `success: true` and a `formatted` value.
Dates are returned as `MM/DD/YYYY`. Timestamps include a 12-hour time with AM or PM.
Multiple dates are returned as a list in their original order. An empty list
returns an empty list.

Invalid input returns HTTP 400 with `success: false` and an `error` message.
Field validation errors also include a `fields` list.

## Example Call for Receiving Data

Continue after the request examples above. Read the response body and convert
its JSON into a Python dictionary, then read the `formatted` value.

```python
def receive(response):
    # Read the JSON response and close the connection.
    with response:
        return json.loads(response.read().decode("utf-8"))
```

### Display the Formatted Date

```python
print(receive(date_response)["formatted"])
```

Output:

```text
11/09/2026
```

### Display the Formatted Timestamp

```python
print(receive(time_response)["formatted"])
```

Output:

```text
11/09/2026 09:05 AM
```

### Display the Formatted Date List

```python
print(receive(list_response)["formatted"])
```

Output:

```text
['11/01/2026', '11/03/2026', '11/09/2026']
```

## UML Sequence Diagram Showing How to Request and Receive Data

This diagram shows a single-date request and response. The test program sends
an HTTP request to `app.py`, which calls `format_date()` in `date_format.py` and
returns the formatted date as JSON.

![Date Formatting UML sequence diagram](UML%20Sequence%20diagram%20date%20formatting.png)
