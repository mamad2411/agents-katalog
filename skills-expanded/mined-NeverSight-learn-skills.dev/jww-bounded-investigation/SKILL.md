---
name: jww-bounded-investigation
description: Keep a written evidence ledger and delegate whole-repository searches during investigation that spans many files. Use for debugging, audits, and archaeology where the relevant code's location is unknown. Do not use when the relevant files are already identified, or for ordinary edits to known code.
allowed-tools: Read Grep Glob
---

# Bounded Investigation

Two practices a long investigation does not produce on its own. Targeted reads
and narrow commands are assumed; they are not what this skill adds.

## Delegate Fan-Out Searches

Send sweeps across unknown locations — many candidate files, uncertain naming
conventions, whole-repository greps — to a read-only search agent when the
harness provides one. It reads the excerpts in its own context and returns the
locations, so the sweep costs a conclusion instead of a corpus.

Run the search directly when the target is specific enough that the output is
small, or when judging the surrounding code matters more than finding it.

## Keep an Evidence Ledger

Record one line per finding: the source, the observation, and what it rules in
or out.

```text
src/Session/Store.swift:88 — writes cache off the main actor — explains the
crash, rules out the decoder path
```

Record ruled-out branches and sources that were checked and added nothing.
Without them, the same file gets read again later in the same investigation.

The ledger is the raw material for a handoff: its lines become the Decisions
and Touched sections of `jww-handoff`, so keeping it makes that handoff nearly
free to write.

## Report

Lead with the conclusion, then the evidence that supports it and the caveats
that affect trusting it. Cite by file and line so the reasoning can be
rechecked without reproducing the search.
