---
name: blocks
description: Fills brief/blocks/*.md for interactive elements checked in 07-interactive.md. Walks each block through the standard 11-section checklist in a dialog.
---

# /blocks

Walks the checklist from `brief/07-interactive.md`. For every checked block — fills the corresponding `brief/blocks/<block>.md`.

## When to use

- After `/brief` (when `07-interactive.md` is checkbox-filled).
- Before `/build` (all configs must exist for assembly).
- When adding a new block to an existing project.

## Process

**Step 1. Read 07-interactive.md**
Find every `[x]` block. Skip `[ ]` — not needed.

**Step 2. For each checked one — walk 11 sections**

Common template (see `brief/blocks/README.md`):
1. Is this block needed → already `[x]`, confirm.
2. Trigger / placement.
3. Fields / content.
4. Validation.
5. Where it's sent.
6. Success flow.
7. Error flow.
8. Analytics.
9. Accessibility.
10. Mobile specifics.
11. Priority.

For each — ask one question at a time, use options from the corresponding `brief/blocks/*.md` as a starting point.

**Step 3. Specifics for the main block — contact-form**

This is the main CTA, requires extra care:
- Ask about backend (see `brief/06-technical.md` → Email backend).
- Confirm recipient (manager email).
- Confirm thank-you flow.
- Confirm UTM handling.

**Step 4. Sanity check**

After filling all blocks:
- Look for conflicts (e.g. cookie-banner checked but no analytics — why cookie then?).
- Check priorities: too many must-haves? Warn.
- Check mobile specifics: if mobile-first — every block must be touch-friendly.
- Check a11y: every interactive keyboard-accessible?

**Step 5. Save + report**

Update all `brief/blocks/*.md`.
Show the user a summary: N blocks configured, M blocks are must-haves.

## Rules

- **Do not pull in extras.** If the user checked chat but can't dedicate an operator — suggest dropping it or replacing with "via form".
- **Always clarify backend for forms.** Without a clear endpoint the form is useless.
- **Show implementation examples.** Not "should we autoplay?" but "autoplay after 30s is usually annoying; recommend no".

## What NOT to do

- Do not create blocks not in 07-interactive.md.
- Do not "improve" — stick to what's checked.
- Do not skip block sections — all 11 are needed for `/build`.

## Next

- `/tokens` (if DESIGN-LOCK is already frozen).
- `/build` (if tokens generated).
