---
name: review-triage
description: >
  Use when consolidating findings from multiple read-only review agents into one report for a
  human — verifying each finding's cited location still exists, dropping only findings the diff
  or file disproves, and collapsing one root cause reported across many files into a single item.
  Load before writing the consolidated review report, not while reviewing.
user-invocable: false
---

# Review Triage

Between "the reviewers reported" and "the human reads one report" there is a gate. Its job is
narrow: make every surviving finding **locatable**, **not-already-disproven**, and **counted once**.

**This gate is for human-facing consolidation only** (`/sdd:review`). Do NOT run it in front of
`/apply` / `/quick` Phase 2's fix loop — there, each fix agent already verifies every finding
against the full codebase before implementing (`orchestrator.md` Phase 2), which is strictly
stronger than anything judgeable from a diff. Inserting a weaker filter upstream of a stronger
one only deletes findings the fix agent would have validated correctly.

## Input contract

Each finding must arrive with an **anchor**: the `file:line` plus the reviewer's verbatim quote of
the code it is about. Reviewer report formats require this. A finding that arrives with no anchor
is not silently dropped — it goes to Step 1's `unanchored` bucket.

**Gate only the items a reviewer reported as findings.** A reviewer running with project review criteria returns several item classes — a demonstrated finding, a suggestion that is correct as it stands, a suspicion it could not demonstrate. Only the first is a finding here. The others pass through to their own sections untouched and are not counted in `U`: a suggestion carries a location but no code quote by design, and an undemonstrated item has nothing to anchor by definition, so anchor-checking either one reports "could not be located" about something that was never lost.

E2E / test-run findings (qa-engineer) **skip Steps 1–2 entirely**. Their evidence is a failing test
run, which is stronger than a code quote; there is nothing to re-anchor and nothing a diff can
disprove. They pass straight to Step 3.

## Step 1 — Anchor check

For each finding:

1. Read the cited `file` around the cited line and compare against the quoted snippet, ignoring
   whitespace and leading diff markers `+`/`-`/` `.
2. **No match there** → `Grep` the snippet's most distinctive line (a literal, a call, an identifier —
   not a lone `}` or `return`) across the review scope, plus the cited file itself when it sits outside
   that scope. One hit ⇒ that is the true location. Several
   hits ⇒ pick the one whose surrounding lines also match the quote; if none does, treat it as no match.
3. Still nothing → `unanchored`.

One grep per finding is the budget. This gate re-locates a drifted citation; it does not go looking
for the defect.

| result | action |
|---|---|
| quote found at the cited line | anchored — keep as-is |
| quote found elsewhere in the same file | **re-anchor**: correct the line number, keep the finding |
| quote found in a different in-scope file | **re-anchor** to that file:line, keep the finding |
| quote not found anywhere searched | mark `unanchored` |
| no quote supplied | mark `unanchored` |

A finding the reviewer labelled **`out-of-scope`** is anchored against its own cited file like any
other — read that file directly. Sitting outside the review scope is not a reason to call it
unanchored; the reviewer read the file, so the quote should be there.

**`unanchored` is a downgrade, never a deletion.** The finding still appears in the report, in its
own section, labelled `unanchored — 位置無法確認`, and it never counts as blocking. A reviewer that
drifted on the location may still be right about the defect; the reader just cannot be pointed at it.

Do not go hunting semantically for "what it probably meant" — a literal-ish match or nothing.

## Step 2 — Falsification-only filter

**You are falsifying, not verifying.** Read each anchored finding and ask one question: *does the
code at its anchor contain direct counter-evidence that the finding's central claim is wrong?*
(Read the anchor's surrounding lines — the guard clause that disproves a "missing null check" is
usually right above it. An `out-of-scope` finding is judged against its own file, same as any other.)

Drop the finding **only** when the answer is yes. Everything else survives.

| verdict | example | action |
|---|---|---|
| disproven | "no null check before `.Value`" — the line above is `if (x is null) return;` | drop |
| disproven | "this endpoint has no `[Authorize]`" — the attribute is on the controller | drop |
| unverifiable from scope | claim rests on another repo's behaviour, a runtime value, business semantics | **keep** |
| you merely doubt it | "feels like a nitpick", "probably fine" | **keep** |

Three rules make this safe:

1. **Cannot-disprove ⇒ keep.** The reviewer had tools and read files you are not re-reading. Its
   context is a superset of yours, so "I can't confirm this" is not evidence against it.
2. **Never drop on severity or taste.** This gate removes *false* findings, not *minor* ones.
   Downranking a nitpick is the report's job, not the filter's.
3. **Dropped findings are logged, not vanished.** Every drop gets one line — finding + the specific
   counter-evidence (`file:line`) — in a collapsed `已濾除（誤報）` block at the end of the report.
   A silent filter is unauditable, and the reader must be able to overrule it.

## Step 3 — Root-cause dedup

Multiple reviewers scanning overlapping scope report the same thing from different angles, and one
systemic mistake shows up once per file it touches. Collapse both.

Merge when findings share **the same root cause and the same fix**:

- same defect reported by two lenses (review-engineer's "unbounded query" = performance-engineer's
  "WILL NOT SCALE" on the same path) → one item, both lenses credited
- the same mistake repeated across N files (missing `ConfigureAwait`, same unescaped interpolation
  pattern) → one item titled by the pattern, with every `file:line` listed under it

Do NOT merge when:

- the fixes differ, even if the wording is similar — two "missing validation" findings on different
  inputs are two findings
- severities differ — keep the higher-severity one separate rather than averaging it away
- they merely sit in the same file or the same module

Keep the highest severity in the group, and keep every anchor. Merging must never lose or hide a
location: an item covering 9 files lists all 9 anchors under it.

## Output

Report the counts so the reader can see the gate ran:

```
findings: N reported → M reported (dropped D 誤報, merged G groups, U unanchored)
```

**`N` counts findings only** — the classes this gate does not touch are not in it. That is what keeps it checkable: `N` lines up with the reviewer's own findings count, so a reader can hold the two numbers against each other, which they cannot do once suggestions are folded in.

**`N` is what the reviewers reported, not what they found.** A reviewer that loaded project review criteria may have suppressed items before reporting; those suppressions are counted in that reviewer's own section, in the vocabulary its criteria define, and this gate never sees them. Keep the two counts apart rather than folding them together — this gate's promise is only that *it* drops nothing on taste, and merging the numbers would quietly extend that promise over a filter it does not control.

Then the report body, in this order: anchored in-scope findings by severity → `unanchored` section →
`out-of-scope` section → collapsed `已濾除（誤報）` block. Omit any section that is empty; always keep
the counts line, so "nothing was dropped" is visibly different from "the gate never ran".

## Guardrails

- **Read-only.** This gate edits no code, changes no severity thresholds, and writes no files
  beyond the report it feeds.
- **Never invent a finding.** Triage only ever drops, re-anchors, or merges what reviewers reported.
- **Never re-review.** If a finding raises a new question about the code, that is a follow-up for
  the reviewer that owns it (`SendMessage`), not something to resolve here.
- **A reviewer's `NEEDS:` is not a finding** — it is an unresolved external fact and passes through
  untouched. Do not filter it, merge it, or treat its absence of evidence as counter-evidence.
- **Language**: report output in Traditional Chinese; code and quoted snippets verbatim.
