from agent import RECOMMENDATION_MAP, build_reason
from ml_model import predict_focus_with_confidence


def analyze_focus(context):
    # Centralize ML access so routes and the LLM layer reuse the same prediction flow.
    focus_level, confidence = predict_focus_with_confidence(context)
    return {
        "focus_level": focus_level,
        "confidence": confidence,
    }


def get_recommendation(focus_level):
    return RECOMMENDATION_MAP.get(focus_level, "Take a Break")


def explain_behavior(context):
    return build_reason(context["focus_level"], context)
