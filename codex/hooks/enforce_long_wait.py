#!/usr/bin/env python3

import json
import sys


hook_input = json.load(sys.stdin)
tool_input = hook_input.get("tool_input")

if (
    hook_input.get("tool_name") == "wait"
    and isinstance(tool_input, dict)
    and not tool_input.get("terminate", False)
    and tool_input.get("yield_time_ms", 0) < 600000
):
    updated_input = dict(tool_input)
    updated_input["yield_time_ms"] = 600000
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "updatedInput": updated_input,
                "additionalContext": (
                    "Short polling was replaced with one event-driven 10-minute wait "
                    "to avoid repeated full-context inference."
                ),
            }
        },
        sys.stdout,
    )
