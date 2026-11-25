---
name: state-matrix
description: Write or lint a feature's UI state matrix (G12).
kind: skill
pack: ui-ux
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: state-matrix

## Premise

A UI feature is designed one state at a time, or it is designed for the happy path only. The state matrix is the design-time contract for every surface the feature touches. It has one row per (surface × state). Each row says what the user sees in that state: the message, the action, and where focus goes. Each row names the story or test that will force the state and prove it. A row may be `n-a` only with a reason that says why the state cannot occur.

The matrix is the input of three later steps:

- **P5:** the acceptance tests come from its rows.
- **P8–P11:** `@ux-reviewer` reviews the surfaces against it.
- **Gate G12 (usability and state coverage):** G12 has a computational half, `scripts/state-matrix-lint.py` (this skill's lint mode), and an inferential half, `@ux-reviewer`.

Its rows are the defects `ui-state-scan` (this pack) looks for afterwards. A matrix row that holds is a class that scan reports as covered.

**Two modes:**

- **Design** writes the matrix at P3, before code.
- **Lint** checks it at P3 (`--phase=design`) and again at the gate, once the stories and tests exist.

## Where the matrix lives

| Context | File | Writer | Notes |
|---|---|---|---|
| Delivery run, `@ux-designer` installed | `ai/runs/<run-id>/ux.md` § `## State matrix` | `@ux-designer` (ui-ux) | [`run-ledger.md`](../../../../snippets/run-ledger.md) § 2: P3, UI lanes, ≤ 150 lines, checked by `@ux-reviewer` |
| Delivery run, before `@ux-designer` ships | `ai/runs/<run-id>/design.md` § `## State matrix`, inside the UI slice | `@architect` (delivery) | `/add-feature` P3 records `skips[]: {phase: P3, covered_by: "design.md UI slice (P4)"}` |
| No run (a design pass, an audit follow-up) | `ai/design/state-matrix/<feature>.md` | the session that runs this skill | lint it by path |

**This skill writes only into the file its caller owns.** `artifact-ownership.sh` denies a write to another role's artifact while a run is open. The lint reads `ux.md` first, then `design.md`.

## The states

| State | Required | The row must say |
|---|---|---|
| `loading` | always | what holds the space (a skeleton sized like the result, or a spinner), `aria-busy`, how long before a timeout turns it into `error` |
| `empty` | always | the copy for "nothing yet", and the copy for "nothing matches" when there is a filter; the action that fixes it |
| `error` | always | the message per failure kind (5xx, network), the retry, the way out |
| `partial` | always | which part fails alone and what the rest still shows |
| `permission` | always | 403: the copy and the request-access path, with no retry. 401: where it goes, and the return path |
| `offline` | always | the indicator; whether a write is rejected with a message or queued and shown as queued |
| `stale` | always | what stays on screen during a refetch, and what says the data may be old when the refetch fails |
| `pending-submit` | every write | the disabled control, the progress text, what happens to the inputs on failure |
| `destructive-confirm` | every delete or irreversible action | the confirm dialog, or the undo toast and its window |
| `not-found` | every detail route | the heading, the way back, the HTTP status on SSR |
| `unsaved-changes` | every form a user can lose work in | the leave guard, or the autosave |
| `long-content` | every surface rendering user data | the longest value, how it truncates, and the 320 px layout |
| `validation` | every form | when an error first shows (blur, not keystroke), and where server field errors land |
| `timeout` | a request with a stated budget | the deadline and what replaces the loader |

The **required** set is the seven above, and the conditional set the seven after them: `THR-UI-STATES` in `templates/governance/thresholds.json` (installed at `.claude/templates/governance/thresholds.json`). The lint reads that entry when installed, else this default; a project's `.claude/thresholds.local.json` may add states, never drop a required one. A state outside this vocabulary is an `unknown-state` finding, so a typo cannot pass as an extra row.

## The format

```markdown
## State matrix

Surfaces:
- `orders-list` — src/features/orders/OrdersPage.tsx, src/features/orders/OrderGrid.tsx
- `refund-dialog` — src/features/refunds/RefundModal.tsx

| Surface | State | Source | Expected (message · action · focus) | Proof |
|---|---|---|---|---|
| orders-list | loading | AC-001 | 10 skeleton rows, aria-busy · — · — | src/features/orders/OrdersPage.stories.tsx#Loading |
| orders-list | error | AC-004 | "Couldn't load orders" · Retry · focus stays on the table | e2e/orders/states.spec.ts::error shows retry |
| orders-list | offline | n-a | n-a — back-office surface on the office network; the client has no offline mode | — |
| refund-dialog | pending-submit | AC-006 | "Refunding…" · button disabled · inputs kept on 500 | src/features/refunds/RefundModal.test.tsx::one refund per double click |
```

The block above is an excerpt. A real matrix carries a row for every required state of every surface; the lint fails the excerpt with eleven `state-missing` findings.

- **Surfaces:** one line per surface, `` `id` — path, path ``. A path may be a directory. Each touched file that looks like a surface must fall under one of these paths.
- **Source:** the REQ or AC id the row comes from. One row per `IF … THEN` clause in `requirements.md`; `n-a` rows say `n-a`.
- **Expected:** what the user sees, in the contract's three parts. An `n-a` row starts with `n-a — ` and gives a reason of at least three words that says why the state cannot occur. "Not needed" is not a reason. "One endpoint feeds the whole list, so it cannot half-fail" is.
- **Proof:** one or more of `path#Export` (a story export), `path::<test title>`, `path:<line>`, split by `;`. The path must be a test or story file. A bare path passes, with a `proof-unanchored` advisory.

## Design mode (P3)

1. **Read the inputs.** Read `requirements.md`: every story's criteria, and every `IF … THEN` clause. Read the surfaces the feature touches: the routes or screens in the ask, `design.md` when it exists, and `build-graph.py --who-breaks` output when the graph exists. Read the design system's state components first, and reuse them before inventing one. To find them, run `ui-state-scan`'s grep 0d: the shared wrappers, the empty, error and skeleton components, and the confirm provider.
2. **List the surfaces** with their paths, in the format above.
3. **Write the required rows for each surface.** Each state either occurs or is `n-a` with a reason. A state occurs when the source can produce it (`ui-state-scan` § The rule, point 2): a network read can fail and can be refused; a list can be empty; a write can be sent twice.
4. **Add the conditional rows the surface has:**
   - `pending-submit` for each write;
   - `destructive-confirm` for each delete;
   - `not-found` for a detail route;
   - `unsaved-changes` for a long form;
   - `long-content` where user data renders;
   - `validation` for a form.
5. **Write the interface contract in each Expected cell.** It has three parts: the message (real copy, in the product's language), the action, and focus. Use the copy the product already uses for the same state elsewhere.
6. **Name the proof** for each row. It is the state-matrix test that will force the state (`ui-state-scan` § Proof): an MSW handler per state, a story per state, or a Playwright `page.route`. On mobile, a fake repository or a fake `UiState` flow. The test does not exist yet; name the file and the title it will have.
7. **Lint it:**

   ```bash
   python3 .claude/skills/state-matrix/scripts/state-matrix-lint.py --run=ai/runs/<run-id> --phase=design
   ```

   Fix every finding.
8. **Return** `DONE <path>`. If an open question changes a row (is a 403 possible for this role?), return `NEEDS_INPUT` with the question and its options. Never invent an answer to it.

## Lint mode (gate G12)

```bash
python3 .claude/skills/state-matrix/scripts/state-matrix-lint.py --run=ai/runs/<run-id> --base=<merge-base> --json
python3 .claude/skills/state-matrix/scripts/state-matrix-lint.py ai/design/state-matrix/<feature>.md --touched=<paths>
python3 .claude/skills/state-matrix/scripts/state-matrix-lint.py --repo=. --json      # whole-repo audit: the STATES line
python3 .claude/skills/state-matrix/scripts/state-matrix-lint.py --self-test
```

**Whole-repo audit (`--repo` alone).** The lint pools every `## State matrix` under `ai/runs/*/` (`ux.md`, else `design.md`) and `ai/design/state-matrix/*.md`. No matrix at all while the repo has surface files is one `no-matrix` finding and exit 1: the audit's STATES line is a gap, never a usage error. Surface files that no matrix covers are one `surfaces-uncovered` advisory with the count. Measured 2026-10-15 on a real NestJS + React monorepo with no matrix: before this mode, `--repo` alone printed the usage text and exited 2, and an audit could not tell "no matrix" from "lint broken"; now it exits 1 with `no-matrix` over 478 surface files (187 views, 122 dialogs, 116 pages, 49 panels, 2 routes, 2 sheets) in 0.3 s. A touched `…Dialog.tsx`, `…Sheet`, `…Drawer`, `…Modal` or `…Panel` file is a surface too: a dialog is a surface by `ui-state-scan` § The rule 1, and before this a touched POS dialog got neither `no-matrix` nor `surface-unlisted`. A backend `list-page.ts` no longer counts (`-page` names a surface only in `.vue` and `.svelte`).

**Exit codes:** 0 means no finding (PASS, or N-A with its reason). 1 means at least one finding. 2 means a usage or read error. This is the convention of `test-integrity.py` and `oracle-check.py`. `gate-check.py` reads 0 and 1 as "ran" and anything else as UNVERIFIED.

**`--json` shape:** `{verdict, reason, matrix, surfaces_checked, findings[{file, line, kind, message}], advisories[]}`.

**Findings:**

| Kind | Meaning |
|---|---|
| `no-matrix` | a T2/T3 UI run, or a touched surface, with no `## State matrix` |
| `surface-unlisted` | a touched page, screen, view, route, dialog, sheet, drawer, modal or panel file that no surface's paths cover |
| `state-missing` | a surface with no row for a required state |
| `na-without-reason` | an `n-a` row with no reason, or a placeholder for one |
| `no-proof` | a row that is not `n-a` and names no proof |
| `proof-missing` | a cited file that does not exist, or a `#Export`, `::title` or `:line` that is not in it (skipped in `--phase=design`) |
| `proof-not-a-test` | a proof that cites the component instead of its test or story |
| `unknown-state` | a state outside the vocabulary |
| `unknown-surface` | a row for an undeclared surface |
| `duplicate-row` | the same surface and state twice |
| `source-unknown` | a Source id that `requirements.md` does not define |

**Advisories** are printed but never fail: `clause-unmapped` (an `IF … THEN` criterion that no row cites) and `proof-unanchored` (a proof that names a file only).

**N-A:**

- the run has no frontend or mobile lane;
- a T1 run with no matrix (P3 is skipped at T1);
- no run, no matrix and no touched surface;
- `--repo` alone, when the repo has no matrix and no surface file.

A copy-only change touches catalogs, not surfaces, so it reads N-A.

**What the lint cannot see.** It proves that a cited test exists, not that the test forces the state or fails first. That half of G12 is `@ux-reviewer`'s: it opens each cited test and checks the handler and the assertion against the row. The state-matrix tests themselves are run at P7 like every other test.

**Gate wiring:** the check is `G12 state-matrix` in `.claude/gates.json`, in shadow mode like every new gate; `gate-check.py` runs the lint once per UI run in the change (`run_g12`), and a missing lint on a UI run is UNVERIFIED, never PASS. `@ux-reviewer` also runs it at P4 (`--phase=design`, on the UI slice) and at P8–P11 (on the diff), and reports the result in its review.

## Output

```
state-matrix — design · ai/runs/20261005-refunds-9c1e/ux.md
Surfaces: 2 (orders-list, refund-dialog) · rows 17 (12 proved · 5 n-a with a reason)
Lint (--phase=design): PASS — 2 surface(s), every required state written and proved or n-a with a reason
Advisories: 1 — AC-007 (IF the refund exceeds the order total THEN …) is cited by no row
Open: is a 403 possible for a support agent on /orders? (A) no — n-a with the role matrix as the reason · (B) yes — a permission row
```

## Halt conditions

- Do not write a row whose Expected is a placeholder ("handle error", "show empty state"). A row names the message, the action and the focus.
- Do not mark a state `n-a` because it is unlikely. `n-a` means it cannot occur, and the reason says why. A network read can always fail.
- Do not cite the component as the proof of its own state. Cite the test or the story that forces the state.
- Do not edit `requirements.md` to make a Source id resolve. Return `NEEDS_INPUT` to its writer.
- Do not write into a file another role owns during an open run. Write into the file your caller owns.
- In lint mode, do not report PASS from reading. The script's exit code is the result.

## Related

- `ui-state-scan` (this pack) finds the surfaces that cannot render a state; its § Proof is the test shape every row names.
- `design-canvas` (this pack) draws the empty, loading and error artboards for the same surfaces before code.
- `@ux-reviewer` reviews the matrix at P4 and the surfaces at P8–P11, and signs G12.
- `/add-feature` (delivery pack) P3 and [`run-ledger.md`](../../../../snippets/run-ledger.md) define who writes `ux.md` and `design.md`.
