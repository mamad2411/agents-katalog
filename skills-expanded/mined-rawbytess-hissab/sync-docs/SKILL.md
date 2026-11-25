---
name: sync-docs
description: Propagate Hissab's syntax documentation from its source of truth (lib/documentation/) out to every downstream surface — the five README.md files and the in-app docs under app/src/docs/. Invoke whenever lib/documentation/ changes (a new category, function, operator, unit, or syntax rule), when engine features land that users need to know about, or when the user asks to "sync docs", "update the docs", "update the READMEs", or fix doc drift. Verifies every example against the real engine before finishing.
---

# Sync Hissab docs from the source of truth

`lib/documentation/` is the **single source of truth** for Hissab's user-facing
syntax. Everything else — the READMEs and the in-app docs — is a hand-written
*view* of it for a particular audience. They drift when the engine gains a
feature and only the source chunks get updated. This skill propagates a change
from the source out to every downstream surface and proves the examples still
run.

This skill does **not** rewrite the syntax reference itself. If a *rule* changed
(new function, new operator, changed precedence), that belongs in
`lib/documentation/` first — see "Did the source change?" below. This skill's job
is to make the downstream copies agree with the source once it's correct.

## The source of truth

```
lib/documentation/
  tags.ts                 OPERATION_TAGS[]  +  tagDescriptions{}   ← master category list
  base.ts                 base overview: basics, labels/prev, pitfalls, limits
  chunks/<tag>.ts          full grammar + examples + gotchas, one file per tag
  system-instructions.ts  LLM system prompts (rarely a sync target)
  index.ts                getFullDocumentation(), getDocumentationChunk(tag)
```

`OPERATION_TAGS` in `tags.ts` is the canonical list of categories (currently 19:
`arithmetic` … `labels_and_prev`). **Every category list on every surface must
match it** — same set, same order, same naming. When a tag is added/removed/
renamed in `tags.ts`, that change has to reach all of the surfaces below.

The ground truth for what an expression actually *returns* is
`engine/tests/expression/valid/*.txt` — engine-verified `["expr", "result"]`
pairs (and `invalid/*.txt` for expressions that must error). Treat those results
as authoritative; never invent an output in the docs.

## Downstream surfaces (what this skill keeps in sync)

| Surface | What to keep in sync with the source |
| --- | --- |
| `README.md` (root) | Intro one-liner examples; "What is Hissab" prose; the **Features** category table (one row per `OPERATION_TAG`); CLI command list; engine-exports paragraph |
| `cli/README.md` | Command list; example invocations; the "Supported syntax" category sentence |
| `engine/README.md` | "Supported expression families" sentence; the public-exports list |
| `skills/README.md` | Category sentence in the intro; the **documentation tags** block (verbatim `OPERATION_TAGS`) |
| `app/README.md` | Currently the stock Vite template — flag it; only replace with the user's go-ahead |
| `app/src/docs/content/**/*.md` | One page per category + reference pages (functions/operators/units); examples in ```hissab blocks |
| `app/src/docs/registry.ts` | Navigation manifest — every category page must be registered here |

Full per-surface detail (exact sections, line anchors, conventions) is in
[`references/surface-map.md`](./references/surface-map.md). Read it before editing
so nothing is missed.

**Out of scope — do not touch here:**

- `skills/hissab-cli/documentation.md` is **generated**. Never hand-edit it.
  Run `pnpm sync:skill-docs` instead.
- `website/` (Astro/Starlight) is a separate doc surface with its own cadence;
  only touch it if the user asks.

## Did the source change?

If the user's request is really "the engine grew feature X, update the docs",
the *source* must capture it first — otherwise there's nothing correct to sync
from. Before propagating:

1. Confirm the rule lives in `lib/documentation/` — the right `chunks/<tag>.ts`,
   plus `tags.ts`/`base.ts` if it's a whole new category. If it doesn't, add it
   there first (that's the project's documented contract in `CLAUDE.md`).
2. Add example expressions to `engine/tests/expression/valid/<category>.txt`
   (and `invalid/` for things that must error) and run the engine tests, so the
   outputs you'll quote downstream are verified.

Only once the source is correct do you fan the change out.

## Workflow

1. **Identify the delta.** What changed in `lib/documentation/`? Diff against the
   last sync if unsure: `git log -p -- lib/documentation/`. Note specifically
   whether `OPERATION_TAGS` changed (a tag added/removed/renamed) — that ripples
   to every category list.
2. **Read the surface map.** Open [`references/surface-map.md`](./references/surface-map.md)
   and treat it as the checklist of places to edit.
3. **Update each surface** to reflect the delta, matching each file's existing
   tone and structure (the READMEs are prose; the app docs use ```hissab blocks +
   `:::caution` bullets). Pull example expressions and their results from
   `engine/tests/expression/valid/*.txt` — don't make up outputs. If you add a
   new app docs page, register it in `app/src/docs/registry.ts` under the right
   section.
4. **Keep category lists identical to `OPERATION_TAGS`** — same set, same order.
   The README Features table, the cli/engine/skills category sentences, the
   `skills/README.md` tags block, and the app docs page set all derive from it.
5. **Regenerate the generated skill docs:** `pnpm sync:skill-docs` (only if
   `base.ts` changed). Never edit `skills/*/documentation.md` by hand.
6. **Verify** (see below).
7. **Report** what you changed surface-by-surface, and call out anything you left
   for the user (e.g. `app/README.md`, or the website).

## Verify before finishing

Run these from the repo root. The verifier needs the engine built once:

```bash
pnpm -F engine build                                          # so @rawbytes/hissab resolves
bun .claude/skills/sync-docs/scripts/verify-examples.ts       # every ```hissab block in app docs must run
pnpm sync:skill-docs:check                                    # generated skill docs not drifted
pnpm check:check                                              # biome lint/format gate
```

- `verify-examples.ts` evaluates every ```hissab block in `app/src/docs/content`
  through the real engine and fails on any line that doesn't parse. Pass file
  paths to scope it to what you touched:
  `bun .claude/skills/sync-docs/scripts/verify-examples.ts app/src/docs/content/guide/<page>.md`
- It checks that examples **run**, not their printed output. For result
  accuracy, cross-check against `engine/tests/expression/valid/*.txt`, or
  spot-check a specific result: `pnpm -F cli dev eval "<expr>"`.
- README code fences are ```text / ```ts (not executable), so verify their
  example *outputs* by hand against the test corpus or `hissab eval`.

## Guardrails

- **Source first.** Never fix a syntax rule only in a README or app doc — change
  `lib/documentation/` and let it flow down, or the surfaces diverge again.
- **One category list.** It's `OPERATION_TAGS`. If you find a surface listing
  categories in a different order or with a stale name, that's the bug — align it
  to `tags.ts`.
- **Never hand-edit `skills/*/documentation.md`** — run `pnpm sync:skill-docs`.
- **Don't duplicate the reference.** The app docs are a *guide*; they shouldn't
  re-paste the full grammar from the chunks — link/point to the source instead
  (see the note at the top of `app/src/docs/registry.ts`).
- **No invented outputs.** Every result you quote comes from the engine
  (`engine/tests/expression/valid/*.txt` or `hissab eval`).
- **Match the surface's voice.** READMEs are prose; app docs use ```hissab fenced
  blocks for runnable examples and `:::caution` bullets for mistakes.

## Done checklist

- [ ] Source (`lib/documentation/`) is correct and, if a rule changed, has
      backing tests in `engine/tests/expression/`.
- [ ] Every surface in the table reflects the delta.
- [ ] Every category list matches `OPERATION_TAGS` (set + order).
- [ ] New app docs pages are registered in `app/src/docs/registry.ts`.
- [ ] `pnpm sync:skill-docs` run if `base.ts` changed; `sync:skill-docs:check`
      passes.
- [ ] `verify-examples.ts` passes; quoted results match the test corpus.
- [ ] `pnpm check:check` passes.
- [ ] Reported what changed and what was deferred to the user.
