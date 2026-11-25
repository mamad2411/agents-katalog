---
name: design-lock
description: Freezes the design constitution. Walks through the 9 sections of DESIGN-LOCK.md, previews each choice, locks it. After LOCK, /build works only with these values. Also appends approved elements from §7 imagery and §8 section vocabulary to references/approved-manifest.md.
---

# /design-lock

**Pivotal moment of the workflow.** Before this: research and decisions. After this: build only.

Fills `DESIGN-LOCK.md` — the design constitution that gets frozen and does not change without explicit override.

## When to use

- After `/refs` (there is a proposal with reasons).
- OR after `/brief` + `/copy-analyze` if there are no references.
- Before `/tokens` and `/build` (they refuse to work without LOCK).

## Requirements

Verify readiness:
- `brief/00-priority.md` — LOCKED (desktop-first / mobile-first).
- `brief/01-business.md` — filled (niche, competitors).
- `brief/05-design.md` — filled (mood, associations).
- `brief/copy-analysis.md` — exists (affects length, tone, section structure).
- `references/proposal.md` — exists (if `/refs` already ran).
- `references/approved-manifest.md` — exists (created by `/refs`; empty is fine).

If anything is missing — offer to run what's missing first.

## Process

Walk the 9 `DESIGN-LOCK.md` sections **strictly in order**. Each is a separate dialog.

**For every section:**

1. Show the current proposed values (from `references/proposal.md` if present, else from `brief/05-design.md`).
2. Explain briefly **why** these values (one sentence).
3. **Show a preview** — generate a mini-HTML example right in the message:
   - For type — a block with H1, H2, body using the actual fonts.
   - For color — palette tiles with HEX values.
   - For radius — 3 squares with different radii for comparison.
   - For spacing — a visual scale.
   - For motion — describe (ease + duration) + offer a URL of a site with the example.
4. Ask: **accept / change / show alternatives**.
5. If "change" — offer 3 variants, let user pick.
6. Write the final value to `DESIGN-LOCK.md`, mark `STATUS: LOCKED`.

**Section order (by dependency):**

1. **Spacing** — base of everything.
2. **Type scale** — depends on spacing.
3. **Color** — independent.
4. **Radius** — independent (but should match density).
5. **Motion** — independent, but should match mood.
6. **Density** — affects spacing multipliers.
7. **Photography** — independent.
8. **Section vocabulary** — depends on structure from `/copy-analyze`.
9. **Anti-patterns** — all on by default; only disable with a reason.

**Final step:**

- Show the full `DESIGN-LOCK.md` to the user.
- Explicit confirmation: "freeze? After this, changes require override with an entry in the decision log."
- If yes — every section gets `STATUS: LOCKED`.
- Record the first entry in `DESIGN.md` → Decisions log about the LOCK.

## Appending to the approved manifest

After the freeze, walk two more passes to update `references/approved-manifest.md`:

**Pass 1. §7 Photography / Imagery items.**

Any concrete visual element the user committed to becomes a manifest entry:

```
[ ] imagery: full-bleed hero photograph, aspect 16:9  ← DESIGN-LOCK §7
[ ] imagery: documentary style, high contrast         ← DESIGN-LOCK §7
```

**Pass 2. §8 Section vocabulary items.**

Every approved section type becomes a "must appear on the landing" contract:

```
[ ] section: hero (large visual + headline)           ← DESIGN-LOCK §8
[ ] section: proof (numbers or logos)                 ← DESIGN-LOCK §8
[ ] section: offer (product + benefits)               ← DESIGN-LOCK §8
[ ] section: cta-form (request form)                  ← DESIGN-LOCK §8
```

If a section type is defined in §8 but never actually needed on this landing (e.g. `proof` was locked in the vocabulary but the client has no numbers yet) — user must explicitly remove it from the manifest here, with a note in `DESIGN.md` decision log. Never silently drop.

**Append, do not overwrite.** `/refs` populated the file first; subsequent skills (`/animation`, `/icons`) will append more.

## Enforcement rules

After LOCK, any edit to `DESIGN-LOCK.md`:
- Requires explicit `override` from the user.
- Is recorded in `DESIGN.md` → Decisions log with a reason.
- Triggers reevaluation of dependent sections (e.g. changing base spacing → recompute the whole rhythm).

## Rules of behavior

- **One section — one screen.** Do not dump the whole thing.
- **Always show a preview.** Abstract numbers are meaningless without a visual.
- **Offer 3 alternatives when the user asks** — not 10, not 2.
- **Do not push fashion.** Serif is trendy right now — but if the brand is tech SaaS, sans is better.
- **Do not accept "just do whatever".** If unsure, show real-site examples.
- **Never skip the manifest append.** Silent drops of approved elements is the failure mode.

## What NOT to do

- Do not fill sections on autopilot without per-section confirmation.
- Do not allow LOCK if any field is still TBD.
- Do not change already-LOCKED sections in the same session ("oh let's try again") — explicit override only.
- Do not skip previews — they save "looked fine on paper, bad in the eye".
- Do not overwrite `references/approved-manifest.md` — always append.

## Next

After LOCK:
- `/blocks` — if `brief/blocks/` interactive block configs aren't filled yet.
- `/animation` — dedicated motion brief; appends animation items to the manifest.
- `/tokens` — generates `site/css/tokens.css` from DESIGN-LOCK.
- `/media` and `/icons` — assets.
- `/build` — section assembly.
