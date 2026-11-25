---
name: feature-sanity-check
description: Sanity-check a feature/task before taking it into work. Use for "assess this feature/task/queue", "is this worth doing", before claiming a task from bd ready, when creating a discovered-from card, when prioritizing the backlog, or in a "business sense vs technical risk" dispute.
---

# Skill `feature-sanity-check` — a sanity check of a feature

> **Seam:** execution queue = beads (`bd ready`, `bd update --claim`, `bd update --notes`). To use another tool, rewrite the `bd` commands in "When to run" and "Mechanics".

## Why

This guards against a technical finding authorizing itself: finding → bd task → task is `ready` → the next session takes it into work, and the queue fills up with high-technical-risk work without real business value (reference example: reordering the hot path of incoming message handling just to get labels on a trace span). Before work, every task goes through two independent roles (product owner and tech lead), the dispute is consolidated, and priority is computed by WSJF.

**The verdict is a proposal to the owner, not an authorization** (AGENTS.md, Operating contract, rule 6). The skill itself does not close, defer or start tasks.

## When to run

- Explicit call: "assess the feature", "assess task <pfx>-XXXX", "assess the queue", "run a sanity check".
- **Before `bd update <id> --claim` from `bd ready`** — blocking, if the task's notes do not yet have a sanity-check verdict. Verdict "do now" → work; anything else → show it to the owner and wait for a decision.
- **When creating a discovered-from task** — assess right away and record the verdict in notes (`bd update <id> --notes`). A task with the verdict "do not do" or "owner answer needed" is not taken into work until the owner decides.

Do not re-run for a task whose notes already have a verdict, unless the context has changed (new information from the owner, the product direction document changed, the task was reworded).

## Roles and project specifics

The assessment is done by two plugin roles, each with its own criteria (they are also useful on their own):

- **`product-owner`** assesses necessity: real pain and its source, product direction, real value ("nothing" is an
  acceptable answer), completeness of surfaces. Scores BV, TC and RR.
- **`tech-lead`** assesses feasibility and risk: feasible, reliable, repeatable, risks and gaps, impact on what exists.
  Scores JS and RR.

Call them as `dark-factory:product-owner` and `dark-factory:tech-lead` (a project's own role overrides it when called by the bare name:
Claude Code `.claude/agents/<name>.md`, Codex `.codex/agents/<name>.toml`). The project-specific facts the roles need go into the task text:

- the product direction document: <`docs/target-picture.md` / vision — specify on deployment>;
- the project's hot paths: <request intake, dispatcher, repositories — specify on deployment>;
- the project's surfaces: `openspec/README.md` §0; the anti-patterns: CODING_STANDARDS, "Project anti-patterns".

## Mechanics

1. Collect the task dossier: `bd show <id>` (or the feature text), related specs in `openspec/`, relevant parts of the product direction document, and the code of the affected places if needed.
2. **Two role calls in parallel, started in a single message, working independently** (two separate `Agent` calls: `subagent_type: "dark-factory:product-owner"` and `"dark-factory:tech-lead"`; the role carries the model and the criteria, do not pass a model). The owner role does not see the developer's opinion, and vice versa. Each task is: the dossier + the project specifics above + a requirement to return a structured assessment (per criterion: conclusion + grounds) and its WSJF components with a justification for each score.
3. **Consolidation in the main session**: compare the assessments, name the disagreements explicitly (e.g. owner "no value", developer "low risk" → that is not an argument for doing it). A score disagreement of more than one step of the scale — work out whose grounds are stronger, do not average.
4. Compute WSJF, give the verdict, show it to the owner.

## WSJF

The formula, the scale and who scores which component live in the `dark-factory:wsjf` skill; read it, do not copy it
here. Short form: `WSJF = (BV + TC + RR) / JS`. A score without a one-sentence justification is invalid. WSJF ranks
"do now/do later" among themselves but does not override a "do not do" verdict: a high score with no real pain (BV
assessed on a hypothesis) is a reason to fix the BV assessment, not to do the task.

## Verdicts (exactly four)

- **do now** — the pain is real, the direction matches, the risk is manageable; WSJF gives it a place in the queue
- **do later** — there is value but it does not expire, or the risk needs prerequisites; propose `bd defer` (done by the owner or on their "yes")
- **do not do** — the pain is hypothetical, outside the direction, or the risk exceeds the value; propose closing with a reason. "Do not do" is a full-fledged positive outcome, not a failure of the assessment
- **owner answer needed** — the assessment hinges on a product fork; phrase a concrete question with a recommendation

## Output format (per task)

```
## <pfx>-XXXX — <title>
Owner: pain=<real/hypothetical: source>; direction=<yes/no/outside: where in the direction document>; value=<what changes>
Developer: feasibility=<...>; reliability=<...>; risks=<main risk>; impact=<layers/volume>
Disagreements: <what and how it was consolidated, or "none">
WSJF: (BV X + TC X + RR X) / JS X = X.X
Verdict: <one of the four> — <one sentence why>
```

For a batch of tasks — a summary table, sorted: first "do now" by descending WSJF, then "do later", "owner answer needed", "do not do".

## Red flags (signs that someone is trying to bypass the assessment)

- "The task is already in `bd ready` — so it is approved" — ready means "not blocked", not "needed"
- "For symmetry/consistency with existing code" — that is not pain, that is aesthetics; write BV as it actually is
- "Since we're in this file anyway" — scope creep, assessed as a separate task
- "Observability/tests/refactoring are always useful" — usefulness ≠ priority; still goes through WSJF
- Assessing both roles in one pass "to save money" — loses the independence the skill exists for
- A WSJF score fitted to the desired verdict — the justification for each score is written before the final formula
