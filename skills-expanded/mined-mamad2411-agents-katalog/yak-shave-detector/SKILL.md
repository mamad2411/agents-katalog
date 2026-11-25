---
name: yak-shave-detector
description: Use when you suspect you've drifted from the original goal — a blunt scope check that tells you if you're yak shaving.
metadata:
  added: 2026-06-27
  last_reviewed: 2026-06-27
  type: meta
  status: draft
  related: [requirements-gathering, brainstorming]
  owns: scope-discipline
---

# Yak Shave Detector

This skill is the cheapest, fastest sanity check in the system. Use it to catch scope drift
before it wastes hours.

"Yak shaving" is when you start with Task A, realize you need B, which requires C, which
needs D... and suddenly you're shaving a yak instead of doing what you set out to do. Apply
this skill blunt and fast — it cares about shipping, not feelings.

To apply it, know: the ORIGINAL task (what was supposed to happen), the CURRENT activity
(what's actually happening now), and optionally the chain of reasoning that got here.

## Detection algorithm

### Level 0: On track

Current activity directly serves the original task. No action needed.

### Level 1: Reasonable detour

Current activity is 1 step removed from the original task AND is necessary to complete it.
**Verdict:** "Necessary detour. Stay focused — get back to [original task] after this step."

### Level 2: Yak shave warning

Current activity is 2+ steps removed from the original task OR is "nice to have" not "must
have." **Verdict:** "YAK SHAVE DETECTED. You started with [A], now you're doing [D]. Is [D]
actually blocking [A]? If not, stop and go back."

### Level 3: Full yak

Current activity has no clear path back to the original task. You've lost the plot.
**Verdict:** "FULL YAK. Stop everything. Original task: [A]. Current task: [D]. These are
unrelated. Drop [D], return to [A] immediately."

## Output format

```
## Yak Shave Check

**Original task:** [what you set out to do]
**Current task:** [what you're actually doing]
**Level:** [0-3]
**Verdict:** [one sentence]

**Chain:** [A] → [B] → [C] → [D] (you are here)
**Cut point:** [where to cut back to — the last step that was actually necessary]
```

## Quick heuristics

- If you're refactoring code that isn't broken: probably a yak shave
- If you're building a tool to do a task you could do manually in 5 minutes: definitely a yak shave
- If you're "just quickly" doing something that isn't part of the current task or goal: yak shave
- If you're optimizing something that hasn't been measured: yak shave
- If you're adding tests for code you're about to delete: yak shave
- If you caught yourself saying "while I'm here, I might as well...": yak shave

## Rules

- Be fast. This check should take < 30 seconds.
- Be direct. No softening, no "you might want to consider..."
- One question matters: "Is what you're doing RIGHT NOW the fastest path to completing the
  ORIGINAL task?"
- If yes: say so in one line and exit.
- If no: say so clearly and prescribe the cut point.
