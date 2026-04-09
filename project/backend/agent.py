RECOMMENDATION_MAP = {
    "High": "Continue Task",
    "Medium": "Take a Break",
    "Low": "Switch Task",
}

ENABLE_TREND_AWARE_RECOMMENDATIONS = True
ENABLE_PERSONALIZATION = True


def is_valid_focus_level(focus_level):
    return focus_level in RECOMMENDATION_MAP


def apply_focus_overrides(base_focus_level, context):
    time_spent = context["time_spent"]
    task_switch_count = context["task_switch_count"]
    idle_time = context["idle_time"]
    user_type = context.get("user_type")

    if ENABLE_PERSONALIZATION and user_type == "multitasker" and task_switch_count <= 6 and idle_time <= 5:
        if base_focus_level == "Low":
            return "Medium"

    if ENABLE_PERSONALIZATION and user_type == "deep_focus" and task_switch_count >= 4 and idle_time >= 8:
        if base_focus_level == "High":
            return "Medium"

    # Very short sessions do not provide enough evidence for strong conclusions.
    if time_spent < 10 and base_focus_level == "Low":
        return "Medium"

    # Strong low-focus signal requires both distraction and inactivity.
    if idle_time > 15 and task_switch_count > 5:
        return "Low"

    # Frequent switching with low idle can still reflect productive coordination.
    if task_switch_count > 5 and idle_time <= 5 and base_focus_level == "Low":
        return "Medium"

    # Moderate switching with low idle is usually not severe enough for a low-focus label.
    if 2 <= task_switch_count <= 4 and idle_time <= 5 and base_focus_level == "Low":
        return "Medium"

    return base_focus_level


def build_reason(focus_level, context):
    time_spent = context["time_spent"]
    task_switch_count = context["task_switch_count"]
    idle_time = context["idle_time"]
    reasons = []

    if time_spent < 10:
        reasons.append("The session is still very short, so the system is avoiding a strong conclusion.")

    if idle_time > 15:
        reasons.append("Higher idle time suggests a period of inactivity.")
    elif idle_time <= 5 and focus_level in ("High", "Medium"):
        reasons.append("Low idle time suggests steady engagement.")

    if task_switch_count > 5:
        if idle_time > 15:
            reasons.append("Frequent task switching combined with high inactivity suggests distraction.")
        else:
            reasons.append("Task switching is high, but low idle time suggests the switching may still be productive.")
    elif 2 <= task_switch_count <= 4:
        reasons.append("A moderate amount of task switching suggests partial context changes without severe distraction.")

    if time_spent > 90:
        reasons.append("Long time spent on the task may indicate mental fatigue.")
    elif 20 <= time_spent <= 90 and focus_level == "High":
        reasons.append("Time spent is in a healthy working range for sustained focus.")

    if not reasons:
        reasons.append("Behavioral signals are balanced and do not show strong signs of distraction.")

    return " ".join(reasons)


def get_switch_decision(context):
    base_focus_level = context.get("focus_level")
    focus_level = apply_focus_overrides(base_focus_level, context)
    recommendation = RECOMMENDATION_MAP[focus_level]
    trend = context.get("trend")

    if ENABLE_TREND_AWARE_RECOMMENDATIONS and trend == "Decreasing" and focus_level != "High":
        recommendation = "Take a Break and Reset"
    elif ENABLE_TREND_AWARE_RECOMMENDATIONS and trend == "Improving" and focus_level == "High":
        recommendation = "Continue Task with Momentum"

    return {
        "focus_level": focus_level,
        "recommendation": recommendation,
        "reason": build_reason(focus_level, context),
    }


# Future scope:
# - Real-world behavioral telemetry instead of synthetic-only inputs
# - User-specific model training for personalized ML thresholds
# - Calendar/task manager integrations for richer context
# - Multi-agent planning and execution roles
# - Reinforcement learning for continuous adaptation
# - Voice-based conversational interaction
# - Mobile app deployment
# - Cloud deployment with scalable shared memory
