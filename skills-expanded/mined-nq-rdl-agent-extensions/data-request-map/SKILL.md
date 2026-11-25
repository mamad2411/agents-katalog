---
name: data-request-map
license: CC-BY-4.0
description: >-
  Propose evidence-backed RDL cohort source-table and query-builder resolver mappings
  from a request, scope, legacy answers.yaml or existing hand SQL; resolve grain,
  keys, timezone and units before SQL drafting. Supports a partial map.
argument-hint: '<request, scope path, answers.yaml, hand SQL path or resolver> [--autonomous|--co-develop]'
user-invocable: true
compatibility: RDL dataops DDL and query-builder column-spec metadata; inspect the checked-out schema and resolver API version.
allowed-tools: Bash, Write, Read, Glob, Grep, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — map

The **Data Engineer** runs mapping from the analyst's research decisions.
Return unanswered research choices to the Data Analyst; establish technical
source, key and join evidence with the engineer.

Invoke `/data-request:guardrails` first and follow its source hierarchy and **House defaults**.
Apply TUH `00200` without asking when no alternative facility scope is named: reuse
one standard assumption from setup's `tuh-facility` entry with its `upstream` marker.
Read `${CLAUDE_PLUGIN_ROOT}/skills/setup/references/recurring-decisions.rst` for wording
and original confirmation; mapping returns the assumption as a proposal/handoff, never initialises a store.
If the request explicitly changes the cohort's facility set (alternative/HHS/network scope), leave the TUH default out, carry the
analyst's recorded answer or return one facility-set question; do not intersect with TUH.
Arguments: `$ARGUMENTS`.

## Lift capture

Ordinary mapping needs no `.sqlreview/` setup. Mapping never initialises
`.sqlreview/`; stages that own the store (setup, bootstrap) still initialise it.
Before a mapping leads to hand SQL, inspect the pinned unit/resolver/tests and
silently publish a candidate for the target pipeline, following
`${CLAUDE_PLUGIN_ROOT}/skills/setup/references/lifts.rst`. Record the pin,
evidence and shortfall; no entry means no hand SQL. If the target path is not
yet known, pass the gap to draft and require capture before writing.

**Proposal-only:** if the run is read-only, the child repo has no `.sqlreview/`
yet, or you cannot write to it, publish nothing. Return the candidate ledger
entry as text, marked proposal-only. A proposal-only entry authorises no hand SQL:
none is committed or run, except exempt probes, until a writable run publishes the entry.

For probe proposals and reported evidence, follow **Probe disclosure control** in
`${CLAUDE_PLUGIN_ROOT}/skills/guardrails/references/release.rst`; gate exemption is not disclosure permission.

**Exempt probes:** an operator probe is outside the hand-SQL gate only when it is
aggregate-only, small-cell-suppressed and single-scan, returns no identifying
values (no patient identifiers, no staff or person keys; clinician and resource
names are not personal information), and feeds no delivered extract. Record any
`NOLOCK` use. Guardrails is the source of truth for these rules.
Classification and confirmation happen in `/data-request:lift` at close-out.

## Inputs

Read every supplied input and say which ones the mapping uses:

- The request, `cohort/request.json` or a confirmed scope.
- A legacy shell's `answers.yaml`, when there is no `cohort/request.json` and no
  confirmed scope.
- **From hand SQL:** existing hand SQL or a pipeline. Trace each output column,
  join and filter back to its requested concept and source. The SQL is evidence
  of intent, not of correctness; each hand-built block is a lift candidate.

Identify population, output grain, anchor, window and requested concepts. Bare
`measurement_granularity: Patient` is unconfirmed, not a requirement. Read guardrails
`references/grain.rst`: propose the grain from intake, prior SQL/delivery or requested
elements with source citations; preserve requested finer outputs and distinguish a
technical proposal from human confirmation. Reuse
a confirmed decision only when a supplied input records the human answer and it
applies to this mapping; otherwise label it unresolved. Autonomous mode never
supplies business decisions or confirmations. Inspect actual column specs, their
dataops `CREATE TABLE` comments, resolver code and tests. Verify the checked-out
resolver API from that source before proposing an API change.

**Ethnicity:** the records hold no ethnicity field. Map an "ethnicity" element to
Indigenous status from `PERSON_INFO`. Offer country of birth and preferred language
as optional surrogates; the requester or engineer decides. Record the limitation
that ethnicity is not held. Check the pinned library for surrogate units; a missing
unit is a lift candidate. Guardrails holds the convention.

## Lookup evidence for codes

When a mapping needs a discovered code, use `/data-request:lookup` and cite the
private lookup record's path, revision and labelled grid for that code. Carry its
label, source, search/expansion provenance, operator/date and limitations into the
mapping evidence. Distinguish observed candidates from analyst-selected codes;
a hit does not confirm clinical inclusion. A pending run, missing grid or unresolved
conflict remains unverified. Do not guess a code from its label or silently broaden
the analyst's selection. Lookup's command dependency may be unavailable; follow
its stop/engineer-reviewed-probe path, not replacement hand SQL. Apply the disclosure
section cited above before carrying lookup values into mapping; cite the evidence
without repeating exact population counts.

## Mapping output

Read guardrails `references/delivery.rst` before proposing delivery: estimate rows
for each output from available probe counts at its final grain and check text
length bands. Record oversized/potentially long-cell outputs as limitations;
near-limit estimates (within 10%) are undecided. Put the delivery choice to the
engineer, flagged for the analyst; carry unverified evidence and choices to draft.

Return one row per requested element (event, date or output) and candidate:
requested concept → table/column or resolver → source grain and join keys →
verified timezone/units → library support → evidence file and revision →
unresolved choice. Library support names the pinned unit or resolver that
expresses the row, or `none` (a lift candidate). When one table is hard to read,
split the rows into one table per output or source system with the same columns.
For competing candidates, explain the semantic difference and what evidence would
select one. Apply the encounter-mediated clinical-event pattern and indexed-bound
rules from guardrails. Mark missing metadata explicitly; do not fabricate a new
column-spec schema or resolve an ambiguity by matching names alone.

**Partial map:** when cohort concepts are confirmed but no data elements are named
yet, map the confirmed cohort concepts only. List the pending data elements
separately, each with the question that would settle it. Do not guess them.

**Autonomous:** complete the proposal using explicit requirements and verified facts;
leave choices requiring business judgement unresolved. **Co-develop:** show those
choices with their consequences and ask focused questions, then revise the proposal.
Without a mode flag, infer the mode from the user's request; ask only when that affects
a decision. In either mode, an unanswered question is not agreement.

Finish with the proposed mapping, evidence and remaining decisions. Hand a defined
mapping to `/data-request:draft`; use `/data-request:bootstrap` when formal scope confirmation
is wanted. A proposal does not update resolver code, column specs or human confirmations.
