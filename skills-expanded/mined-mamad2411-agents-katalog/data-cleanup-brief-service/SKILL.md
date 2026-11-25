---
name: data-cleanup-brief-service
description: Design and price a productized weekly service that turns a client's messy recurring CSV/spreadsheet exports into a clean, verified one-page change brief — deterministic data cleanup first, AI narrative only after the numbers are locked. Use when someone wants to build a service around recurring data cleanup, is asked to package "spreadsheet cleanup" or "reporting" work into a subscription, or wants a concrete, low-hype worked example of pricing an early AI-adjacent service.
---

# Data Cleanup + Brief Service

Source: reviewed from an uploaded photo batch — a 6-image "AI Income
Playbook" carousel (@zhiprompts, TikTok), each card citing "SOURCE CHECKED
— github.com" against a real repo (link partially obscured by the
carousel's own watermark in the screenshots, so the specific repo wasn't
independently confirmed — treat the methodology as the deliverable, not
the unconfirmed citation). Unlike several other carousels reviewed into
this repo, this one has no clickbait framing or inflated claims — it
explicitly labels its own $300/month price as "a testable example" and
tells the reader to "validate the sample package with a real buyer before
treating it as recurring revenue." That honesty is worth preserving, so
this skill keeps it.

This is a companion to `content-repurposing-service` (same "productized
weekly service" shape) but for a different, narrower service: recurring
data cleanup and reporting, not content. `the-productize-yourself-blueprint`
covers the general pattern of packaging expertise into a service;
this skill is a concrete, worked example the same way
`content-repurposing-service` is one for content.

## The service, in one line

Target a client with recurring messy exports (ad/lead/sales CSVs) and a
recurring decision to make from them. Sell the recurring decision, not the
recurring spreadsheet — deterministic code does the cleanup, AI drafts the
narrative only after the numbers are locked and verified.

## 1. Find the target: recurring input + recurring decision

Look for a small agency (or any team) combining the same export sources
every week before a recurring meeting or client call — e.g. merging ad
platform, lead-gen, and sales CRM exports every Friday. The service only
works if both halves repeat: the same export sources *and* the same
question the client asks of them. A one-off cleanup isn't a service; a
recurring input feeding a recurring decision is.

## 2. Lock the mapping before writing any code

Collect the original CSVs and get the client to approve one column mapping
covering names, dates, identifiers, missing-value handling, and duplicate
rules. This mapping is the contract for every future run — write it down,
get sign-off, and treat it as versioned. Keep raw files unchanged (never
overwrite the source export), flag invalid rows rather than silently
dropping them, and version every schema change instead of quietly
patching the mapping.

## 3. Do the cleanup deterministically, in code — not in the model

Use pandas for familiar Python transforms, or DuckDB to query the CSVs
directly, whichever fits the client's actual formats better. Save the
exact cleanup rules as code (not as a one-off prompt), because
deterministic data cleanup has to happen *before* any language model
touches the data. Concretely: normalize dates and column names, deduplicate
by the approved key from step 2, and export a clean, versioned audit file
that both you and the client can point to.

## 4. AI drafts the narrative — after the numbers, never instead of them

Only once the clean file and calculations are final, use AI to draft a
one-page narrative from it — then verify every number in that narrative
against the clean file before it goes out. Deliver exactly three changes,
three open questions, and three next actions per brief, not an open-ended
essay. Discipline that keeps this trustworthy: separate facts from
hypotheses explicitly, link every number in the narrative back to a
specific row or query (so any claim is traceable), and always have a human
review the narrative before send — the AI drafts, it doesn't ship
unsupervised.

## 5. Price a sample package, then validate it against a real buyer

A concrete package to test, not a claim about guaranteed demand: four
scheduled runs a month, a 48-hour turnaround, one correction round
included, at a sample price point (the source uses $300/month as an
example figure to validate — pick your own based on the client's actual
willingness to pay). Operating rhythm: client submits raw exports by
Thursday, you deliver the brief every Friday, and any new data source or
schema change triggers a re-scope conversation rather than silently
absorbing scope creep into the same price.

**Before treating any price as recurring revenue, validate the sample
package with a real buyer.** The price in this skill is a starting
hypothesis, not a benchmark.

## Prompt/methodology, cited in plain text

The source carousel's five cards, reproduced verbatim for reference:

```text
#01 — An agency merging 4 exports
Target a small agency that combines the same ad, lead, or sales CSV
exports every Friday before a client call.
How to sell it: Recurring input plus a recurring decision can support a
service. Same export sources. Same weekly cleanup. Same client questions.

#02 — CSVs + one column map
Collect the original CSVs and one approved mapping for names, dates,
identifiers, missing values, and duplicate rules.
How to sell it: The mapping is the contract for every future run. Keep
raw files unchanged. Flag invalid rows. Version schema changes.

#03 — Pandas or DuckDB
Use pandas for familiar Python transforms or DuckDB to query CSV files
directly; save the exact cleanup rules as code.
How to sell it: Deterministic data cleanup comes before the language
model. Normalize dates and columns. Deduplicate by approved key. Export a
clean audit file.

#04 — Clean file + change brief
Use AI only to draft a one-page narrative after calculations are
complete, then verify every number against the clean file.
How to sell it: Deliver three changes, three questions, and three next
actions. Separate facts from hypotheses. Link every number to a row or
query. Human-review the narrative.

#05 — 4 runs. 48 hours. 1 revision.
Position a sample $300 monthly package around four scheduled runs, a
two-day turnaround, and one correction round.
How to sell it: The price is an example to validate, not guaranteed
demand. Client submits by Thursday. Deliver every Friday. Re-scope new
sources or schemas.
```

## Related skills in this repo

- **content-repurposing-service**: the sibling worked example for a
  productized content service — same weekly-cadence, human-approval-gated
  shape, different deliverable.
- **the-productize-yourself-blueprint** / **the-specific-knowledge-excavator**:
  the general pattern this is one concrete instance of.
- **saas-idea-validator**: run this against the sample package from step 5
  before quoting a real client, given the source's own "validate before
  treating as revenue" caution.
- **lean-software-stack**: pandas and DuckDB are both free/open-source —
  this service needs no paid tooling to deliver.
