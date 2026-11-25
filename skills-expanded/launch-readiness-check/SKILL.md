---
name: launch-readiness-check
description: "When the user wants to grade a full set of launch assets against the company canon before go-live. Reads the project SSOT and any stricter company claims register, then returns a go/no-go scorecard. Use for launch QA, pre-launch audits, and launch readiness. It is the Rung 4 gate. For cross-channel consistency outside a launch gate, see messaging-consistency-audit. For the launch sequence itself, see market-entry-orchestration."
metadata:
  version: 1.0.0
---

# Launch Readiness Check


**Use the company SSOT when present:** follow `../_shared/ssot-consumption.md` and the project manifest to load only relevant approved context. Preserve covered strategic meaning while keeping this skill’s existing scope and frameworks.

You are the last gate before go-live. You grade every launch asset against one company canon and return a go/no-go scorecard. One banned claim in one asset is enough to stop the launch.

Deliver the scorecard, not advice about how to review copy.

## Launch-wide readiness and independent reviews

Read the approved launch plan and required scope, not only supplied assets. Inventory review coverage, canon version, approvals, enablement/training, product availability, operational handoffs and measurement readiness.
Consume current `output-quality-check` reports and `messaging-consistency-audit` results; they retain separate responsibilities. Missing/stale required reports are unverified dependencies, not implicit passes.
The asset claim checks below apply stricter launch safeguards and do not replace those reviews. A clean asset alone cannot clear the launch.
Record each readiness item with requirement, evidence, owner, status, blocker, resolve-by milestone and approval. Product/Sales/CS/RevOps/analytics owners confirm availability and operational readiness.
Launch-wide Ready requires all required assets, review results, approvals, enablement, availability, handoffs and measurement gates to pass. Unknown coverage or an unresolved required dependency means Not ready.
Append this launch-wide checklist and remediation ownership to the scorecard; preserve evidence labels and human launch approval.


## Before Starting

**Load the shared references:**
- `../_shared/launch-stages.md`: Rung 4 entry criteria, the gate, and the handoff contract.
- `../_shared/evidence-gaps.md`: Sourced, Assumed, and Gap labels, and the rule for `[Gap: ...]` placeholders.

**Load available canonical sources.** If the company's rule book exists at `../[company]-messaging/`, load its `references/` in this order:
1. `canon.md`: the Approved numbers table and the canon version.
2. `claims.md`: Approved (A), Conditional (C), and Banned (B) claims, plus competitor rules.
3. `terminology.md`: product names, spelling, and voice.
4. `audiences.md`: the overlay each asset is written for.

Read the rule book's own `SKILL.md` review mode too. Its severity definitions win where they are stricter than the ones below.

Also load the active project's manifest-mapped SSOT files using
`../_shared/ssot-consumption.md`. The SSOT is authoritative for covered strategic
claims. Apply any stricter legal or claims-register restrictions too. If the two
sources conflict, flag the conflict and stop the affected check for human review.
Do not resolve it by silently preferring an asset or rewriting either canon.

**If neither a company rule book nor an applicable SSOT exists, stop.** Write: "No company canon found. Establish the company messaging canon before launch review." Never grade against memory or a generic standard. If only the SSOT exists, use its mapped core and evidence files as the canon for the checks below. If both sources exist, SSOT owns covered strategy and the rule book adds any stricter claims, legal, terminology, or launch constraints. Flag a conflict and hold the affected check for human review.

**Collect the asset set.** List every asset with its type (email, landing page, deck, battlecard, social, other) and its canon stamp. If the user says more assets exist than they pasted, grade what you have and list the rest as not reviewed.

An incomplete declared launch set cannot receive a launch-wide Ready verdict.
Report the supplied assets' individual results, but hold the launch as Not ready
until every required asset is reviewed. If scope is unknown, state that coverage
cannot be confirmed rather than imply launch-wide clearance.

## Core Principles

**One canon, every asset.** Grade every asset against the same canon version. Never mix versions in one scorecard.

**Every flag cites its rule.** Name the file and the rule ID, such as `claims.md B4` or `canon.md section 5, Customers row`. For terminology, name the file and the row, such as `terminology.md, Product names`. A flag with no rule is an opinion. Cut it.

**A Block anywhere means Not ready.** The launch verdict is only as good as the worst asset.

**Never invent flags.** A clean asset gets zero claim flags and an asset-level Ready verdict. Launch-wide clearance still requires every readiness gate. Padding the table to look thorough erodes trust in the real Blocks.

**Grade the asset, not the brief.** A good reason for a claim does not make it on-canon.

## Severity

| Severity | Use for |
|---|---|
| **Block** | A Banned claim (B rows). A number that is wrong, unscoped, or unsupported by approved canon evidence. A Conditional claim (C rows) missing its qualifier. A regulatory or legal misstatement. Anything stated as done that is still pending. A named competitor in customer-facing copy when applicable canon prohibits it. A `[Gap: ...]` placeholder with no fallback line. |
| **Fix** | Off-canon positioning or category. A wrong product name or spelling. Table stakes leading the message. A `[Gap: ...]` placeholder that still needs its fallback swapped in. A missing or stale canon stamp on the asset. |
| **Suggest** | Voice, emphasis, or a stronger on-canon line. |

## Process

### 1. Confirm the canon
Name the company, applicable canonical sources, and version in the scorecard. Use the rule book version from `canon.md` when present. Otherwise, stamp the SSOT client and relevant `last_reviewed` date or decision record. Do not mix canon versions in one scorecard.

### 2. Review each asset
For each asset, check it line by line against manifest-mapped SSOT positioning, product truth, persona, evidence, and anti-patterns, plus `claims.md`, the Approved numbers table in `canon.md`, and `terminology.md` when the rule book exists. Cite the exact SSOT file and section or rule ID, such as `claims.md C2` or `core/02-product.md, capabilities`. Log the issue's severity, exact asset text, rule, and on-canon fix.

Give each asset its own verdict:
- **Ready:** no Block and no Fix.
- **Ready after Fix items:** Fix items only.
- **Blocked:** one or more Block items.

### 3. Roll up
Count assets and flags by severity. Pick the top blocking issues: every Block, ordered by how many assets repeat it, then by customer exposure (web and email before internal decks).

### 4. Give the launch verdict
- **Ready:** every required launch asset is Ready and every required launch-wide readiness gate has passed.
- **Ready after fixes:** every required launch asset has been reviewed, no asset is Blocked, at least one has Fix items, and all required non-asset readiness gates have passed. Launch only after the Fix items close. An unresolved required gate means Not ready.
- **Not ready:** any asset is Blocked, a required launch asset is not reviewed, or any required launch-wide gate is unresolved.

Write the verdict as one line and put it first.

## Output Format

The verdict comes first because the scorecard is a decision document. The "Inputs and assumptions" note follows the header, as in market-entry-brief.

```
**Verdict: [Ready / Ready after fixes / Not ready].** [One line: the count of Block and Fix items, and the deciding issue.]

Artifact: go/no-go scorecard
Rung: 4
Canon: [company rule book version and/or SSOT client plus reviewed date]
Built from: [canonical source references]; [n] launch assets

## Inputs and assumptions
| Item | What was used, missing, or assumed | Label |
|---|---|---|

## Rollup
| Total assets | Block | Fix | Suggest | Assets Ready | Ready after Fix items | Blocked |
|---|---|---|---|---|---|---|

## Top blocking issues
| # | Issue | Rule (file + ID) | Assets affected |
|---|---|---|---|

## Asset scorecard
| # | Asset | Type | Asset stamp | Block | Fix | Suggest | Asset verdict |
|---|---|---|---|---|---|---|---|

## Flags by asset
### [Asset name]
| # | Severity | Asset text | Rule broken (file + rule ID) | On-canon fix |
|---|---|---|---|---|
[Or one line: "No issues. Ready."]

## Not reviewed
[Assets named but not provided, or "None."]

## Evidence gaps (top five)
[Ranked per ../_shared/evidence-gaps.md: open Gap placeholders and out-of-canon claims first.]

Canon [same stamp]
```

## Common Failure Modes

- A flag with no file or rule ID.
- Returning Ready after fixes when one asset has a Block.
- Grading against memory because the company canon was missing.
- Inventing Suggest flags on a clean asset.
- Restating each asset before flagging it.
- Mixing two canon versions in one scorecard.
- Leaving off the canon stamp.

## After Delivering

If the verdict is not Ready, offer to run the company rule book's review mode on the Blocked assets to draft corrected versions. Route any out-of-canon claim that should become canon to the canon owner for the next version.

## Output Rules

- No em dashes in output.

## Related Skills

- **market-entry-orchestration**: Runs the launch chain this check gates
- **marketing-copy**: Polishes assets after the Fix items are closed
- **sales-enablement**: Rebuilds decks and battlecards that come back Blocked
