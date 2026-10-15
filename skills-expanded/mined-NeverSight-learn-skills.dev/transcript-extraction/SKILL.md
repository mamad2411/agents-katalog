---
name: transcript-extraction
description: Create or update evidence-linked extract.md reports that capture decision-ready product, business, domain, constraint, change, and bug claims. Use when the user asks to process a conversation transcript, capture what a transcript says, or extract decisions, requirements, bugs, or domain knowledge from transcript.txt.
disable-model-invocation: true
---

# Transcript Extraction

Turn transcripts into durable, evidence-linked extractions; this is a capture pass, not planning or implementation, and it preserves each claim's actual certainty.

## Inputs

### A. Transcript sources

A required selection of one or more user-supplied `docs/transcripts/<day>/<order>-<slug>/` directories or their direct `transcript.txt` files, resolved from the repository root. `<order>` is a two-digit conversation sequence. Each directory must contain exactly one source named `transcript.txt`; sources are read-only.

### B. Current repository record

Repository-supplied context documents, the initial idea, relevant ADRs, and verified product behavior that bear on transcript claims. Individual records are optional when absent; every existing relevant record is required context and authoritative for reconciliation.

### C. Report template

The required bundled [`references/report-template.md`](references/report-template.md), which defines every extraction report's required shape and empty-section notation.

## Outputs

### A. Extraction reports

For each source, a created or revised `docs/transcripts/<day>/<order>-<slug>/extract.md` beside `transcript.txt`, following the report template. It is complete when every relevant atomic claim appears once with certainty, reconciliation, a short verbatim quote, and its transcript source, and every empty section says `None.`

### B. Completion report

A response listing each extraction path and whether it was created or updated, followed only by decided items needing promotion, reported bugs needing verification, conflicts, open questions, and the preservation boundary. Use `None` for an empty list.

## Procedure

### 1. Resolve and read the sources

Resolve every supplied path from the repository root, deduplicate it, and map a directory to its direct `transcript.txt`. If a path is missing, a file is not named `transcript.txt`, or a directory does not contain exactly that one transcript source, stop and identify the invalid input; otherwise read every transcript completely without changing it. This step is complete when there is a validated list of distinct source files and each has been read end to end.

### 2. Build the evidence and current-record map

For each transcript, identify candidate assertions and attach a short verbatim quote. Before reconciling them, use `CONTEXT-MAP.md` to select relevant context files when present, otherwise read `CONTEXT.md` when present; also read `docs/initial-idea.md` when present and every ADR touching a candidate. When a candidate reports a bug or says a feature already exists, search the repository for the relevant product behavior; if behavior cannot be verified, retain that uncertainty rather than infer it. This step is complete when every candidate links to transcript evidence and to each found record or behavior that supports, refines, or conflicts with it.

### 3. Atomize and classify the claims

Retain every claim that could affect product behavior, user experience, domain language, process ownership, business strategy, customer or market understanding, risk, or a future decision. Make each claim one subject plus one asserted fact or requested outcome, and place it once under **Decisions and requirements**, **Change requests**, **Bugs and observed behavior**, **Business and domain knowledge**, **Constraints and boundaries**, or **Open questions and hypotheses**. Omit greetings, navigation commentary, speculative implementation detail, and repetition without a new claim; include both sides of a discussion only when each is materially relevant. Classify certainty as **Decided** (explicit commitment), **Observed** (reported fact or behavior), **Proposed** (unaccepted candidate), or **Open** (unresolved). For a reported bug, separate its symptom and reproduction context from any unverified cause. If wording is garbled or intent is unclear, record the narrowest faithful claim as **Open**; never manufacture intent, causes, requirements, metrics, or owners. This step is complete when every relevant assertion is represented once as an atomic, categorized, certainty-preserving claim with evidence.

### 4. Reconcile without replacing authority

Compare each claim with the current record and mark it **New**, **Confirms**, **Refines**, or **Conflicts**. When a transcript differs from an accepted ADR, canonical document, or verified behavior, preserve both records, cite the current one, and surface **Conflicts** rather than silently choosing or rewriting either. Treat the transcript as evidence for a candidate, not authority to alter canonical state. This step is complete when every claim has exactly one supported reconciliation status and every conflict names the competing record.

### 5. Materialize and validate each extraction

Create a missing `extract.md` or revise the existing one in place from the bundled template, keeping each report scoped to its adjacent transcript. Re-running is an update, not an append: merge duplicates and preserve still-supported claims so each appears once. Fill every template section or write `None.`, then compare the report back to the full transcript and current-record map to correct omissions, unsupported certainty, missing evidence, duplicate claims, and undisclosed conflicts. Do not create tickets or modify transcripts, `CONTEXT.md`, context-map targets, ADRs, product documentation, or application code. This step is complete when every report satisfies Output A and the only repository files changed by this workflow are the intended `extract.md` files.

### 6. Report completion

Report exactly `Extraction: <path> (created|updated)` for each output, then `Promote:`, `Verify:`, `Conflicts:`, `Open:`, and `Boundary: Only the listed extract.md files changed.` List only the corresponding decided items needing promotion, reported bugs needing verification, conflicts, and open questions; write `None` after any empty label. The workflow is complete only when every validated source has one adjacent, template-conformant report whose relevant claims are classified, evidence-linked, reconciled, and represented once, all preservation boundaries hold, and this exact completion report has been returned.

## Callstack Simulation

**Transcript Extraction**(transcript sources, current repository record, report template)
│
├─ **Resolve And Read The Sources**(supplied paths, repository root)
│  │
│  ├─ if (a path is missing, a file is not transcript.txt, or a directory lacks exactly one transcript source): stop and identify the invalid input
│  │
│  └─ else: resolve and deduplicate the sources, then read every transcript end to end without changing it
│
├─ **Build The Evidence And Current Record Map**(validated transcripts, repository records)
│  │
│  ├─ **Identify Candidate Assertions**(each complete transcript)
│  │  │
│  │  └─ attach a short verbatim quote to every candidate
│  │
│  ├─ **Select Relevant Context**(candidate assertions, repository root)
│  │  │
│  │  ├─ if (CONTEXT-MAP.md is present): read the selected relevant context files
│  │  │
│  │  ├─ else if (CONTEXT.md is present): read CONTEXT.md
│  │  │
│  │  └─ else: continue without either context index
│  │
│  ├─ **Read Current Records**(initial idea when present, every candidate-relevant ADR)
│  │
│  └─ **Verify Reported Product Behavior**(bug reports and existing-feature claims)
│     │
│     ├─ if (relevant behavior is verified): link it to the candidate
│     │
│     └─ else: retain the uncertainty rather than infer behavior
│
├─ **Atomize And Classify The Claims**(candidate assertions, report categories, certainty classes)
│  │
│  ├─ **Retain And Categorize Atomic Claims**(candidate assertions, six report categories)
│  │  │
│  │  └─ represent every relevant assertion once and omit non-claim content and repetition
│  │
│  └─ **Preserve Certainty And Evidence**(Decided, Observed, Proposed, Open)
│     │
│     └─ keep bug causes unverified and unclear intent Open rather than manufacture details
│
├─ **Reconcile Without Replacing Authority**(atomic claims, current record)
│  │
│  ├─ if (a claim differs from an accepted record or verified behavior): preserve both, cite the current record, and mark Conflicts
│  │
│  └─ else: assign exactly one supported status from New, Confirms, or Refines
│
├─ **Materialize And Validate Each Extraction**(each transcript, adjacent extract.md, report template)
│  │
│  ├─ **Materialize Each Extraction**(transcript claims, adjacent report)
│  │  │
│  │  ├─ if (extract.md is missing): create it from the bundled template
│  │  │
│  │  └─ else: revise it in place, merging duplicates and preserving still-supported claims
│  │
│  ├─ **Populate The Report Template**(reconciled claims, required sections)
│  │  │
│  │  └─ if (a section has no claims): write None.
│  │
│  ├─ **Validate Each Extraction**(full transcript, current-record map, report)
│  │  │
│  │  └─ correct omissions, unsupported certainty, missing evidence, duplicates, and undisclosed conflicts
│  │
│  └─ **Enforce The Preservation Boundary**(repository changes)
│     │
│     └─ change only the intended extract.md files
│
└─ **Report Completion**(extraction paths and states, promotions, verifications, conflicts, open questions, preservation boundary)
   │
   └─ return the required Extraction, Promote, Verify, Conflicts, Open, and Boundary labels; use None for every empty category
