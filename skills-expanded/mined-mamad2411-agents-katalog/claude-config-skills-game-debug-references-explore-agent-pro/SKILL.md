# Game Debug — Explore Agent Prompt (PHASE 2)

Static prompt template for the PHASE 2 investigation agent. Fill the `{...}` placeholders from PHASE 0 (DEBUG_CONTEXT) and PHASE 1 (problem summary) before spawning.

---

```
Investigate this Godot bug. Perform 3 passes that build on each other.

DEBUG_CONTEXT:
{DEBUG_CONTEXT from PHASE 0}

PROBLEM:
{problem summary from PHASE 1}
{error message / stack trace / details}

PASS 1 — ERROR TRACE:
- Parse stack trace / error message → identify root location
- Read the source file at the error location (GDScript .gd files)
- Trace the call stack: what called this code? What signals trigger it?
- Map the exception/error flow: where is it caught (or not)?

PASS 2 — CONTEXT MAP (use locations from Pass 1):
- Read the scene tree: which nodes reference each other? Parent/child?
- Check signal connections: connect() calls, @onready vars, $NodePath references
- Trace data flow: exports, autoloads, Resources passed between scripts
- Identify external factors (physics layers, input actions, scene transitions)

PASS 3 — CHANGE ANALYSIS (use files from Pass 1+2):
- git log --oneline -10 -- {affected files}
- git blame {error location}
- Was this working before? What changed?
- Check KNOWN PITFALLS in DEBUG_CONTEXT: if a pitfall matches on symptom or location,
  include it as a strong hypothesis — add as "Pitfall match: {summary}" in return format

RETURN FORMAT:
INVESTIGATION_START
Error location: {file:line}
Call stack: {caller → callee chain, including signals}
Root code: {the problematic code snippet, max 20 lines}
Scene tree: {relevant node hierarchy}
Signal flow: {signal chain involved}
Recent changes: {relevant commits with dates}
Regression risk: {yes/no — was this area recently modified?}
Pitfall match: {matching pitfall summary, or "none"}
INVESTIGATION_END
```
