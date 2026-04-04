import json
import os

from tools import analyze_focus, explain_behavior, get_recommendation

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


FALLBACK_MESSAGE = "Suggestion unavailable"


def _build_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "analyze_focus",
                "description": "Predict the current focus level from the user's behavioral context.",
                "parameters": {
                    "type": "object",
                    "properties": {"context": {"type": "object"}},
                    "required": ["context"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_recommendation",
                "description": "Return the task recommendation for a focus level.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "focus_level": {
                            "type": "string",
                            "enum": ["High", "Medium", "Low"],
                        }
                    },
                    "required": ["focus_level"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "explain_behavior",
                "description": "Explain the behavioral pattern behind the focus level.",
                "parameters": {
                    "type": "object",
                    "properties": {"context": {"type": "object"}},
                    "required": ["context"],
                },
            },
        },
    ]


def _execute_tool(tool_name, arguments, base_context):
    if tool_name == "analyze_focus":
        return analyze_focus(arguments.get("context", base_context))

    if tool_name == "get_recommendation":
        focus_level = arguments.get("focus_level", base_context["focus_level"])
        return {"recommendation": get_recommendation(focus_level)}

    if tool_name == "explain_behavior":
        context = {**base_context, **arguments.get("context", {})}
        return {"reason": explain_behavior(context)}

    return {"error": f"Unknown tool: {tool_name}"}


def _serialize_tool_calls(tool_calls):
    return [
        {
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments,
            },
        }
        for tool_call in tool_calls
    ]


def generate_agent_response(context):
    if OpenAI is None or not os.getenv("OPENAI_API_KEY"):
        return FALLBACK_MESSAGE

    try:
        client = OpenAI()
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a productivity coach. Use the available tools before answering. "
                    "Briefly explain the situation, then give one specific actionable suggestion. "
                    "Keep the response under two sentences. Adapt tone to the user's trend, session state, "
                    "and optional user_type when provided."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Generate a concise coaching suggestion using this structured context:\n"
                    + json.dumps(context)
                ),
            },
        ]

        for _ in range(3):
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=_build_tools(),
                tool_choice="auto",
                temperature=0.4,
                max_completion_tokens=120,
            )
            message = response.choices[0].message

            if not getattr(message, "tool_calls", None):
                return (message.content or FALLBACK_MESSAGE).strip() or FALLBACK_MESSAGE

            messages.append(
                {
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": _serialize_tool_calls(message.tool_calls),
                }
            )

            for tool_call in message.tool_calls:
                arguments = json.loads(tool_call.function.arguments or "{}")
                tool_result = _execute_tool(tool_call.function.name, arguments, context)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result),
                    }
                )

        return FALLBACK_MESSAGE
    except Exception:
        return FALLBACK_MESSAGE
