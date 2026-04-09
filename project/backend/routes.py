from flask import Blueprint, request

from .analytics import analyze_trend, get_session_summary, update_history, update_session
from .agent import get_switch_decision
from .llm_agent import generate_agent_response
from .memory import get_recent_interactions, remember_interaction
from .tools import analyze_focus
from .utils import bad_request, success_response, validate_prediction_input

ENABLE_MEMORY = True
ENABLE_CONFIDENCE_NOTE = True
ENABLE_SESSION_INSIGHT = True


api = Blueprint("api", __name__)


def generate_session_insight(session_data, trend):
    average_focus_score = session_data["average_focus_score"]
    total_switches = session_data["total_switches"]
    total_idle = session_data["total_idle"]

    if trend == "Decreasing" and total_switches >= 4:
        return "Focus has been declining with repeated switching, so a short reset may help."
    if trend == "Improving" and average_focus_score >= 60:
        return "Focus is improving and the session looks more stable."
    if total_idle >= 15:
        return "Extended idle time suggests energy may be dropping during the session."
    return "Consistent focus has been maintained without major disruption."


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
    update_history(focus_analysis["focus_level"])
    trend = analyze_trend()
    result = get_switch_decision({**payload, "focus_level": focus_analysis["focus_level"], "trend": trend})
    result["confidence"] = focus_analysis["confidence"]
    result["trend"] = trend
    update_session(payload, result["focus_level"])
    session_summary = get_session_summary()
    result["session_summary"] = session_summary

    if ENABLE_CONFIDENCE_NOTE and result["confidence"] < 0.6:
        result["confidence_note"] = "Prediction may be uncertain due to limited or inconsistent data."

    if ENABLE_SESSION_INSIGHT:
        result["session_insight"] = generate_session_insight(session_summary, trend)

    if ENABLE_MEMORY:
        remember_interaction(result["focus_level"], result["recommendation"])
        result["recent_patterns"] = get_recent_interactions()

    result["llm_suggestion"] = generate_agent_response({**payload, **result})

    return success_response(result)


# Future scope:
# - Shared persistent memory across devices and sessions
# - External productivity tool integrations
# - Planner/executor multi-agent orchestration
# - Cloud-native scaling with streaming updates
