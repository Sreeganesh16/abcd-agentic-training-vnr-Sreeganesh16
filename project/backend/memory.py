from collections import deque
from datetime import datetime


# Optional lightweight memory for repeated-pattern awareness.
_interaction_memory = deque(maxlen=10)


def remember_interaction(focus_level, recommendation):
    _interaction_memory.append(
        {
            "focus_level": focus_level,
            "recommendation": recommendation,
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }
    )


def get_recent_interactions():
    return list(_interaction_memory)
