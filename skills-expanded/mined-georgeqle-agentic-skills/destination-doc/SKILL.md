---
name: destination-doc
description: Serialize taste-calibration alignment into a lightweight destination document
type: planning
version: v0.0
argument-hint: "[optional topic override]"
---

# Destination Doc

Serialize operator-agent alignment into a short, disposable destination document.

## Process

1. **Read conversation context** for a taste-calibration summary. If running standalone, gather context from `$ARGUMENTS` and project files.
2. **Determine topic slug** (kebab-case) from the subject matter.
3. **Archive existing file** if `research/destination-[topic].md` already exists (Archive-First policy).
4. **Write `research/destination-[topic].md`** with the structure below.
5. **Write an alignment review page** at `alignment/destination-doc-[topic].html`. If that file already exists, archive it first to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/destination-doc-[topic].html`.
6. **Attempt to open the HTML page** in the browser and report whether the browser open succeeded or was blocked.

## Document Structure

```markdown
> Checkpointed alignment state — not a contract. Verify against code before treating any claim as current.

## Intent
[What and why — 2-4 sentences]

## Success Criteria
- [Bulleted, testable criteria]

## Taste Notes
[What would be wrong even if tests pass — qualitative signals]

## Out of Scope
- [Explicit exclusions]

## Open Questions
- [Unresolved items, if any]
```

Keep to 1-2 pages. Cut anything that belongs in a full spec.

## Output

- `research/destination-[topic].md`
- `alignment/destination-doc-[topic].html`

## Archive-First Replacement Policy

- Before replacing an existing `research/destination-*.md`, copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed; do not edit the archived copy.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Before replacing an existing alignment page, copy it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/<filename>.html`.

## Shipping

Commit and push the destination doc.

## Next-Step Routing

After writing: "Run `$vertical-slice-splitter research/destination-[topic].md` to split into issue cards."

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

