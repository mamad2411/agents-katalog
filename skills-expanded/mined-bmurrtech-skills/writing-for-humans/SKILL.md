---
name: writing-for-humans
description: >
  Mode-route human writing: STE-inspired instructions, slop-free prose, or
  mixed by function. Use when drafting or editing procedures, runbooks,
  troubleshooting, READMEs, commands, explanations, essays, or technical
  replies that mix diagnosis with steps; when clearing AI filler from
  human-facing prose; or when the user wants strict / controlled / STE-style
  procedural English (this skill’s controlled variant — not official
  ASD-STE100).
disable-model-invocation: true
---

# writing-for-humans

Simplify the **expression** of an idea, not the idea. Route by **function**,
not document type: actionable parts use STE-inspired discipline; explanation
and voice use prose rules; mixed replies apply both by section.

## Workflow

### 1. Lock job + mode

Pick **job** and **mode** from the ask (do not ask when clear).

| Job | When |
|-----|------|
| **Generate** | No usable draft — write new content |
| **Edit** (default when a draft exists) | Improve an existing draft; *minimum effective edit* |
| **Detect** | Audit AI-slop patterns only; do not rewrite |

| Mode | Function | Load |
|------|----------|------|
| **Instructions** | Steps, install, config, runbooks, commands, checklists | [references/instructions.md](references/instructions.md) |
| **Prose** | Explanations, analysis, essays, email, opinion, creative | [references/prose.md](references/prose.md) |
| **Mixed** | Debug, migrate, deploy, architecture + steps | Both refs; apply per section |

Route by function inside Mixed (and inside long docs): diagnosis/trade-offs →
Prose; procedures/commands/verify/recovery → Instructions. Optional Mixed
shape when useful: Finding → Why → What to do → Verify → If that fails —
omit empty sections.

**Controlled overlay:** when the user asks for strict STE, controlled English,
or ASD-STE100-style procedural writing, also load
[references/controlled.md](references/controlled.md) on Instruction surfaces.
That file is this skill’s owned variant — never claim official ASD-STE100
compliance.

If job is **Edit** or **Detect** and no draft is in the ask or context, ask
once for the text (or path). Generate does not need a draft.

**Done when:** job + mode named; controlled overlay chosen or skipped; draft
present when Edit/Detect requires it.

### 2. Load refs for the mode

Read only the mode file(s) from the table (+ controlled.md when overlay is
on). For Detect, load prose patterns only. For Edit, identify voice traits
before changing prose. For Generate/Edit quality check, also read
[references/lint.md](references/lint.md).

Ask at most one clarifying question when audience, goal, or a material
ambiguity would change the command, config, security, data-loss risk, or
recommended action. Otherwise proceed with a stated assumption.

**Done when:** required refs loaded; audience/goal known or assumed aloud.

### 3. Write or edit by function

Apply global rules below, then mode rules. Generate optimizes for complete
actionable sequences (do not drop needed steps for elegance). Edit preserves
strong existing language. Detect: name each pattern, quote the line, give a
short fix — no rewrite, no AI-authorship guess, no score.

Preserve exact commands, flags, paths, identifiers, UI labels, error text,
and product terms. Warn before destructive actions. Do not invent facts,
outputs, metrics, or “verified” results.

**Done when:** draft or detect report matches the locked mode(s).

### 4. Measure, judge, budget

For **Detect**: skip the linter unless the user asks for metrics; finish with
[references/eval.md](references/eval.md) judgment only.

For **Generate** / **Edit** — run after the draft is substantially complete:

1. Run the measure-only linter (see [references/lint.md](references/lint.md)):

```bash
# From this library repo root (or installed skill path under skills/):
python3 skills/writing-for-humans/scripts/writing_for_humans_linter.py /path/to/draft.md
# From the skill directory itself:
# python3 scripts/writing_for_humans_linter.py /path/to/draft.md
```

2. Prefer JSON `agent_summary` (compact). Use `findings` only when you need
   sentence context. The script counts and matches; you judge material vs
   cosmetic.
3. Honor `agent_summary.recommendation` / `revision_budget`:
   - **STOP** (budget **0**) → accept; do not revise solely to reduce metrics.
   - **REVISE_ONCE** (budget **1**) → one targeted revision for material
     issues only → re-lint **once** → **STOP**.
4. Run [references/eval.md](references/eval.md). For Edit, return the artifact
   plus a short **What changed** when useful.

**Done when:** lint budget spent or unused correctly; eval passes or waived
with reason; no further metric-chasing revisions.

## Global rules

- Preserve technical meaning and material caveats (data loss, downtime,
  security, irreversibility, version/compat constraints).
- Distinguish known facts, assumptions, inferences, estimates, and
  recommendations.
- Consistent terminology beats synonym variety.
- Do not flatten reasoning into a fake procedure; do not turn a procedure
  into a vague essay.

## Boundaries

- Never claim official ASD-STE100 compliance; use this skill’s controlled
  variant when strict procedural English is requested.
- Do not invent test results, command output, system state, sources, or
  successful execution.
- Do not apply Instructions/controlled style to creative writing, essays, or
  opinion merely because the topic is technical.
- Do not let prose cuts remove required procedural repetition, warnings,
  verification, exact terms, or conditional branches.
- Do not rewrite commands, code, config, or paths for style.
- Do not ask filler questions when a low-risk assumption keeps the answer
  useful.
- Do not rewrite solely to satisfy a word-count threshold. Do not spend more
  than one lint-driven revision unless a substantive new defect appears
  (unrelated to the prior metric). When `agent_summary.recommendation` is
  **STOP**, stop.
