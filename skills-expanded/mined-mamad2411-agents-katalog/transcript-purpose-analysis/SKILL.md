---
name: transcript-purpose-analysis
description: Segment a transcript and label each passage by its communicative purpose in an evidence-linked Markdown report. Use when asked to segment, categorize, label, map, or analyze what parts of a transcript are doing.
---

# Transcript Purpose Analysis

Produce a source-faithful purpose map of a transcript; this workflow does not extract requirements, judge speakers, infer motives, or rewrite the source.

## Inputs

### A. Transcript

A required complete transcript, supplied inline or as a UTF-8 text-file path relative to the active repository root. Speaker labels and timestamps are optional source anchors. The transcript is read-only.

### B. Purpose taxonomy

An optional user-supplied set of labels and definitions. When absent, the taxonomy is **Opening/rapport**, **Framing/context**, **Discovery/questioning**, **Explanation/evidence**, **Problem/need**, **Goal/requirement**, **Proposal/ideation**, **Evaluation/objection/risk**, **Decision/commitment**, **Coordination/action item**, **Administration/navigation**, **Closing**, and **Other/unclear**. Labels describe a passage's communicative function, not merely its topic.

### C. Output destination

An optional Markdown path. For a file-based transcript, the default is `purpose-analysis.md` beside the source. For inline text without a destination, the output is returned inline. An existing report is user-owned unless the user explicitly requests its revision.

## Outputs

### A. Purpose analysis report

A Markdown report at the resolved destination, or inline, containing the source identifier, taxonomy used, and an ordered table with `Section`, `Source span`, `Primary purpose`, `Secondary purpose`, `Summary`, `Evidence`, and `Confidence`. `Source span` uses timestamps or speaker-turn ranges when available, otherwise short verbatim opening and closing anchors. `Secondary purpose` is `—` unless a distinct supporting function is material; `Evidence` is a short verbatim quote; `Confidence` is `High`, `Medium`, or `Low`. It is complete when contiguous spans represent the entire source exactly once, in order, and every label is traceable to source text.

### B. Ambiguity notes

A short list after the table identifying every low-confidence boundary, unclear passage, or taxonomy mismatch; `None` when none exist. It is complete when no uncertainty has been silently resolved.

## Procedure

### 1. Establish the source and destination

Resolve a supplied path from the repository root or capture the complete inline text, read it end to end, record its source identifier, exact contents, available timestamp or speaker anchors, and resolved output destination.

- If the path is missing, unreadable, or not a text file, stop and request a valid transcript; the result is a reported input blocker and no file change.
- Otherwise, this step is complete when the full read-only source, usable anchors, and destination are recorded.

### 2. Fix the allowed taxonomy

Adopt the user's labels and definitions exactly when supplied; otherwise adopt the default taxonomy from Input B.

- If a supplied taxonomy cannot describe a passage, retain that taxonomy, use `Other/unclear`, and record a mismatch rather than inventing a label.
- This step is complete when every allowed label has one fixed meaning and the report can state the taxonomy used.

### 3. Mark purpose transitions

Partition the transcript into contiguous sections at changes in communicative function, including within a speaker turn. Let one section span multiple turns when they jointly perform the same function; do not split on equal length or topic change alone. Merge adjacent spans only when their primary function is the same and no meaningful transition is hidden. This step is complete when an ordered boundary list covers the source once with no gap or overlap.

### 4. Classify the sections

Give each section one primary label and, only when materially useful, one secondary label. Support classifications with explicit language and conversational role; do not infer hidden motives, sentiment, agreement, authority, or unstated requirements.

- If no purpose is supportable, assign `Other/unclear` with `Low` confidence and add an ambiguity note.
- This step is complete when every boundary has supported labels and a `High`, `Medium`, or `Low` confidence rating.

### 5. Construct the report

For every section, add the narrowest reliable source span, a one-sentence neutral summary, and a short verbatim quote demonstrating the label; preserve source order and exact wording in anchors and quotes. Add all required ambiguity notes or `None`.

- If the destination exists and the user explicitly requested an update, revise that report only.
- If the destination exists without explicit revision authority, stop and ask whether to revise it; the result is a reported overwrite blocker with both source and existing report unchanged.
- Otherwise, this step is complete when the in-memory report has every field and note required by Outputs A and B.

### 6. Validate coverage and fidelity

Compare all boundaries, anchors, quotes, and labels against the complete source. Correct gaps, overlaps, duplicated coverage, altered quotations, unsupported labels, topic-only labels, and unreported uncertainty. Confirm the transcript's exact contents are unchanged. This step is complete when every passage appears in exactly one ordered span, every quote is verbatim, every label is auditable, all uncertainty is explicit, and the source matches the recorded contents.

### 7. Publish and report completion

Write the validated report to the resolved unused or authorized destination, or return it inline. Report exactly: `Result: <path|inline>`, `Sections: <count>`, `Low confidence: <section numbers|None>`, and `Source unchanged: yes`. The workflow is complete only when that report accompanies a published, fully validated purpose analysis and the transcript remains unchanged; otherwise it ends only with the applicable input or overwrite blocker explicitly reported.

## Callstack Simulation

**Transcript Purpose Analysis**(transcript, purpose taxonomy, output destination)
│
├─ **Establish The Source And Destination**(supplied path or complete inline text)
│  │
│  ├─ if (the path is missing, unreadable, or not a text file): stop, request a valid transcript, and make no file change
│  │
│  └─ else: record the read-only source, usable anchors, and resolved destination
│
├─ **Fix The Allowed Taxonomy**(user-supplied taxonomy or default taxonomy)
│  │
│  ├─ if (a user-supplied taxonomy is present): adopt it exactly; use Other/unclear and record a mismatch for any uncovered passage
│  │
│  └─ else: adopt the default taxonomy
│
├─ **Mark Purpose Transitions**(complete transcript, fixed taxonomy)
│
├─ **Classify The Sections**(ordered boundary list)
│  │
│  └─ if (no purpose is supportable): assign Other/unclear with Low confidence and add an ambiguity note
│
├─ **Construct The Report**(classified sections, source anchors, resolved destination)
│  │
│  ├─ if (the destination exists and revision was explicitly requested): revise that report only
│  │
│  ├─ else if (the destination exists without revision authority): stop, request authority, and leave the source and report unchanged
│  │
│  └─ else: build the report with every required field and ambiguity note
│
├─ **Validate Coverage And Fidelity**(complete source, report boundaries, anchors, quotes, labels)
│  │
│  └─ if (a fidelity or coverage defect exists): correct it before publication
│
└─ **Publish And Report Completion**(validated report, resolved destination)
   │
   ├─ if (the destination is a file): write the report to the unused or authorized path and report the required result fields
   │
   └─ else: return the report inline and report the required result fields
