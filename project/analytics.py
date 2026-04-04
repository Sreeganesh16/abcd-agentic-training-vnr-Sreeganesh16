from collections import deque


FOCUS_SCORE_MAP = {
    "Low": 30,
    "Medium": 60,
    "High": 90,
}

# In-memory analytics are sufficient for this single-user demo flow.
_recent_focus_levels = deque(maxlen=5)
_session_totals = {
    "total_time": 0.0,
    "total_idle": 0.0,
    "total_switches": 0,
    "focus_scores": [],
}


def update_history(focus_level):
    _recent_focus_levels.append(focus_level)


def analyze_trend():
    if len(_recent_focus_levels) < 2:
        return "Stable"

    scores = [FOCUS_SCORE_MAP[level] for level in _recent_focus_levels]
    if scores[-1] > scores[0]:
        return "Improving"
    if scores[-1] < scores[0]:
        return "Decreasing"
    return "Stable"


def update_session(context, focus_level):
    _session_totals["total_time"] = max(_session_totals["total_time"], float(context["time_spent"]))
    _session_totals["total_idle"] = max(_session_totals["total_idle"], float(context["idle_time"]))
    _session_totals["total_switches"] = max(
        _session_totals["total_switches"],
        int(context["task_switch_count"]),
    )
    _session_totals["focus_scores"].append(FOCUS_SCORE_MAP[focus_level])


def get_session_summary():
    average_focus_score = sum(_session_totals["focus_scores"]) / len(_session_totals["focus_scores"])

    return {
        "average_focus_score": round(average_focus_score, 2),
        "total_switches": _session_totals["total_switches"],
        "total_idle": round(_session_totals["total_idle"], 1),
    }
