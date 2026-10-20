---
name: fixedness-audit
description: Use this skill when someone wants to find what their accumulated professional material is worth NOW — recordings, transcripts, dead course modules, client intake forms, failed offers, idiosyncratic methods — after a market shift changed what it is worth. The Fixedness Audit beats the functional fixedness that hides the answer: it inventories the archive, asks of each asset "under the new selection pressure, what is this actually good for now?" (never "how do I improve it?"), scores the answers, and returns a ranked list with the top 1-3 to act on this week. Trigger phrases include "run a fixedness audit", "run an exaptation audit", "audit my archive", "what is my old material worth now", "I have years of content sitting there doing nothing", "repurpose my back catalog", "AI killed my offer — what do I still have", "what am I sitting on". Also use when someone describes competence that stopped converting and asks what to do with what they already built, even if they never say fixedness or exaptation.
---

# The Fixedness Audit

Re-price the substrate someone already carries, under a shift that changed what it's worth.
Output: a ranked list, top 1-3 flagged for immediate action.

**Why the two names.** *Functional fixedness* (Karl Duncker, 1935/1945 — people can't see a tack
box as a platform because they've filed it under "container") is the psychological reason the
owner can't see what their own archive is now good for. *Exaptation* (Gould & Vrba, 1982 — a
structure built for one function that turns out to be valuable in a different one) is what has
actually happened to the asset. The audit is named for the blind spot it defeats; the mechanism
it uncovers is exaptation.

## Gotchas — read before running

1. **This is not repurposing.** Repurposing keeps the function and changes the channel (webinar
   → YouTube clips). Exaptation keeps the *material* and changes the *function* (the webinar
   recordings become the training corpus for a diagnostic, and nobody watches them). If a
   proposed new function is the old function in a new wrapper, score `pressure_fit` low and say
   why. Most first-pass answers fail here — check every one.
2. **The selection pressure is a required input, not a preamble.** You cannot answer "good for
   what now?" without "now" being specified. If the user hasn't named the shift, stop and get it
   (Step 0). An audit run against a vague pressure produces confident garbage.
3. **"No new function" is a legitimate verdict** and the script scores it 0. Resist the pull to
   find value in everything — an audit that recommends all 40 assets recommends nothing. Expect
   half the archive to score zero. That honesty is what makes the top of the list credible.
4. **Judge the substrate, not the artifact.** A dead product's value is rarely the product. It's
   the 200 intake forms that shipped with it, the objection log, the failure cases. Look under
   the deliverable for the accumulated reality.
5. **The scan is a partition, not a search.** Every file lands in exactly one asset cluster.
   If the clusters come back too coarse (one asset = 2,000 files), re-run with `--depth 3`.
   Too granular (80 assets of 2 files)? `--depth 1`.
6. **Never invent file contents.** If an asset's nature isn't clear from its path, category,
   and sample filenames, read a file or two before judging it. Guessing here is the failure
   mode that produces a plausible, useless ranking.

## Steps

| # | Step | Classification | How |
|---|---|---|---|
| 0 | Name the selection pressure | inference | Elicit + sharpen with the user |
| 1 | Inventory the archive | **code** | `audit.py scan` |
| 2 | Re-price each asset | inference | One asset, one judgment, fixed schema |
| 3 | Score + rank | **code** | `audit.py rank` |
| 4 | First move for the top 1-3 | inference | One concrete action each |

Steps 1 and 3 are deterministic and must never be done by reading and reasoning about files
by hand — the scoring weights and the ranking exist so the result is reproducible.

---

### Step 0 — Name the selection pressure (inference)

Ask, and don't proceed on a vague answer:

> What changed, and what does it now reward that it didn't before?

Bad: "AI." Good: "Buyers can generate a competent strategy document in four minutes, so they no
longer pay for the document — they pay for someone who can tell them which of the four they
generated is wrong."

Write the sharpened pressure down verbatim. Every judgment in Step 2 is relative to it, and it
goes at the top of the final report.

### Step 1 — Inventory (code)

```bash
uv run --script ~/.claude/skills/fixedness-audit/scripts/audit.py scan \
  ~/Documents ~/Articles ~/vault --out inventory.json
```

Read-only. Flags: `--depth N` (path components per asset cluster, default 2), `--min-files N`
(default 2), `--limit N` (default 60, largest-substrate first). Exit 2 means nothing found —
check the roots or lower `--min-files`.

Ask the user which roots to scan and what is off-limits before running. If assets live off
disk — Zoom cloud, YouTube, a course platform, a CRM, relationships, undocumented methods —
read `references/off-disk-assets.md` and add them manually to the judgment file.

### Step 2 — Re-price each asset (inference)

For each asset in `inventory.json`, one judgment. **The question is not "how do I improve
this?" It is "under the pressure named in Step 0, what is this actually good for now?"**

Prompts that break the frame, in order — use them when the obvious answer is the old function:
- What did this accidentally accumulate that nobody was collecting on purpose?
- Who would want this that the original buyer was not?
- What is now scarce that this is dense in? (judgment, failure data, real language, edge cases)
- If a competitor with the best model but none of this history tried to fake it, where exactly
  would they get caught?

Emit a JSON list. Every field required; `id` must match the inventory.

```json
[{"id": "A001",
  "new_function": "What it is good for now — one sentence, states the FUNCTION not the format",
  "buyer": "Who wants that function, specifically. Not 'coaches'.",
  "evidence": "What in the asset proves the claim — counts, spans, specifics from the scan",
  "pressure_fit": 4, "substrate_depth": 5, "exclusivity": 4, "distance": 2}]
```

Scoring, 0-5 each. Anchor at 0 and 5; do not cluster at 3.

- **pressure_fit** — does the pressure from Step 0 *create demand* for this new function?
  `0` = no new function found, or the proposal is the old function repackaged (score 0 freely).
  `5` = the shift is the reason someone would pay for this now.
- **substrate_depth** — how much irreplaceable accumulated reality is in it?
  `0` = thin, generic, reconstructible from a prompt. `5` = years of real specifics, failures,
  and language that only running the actual business produces.
- **exclusivity** — could a competent rival with the best model rebuild this in a quarter?
  `0` = trivially. `5` = not without living the same years. Scores of 0-1 are capped at 40 by
  the scorer, on purpose — commodity substrate doesn't get to top the list.
- **distance** — inverted effort. `5` = shippable this week roughly as-is. `0` = a year of work.

One asset per judgment. Do not bundle. If two assets only work together, say so in
`new_function` and score them as one, dropping the other.

### Step 3 — Score and rank (code)

```bash
uv run --script ~/.claude/skills/fixedness-audit/scripts/audit.py rank \
  judgments.json --inventory inventory.json --out fixedness-list.md
```

Exit 1 means the judgments failed validation — it prints exactly what's wrong (bad ids,
out-of-range scores, stub prose like "n/a"). Fix and re-run; it's idempotent. `--dry-run`
validates and writes nothing. `--json` for the scored records.

Weights are fixed at `pressure_fit .30 · substrate_depth .25 · exclusivity .25 · distance .20`.
Do not re-weight per run — the whole point is that two people scoring the same archive get a
comparable answer.

### Step 4 — First move (inference)

For each recommended asset (top 3, score ≥ 50), append one concrete action that can start
within a week: what to make, from what, for whom, and what would prove it wrong. No roadmaps.
If nothing scored ≥ 50, say so plainly and name the highest-scoring asset with what would have
to be true for it to clear the bar. Do not lower the bar.

## Deliver

Hand over `fixedness-list.md` plus the Step 0 pressure statement and the Step 4 moves. Keep
`inventory.json` and `judgments.json` — re-running Step 3 after a scoring argument costs nothing.

Non-AI-native users, or anyone who wants to run this on paper: point them at the companion
worksheet, `~/Articles/exaptation-flagship/artifact/fixedness-audit-worksheet.md`.

## Verify

`uv run --script ~/.claude/skills/fixedness-audit/scripts/audit.py selfcheck` — asserts the
scoring gates, the validator, the ranking order, and that the scan partition is exhaustive.
Run it if you change the weights or the rubric.
