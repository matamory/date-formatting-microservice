"""Date Formatting microservice skeleton (Robert)."""

from flask import Flask, jsonify, request

from date_format import format_date, format_dates
from timestamp_format import format_timestamp

app = Flask(__name__)


@app.post("/format")
def format_value():
    # All requests must contain a JSON object with a type and value.
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(success=False, error="Send a JSON object."), 400

    if data.get("type") not in ("date", "dates", "timestamp"):
        return jsonify(success=False, error="Type must be date, dates, or timestamp.",
                       fields=["type"]), 400

    if "value" not in data:
        return jsonify(success=False, error="Value is required.", fields=["value"]), 400

    try:
        # Each formatter handles its own input validation.
        if data["type"] == "date":
            result = format_date(data["value"])
        elif data["type"] == "dates":
            result = format_dates(data["value"])
        else:
            result = format_timestamp(data["value"])
    except ValueError as error:
        return jsonify(success=False, error=str(error), fields=["value"]), 400

    return jsonify(success=True, formatted=result), 200


if __name__ == "__main__":
    # Run this service separately from the other microservices.
    app.run(host="127.0.0.1", port=5001)
