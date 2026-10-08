---
name: eval-skill
description: Run the eval.json suite for a toolkit skill via your IDE's own agent — no API key.
author: ai-toolkit
presets:
  - skill-development
---

# /eval-skill

Run the `eval.json` for a toolkit skill in this same conversation. Uses your IDE's running model — no separate API key needed.

## Usage

```
/eval-skill <skill-or-agent-name>
```

If no name is provided, ask the user which skill to evaluate, or list every directory under `skills/` and `agents/` that has an `eval.json` and let them pick.

## What this command does

This command is a thin shim that invokes the [`skill-evaluator`](../skills/skill-evaluator/SKILL.md) skill against the named target. Concretely:

1. Resolve the target path: try `skills/<name>/` first, then `agents/<name>/`. If neither exists, surface a clear error.
2. Confirm `eval.json` is present at that path. If missing, point the user at `docs/eval-format.md` and stop.
3. Apply the **skill-evaluator** procedure (Step 1 through Step 4 in its body). Use the target skill's body as the simulated system prompt; iterate through every test in the eval suite; report per-test results and aggregate pass rate.

Do NOT propose edits to the skill body. This command is read-only. If the user wants to fix failures, route them to `/improve-skill <name>`.

## Output

A per-test table plus a one-line summary at the top:

```
skill: comprehensive-review   pass rate: 4/5 (80%)   target: 85%

Test results:
  ✓ rejects-bare-lgtm
  ✓ avoids-design-rant
  ✗ anchors-claims-to-specific-frames
     ⤷ contains_any_of: did not surface a specific frame
     ⤷ not_regex: response contained a speculative pattern
  ✓ tests-section-present-when-tests-changed
  ✓ rejects-whitespace-only-review

Below target. Run /improve-skill comprehensive-review to iterate.
```

Include the simulated response for any failing test in a collapsed block so the user can read what the model emitted.

<!-- MIT, see LICENSE -->
