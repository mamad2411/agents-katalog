---
name: hillclimb-brainstorm
description: >
  Refresh the idea pool of a hill-climbing project. Reads the run history and
  current ideas, detects whether progress has stalled, then generates new
  candidate directions, biased toward exploration when stuck, toward
  exploitation when a recent run improved things. Use this skill when the
  user is out of open ideas, the last several runs failed to improve `best`,
  the user explicitly asks for new ideas, or says "run the hillclimb-brainstorm skill",
  "I'm stuck", "what else could we try", "give me more directions".
---

# hillclimb-brainstorm: diversify or focus the idea pool

The explicit "kick" hill-climbing search needs to escape local optima.
Call it deliberately. It does NOT execute ideas or run the verifier; it
only diagnoses the search and updates the idea list.

See `hillclimb-execute` skill's First principle. Never propose ideas that
game the verifier. If the verifier itself is wrong, propose fixing it
correctly, not making it more lenient.

## Step 1: Locate state and read the search

```bash
STATE_PY="$PWD/.hillclimb/state.py"; STATE_HTML="$PWD/.hillclimb/state.html"
[ -f "$STATE_PY" ] && [ -f "$STATE_HTML" ] || { echo "no .hillclimb/, run the hillclimb-onboard skill first"; exit 1; }
python3 "$STATE_PY" read "$STATE_HTML"
```

Extract `objective`, `baseline`, `best`, all `ideas[]` (note status), and
the last 5 `runs[]` with their verifications.

## Step 2: Diagnose

Classify the recent state into one of four cases. State the diagnosis in
one sentence to the user before generating ideas, so they understand the
framing.

| Diagnosis      | Trigger                                                 | Bias                                    |
|----------------|---------------------------------------------------------|-----------------------------------------|
| **Cold start** | ≤1 verified run, or all ideas open                      | Broad, diverse, easy-first ideas       |
| **Promising**  | Most recent run improved `best`, or last few trend up   | Exploitation, variants of what works (parameter sweeps, ablations, "more of the same but bigger") |
| **Stuck**      | Last 3+ verified runs failed to improve `best`          | Diversification, fundamentally different angles. List what's been tried so new ideas don't duplicate |
| **No-signal**  | Many `inconclusive` verifications                       | Meta, propose verifier fixes (tighter checks, better metric) at high priority |

(Hardcoded threshold "last 3", tune in this SKILL.md if your runs are
unusually fast or slow.)

## Step 3: Generate ideas

Two tools: pure reasoning, and a `general-purpose` subagent for
diversification. Use the subagent for **stuck** and **no-signal**; pure
reasoning is fine for **cold start** and **promising**.

When spawning the subagent, brief it with: project objective, the list of
ideas already tried (titles + status), recent run summaries + verification
notes, the current `best`. Ask for **5–8 distinct candidate directions**
with a one-line rationale each, biased to whichever case applies. Cap at
~300 words. Run it in foreground, you need the output.

Filter the returned ideas: drop fuzzy duplicates of existing
title/description (case-insensitive). Pick the best **3–6**.

## Step 4: Append ideas, optionally reprioritise

```bash
python3 "$STATE_PY" append-idea "$STATE_HTML" \
  '{"title":"...","description":"...","priority":"high|medium|low"}' \
  --added-by brainstorm
```

Priority guidance:

- `high`, small effort, large expected payoff; aligns with current best
  direction (exploitation) OR opens a fundamentally different promising
  avenue (diversification when stuck).
- `medium`, default.
- `low`, speculative, mainly for breadth.

To **abandon** an existing idea that runs have actively disproved: `set`
refuses list traversal, so read state, mutate the entry in memory, write
the whole `ideas` array back:

```bash
IDEAS=$(python3 "$STATE_PY" read "$STATE_HTML" | python3 -c "
import json, sys
s = json.load(sys.stdin)
for i in s['ideas']:
    if i['id'] == '<I-id>': i['status'] = 'abandoned'
print(json.dumps(s['ideas']))
")
python3 "$STATE_PY" set "$STATE_HTML" ideas "$IDEAS"
```

In practice, leaving low-value ideas as `low` priority is usually enough.
Abandon only when the noise actively hurts.

## Step 5: Log and hand off

```bash
python3 "$STATE_PY" log "$STATE_HTML" brainstorm "<diagnosis>: added N ideas (<titles>)"
```

Tell the user the diagnosis, the ideas added, and "run the `hillclimb-execute` skill next."

## Rules

- Don't add filler to hit a count. Three sharp ideas beat eight vague ones.
- Don't propose ideas already tried-and-failed unless you have specific
  new evidence or a flaw in the previous attempt to address.
- **Don't propose verifier-loosening ideas.** See First principle above.
  If the verifier is genuinely wrong, suggest fixing it correctly.
- Don't run the verifier or execute anything here.
- Never edit `state.html` by hand. Always go through `state.py`.
- If the verifier itself looks broken (everything inconclusive, scores
  not making sense), say so explicitly, don't paper over it with more
  ideas. Suggest the user fix `verify.sh` first.
