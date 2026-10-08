---
name: crucible-meta-governance
description: deciding whether to pivot or persist, whether to ship or hold, whether to scope-narrow a partial pass, how to manage.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Meta-governance — 6 decision-layer patterns

> **Self-Evolving Skill**: If any pattern here misled decisions, update the section AND append to `references/evolution-log.md`. Don't defer.

These patterns are meta-level — they're about the investigation itself, not its content. Invoke when a decision must be made: pivot vs persist, kill vs narrow, ship vs hold.

---

## 1. Physical-constraint-first pivot

When brute force yields null, extract the **execution constraint** and redesign the hypothesis class to fit it. Don't iterate on a hypothesis that ignores reality.

Session example: 17 directional-signal null campaigns → user pivoted:

> "What's the best strategy for a highly random walk market?"
> "I can only trade on a traditional MT5 broker that allows hedging positions."

From this came the synthetic straddle (BUY_STOP + SELL_STOP pending orders, OCO). Constraint-driven design unlocked the strategy class. The math (diffusive displacement in random walks: `E[|ΔS|] > 0`) was always available; what was missing was honoring the execution venue.

**Ask yourself**:

- What execution venue is the user actually on?
- What types of orders are possible?
- What's the realistic slippage / commission / spread?
- What position-sizing constraints apply?

If the hypothesis doesn't survive these questions, pivot the hypothesis, not the statistics.

---

## 2. Incremental artifact promotion (/tmp → repo early)

Move findings from `/tmp/` to the persistent repo (`audits/YYYY-MM-DD-slug/`) **as soon as a result survives two independent tests**, not "when done".

Session anti-pattern: reproducers written in `/tmp/` during exploration, causing reproducibility loss on reboot. The moment a result passed Gate C (OOS) it should have been promoted — not after the 4-gate suite completed.

**Promotion triggers** (at least one required):

- Result passed shuffled-null z > 3 AND hasn't been contradicted
- An agent synthesized a verdict that supersedes an earlier one
- A reproducer script ran successfully twice

**Mechanics**:

```bash
mkdir -p findings/evolution/audits/$(date +%Y-%m-%d)-slug
cp /tmp/reproducer.py /tmp/artifact.json findings/evolution/audits/.../
# Write CLAUDE.md navigator + verdict.md
# Append to evolution.jsonl
```

What's impermanent gets lost.

---

## 3. Gate-failure scopes not kills

When a signal fails one of the serial gates (see Skill B §2), downgrade its **scope**, don't kill it outright.

| Failed gate                    | Action                                                         |
| ------------------------------ | -------------------------------------------------------------- |
| Gate A (directional breakdown) | Learn which side — often simplify to one-side                  |
| Gate B (mirror symmetry)       | Note asymmetry; record as "direction-biased" feature           |
| **Gate C (OOS time-split)**    | **Kill.** No scope-narrowing rescues in-sample overfit.        |
| Gate D (cross-asset)           | Downgrade to `<asset>-specific`; keep                          |
| Gate E (per-year)              | Flag bad years as "regime-unfavorable"; explore regime filters |

NGRAM3FU-STRADDLE-001 failed Gate D (XAUUSD, GBPUSD) but passed A/B/C/E. Status downgraded to `eur-only`, NOT killed. A year later, if XAUUSD develops different microstructure, it could be retested — this is the `resurrect_if:` trigger (see Skill D).

**Principle**: scope-narrowing preserves optionality. Hard kills lose negative knowledge.

---

## 4. Agent-lens disagreement as signal

When parallel agents DISAGREE, the disagreement itself is diagnostic.

Session example: 4 agents reported "lower rejection at bottom → 67.8% UP" as a signal. Agent 5 (hidden-signal hunter, critic) flagged it as label leakage. The disagreement pointed precisely at the bug.

**When agents disagree**:

1. Don't average or vote — map WHAT they disagree about
2. Check: does one agent's evidence involve an implicit assumption the other rejects?
3. Disagreement about mechanism → investigate mechanism (may be label leakage, confound, or real but lens-bound effect)
4. Disagreement about significance → check each agent's multiple-testing burden

**Anti-pattern**: picking the agent that gives the answer you want. If the critic-agent disagrees with the proposer-agents, the critic is usually right.

---

## 5. Context-budget discipline

Conversation and data context are scarce. Reserve them for the most ambiguous questions; compress known-good findings ruthlessly.

**Hierarchy of compression**:

- Raw bars (not for agents; 67 MB)
- Token-rendered bar sequences (60 KB; good for one agent)
- Stats tables (60 KB; consumable by 5 parallel agents) — PREFERRED
- Ledger entries (1 KB; tracks findings)

**When context feels tight**:

1. Emit a fresh audit folder with artifacts; future sessions load that, not the transcript
2. Drop detailed raw data from agent prompts; use markdown summaries
3. If you must hand off mid-session, write a handoff file in `.planning/` (not plugin scope; see project root)

**Signal: context is BLOCKED when**: you find yourself re-reading the same file twice in one session; or agents ask for re-briefings; or you can't remember what was decided 10 turns ago. Compress to an audit folder.

---

## 6. Supersede-not-rewrite

When a later finding replaces an earlier one, **add** a new ledger entry with `supersedes: "OLD-ID"`; **update** the old entry with `superseded_by: "NEW-ID"`. Never rewrite or delete.

**Why**:

- Future auditors need the trail, not the final answer
- A superseded finding may contain negative knowledge (why it failed) that informs future work
- Deletions create "mysterious silences" that agents can't interpret

**Canonical chain** from session:

```
NGRAM3FU-STRADDLE-001                     preliminary-positive
  ↓ supplemented by
NGRAM3FU-STRADDLE-001-GATES               gates-validated (Gate D failed → eur-only)
  ↓ supplemented by
NGRAM3FU-STRADDLE-001-FULL-HISTORY        confirmed at 7.18M bars
  ↓ supplemented by
NGRAM3FU-STRADDLE-001-FILTERED            Phase-L filter validated
  ↓ supplemented by
NGRAM3FU-STRADDLE-001-FULL-STACK          Phase-L + Phase-M final
```

Note `supplements` vs `supersedes`: supplement EXTENDS; supersede REPLACES. Pick the right relationship.

**Anti-pattern**: editing an old ledger entry because the finding "got better". That's rewriting history. Add a new entry.

---

## Confirmation counts

| Pattern                      | Confirmed | Notes                                               |
| ---------------------------- | --------- | --------------------------------------------------- |
| 1. physical-constraint pivot | 1         | The session-defining pivot (directional → straddle) |
| 2. artifact promotion        | Multiple  | Every /tmp → audit folder move                      |
| 3. gate-failure scopes       | 1         | NGRAM3FU-STRADDLE Gate D → eur-only                 |
| 4. disagreement as signal    | 2         | Act-2 label leakage catch; Phase L agent variance   |
| 5. context-budget            | Implicit  | Used every time we preferred stats tables over raw  |
| 6. supersede-not-rewrite     | 5         | NGRAM3FU-STRADDLE chain, 5 entries                  |

---

## Post-Execution Reflection

After invoking this skill:

1. Did a pattern save you from a bad decision? Increment `confirmed` count; note in `references/evolution-log.md`.
2. Did a pattern produce the wrong call? Demote it; record context + link to where it misled.
3. A new decision pattern emerged that isn't here? Draft a section.
4. A pattern could be better-phrased for future agents? Edit the text directly; log why.
