---
name: add-decision-adr
description: Add a new architecture decision record entry. Use when the user says "let's record this decision" / "add an ADR for X" / "this needs to go in decisions.md" / when a design call has been made that future contributors need to understand.
---

# Skill — Add a decision (ADR)

The ADR log is the single source of truth for "what did we agree on?"
about system shape. Process / workflow meta-decisions don't go here —
they go in `.cursor/rules/process-gates.mdc`.

## 1. Pick the next D-number

Look at both files:

- `docs/decisions.md` (active — D17 onward).
- `docs/decisions-archive.md` (D2–D14).

Take the highest D-number across both files and add 1. D-numbers are
unique and monotonic.

## 2. Append at the top of the active file

Right after the intro `---` separator. Don't edit any existing entry.

Template:

```markdown
## YYYY-MM-DD — D<N>: <one-line decision>

**Context.** What we knew at the time. One paragraph.

**Decision.** What we agreed. Bullets if it's multi-part.

**Rationale.** Why this over the alternatives.

**Postmortem-in-advance.** *Six months from now we rolled this back. What happened?*

1. **Failure mode:** ... **Mitigation:** ...
2. **Failure mode:** ... **Mitigation:** ...

**Reversible by.** What action would undo this — a `git revert`, a
specific code change, a follow-up ADR.
```

## 3. If you're superseding an older entry

Add a single line to the older entry's top:

```markdown
**Status (YYYY-MM-DD):** Superseded by D<N>. <one sentence why>.
```

That's the only allowed edit to a historical entry. Don't rewrite the
reasoning.

## 4. Don't break the rules

- Don't edit history. Append at the top.
- Don't put process / workflow stuff here. That goes in
  `.cursor/rules/process-gates.mdc`.
- Don't omit the postmortem-in-advance for substantive decisions —
  it's the gate that catches the dumb things early.
