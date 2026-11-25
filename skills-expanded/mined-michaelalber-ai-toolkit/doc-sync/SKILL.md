---
name: doc-sync
audience: team
description: Documentation staleness detection, XML doc comment generation, and README synchronization -- keeps documentation accurate and in sync with code changes. Use when auditing documentation coverage, generating XML doc comments, or systematically syncing READMEs after code changes. Do NOT use for a single, already-identified fix like "there's a typo, fix it" -- just make the edit directly.
---

# Doc Sync

> "The only thing worse than no documentation is wrong documentation — someone will trust it and
> make a bad decision."
> -- adapted from Steve McConnell, "Code Complete"

## Core Philosophy

Documentation decays the moment code changes. This skill detects when documentation has drifted
from code, generates accurate XML doc comments from implementation analysis, and keeps READMEs
synchronized with the project's actual state. The goal is not comprehensive documentation — it is
*accurate* documentation. A perfectly documented codebase that was accurate six months ago is a
liability; a minimally documented one verified this morning is an asset. Freshness and accuracy
always beat completeness. Documentation is a derived artifact of code: when they diverge, the code
is always right and the docs must change to match.

**Non-Negotiable Constraints:**
1. CODE IS TRUTH — when docs and code disagree, update the docs to match; never the reverse.
2. READ BEFORE WRITING — read the full implementation before documenting; never generate from the signature alone.
3. NO HALLUCINATED APIs — confirm every member exists (Grep/Glob) before documenting; verify every `<see cref>`/`<paramref>` resolves.
4. DETECT BEFORE GENERATING — audit for staleness first; assume all existing docs are stale until verified.
5. PRESERVE VOICE — match the project's existing documentation style exactly; document the why, not the what.

Full principle table, discipline rules, anti-patterns, and error recovery live in
`references/conventions.md`.

## Workflow

```
STALENESS DETECTION
    SCAN      Identify scope: target dir/namespace, file types (.cs/.md/.xml), doc types.
    COMPARE   Per documented file: code vs. doc modification dates (git log); signatures vs. doc
              content; new public members without docs; removed members still in docs.
    CLASSIFY  CURRENT | STALE (code changed after doc) | MISSING (public API, no doc) |
              ORPHANED (doc references gone code) | DRIFT (doc ≠ current signatures).
    PRIORITIZE  ORPHANED → DRIFT → STALE → MISSING-on-public → CURRENT.
    (Heuristics: references/staleness-detection.md.)

XML DOC GENERATION
    READ      Full implementation; exact signature; throwing paths; edge cases; existing docs.
    GENERATE  <summary> WHAT+WHY not HOW · <param> each param + constraints · <returns> each
              non-void · <exception> each throw + condition · <remarks> edge/threading/perf ·
              <example> only when non-obvious · <see cref> related members.
    VERIFY    Every <param name> matches a real param; every <exception cref> is actually thrown;
              every <see cref> resolves; no <returns> on void; examples compile; summary ≠ name.
    (C# tag patterns: references/xml-doc-patterns.md.)

README SYNC
    INVENTORY  What the README covers (description, setup, config, usage, API, deps, contributing).
    DIFF       Each section vs. current state: setup vs. build files; deps vs. manifests; examples
               vs. current signatures; description vs. current capabilities.
    UPDATE     Read the current code/config; update to match; preserve existing style/format; don't
               add sections without an obvious gap; note anything you cannot verify.
    VALIDATE   All paths exist; commands valid; dep versions match manifests; API refs current.
```

**Exit criteria:** every in-scope item classified; updated docs match the implementation; every
reference verified to resolve; unverifiable items flagged with a note; README sections validated
against manifests and build files.

## State Block

```
<doc-sync-state>
phase: SCAN | COMPARE | CLASSIFY | GENERATE | VALIDATE
scope: [directory, namespace, or file]
files_scanned: [count]
gaps_found: [count]
stale_docs: [count]
items_updated: [count]
items_validated: [count]
last_verified: [description of last action]
</doc-sync-state>
```

## Output Template

- **Staleness report, XML doc coverage report** — `references/output-templates.md`.
- **C# XML tag patterns, when to use each tag, quality examples** — `references/xml-doc-patterns.md`.
- **Staleness heuristics (git-blame compare, signature drift, coverage, broken examples)** — `references/staleness-detection.md`.
- **Principle table, discipline rules, anti-patterns, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `architecture-journal` | When an audit reveals undocumented architecture decisions, record them as ADRs there — documentation gaps often indicate decision gaps. Typical flow: doc-sync audit → discover an undocumented API redesign → architecture-journal records the decision → return to doc-sync to update XML docs + README. |
