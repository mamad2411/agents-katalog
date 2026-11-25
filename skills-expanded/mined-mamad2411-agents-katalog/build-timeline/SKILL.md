---
name: build-timeline
description: Use when the sequence of events matters — assembles a dated timeline from analyses, source records, and the evidence register, marking each entry with how firmly its date is established. Triggers - "build the timeline", "what happened when", "chronology of this matter".
allowed-tools: Bash(grep *), Bash(find *), Bash(mkdir *), Bash(date *), Bash(sort *), Read, Write
---

# Build Timeline

Assemble a dated chronology from the material already in the workspace, marking how
firmly each date is established.

## When to use

- Events are accumulating faster than their order is clear.
- Preparing a brief or report that turns on sequence.
- Checking whether the material actually supports a claimed chronology.

## Inputs

- `--from <date>` and `--to <date>` — optional bounds.

## Procedure

### 1. Gather dated material

Read whatever the workspace has, and say which of these were present:

- `research/` and `analyses/` — dates recorded during document analysis.
- `sources/register.jsonl` — access times and any dates observed in the material.
- `findings/` — dated events in investigation notes.
- `evidence/register.jsonl`, if the companion evidence agent has created one —
  acquisition times and item dates. Read only; never write to that register.

### 2. Classify every date

This is the part that makes a timeline worth having. Tag each entry:

- **Documented** — the date appears in the material itself and is cited to it.
- **Metadata** — the date comes from a file's embedded or filesystem metadata, which is
  self-reported and can be wrong or deliberately set.
- **Asserted** — someone said so, without a document.
- **Inferred** — derived from other dates, with the derivation stated.

An entry with no classification does not go in the timeline.

### 3. Normalise

Convert to ISO 8601. Keep the timezone where it is known and mark it where it is not —
an event recorded in local time and an event recorded in UTC can appear to be in the
wrong order otherwise. Where only a month or year is known, keep the imprecision rather
than inventing a day.

### 4. Sort and write

Write `timeline/timeline.md`, one entry per line in date order:

```
2026-03-14  [documented]  Notice served on tenant.  research/notice-analysis.md:22
2026-03-18  [metadata]    Photograph taken.  evidence/register.jsonl id 2026-03-18T…
2026-04-02  [asserted]    Verbal complaint made.  findings/complaint.md
```

### 5. Report the gaps

Name the conflicts and the holes explicitly:

- Entries that disagree about the same event.
- Periods with no entries at all, where the matter implies something happened.
- Entries resting only on metadata or assertion at points that carry weight.

A timeline that hides its weak points is worse than none, because it reads as settled.

## Output

- `timeline/timeline.md`, regenerated in full each run.
- A list of conflicts and gaps.

## Notes

- The file is regenerated, not appended to. Source material is the record; the timeline
  is a view of it.
- A metadata date is a claim made by whatever wrote the file, not an observation.
