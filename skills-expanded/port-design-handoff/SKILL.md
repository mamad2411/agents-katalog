---
name: port-design-handoff
description: Faithfully re-implement a tab/screen from a design handoff in frontend/design_handoffs/ — pixel-identical, E2E, backend included. Use whenever the owner says "reimplement/port/redo the <X> tab to match the design", "follow the design strictly, no deviation", or points at a design_handoffs/<X>_handoff/ folder. Encodes the verbatim-port + real-data-seam workflow used for the Accounts and Plan redesigns.
---

# Port a design handoff (faithful, E2E)

A handoff in `frontend/design_handoffs/<name>_handoff/` ships a **complete interactive prototype**
(`prototype/` — its own React/babel app + the production stylesheet) plus prose specs
(`NN-*.html`) and screenshots (`shots/`). The owner's bar is **zero design drift**: the shipped
look + behavior match the prototype *exactly*. Do not "compromise" by claiming the current app
already covers it. Precedents: `docs/adr/2026-06-28-accounts-tab-redesign-faithful-port.md`,
`docs/adr/2026-07-01-plan-tab-redesign-faithful-port.md`.

This is multi-agent orchestrator work on a feature branch (never `main`). Drive it E2E.

## The one rule

**The prototype IS the spec.** Port its JSX → app React/TS and its `.css` **verbatim** — same DOM,
same class names, same structure — so the result is pixel-identical. Re-deriving from prose on top
of generic primitives guarantees drift and is the failure mode. Only the data layer changes.

## 0. Commit first, branch

Commit any in-progress work, then `git checkout -b feature/<name>-redesign`.

## 1. Read everything (orchestrator, full context)

- The whole `prototype/<name>/` source (the engine module, the shell/app, every sub-tab, charts,
  the `.css`). These files are the contract — read them in full, not excerpts.
- All `NN-*.html` handoff docs (architecture + per-section feature inventory + the **backend
  surface** section — usually `05-components.html`). Look at `shots/*.png`.
- The DS bundle comment in `prototype/_ds_bundle.js` tells you which `window.ONW.*` map to real
  `components/ui/*` primitives (they're built FROM them — `Container`/`PageHeader`/`PageTabs` etc.).

## 2. Map the real app + backend (parallel Explore agents)

Fan out read-only agents: (a) how the tab is routed/rendered today (RouterShell, `tabs.ts`,
the slug map) + existing components/hooks; (b) the **backend surface** for each section — services +
endpoints (often far more complete than expected); (c) CSS architecture + `scripts/check-css-classes.mjs`
+ DS primitives + the LuciusDock API. Decide per section: **EXISTS (wire to it)** vs **MISSING (build it)**.

## 3. Strategy (record as an ADR via `/adr`)

- **Verbatim port, real-data seam.** Keep the prototype's client-side engine/derivations (they
  produce the exact visuals + live interactions); seed its INPUTS from real endpoints and persist
  writes through them. If the server exposes a thinner shape than the design needs (e.g. MC bands),
  the client engine stays authoritative for rendering — document it.
- **Reuse the backend.** Wire to existing services/endpoints; build ONLY the genuine gaps (use
  `add-endpoint`/`add-store`/`write-test`). Re-derive status/labels client-side where the prototype
  does, so edge states (overspent/overfunded/…) match exactly.
- **Consume frozen shared services.** Do NOT port the prototype's bundled nav rail, Lucius
  side-panel, or Tweaks panel — the real `RouterShell` + `LuciusDock` host the tab. Route every
  "Ask Lucius" affordance to the real `onAskLucius` prefill path.
- **Document, don't drop silently.** Anything the design omits that the app supports today, and any
  design feature not yet backed by the server, goes in `PARITY_AND_GAPS.md` (mirror the Accounts
  redesign's `FEATURE_LOSS.md`/`DIVERGENCES.md`) for owner review.

## 4. Foundation first, then parallel sub-tab lanes

1. **Foundation (do it yourself or one tight agent; verify before fanning out):** port the engine
   module → typed `.ts`; the charts; the shared icons; the `.css`; the shell (PageHeader+PageTabs
   masthead, modals); wire routing. Then fan out.
2. **Sub-tab lanes (parallel, git-worktree isolation, one file each):** one `senior-engineer` per
   sub-tab, each porting its prototype file VERBATIM and wiring its real data. Give each the exact
   foundation contracts (import names/types) + the data adapter. They self-verify in their worktree
   and commit; you merge each lane's SHA (disjoint files → clean merges).

### CSS discipline gotchas (these WILL bite)

- Copy the prototype `.css` to `frontend/src/components/tabs/<name>/<name>.css`, **strip the
  standalone-shell scaffolding** (`html/body`, `*{}`, `.onw-*` nav rail, `.<pfx>-content`,
  duplicate `:root` token defs), scope any `.ui-*` DS overrides under the page class, leave it
  **unlayered** (wins, like `accounts.css`/`investments/design.css`), and import it from the tab.
- **Register the new `.css` path in `CSS_FILES`** in `frontend/scripts/check-css-classes.mjs`, or
  every new class is flagged undefined.
- A multi-line CSS header comment must not contain `*/` (e.g. write `pl- and cfx-`, not `pl-*/cfx-*`)
  — it closes the comment early and breaks the lightningcss build.
- `lint:classes` has a **dead-class ratchet** (`scripts/.css-debt.json`): registering the full
  stylesheet while sub-tabs are stubs spikes the dead count and fails. So gate the **foundation on
  `typecheck` + `build` only** (they ignore dead CSS); make **`lint:classes` green at the END**, after
  the sub-tabs reference the classes — then run `STRICT_DEAD=1 npm run lint:classes` to list and strip
  genuinely-dead rules (the dropped LuciusSide/Tweaks styles).
- `noUncheckedIndexedAccess` is ON — array index access is `T|undefined`; add `!` on provably
  in-bounds accesses in the ported math. The branch may already carry **pre-existing** typecheck
  errors in unrelated files — verify only that YOUR feature dir is clean (`npm run typecheck 2>&1 |
  grep components/tabs/<name>/`), don't chase the rest.

## 5. Verify gate (BLOCKING) + reviews

- `npm run typecheck` (your dir clean) → `npm run build` (EXIT 0) → `npm run lint:classes` green →
  backend import smoke + `pytest -m "not integration"` + `make lint`.
- **UI Quality Gate** (`docs/UI_QUALITY_GATE.md`): an acceptance file in `docs/qa/acceptance/`,
  `make qa-e2e` green for the touched IDs, `make ui-gate` clean, and **screenshot evidence diffed
  against `shots/`** at desktop AND narrow widths (charts, sticky headers, table scroll, responsive
  container-queries). "It renders" is NOT a pass.
- BLOCKING dual+ verify: `code-reviewer` (logic/drift), `qa-engineer` (every interaction on the
  running app), `ui-designer` (rendered build matches the prototype). Fix findings before merge.

## 6. Ship

ADR in `docs/adr/`, `PARITY_AND_GAPS.md` for the owner, legacy components dispositioned (kept-and-
flagged vs removed) once the gate is green. Conventional commits; never `git add -A` for data files.
