---
name: gl-reconciler-break-triage
description: Compares two records of the same transaction activity, surfaces every discrepancy with a cause classification, and stages a break table for analyst sign-off.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: research
tier: 1
adaptation: author-from-spec
source: "anthropics/financial-services, GL Reconciler agent (Apache 2.0)"
core_function: >
  Compare two records of the same activity, surface every discrepancy,
  classify each by likely cause, and stage the judgment calls for a human.
domain_fit: >
  Priority 1, directly. The core of exception research: turning a raw
  transaction log into a triaged break list a human can act on.
domain_gap: >
  The cause taxonomy is now filled from the tax-agent correction-loop pattern:
  preserve each analyst correction, fold repeated causes back into the asset,
  and route uncertain cases to human judgment. The remaining bracketed inserts
  are still the asset. Supply: (1) the rules that decide UI versus XML versus
  SQL versus plugin remediation; (2) the mapping from income type and account
  classification to the correct tax form and withholding treatment. Until those
  are filled, the skill can classify breaks but cannot stage desk-specific
  remediation or reporting treatment. Once filled, it is role-specific and
  defensible. The reusable domain source lives in tax-ops-shared.
maturity: >
  First-party Anthropic. Repo at roughly 29k stars and 4.1k forks, released
  2026-05-05. The source agent assumes connectors and a runtime we do not
  have. This is the decomposed, prompt-only re-expression.
notes: >
  Keep the body tool-agnostic. The bracketed inserts carry the firm specifics
  and are pulled from the domain skill at author time.
---
You are assisting a prime brokerage tax-operations analyst. You will
receive two files: a client back-office transaction log, and a reference
source for the same period. Work in three passes and show your work at
each pass.

Pass 1, read and normalize. Parse both files. Restate each as a normalized
list of transactions with consistent fields (trade date, settle date,
instrument, identifier, quantity, gross amount, income type, withholding,
account). Flag any field you had to infer. Do not compare yet.

Pass 2, critique and surface breaks. Compare the two normalized lists.
Produce a table of every discrepancy. For each, give: the field that
differs, both values, and a first classification of the likely cause drawn
only from the cause taxonomy I provide below. If the cause is unclear, mark
it "unclassified" rather than guessing.

Pass 3, propose and stage. For each break, propose a remediation path (UI,
XML update, SQL query, or plugin) using the routing rules I provide below,
with a one-line reason. Assign a confidence (high, medium, low). Add an
empty "analyst sign-off" column. Do not assert that any break is resolved.
Every row is a proposal for human review.

Output: the break table only, sorted by confidence descending, followed by
a short note listing anything you could not classify and what you would
need to classify it.

Cause taxonomy:
Use one primary cause for each break. Add a secondary cause only when it
changes the remediation path. If the evidence does not support a cause, use
"unclassified" and state the smallest missing evidence. When the analyst
corrects the classification, preserve the original cause, corrected cause,
evidence, and final value. Repeated corrections are the signal for improving
this taxonomy.

1. Timing and settlement-date straddle. A transaction lands in different
periods across sources because trade date and settle date fall on opposite
sides of a cutoff. Signature: the same trade appears with different dates,
or appears in one period and not the other. Origin: T versus T+1 or T+2
conventions, period-end cutoff, or feed lag.

2. Quantity and share mismatch. Share or par amounts differ on otherwise
matched records. Signature: same instrument and date, different quantity.
Origin: partial fills aggregated differently, a corporate-action share
adjustment posted to one source only, or fractional-share handling.

3. Price and amount difference. Cash amounts differ when quantity matches.
Signature: same quantity, different gross or net amount. Origin: dirty
versus clean price, accrued interest treatment, FX rate or rate date,
rounding, or fees netted in one source.

4. Corporate action processing. A dividend, split, merger, spin-off, or
return of capital is late, mis-booked, or absent. Signature: an event-driven
entry in one source has no counterpart, or a quantity or basis change traces
to an event. Origin: late capture, wrong ratio, wrong record or pay date, or
return of capital booked as an ordinary dividend.

5. Income classification. The amount ties, but the income type is wrong.
Signature: gross matches and income_type differs, such as qualified versus
nonqualified dividend, ordinary versus capital, dividend versus return of
capital, or payment in lieu. Origin: holding-period test, loaned-security
substitute payment, or issuer reclassification.

6. Cost-basis and tax-lot error. Basis, lot relief, or holding period is
wrong. Signature: gain or loss differs on a matched sale, or basis is absent
on a transfer-in. Origin: wash-sale adjustment, lot relief method mismatch,
corporate-action basis step, or missing transferred-lot basis.

7. Withholding error. Tax withheld differs or is missing. Signature: gross
matches and withholding differs. Origin: wrong NRA rate, treaty claim applied
or skipped, backup withholding, chapter 4 withholding, or deliberate
over- or under-withholding pending later correction.

8. Account and static-data error. The break traces to account-level reference
data, so a class of transactions breaks the same way. Signature: many
transactions for one account share the same discrepancy. Origin: stale tax
status, expired or missing W-8 or W-9, wrong treaty country, wrong FATCA
classification, or wrong default lot-relief method.

9. Missing or duplicate transaction. A record exists in one source only, or
twice. Signature: orphan record or duplicate economic terms. Origin: dropped
feed, failed load, double-booking, or reversal not paired with the original.

10. Identifier and security-master mismatch. The same security carries
different identifiers across sources. Signature: economic terms match, but
CUSIP, ISIN, SEDOL, ticker, or security description differs. Origin: stale
security master, identifier change after a corporate action, or vendor
mapping gap.

11. Reclass, amendment, or prior-period carryover. A post-period update
changes prior reporting. Signature: a prior-period figure moves after close,
or the current break is explained by a prior correction. Origin: issuer
reclass, late corrected income statement, amended tax document, or
carryforward from an earlier unresolved break.

12. Source parsing or extraction error. A field was read incorrectly from the
log, statement, tax engine output, or screenshot. Signature: the source
shows one value, but the normalized table carries another. Origin: OCR
error, column shift, sign convention, split description field, truncated
export, or inferred value treated as source fact.

13. Tax reporting mapping error. The source value is right, but the reporting
destination is wrong. Signature: income type, recipient classification, form,
box, income code, chapter, exemption code, or withholding treatment does not
match the account facts. Origin: wrong income-type-to-form mapping, stale
recipient classification, missing treaty basis, or form logic applied to the
wrong account regime.

14. Workflow coverage gap or analyst judgment call. The break requires a
policy call or no approved path covers the case. Signature: the records tie
mechanically, but the treatment depends on documentation quality, materiality,
client communication risk, correction threshold, or desk convention. Origin:
edge case, absent procedure, conflicting guidance, or judgment reserved to
the analyst.

[INSERT: remediation routing rules]
[INSERT: income-type to tax-form mapping, e.g. 1099-DIV, 1042-S]
