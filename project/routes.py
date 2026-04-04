from flask import Blueprint, request

from agent import get_switch_decision
from llm_agent import generate_agent_response
from tools import analyze_focus
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

    focus_analysis = analyze_focus(payload)
    result = get_switch_decision({**payload, "focus_level": focus_analysis["focus_level"]})
    result["confidence"] = focus_analysis["confidence"]
    result["llm_suggestion"] = generate_agent_response({**payload, **result})

    return success_response(result)
