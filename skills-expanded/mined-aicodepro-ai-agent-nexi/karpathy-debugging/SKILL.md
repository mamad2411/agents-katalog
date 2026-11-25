---
description: "Behavioral, evidence-first debugging methodology (Karpathy-style). Use when a bug report names a symptom but the cause is unknown."
license: "MIT"
---
# Karpathy Debugging

Root-cause debugging discipline for this repo. No speculation, no symptom
patches.

## Method

1. **Reproduce first.** If you cannot trigger the bug reliably, find the
   conditions before touching code. Note whether it's consistent or
   intermittent.
2. **Read the whole error.** Full stack trace, not just the top frame. Every
   word matters — "NoneType has no attribute X" and "AttributeError" point to
   different root causes even when the symptom looks the same.
3. **Diff against a working case.** Compare the broken path to a known-good
   one in the same module. Trace data flow from input to the failure point.
4. **One hypothesis at a time.** Write it down before editing. Name the test
   that would prove or disprove it.
5. **Minimal fix.** Fix the root cause where all callers route through it —
   not a guard bolted onto the one caller the ticket named. Grep every caller
   of the function you're about to touch first.
6. **Circuit breaker.** After 3 failed hypotheses, stop. The bug is probably
   somewhere else than you think — escalate instead of trying a 4th variant
   of the same idea.

## Anti-patterns to avoid

- Adding a null check instead of asking "why is it null?"
- Refactoring while fixing ("since I'm in here...").
- Trusting a fix because the symptom disappeared without understanding why.
- Treating "probably a race condition" as a finding instead of a guess.

## Nexi-specific gotchas

- `./.venv/Scripts/python.exe` only — bare `python` resolves to a different
  venv missing openwakeword/cv2/sentence-transformers and gives wrong
  answers.
- A tool needs entries in `_TOOLS` + `ALLOWED_INTENTS` + `TOOL_INTENTS`
  (`engine/tool_registry.py`) or it fails silently (routes to chat instead of
  erroring). Check all three lists before concluding a tool is "broken."
- Model names are selected dynamically (`engine/model_registry.py`) from
  probed capability facts — a hardcoded model name in a test or fix is a
  smell, not a solution.
