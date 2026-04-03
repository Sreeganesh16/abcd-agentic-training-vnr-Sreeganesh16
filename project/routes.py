from flask import Blueprint, request

from agent import get_switch_decision
from ml_model import predict_focus
from utils import bad_request, success_response, validate_prediction_input


api = Blueprint("api", __name__)


@api.route("/health", methods=["GET"])
def health_check():
    return success_response(
        {
            "status": "ok",
            "service": "Context-Aware Task Switching Agent",
        }
    )


@api.route("/decision", methods=["POST"])
def decision():
    payload = request.get_json(silent=True)
    validation_error = validate_prediction_input(payload)

    if validation_error:
        return bad_request(validation_error)

    focus_level = predict_focus(payload)
    result = get_switch_decision({**payload, "focus_level": focus_level})
    return success_response(result)
