#!/usr/bin/env python3
# Gemini CLI BeforeAgent hook → mesin alur skill (~/.agents/skill-flow.py)
import sys, json, os, importlib.util
try:
    p = json.load(sys.stdin).get("prompt", "")
    sp = importlib.util.spec_from_file_location("sf", os.path.expanduser("~/.agents/skill-flow.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "BeforeAgent", "additionalContext": m.hook(p)}} if p else {}))
except Exception:
    print("{}")
