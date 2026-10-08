---
name: improve-skill
description: Run a toolkit skill's eval.json and, on failure, propose iterative edits to the skill body until the target pass rate is hit.
author: ai-toolkit
presets:
  - skill-development
---

# /improve-skill

The self-improving variant of [`/eval-skill`](./eval-skill.md). Runs the eval suite, and if the pass rate is below the target declared in `eval.json`, the agent proposes edits to the skill body, asks for approval, applies them, and re-runs.

## Usage

```
/improve-skill <skill-or-agent-name> [--max-iterations N]
```

`--max-iterations` defaults to 3 to keep loops bounded. The user can override.

## What this command does

1. Run the eval (the [`skill-evaluator`](../skills/skill-evaluator/SKILL.md) procedure, Step 1 through Step 4).
2. If the pass rate ≥ `target_pass_rate` from the eval file, stop. Report success.
3. Otherwise, **identify the smallest plausible edit** to the skill body that would fix the failing tests without breaking the passing ones. Concretely:
   - Look at every failing assertion. Group by likely root cause.
   - Draft an edit to the relevant section of `SKILL.md`.
   - Be conservative — prefer adding a clarifying paragraph, sentence, or list item over rewriting a section.
4. **Present the diff to the user.** Use a unified-diff-style block or your IDE's native diff preview. Do not write to the file yet.
5. Wait for approval. If the user declines or asks for a different approach, iterate.
6. On approval, apply the edit and re-run from Step 1.
7. Stop when one of these is true:
   - Pass rate ≥ target.
   - `--max-iterations` reached.
   - User cancels.

## Hard rules

- Never edit `eval.json` to make a test "pass". The eval is the spec; the skill is what changes.
- Never silently merge multiple iterations into a single diff. Each iteration is reviewable on its own.
- If two iterations in a row don't move the needle, stop and ask the user what to try next — looping past that is just spending the user's context for no signal.
- If the skill body has uncommitted git changes the user didn't write themselves, surface that before doing anything destructive.

## Output

Per iteration, show:

```
== iteration 1/3 ==
eval before: 3/5 (60%)
proposed diff:
  --- skills/comprehensive-review/SKILL.md
  +++ skills/comprehensive-review/SKILL.md
  @@ ...
  + (clarifying paragraph or section)
apply? [y/N]
```

Then on approval re-run and report the new pass rate.

A final summary at the end:

```
done — 4 iterations, pass rate 3/5 → 5/5 (100%)
edits committed to skills/comprehensive-review/SKILL.md (not yet staged).
```

## Limitations

The IDE-driven approach is approximate (your IDE's model is simulating, not making a fresh API call with the skill as system). Multiple consecutive 100% rates would be more believable than a single one. If you need hermetic eval-driven iteration, write an out-of-band runner — `docs/eval-format.md` describes the schema you'd target.

<!-- MIT, see LICENSE -->
