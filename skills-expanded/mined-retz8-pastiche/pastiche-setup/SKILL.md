---
name: pastiche-setup
description: Use when bootstrapping pastiche for first-time adoption (post-`/pastiche-init`) — fills `KNOWLEDGE.md` and seeds `[GENERAL]` `WISDOM.md` rules section by section. Resumable across sessions; re-invoke to continue.
---

# Pastiche — setup

Resumes from `setup_progress` in `pastiche/config.yaml`. Unit of work is one section per turn; within a section, draft candidates as a numbered list, confirm in natural language, write once after agreement.

## Preflight

1. Read `pastiche/config.yaml`. On parse failure: print the parser error verbatim and stop — *"Fix the YAML and re-invoke."*
2. Read `pastiche/FACT.md`. If empty or missing, stop: *"`pastiche/FACT.md` is empty or missing. Run `/pastiche-sync` (or re-run `/pastiche-init`) and re-invoke."*
3. **Re-derive `setup_progress` from files** (the file is the source of truth; config is the cache). For each KNOWLEDGE section: marker still present → `stub`, otherwise `done`. For `general-wisdom`: any `[GENERAL]` bullet present in `pastiche/WISDOM.md` → `done`, otherwise `stub`. Update config silently.

## Lint

Every lint call below: shell `pastiche-lint` (on PATH via plugin `bin/` — do not search for it), cwd = repo root. Forward stdout; on non-zero exit, also forward stderr. Don't revert; don't abort.

## First run vs. returning run

If every `setup_progress` entry is `stub`, this is a first run.

**First run:**

1. Greet (two lines): *"Let's set up pastiche — we'll fill `KNOWLEDGE.md` with how your DS gets used, and seed a few system-wide rules in `WISDOM.md`. You can pause any time; I'll resume where we left off."*
2. **DESIGN.md handshake.** If `design_md_reference` is set in config, skip. Otherwise scan repo root for `DESIGN.md`:
   - **Found** → ask: *"I found `./DESIGN.md`. Want me to use it as reference? I'll draft candidates from it so you mostly review."*
     - Yes → validate the path (resolve absolute, in-repo, readable, ≤200KB). On any failure, warn and proceed as if declined. On pass, write `design_md_reference: ./DESIGN.md` to config. Scan the body for `^## Overview` or `^## Brand & Style`; if either is present, copy that section's body into KNOWLEDGE.md's `## Brand Identity` (replacing the placeholder).
     - No → leave `design_md_reference: null`.
   - **Not found** → one line: *"No `DESIGN.md` at repo root — we'll go through this from scratch."*
3. Start with Brand Identity (below).

**Returning run:** skip greet and handshake. Print: *"Picking up where we left off — `<X>` of 13 done. Next up: `<next stub>`. Continue?"* Then resume.

## Section loop

Pick the next section: lowest stub in canonical order, or `--section <name>` if provided.

After each section, prompt: *"Next section: `<next stub in canonical order>`. Continue / switch / pause?"*

- Continue → next stub in canonical order.
- Switch → ask which section; jump.
- Pause → stop; adopter resumes by re-invoking.

If `--all` was passed, skip this prompt. Stop only when every stub is `done` (then run **Wrap**).

## Brand Identity

**Auto-ported case** (the placeholder was replaced from DESIGN.md): show the ported prose verbatim. Offer `keep / edit / rewrite`.

- `keep` → write + flip + lint.
- `edit` → take natural-language patches, re-show, loop until `keep`.
- `rewrite` → fall through to the freeform case.

**Freeform case** (no auto-port, or adopter chose `rewrite`): prompt:

> *"Write or paste your Brand Identity prose — voice, posture, density, restraint, anything that matters for downstream design decisions. Length is your call; round-1 reads this in full on every task.*
>
> *Not sure where to start? Say "guide me" and I'll walk you through 4–5 prompts to draft it together."*

- If the adopter pastes prose, take it as-is, read back for confirmation, loop on natural-language edits until `yes`.
- If they say "guide me" (or equivalent), ask 4–5 prompts in sequence: brand voice in 1–2 adjectives; density posture (dense vs. spacious, why); restraint signal (when the DS pulls back); the one rule that makes a screen feel off-brand; optional anti-example. Draft a prose paragraph from the answers, read back, loop.

Write the final prose into `## Brand Identity` (replacing whatever was there). Flip `setup_progress.brand-identity: done`. Run lint.

## Scenario sections (11)

Canonical order: Action buttons, Forms & input collection, Feedback & status, Overlays, Navigation & wayfinding, Content display, Layout & page structure, Date & time selection, Iconography, Visual hierarchy, Domain-specific patterns.

Per section:

1. **Draft candidates** as a numbered list, blending two sources:
   - **DESIGN.md** (if `design_md_reference` is set): mine narrative for scenarios in this section's territory.
   - **Canonical seeds** (always; see **Seed scenarios** below).

   Adapt to the adopter's FACT: drop seeds whose atoms aren't in FACT; add candidates suggested by FACT atoms that no canonical seed covered. Atom names backticked (FACT entries verbatim); prop expressions bare. Example: `` → `Button` variant="primary" ``. Soft target 5–8; no hard cap, no padding.

2. **Confirm.** Show the list. *"Accept all, or tell me what to change (accept some / reject some / edit some / add new)?"* Loop on natural-language responses until the adopter accepts.

3. **Write.** Replace the section's `_(empty — …)_` marker with the confirmed scenarios. Each scenario: one or more prose framing lines, then one or more `→ <atom expression>` lines.

4. **Flip + lint.** Set `setup_progress.<section>: done` in config. Run lint.

5. **Cadence prompt** (unless `--all`).

## `[GENERAL]` WISDOM phase (last)

Runs only when every KNOWLEDGE stub is `done`. Same shape as a scenario section; writes to `pastiche/WISDOM.md`; the unit is a tagged rule.

1. **Draft candidates**, blending:
   - **DESIGN.md** (if set): mine posture / invariants, especially any "Do's and Don'ts"-shaped content.
   - **Canonical seeds (4):**
     - *Tokens-only* — never raw hex / px; always reference DS tokens.
     - *Spacing scale discipline* — no arbitrary gap / padding values.
     - *Breakpoint discipline* — no arbitrary media queries.
     - *Accessibility floors* — contrast, focus-visible, semantic HTML by default.

   Adapt seed wording to the adopter's FACT token naming.

2. **Gate DESIGN.md-mined candidates.** For each DESIGN.md-mined candidate, apply: (a) can it be tagged to specific FACT atom(s) instead? (b) does it hold for *all* UI in the project regardless of atoms used? On either failure, drop and note: *"`<rule>` sounds scenario-conditional — re-route to KNOWLEDGE during the relevant section."* Canonical seeds skip this gate.

3. **Show, confirm, write.** Numbered list, natural-language response, loop until accepted. Write each accepted rule as `- [GENERAL] <rule text>.` Append to WISDOM.md (after any existing content, before EOF). Flip `setup_progress.general-wisdom: done`. Run lint.

## Wrap

After every section write, check `setup_progress`. If every entry is `done`, run the wrap on this turn (includes `--section` and `--all` invocations).

Print:

1. Completion line, warm and brief: *"Setup complete — pastiche is wired up for your DS."*
2. Light stats: sections done, total scenarios authored, `[GENERAL]` rules added.
3. One concrete next step: *"Invoke `/pastiche` on a frontend task — your loop will gate against KNOWLEDGE + WISDOM. As your DS grows, use `/pastiche-write-knowledge` and `/pastiche-write-wisdom` for incremental additions."*

No emoji, no theatrics.

## Mid-session degradation

If `design_md_reference` is set but DESIGN.md becomes unreadable during the session (deleted, renamed, exceeds 200KB cap), warn once: *"`DESIGN.md` at `<path>` is no longer readable. Continuing without DESIGN.md context — candidates fall back to canonical seeds."* Do not clear `design_md_reference` in config. Proceed with canonical seeds for the rest of the session.

## Flags

- `--section <name>` — jump to a specific section (revise a `done` section, or skip ahead). Wrap fires if this invocation lands the final flip.
- `--all` — same flow, no continue / switch / pause prompt between sections.

## Seed scenarios

- **Action buttons** — primary CTA; destructive action; secondary / alternative path; loading state; icon-only; link-style.
- **Forms & input collection** — text input; selection (radio / select); multi-select; date / time pick; file upload; inline validation; field grouping; submit / cancel.
- **Feedback & status** — success confirmation (toast / inline); error (inline / banner / modal); warning; loading indicator; empty state; progress.
- **Overlays** — modal (informational); modal (confirmation); modal (destructive confirmation); slide-over / drawer; popover; tooltip.
- **Navigation & wayfinding** — primary nav; secondary nav; breadcrumb; tabs; pagination; back / cancel.
- **Content display** — list (compact); list (rich); card grid; table; detail view; media (image / video).
- **Layout & page structure** — page header; section header; sidebar; main / detail split; footer; container widths.
- **Date & time selection** — single date pick; date range pick; time pick; relative date display.
- **Iconography** — decorative icon; action icon (with affordance); status icon; brand mark.
- **Visual hierarchy** — primary heading; section heading; emphasized text; muted / secondary text; numeric / metric display.
- **Domain-specific patterns** — patterns unique to the adopter's product (e.g., refund flow, KYC step, dashboard widget). DESIGN.md drives this section heavily when present; canonical seeds are minimal.
