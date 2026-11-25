---
name: audit-marketplace
description: Adversarially audit the Polymath marketplace for production readiness, gaps, and bloat.
---

# audit-marketplace

> Walk every plugin and tool as a hostile reviewer. Emit one ranked ADD/FIX/CONSOLIDATE/REMOVE list — simplicity is the tiebreaker.

## When to use

- A release or maturity review of the whole marketplace ("audit the marketplace", "red-team every plugin").
- After a burst of plugin/skill additions, to catch redundancy and over-engineering before it sets.
- You suspect surfaces exist that no real workflow, command, or user reaches.

Not for reviewing one SKILL.md (`polymath-author:skill-author-critic`) or one plugin's structure (`polymath-author:validate-plugin`) — this is the marketplace-wide lens that calls those per item.

## Inputs

- The marketplace root (default: the repo you are in).
- Optional scope: a subset of plugins/tools. Absent → the whole catalog.

## Procedure

### 1. Enumerate from ground truth, not memory

Run the deterministic inventory first — never audit from recollection:

```bash
tools/token-report.py budget          # always-on cost per plugin
tools/check-command-overlap.py        # commands that only shadow a skill
tools/check-workflow-invokes.py       # workflow steps -> real skills
tools/lint-descriptions.py --strict   # description collisions = redundancy signal
tools/build-surface-index.py --check  # every routed surface, in sync
```

Build the work-list — each entry is one audit unit:

- every plugin (`plugins/polymath-*/`)
- every catalog tool-surface (`plugins/*/tools/*/tool.json`) — **not** the top-level `tools/` dir, which holds maintainer/CI scripts (audit those as a separate pass)
- every workflow (`plugins/polymath-flows/workflows/*.yaml`)

### 2. Loop — the devil's-advocate lens (per unit)

For each unit, answer all five. Quote a `file:line` for every claim:

1. **Would a real practitioner reach for this mid-SDLC, or is it theater?** Name the concrete scenario. No scenario → REMOVE candidate.
2. **What breaks the first real use?** Walk the unhappy path, not the demo.
3. **What does it duplicate?** Overlapping description, twin procedure, or a workflow that already chains it.
4. **Cost vs. payoff.** Always-on tokens (step 1 numbers) against the manual work it actually saves.
5. **Deletion test.** If removed, who complains and why? Nobody → REMOVE.

Delegate the deep per-item critique instead of redoing it inline:

- SKILL.md craft → `polymath-author:skill-author-critic`
- Adversarial design objections → `polymath-thinking:red-team` / the `architecture-critic` agent
- Structure / manifest → `polymath-author:validate-plugin`

### 3. Hunt the two failure directions

- **Gaps (ADD).** Per SDLC stage, name a real scenario a team hits that nothing covers. A gap is real only if (a) a concrete scenario needs it and (b) no existing surface — even an adjacent one — covers it. Otherwise it is not a gap.
- **Bloat (REMOVE / CONSOLIDATE).** Surfaces with no invoker, twin skills, commands that only shim a skill ([AGENTS.md authoring policy §5.1](../../../../AGENTS.md)), machinery with no user, references nothing links to.

### 4. Classify and rank

Every unit gets exactly one verdict: ADD / FIX / CONSOLIDATE / REMOVE / KEEP. Each carries evidence (`file:line` or tool output), the real-world scenario, severity (blocker / major / minor), and effort.

Simplicity is the tiebreaker:

- ADD only with a named scenario **and** proof nothing covers it.
- Prefer CONSOLIDATE over ADD; prefer REMOVE over FIX when a surface has no demonstrated use.
- Track the **net surface delta** (added − removed). It must be ≤ 0 unless a gap is proven — a quality audit shrinks the catalog more often than it grows it.

## Output

```text
audit-marketplace: <marketplace> @ <commit>

Scorecard:
  plugins N · skills N · tools N · workflows N · always-on tokens N
  verdicts: ADD a · FIX f · CONSOLIDATE c · REMOVE r · KEEP k
  net surface delta: +a −r = <±n>   (target ≤ 0)

Blockers (production readiness):
  - [FIX] polymath-foo:bar (SKILL.md:42) — breaks on <unhappy path>. Scenario: <real use>. Fix: <change>.

Consolidate:
  - [CONSOLIDATE] polymath-x:a + polymath-x:b — twin procedures (a/SKILL.md:10 ≈ b/SKILL.md:12). Merge into a; drop b. Saves <n> tokens.

Remove:
  - [REMOVE] polymath-y:z — no workflow/command/user invokes it. Deletion test: nobody complains. Evidence: check-workflow-invokes.py.

Add (gaps — each with proof nothing covers it):
  - [ADD] <stage>: <scenario>. Nearest existing: <surface> — why it does not cover it.

Verdict: SHIP / FIX-FIRST / OVERBUILT.
  Top 3 actions, in order.
```

## Quality bar

- Every finding cites `file:line` or the tool output that proves it. No "feels redundant".
- Each ADD names the real-world scenario and the nearest existing surface it is NOT covered by.
- The net surface delta is stated. An audit that only adds is a failed audit.
- Verdicts are decisions (REMOVE — not "consider removing").

## Anti-patterns to avoid

- Auditing from memory instead of running the inventory tools in step 1.
- Proposing a new plugin/skill when an existing one stretches to cover the scenario.
- "Nice to have" ADDs with no scenario — that is how the bloat got here.
- Re-implementing red-team / skill-author-critic / validate-plugin inline instead of delegating.
- Polishing minor wording while a surface that nothing invokes survives.
