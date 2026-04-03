from flask import jsonify


REQUIRED_INPUT_FIELDS = {
    "time_spent": (int, float),
    "task_switch_count": (int,),
    "idle_time": (int, float),
    "task_difficulty": (int,),
}


def success_response(data, status_code=200):
    return jsonify({"success": True, "data": data}), status_code


def error_response(message, status_code):
    return jsonify({"success": False, "error": message}), status_code


def bad_request(message="Bad request."):
    return error_response(message, 400)


def validate_prediction_input(payload):
    if payload is None:
        return "Request body must be valid JSON."

    for field, expected_types in REQUIRED_INPUT_FIELDS.items():
        if field not in payload:
            return f"The '{field}' field is required."

        if not isinstance(payload[field], expected_types):
            return f"The '{field}' field must be a valid number."

    if payload["task_switch_count"] < 0:
        return "The 'task_switch_count' field must be 0 or greater."

    if payload["time_spent"] < 0:
        return "The 'time_spent' field must be 0 or greater."

    if payload["idle_time"] < 0:
        return "The 'idle_time' field must be 0 or greater."

    if payload["task_difficulty"] not in (1, 2, 3):
        return "The 'task_difficulty' field must be 1, 2, or 3."

    return None
