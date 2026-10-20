---
description: "Decision scoring rubric: intent/state/evidence/recency/pref with thresholds & gates"
globs: ["**/*"]
alwaysApply: false
---

# Decision Scoring Policy
Score each candidate c under context x:
score(c|x) = w_intent·sim(intent(x), profile(c))
           + w_state·compat(state(x), preconds(c))
           + w_evidence·evid(c; x)
           + w_recency·rec(x)
           + w_pref·pref(x)

## Defaults (use weights.json if provided)
- w_intent=0.30, w_state=0.25, w_evidence=0.20, w_recency=0.15, w_pref=0.10
- Normalize all component scores to [0,1].

## Threshold Gates
- CONF_HIGH (≥0.75): emit NEXT_STEP (single best candidate).
- CONF_MID (0.55–0.75) with Top-2 gap ≤ ε=0.05: emit OPTION_SET (top 2–3).
- CONF_LOW (<0.55): ASK_CLARIFY unless RISK ≥ MEDIUM → RISK_ALERT/ABSTAIN.
- Fail-closed for destructive/compliance-sensitive actions.

## Output Schema (JSON only)
{
  "context_summary": "string",
  "candidates": [
    {
      "id": "string",
      "action_type": "NATURAL_STEP|COMMAND_TRIGGER",
      "scores": { "intent":0.0,"state":0.0,"evidence":0.0,"recency":0.0,"pref":0.0,"final":0.0 },
      "explanation": "short, cites evidence paths if any"
    }
  ],
  "decision": { "type":"NEXT_STEP|OPTION_SET|ASK_CLARIFY|RISK_ALERT", "reason":"..." },
  "evidence_paths": ["file://...","tool://..."]
}

## Evidence Discipline
- For evid(c;x), cite tool/file paths (e.g., memory-bank/*.md, test logs).
- For compat(state vs preconds), list unmet preconditions explicitly.
