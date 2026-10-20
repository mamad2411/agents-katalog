---
description: >-
  LLM self-initiative and oscillation ban. @ this rule when the operator reports
  ignored instructions, layout whack-a-mole, bad reverts, or scope creep.
alwaysApply: false
---

# Agent Self-Initiative Ban

## Purpose

Agents ship **plausible diffs** that ignore the last operator message, swing between opposite layout fixes, over-engineer adjacent surfaces, and say **done/deployed** while the screenshot still fails. This file is the **discipline contract** for those failures. General lie catalog: `anti-slop.mdc` (**LLM dishonesty patterns**). Frontend layout: `ui.mdc`, `frontend-slop.mdc`. Verification honesty: `quality.mdc`.

**Operator use:** `@agent-self-initiative.mdc` on any turn where the agent ignored you, improvised, or made things worse. When cited, this rule is **binding for that turn** before any edit.

## Mandate when this rule is cited

| Step | Action |
| :--- | :--- |
| 1 | **Stop** new features, refactors, shell edits, deploys until the current ask is satisfied |
| 2 | **Quote** the operator's last instruction in one sentence (no reinterpretation) |
| 3 | **List** what you will **not** touch (files/surfaces not named in the ask) |
| 4 | **Pick** one reference implementation in-tree (`billing_exports.tsx`, existing primitive, or named commit) |
| 5 | **Diff** only what the ask requires; no compensating wrappers |
| 6 | On **revert** ask: use `git show` / `git diff` on a named baseline; never "reconstruct from memory" |
| 7 | Say **done** only after scoped check; paste command + exit code or **not run** |

If step 2 and your planned diff disagree, **stop and ask** once. Do not ship and hope the operator accepts.

## Failure modes (SD-* catalog)

| ID | Pattern | What the agent does | What the operator meant | Prevention |
| :--- | :--- | :--- | :--- | :--- |
| SD-OSC | Oscillation | Fix A, then opposite fix B, then blend of A+B | One stable target | Write invariant table before edit; ban undoing last fix without operator OK |
| SD-CARD | Card vs content | Shrinks card (`w-fit`) when asked to align content left; stretches grid when asked for margin right | **Card** = full width of panel; **fields** = compact band left; **air** = inside card, right of fields | See **Layout invariant** below |
| SD-SPEC | Spec + slop | Implements operator grid ratios plus h-10, new card chrome, moved blocks, extra buttons | Spec describes **proportions only**, not a redesign | Change only named surfaces; no new components unless asked |
| SD-PAGE | Page-local layout soup | `EXPORT_*_CLASS`, `max-w-[72rem]`, `75%` band, per-page `headerClassName` | Layout lives in shell (`FilterPanel`, `PageChrome`, `ui.mdc`) | Zero new `*_GRID_CLASS` in `domains/` |
| SD-SHELL | Shell smuggle | Edits `page_layout.tsx`, global toast CSS, calendar tokens for one route fix | Page-only ask stays in page file or primitive | Forbidden paths table |
| SD-ACCENT | Color inflation | Adds accent/destructive/outline to every button after "accent on FAQ only" | Named control(s) only | Grep `variant=` diff; revert unasked color changes |
| SD-BORDER | Border inflation | Adds focus rings / contrast borders after "no contrast borders" | Match existing card border token | No new `border-primary`, `ring-*` without ask |
| SD-REVERT | Fake revert | "Reverted" but mixes eras (tooltips + old grid + new h-10) | Exact tree at named point in time | `git show <rev>:path` copy or `git checkout <rev> -- path` |
| SD-DONE | Premature done | "Deployed / fixed / aligned" without screenshot parity | Visual ask needs visual confirmation or honest not run | Ban "should look" language |
| SD-DEPLOY | Deploy theater | Rebuild + VPS restart on every className tweak | Deploy when operator asks or batch is verified | One deploy per logical slice, not per guess |
| SD-SORRY | Apology loop | "Понял, извини" then repeats SD-OSC | Stop and follow **Mandate** table | Apology without invariant table = banned |
| SD-READ | Screenshot blindness | Tweaks code without stating what annotation/region shows | Read image: which band, which edge, which control | One-line "screenshot shows X" before fix |

## Layout invariant (admin pages)

Use this table when the operator mentions width, void, gap, or alignment. **Do not improvise a third model.**

| Layer | Width | Alignment | Forbidden |
| :--- | :--- | :--- | :--- |
| Filter card / `FilterPanel` | `w-full` of workspace | N/A | `w-fit` on panel root |
| Field band inside card | `w-full` with `max-w-*` only if operator named a cap | `justify-items-start` / left grid | `fr` grid spanning entire viewport beyond card |
| Individual controls | Content-sized columns inside band | Same row baseline via shared primitives | Per-page `h-10` shell hacks |
| Page workspace | Fills outlet | No phantom right column when scrollbar absent | `mx-auto` + narrow card without ask |

**Reference:** `web/src/domains/billing/billing_exports.tsx` (minimal domain layout).

**Exports disaster (2026-09):** operator said full-width card + left content + right air **inside** card; agent repeatedly shrank the card or stretched the grid to the viewport. That is SD-CARD + SD-OSC.

## Scope boundary

| Operator ask type | Allowed | Forbidden without explicit ask |
| :--- | :--- | :--- |
| "Fix field width on Exports" | `web/src/domains/exports/*` | `page_layout.tsx`, `tailwind.css`, `filter_panel_classes.ts` |
| "Style this page" | Domain TSX + existing primitives | New global tokens, new `*_CLASS` constants in domain |
| "Revert" | Named paths at named revision | "Improve while reverting" |
| "Skeleton only / no styles" | Semantic HTML + handlers + `Button`/`Input` defaults | `adminKit` layout classes, custom grids |
| "Deploy" | Build + ship once | Deploy after every intermediate guess |

## Revert protocol (mandatory)

1. Operator names **target** ("before message about width", commit hash, or file snapshot).
2. Agent runs `git log -n 20 --oneline -- <paths>` and picks revision **with operator confirmation** if ambiguous.
3. Restore with `git show <rev>:path` or `git checkout <rev> -- path` (no hand-merged Frankenstein).
4. Paste `git diff --stat` for restored paths.
5. Do **not** re-apply "improvements" from rejected slices in the same turn.

## Forbidden without explicit operator ask

| Action | Why |
| :--- | :--- |
| New layout constant in `domains/` (`FOO_GRID_CLASS`, `FOO_PANEL_CLASS`) | SD-PAGE |
| `PageChrome` / `PageLayout` prop overrides for one route | SD-SHELL |
| Opposite of the previous fix because "maybe this time" | SD-OSC |
| Subagents for "explore styling" on a revert/skeleton ask | Scope explosion |
| Replacing working UI with a new component architecture | SD-SPEC |
| Touching unrelated routes "while here" | SD-SHELL |
| `justify-between` / `w-full` on button rows after stretch complaint | SD-OSC |

## Required pre-edit block (paste in chat when @ cited)

```text
Operator ask (verbatim): ...
My interpretation: ...
In scope: ...
Out of scope: ...
Reference file: ...
Layout model: card=w-full | band=left | air=inside-card-right
I will NOT: ...
```

## Required completion block

```text
SD checklist: SD-* considered -> none triggered | SD-XXX avoided by <action>
Files touched: ...
Gates: <command> -> exit <code> | not run
Operator must verify visually: yes | no (explain)
```

## Stop signal

When the operator says stop, revert, "ты тупой", or "самодеятельность":

1. **Do not** add wrappers, portals, or CI layers.
2. **Revert** the rejected slice (`git checkout` / restore), not a cosmetic patch.
3. **Deliver only** what was asked (rules-only turn = zero code diff).
4. Next turn: smaller diff, same reference file, no deploy until asked.

## Cross-ref

| Topic | Rule |
| :--- | :--- |
| Lie modes, deploy honesty | `anti-slop.mdc` |
| Admin layout contract | `ui.mdc` |
| Frontend catalog IDs | `frontend-slop.mdc` |
| Doc ask -> code ban | `anti-slop.mdc` **Lie types** |
| Operator rejection | `anti-slop.mdc` **On operator rejection** |
