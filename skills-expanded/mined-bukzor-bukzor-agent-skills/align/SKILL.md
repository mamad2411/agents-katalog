---
name: align
description: "Human-alignment pass — check an artifact's goals against the user's goals. Agent MUST load on /align, or when asked whether a body of work's goals match the user's."
---

# /align [target]

Target: a file path (read it), an in-context reference ("the plan
above"), or a list of files. This checks **intent**: do the goals the
target embodies (explicit or implicit) match the user's goals? It is
not a content/technical audit — don't critique correctness,
completeness, or quality.

> **IMPERATIVE:**
>
> Your FIRST action when this skill loads MUST be:
> `Bash("ls -RF skill.kb/must-read.kb/")`
>
> That listing is an index of triggers: each filename names the occasion to
> read it. Walk it while planning, before ANY action, and read every entry
> whose trigger matches the work at hand — `before/` entries must be read
> *before* the action they name, not alongside it.

## Posture

- The user owns the goals. You only surface the goals the target embodies; the
  user judges them.
- Small steps. Present, then stop. Don't bundle in audits or recommendations.
- Don't edit until alignment is confirmed.

## Procedure

1. **Extract** the goals the target embodies — explicit and implicit — plus any
   non-goals it implies. Plain list, nothing else.
2. **Ask** which are the user's, which aren't, what's missing. More than a
   handful of goals: the ask is a ruling batch — run it under
   `Skill(review-open-questions)`, whose register law says where each goal
   lands and how the user rules on it.
3. **Reconcile** corrections into a clarified goal set; reflect it back to confirm.
4. **Adjust** the target to match.
5. **Repeat** until a pass surfaces no misalignment.
