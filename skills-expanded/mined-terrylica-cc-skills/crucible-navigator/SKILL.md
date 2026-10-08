---
name: crucible-navigator
description: starting a new research campaign, entering a new Claude Code session on a research repo, or when unsure which methodology.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# crucible-navigator — Research campaign orientation

> **Self-Evolving Skill**: This skill improves through use. If the routing guidance is wrong (wrong skill invoked for a user intent), fix the description's TRIGGERS list and the routing table below. Append reason to `references/evolution-log.md`. Don't defer.

## What this skill does

You are orienting an agent to research methodology. Route the agent to the right sub-skill based on what kind of research task is at hand. The four sub-skills cover epistemics (A), execution (B), decisions (C), and archive (D).

## Routing table — map user intent to skill

| User intent signal                                                                                       | Route to                      |
| -------------------------------------------------------------------------------------------------------- | ----------------------------- |
| "Is this finding real?", "check significance", "shuffled null", "causal feature", "label leakage"        | `a-research-foundations`      |
| "Test a hypothesis", "sweep parameters", "multi-agent analysis", "gate validation", "per-trade analysis" | `b-investigation-methodology` |
| "Should we pivot?", "ship this?", "kill or refine?", "too much context", "supersede a finding"           | `c-meta-governance`           |
| "Check dormant ideas", "what's archived?", "resurrect this", "conditions have changed"                   | `d-emergent-resurrection`     |

If unsure, start with **A** (foundations). Epistemic discipline is the hardest prerequisite.

## The core genetic-evolutionary framing

Research in this plugin is treated as a population under selection:

```
Population ───────────> (multi-lens agents propose candidates)
    │
    ▼
Fitness ──────────────> (z-score vs shuffled null, OOS replication, kill-selectivity)
    │
    ▼
Selection ────────────> (serial adversarial gates A→B→C→D→E)
    │
    ▼
Surviving individuals ─> (champion stacked as supersedes chain in evolution.jsonl)
    │
    ▼
Mutation/Crossover ───> (agent proposes perturbations of winner; orthogonal components recombined)
    │
    ▼
Archive failures ─────> (d-emergent-resurrection preserves with resurrect_if conditions)
    │
    └──────── NEXT GENERATION ───────┐
                                     ▼
                                 (new audit folder)
```

A "hypothesis" is a **triple**: `(trigger, filter_cascade, management_rule)`. Each component mutates independently. Crossover combines validated components from different campaigns. Failed individuals go to archive, not trash.

## Reading order for a new campaign

1. **Read this file.** Understand the genetic framing.
2. **Read `a-research-foundations/SKILL.md`.** 6 epistemic disciplines.
3. **Read `b-investigation-methodology/SKILL.md`.** 6 execution patterns. This is the workhorse.
4. **Reference `c-meta-governance/SKILL.md` as needed** during pivots/decisions.
5. **Check `d-emergent-resurrection/SKILL.md` first** if the hypothesis resembles an archived dead one — you might be resurrecting.

## Anti-patterns

1. **Treating principles as universal from N=1 evidence.** Each principle has a `confirmation_count`; defer to re-confirmed ones.
2. **Skipping A.** Experienced agents skip epistemics — don't. The label-leakage trap, wrong-null trap, and agent-z overstatement trap all live in A.
3. **Running a new campaign without checking D.** Ideas recur. Check archive before re-exploring.
4. **Writing conclusions without ledger entries.** See A5 (record-keeping-discipline).

## Repository landmarks

In `opendeviationbar-patterns/`:

- `findings/methodology/` — original 10 principle files (pre-plugin)
- `findings/evolution/evolution.jsonl` — ledger of findings (append-only)
- `findings/evolution/audits/` — dated audit folders (one per campaign)
- `findings/evolution/audits/CLAUDE.md` — audit index

## When you're done in a session

Update `references/evolution-log.md` if you noticed that:

- The routing table missed a user intent (add the row)
- A TRIGGER keyword didn't fire on a relevant prompt (extend the description)
- A sub-skill was weaker than expected (flag it for refinement)

---

## Post-Execution Reflection

After invoking this skill, if the routing produced a wrong-skill-selected outcome, or if a new user-intent pattern emerged that isn't covered:

1. **Identify the gap.** What did the user ask for that wasn't routed?
2. **Determine the fix.** Add a new row to the routing table? Add keywords to TRIGGERS? New sub-skill needed?
3. **Apply the fix.** Edit this file in-place. Append to `references/evolution-log.md` with: date, trigger text, what was changed, and link to the session where this came up.
4. **Never silently defer.** A quiet gap is worse than a noisy one.
