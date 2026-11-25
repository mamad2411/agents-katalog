---
name: data-request-lookup
license: CC-BY-4.0
description: >-
  Help a Data Analyst discover source codes for an order field, clinical event or
  event set, medication, diagnosis or procedure, or pathology task assay. Choose
  the lookup family and direction, generate a count-only probe for a human to run,
  then write a private lookup record for mapping. Never runs a database query or
  chooses the clinical code set for the analyst. Use when an analyst needs a source
  code and has no confirmed code list.
argument-hint: '<lookup question or private lookup record>'
user-invocable: true
compatibility: >-
  RDL request repositories; query-builder lookup depends on nq-rdl/query-builder#231
  (open and unmerged when authored). No released command version is assumed;
  verify the installed pin, help and private lookup documentation before use.
allowed-tools: Bash, Write, Read, Glob, Grep, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Data Request — lookup (Data Analyst)

Use during the analyst's answers-filling pass before the engineer's
`/data-request:bootstrap`, or when `/data-request:map` needs code evidence.
`/data-request:intake` guides that pass and calls this skill for code discovery; read
`${CLAUDE_PLUGIN_ROOT}/skills/setup/references/analyst-intake.rst` for its record.
The analyst owns clinical inclusion, exclusions and code-set edges; the engineer
owns source and implementation questions. A lookup hit is not clinical approval.

Invoke `/data-request:guardrails` first. Arguments: `$ARGUMENTS`.
This public skill holds only the workflow, not local schema facts, code values
or SQL. Keep generated scripts and disclosure-controlled lookup records in the
private child repository of the request; keep original grids only in a results
store allowed by the disclosure section below; never copy them into this catalog.

## Verify the private reference first

The command and lookup documentation depend on
[query-builder #231](https://github.com/nq-rdl/query-builder/issues/231).
That issue is a proposal, not proof of an installed capability. Its private home
is spec 020, `specs/020-iemr-code-lookup/` on branch `020-iemr-code-lookup`.
Read that spec and its research; verify against the installed dependency pin,
implementation, tests and current dataops DDL before generating a probe.
Record exact source paths and revisions; draft docs do not establish released support.

Use the private docs for the table chains and all storage/read rules. The private
supporting sources are `rdl-ide-settings/snippets/SQL/`, the child-repository
lookup probes located through private query-builder #231 and spec 020, query-builder
spec 017 research R12/R13 (merged in nq-rdl/query-builder#198), and the dataops
catalogue YAML/DDL. Historical snippets and probes are evidence to reconcile,
not authority to copy SQL blindly.

Read each very large table only through a temp table of keys; the private reference
says which tables and how. Consult that reference
for latest-row selection, identifier representation, label matching, validity,
schema placement, collation and source-timezone handling. State no local rule
from memory. If sources conflict or the docs leave a rule unresolved, show the
private locations and hand the question to the engineer before dependent work;
do not select a winner or patch the generated SQL.

## Choose and generate

1. **Capture the question.** Read request/intake/scope and any earlier lookup
   record. Record search terms verbatim, why they were chosen, the source system
   and intended clinical meaning. Missing clinical choices go to the analyst;
   missing technical bounds go to the engineer. Never invent a code or broaden
   a supplied code set.
2. **Choose the family:** order field; clinical event code or event set;
   medication; diagnosis or procedure (ICD-10-AM, ACHI, SNOMED CT); pathology task
   assay. Record the choice and rationale. Family selection does not establish
   command support: #231 proposes no diagnosis/procedure builder and supplies no
   task-assay command syntax. For an unsupported family, stop and hand off or
   use an engineer-reviewed probe under the guardrails exemption below.
3. **Choose the direction for an order field.** Forward discovers configured
   fields from order-type search terms. Reverse discovers fields actually
   recorded on a narrowed order set, rather than merely configured fields.
   Reverse needs an evidenced order type and a short date window first; record
   bounds and their source. Do not replace reverse with an unbounded scan. For
   other families, record the search/expansion route supported by the private docs.
4. **Check availability, then generate with `query-builder lookup`.** Inspect
   installed help without connecting to a database. At the interface level #231
   proposes order-type terms for forward discovery, order type and date bounds
   for reverse discovery, event terms/set expansion, and medication terms.
   Invoke it only after the installed help/docs confirm it prints a count-only
   script to stdout and opens no database connection; otherwise stop and hand off
   to the engineer. The proposed JSON format supplies a manifest of labelled grids;
   verify support before using it. Use only options documented by the installed
   version, not guessed flags. Save the invocation, pin, script and available grid
   manifest privately.

**Dependency unavailable:** if the command, family, private reference or required
rule is unavailable, do not write hand SQL. Stop, mark the lookup blocked and hand
the question, terms, family, bounds and missing capability to the engineer.
Alternatively use an existing engineer-reviewed probe unmodified, only when it
satisfies `/data-request:guardrails`; record its review evidence and provenance.
Any change to terms, bounds or SQL, or rerun of a generator with new terms, goes
back to the engineer for review: that is hand SQL in effect. This is not permission
for the agent to invent a replacement query or run one.

## Human run and paste-back

Before handoff, check that the probe returns only codes, labels and counts, with
matched-term provenance so short-term collisions remain visible. No patient
values, patient dates, identifiers, staff/person keys or free-text results.
Read **Probe disclosure control** in
`${CLAUDE_PLUGIN_ROOT}/skills/guardrails/references/release.rst` before proposing,
reporting or recording a probe. That section owns the effective floor, rounding,
complementary controls, rare-label folding and perimeter rules; gate exemption is
not disclosure permission. Distinct-code/label inventory counts use its structural
count treatment, including the folded-label-total exception; counts of cases or
events behind each code are population counts, not structural inventory counts.
Confirm the script's population-count floor equals the effective F from Probe
disclosure control; if the installed command cannot take F, stop and hand off.
Never accept a paste-back exposing below-F population cells.
Follow guardrails for bounded single-scan probes, isolation disclosure and no
delivered-extract use. If the disclosure policy or probe conditions cannot be
verified, stop for engineer review, not a live test.

The authorised human runs the saved script in SSMS and pastes the labelled grids
back, formatted under that disclosure section. The agent runs no query, including
through a database tool or connection helper. Ask for missing grid labels or run
provenance; no paste-back means no observed code evidence. If exact population
counts are pasted, do not repeat or commit them: ask for formatted output and
apply the section before writing any text. Unexpected patient data must not be
reproduced or stored as a lookup record: stop and return the unsafe probe to the engineer.

Check term collisions and distinguish no hit, suppressed count and missing grid.
Do not reconstruct suppressed counts or treat missing evidence as zero. Separate
candidate codes from analyst-selected codes; send ambiguous clinical matches to
the analyst and technical/schema conflicts to the engineer. A folded "other" row
is not code evidence for its hidden members; do not recover or list them in the record.

## Private lookup record

Ask the analyst/engineer where to keep the Markdown record in the private child
repository and record the chosen path; there is no default path. Commit only the
disclosure-controlled record there so map can cite its path and revision. A private
commit is not automatically RDL-only: classify its perimeter under the disclosure
section before writing it. A committed record that map cites is handover tier unless
excluded from the handover set. This is not a new `.sqlreview` document type. Use
the following fields (no live values belong in this public template):

- **Question and context:** request/intake/scope citation and revision, intended
  meaning, family, direction/route and rationale.
- **Search:** exact terms and their rationale; order type/date bounds if needed,
  with source and timezone basis from the private reference.
- **Provenance:** private docs/DDL/probe paths and revisions, installed library
  pin, exact generation invocation, saved script and labelled-grid manifest path
  (or explicitly unavailable); for a fallback, engineer review evidence. Record the
  disclosure perimeter, assessment/approval source and formatting provenance.
- **Run:** actual execution date/time and timezone, environment, who ran it and
  pasted-grid location. Use an operator handle, never an email or workstation
  identity, following intake's actor rule. Never invent execution or approval.
- **Candidates:** one row per code with its label, source table/resolver, matched
  term or expansion origin, labelled-grid citation and disclosure-controlled count
  as shown, classified as structural or population under the disclosure section.
  Keep schema names and code values here privately, not in the skill.
- **Disposition:** selected, rejected or unresolved, with rationale; analyst
  decisions retain actual actor/date/source. Record no hits, missing grids,
  limitations, collisions and engineer questions explicitly.

Before a run, record only the proposal and blocked/pending state; never label it
OBSERVED. After paste-back, label observations with their scope and cite the
original results in their access-controlled store, not by copying exact population
counts into the record. Preserve the reviewed display and formatting provenance.
A rerun records new provenance rather than
silently replacing earlier evidence. No lookup code is promoted automatically
into a resolver or concept registry.

Hand the record path and revision to `/data-request:map` as the evidence for each
code. Analyst-selected codes become intake `topic: codes` decisions: cite the
committed lookup record's path and revision in the rationale and preserve the
analyst's actual confirmation. Carry unresolved clinical decisions into intake
questions; lookup does not confirm scope, publish an extract or release data.
