---
name: implement-with-design
version: 2
description: >-
  Execute one phase of a phased plan file at `<cwd>/.plans/<feature>/plan.md` when the phase touches UI (components, pages, layouts, styling, interactions) or mixes UI with non-UI work. For purely non-UI phases (backend, library, CLI, infra, scripts), don't fire. Triggers include "implement phase X", "do phase N", "start implementation", "build phase 2 of <feature>". Writes production code satisfying every acceptance criterion and creates one atomic git commit per AC. FP-first with OOP fallback; supports optional TDD mode (red → green → refactor) when the user opts in.
---

# Implement-with-design (FP-first)

Execute exactly **one phase** of a plan. Output is real production code plus an implementation report. The skill leaves the working tree on a clean series of atomic commits — one per acceptance criterion — and never amends.

## Inputs and outputs

- **Plan input:** `<cwd>/.plans/<feature>/plan.md` — a phased plan file. Phases are demarcated by `---` separators with `## Phase N: <Title>` headings and `- [ ]` acceptance criteria.
- **Design input (UI phases only):** `<cwd>/.plans/UI-RULES.md` (the project's UI rulebook — aesthetic direction, typography, colour & theme, spatial & motion decisions, project-specific bans, AI Slop Test) and `<cwd>/.plans/DESIGN.md` (design tokens — `colors`, `typography`, `rounded`, `spacing`). Both are loaded during precondition step 3 — see step 3 for behaviour when either is missing.
- **Code output:** edits to project source.
- **Report output:** `<cwd>/.plans/<feature>/implementations/with-design/{feat,fix,refactor}/<phase_number>.md` — what was built, decisions made (FP choices, complexity, design decisions for UI), and any deviations from the plan. Subdirectory choice (`feat` / `fix` / `refactor`) follows the dominant intent of the phase: new behaviour → `feat`, bug-fix → `fix`, internal restructure with no behaviour change → `refactor`. If mixed, default to `feat`.

## Modes

Two modes — **default** and **TDD**. Pick once at the start of the invocation; do not switch mid-phase.

- **Default mode** — write code, then run the narrowest automated check that proves the AC, then commit. One commit per AC.
- **TDD mode** — strict red → green → refactor per AC. Activated when the user's prompt contains "tdd", "use tdd", "tdd mode", or "test-first", **or** when (during preconditions) the user explicitly opts in. In TDD mode, each AC produces 2–3 commits (`[red]` failing test, `[green]` passing code, optional `refactor`). Full discipline in [TDD.md](TDD.md).

If the prompt contains a near-trigger that doesn't match the list exactly (e.g. "write tests as you go", "test everything"), ask once with AskUserQuestion during preconditions; default to non-TDD if they decline to choose. Do **not** ask when no trigger phrase appeared — silence means default mode.

## Mandatory preconditions

Run **before** writing any code, in this order:

1. **Discover the plan.** Glob `<cwd>/.plans/*/plan.md`. If multiple, AskUserQuestion which `<feature>`. If zero, hard-stop and tell the user no plan file exists at `<cwd>/.plans/<feature>/plan.md` — one must be created before this skill can run.
2. **Pick the phase.** Read the plan and list every phase title with its count of unchecked ACs. AskUserQuestion which phase number. If the user already supplied "phase N" in the prompt, use it directly. **Hard-stops:**
   - Plan has no phases (malformed) → tell the user the plan file is missing `## Phase N:` headings and needs to be fixed.
   - Requested phase number does not exist → list the valid numbers and stop.
   - Every AC in the chosen phase is already `[x]` → tell the user the phase is complete; suggest the next phase with unchecked ACs, or ask them to explicitly re-open an AC.
3. **Load design context (only if the phase touches a UI surface).** Read `<cwd>/.plans/UI-RULES.md` end-to-end — its content sections are authoritative for UI work in this project (canonical section list in [REFERENCE.md](REFERENCE.md) §1). Read `<cwd>/.plans/DESIGN.md` — its frontmatter (`colors`, `typography`, `rounded`, `spacing`) and prose sections are the token source of truth. **Hard-stops:**
   - `<cwd>/.plans/UI-RULES.md` is missing → hard-stop and tell the user UI work requires a persisted `<cwd>/.plans/UI-RULES.md` rulebook (canonical section list in [REFERENCE.md](REFERENCE.md) §1). There is no ad-hoc fallback; project UI rules must be explicit and persisted.
   - `<cwd>/.plans/DESIGN.md` is missing → hard-stop and tell the user UI work requires a `<cwd>/.plans/DESIGN.md` token file (frontmatter: `colors`, `typography`, `rounded`, `spacing`).
4. **Research third-party patterns.** Confirm versions from `package.json` / `pyproject.toml` / etc. before assuming APIs. **Source order:** check `<cwd>/.library/` first — if a directory matching the library name (or close variant) exists, treat it as the authoritative local cache and read it directly. If absent or clearly stale relative to the manifest version, fall back to Exa (`get_code_context_exa` for fresh code examples, `web_search_exa` for recent docs/tutorials). Use Context7 (`resolve-library-id` + `query-docs`) as a final fallback for canonical API reference when Exa results are insufficient. Note in the implementation report which source was used per library.

   **Before installing or upgrading any third-party package**, run the package manager's view command first to confirm the latest published version, then pin to that version explicitly (or the latest within the project's allowed range). Pick the command that matches the project's manager:
   - npm → `npm view <pkg> version` (or `npm view <pkg> versions --json` to see all)
   - pnpm → `pnpm view <pkg> version`
   - yarn → `yarn info <pkg> version`
   - bun → `bun pm view <pkg> version`
   - pip / uv → `pip index versions <pkg>` (or `uv pip index versions <pkg>`)
   - poetry → `poetry search <pkg>` then `poetry show <pkg> --latest`
   - cargo → `cargo search <pkg> --limit 1` (or `cargo info <pkg>`)
   - go → `go list -m -versions <module>`
   - gem → `gem search -e <pkg>`
   - composer → `composer show <pkg> --available`

   If the latest version is materially newer than what the project would otherwise pin (e.g., a major-version jump), surface the choice to the user before installing — do not silently adopt a major upgrade as part of an AC.
5. **Detect language paradigm.** Determine whether the target language is inherently OOP (Java, C#, Kotlin/JVM, Swift, Dart, Objective-C, Smalltalk family) or whether the existing codebase already uses OOP heavily. **Ruby and PHP are FP-default but flip to OOP when the codebase is class-heavy** — see [FP.md](FP.md) for the full classification. The result drives FP discipline.
6. **Verify the working tree is clean.** Run `git status --short`. If anything is staged, modified, or untracked-and-relevant, surface the diff and **hard-stop** — do not absorb the user's unrelated work into AC commits.

Only proceed to implementation after 1–6 are complete.

## Implementation loop (default mode)

For each acceptance criterion in the chosen phase, run this loop:

1. **Re-confirm the tree is clean** before staging — automated tooling between ACs (formatters, generated files, hooks) can dirty it. If dirty for an unexpected reason, stop and surface to the user.
2. **Write the code.** Apply FP discipline (see [FP.md](FP.md)): pure functions over methods on classes, immutable data, composition over inheritance, exhaustive switch / pattern matching where the language supports it. Optimize for readability first; then keep an eye on asymptotic complexity — call out any non-trivial Big-O choice in the report.
3. **Run the narrowest automated check that proves the AC.** Pick by type: **unit test** for pure functions, **integration / contract test** for API endpoints, **end-to-end test or visual inspection through the AI Slop Test** for UI ACs. For UI work, also follow the full checklist in [REFERENCE.md](REFERENCE.md) before marking the AC done.
4. **Tick the AC** in `plan.md` from `- [ ]` to `- [x]`.
5. **Commit atomically.** One commit per AC. Stage only the files that changed for this AC (never `git add -A`). Message format: `<feature> phase <N> AC<i>: <verb-led summary>` where `<feature>` is the directory name verbatim (hyphens, underscores, and case preserved as-is — e.g. `user-auth`, not `user auth`) and `<i>` is the AC's **1-based ordinal position in the plan** (fixed across re-runs), not the loop iteration. Example: `auth phase 2 AC3: validate session cookie on /me`. Include the AC text verbatim in the commit body.
6. **Never amend.** If a pre-commit hook fails, fix the underlying issue and create a **new** commit. Do not use `--no-verify` to bypass hooks unless the user explicitly authorizes it (see What NOT to do for the bar that counts as "explicit").

When all ACs in the phase are checked, write the implementation report (see below). Do not push — leave that to the user.

## Implementation loop (TDD mode)

When TDD mode is active, replace steps 2–5 with the **red → green → refactor** cycle per AC. Full discipline (triangulation, multi-behaviour AC handling, carve-out catalogue) in [TDD.md](TDD.md).

The `test:` / `feat:` / `refactor:` prefixes below are intentional — they make the three TDD phases machine-distinguishable in `git log`. Default-mode commits deliberately omit a conventional-commit prefix to stay simpler; do not retrofit.

1. **Re-confirm the tree is clean.**
2. **Red.** Write the smallest failing test that pins the AC. Run it; **verify it fails for the right reason** (assertion, not import error or syntax). Stage only the test source file(s) — exclude any auto-generated snapshots, fixtures, or coverage artefacts. Commit: `test: <feature> phase <N> AC<i> [red]: <summary>`. Body: AC verbatim + the failing assertion.
3. **Green.** Write the **minimum** production code to make the test pass — no extras, no speculative abstractions. Run the full test suite for the touched area; everything must pass. Stage only the production code. Commit: `feat: <feature> phase <N> AC<i> [green]: <summary>`. Body: AC verbatim.
4. **Refactor (optional).** Only if cleanup is warranted (duplication, naming, FP-discipline pull from [FP.md](FP.md)) and tests stay green throughout. Never mix new behaviour into a refactor commit. Commit: `refactor: <feature> phase <N> AC<i>: <what changed>`.
5. **Tick the AC** in `plan.md` after the green commit (or the last green for a multi-behaviour AC). Same plan-ordinal `<i>` rule as default mode. A subsequent refactor commit does **not** require un-ticking.
6. **Never amend** — same rule as default mode.

If an AC genuinely cannot be tested first, document the carve-out in the implementation report and fall back to the default-mode loop for that AC only — see [TDD.md](TDD.md) for the catalogue of legitimate cases and the boundary tests.

## Implementation report

Write to `<cwd>/.plans/<feature>/implementations/with-design/{feat,fix,refactor}/<phase_number>.md`. Include:

- **Summary** — one paragraph: what the phase delivered end-to-end.
- **Acceptance criteria** — copy each AC verbatim with its commit SHA. In TDD mode, list the red / green / (optional) refactor SHAs per AC, plus any "Don't test" carve-outs with reasoning.
- **FP decisions** — which FP idioms were used and why; any place OOP was unavoidable (with the language/codebase reason).
- **Complexity notes** — Big-O for any non-trivial loop, recursion, or data-structure choice.
- **Design decisions** (UI phases only) — aesthetic direction, font pairing + rationale, palette in OKLCH, motion choices, which Absolute Bans were actively avoided.
- **Deviations from the plan** — any AC reinterpreted or split, with reasoning.
- **Open follow-ups** — anything surfaced during implementation that belongs in the next phase or a new plan. Always include this section; if nothing surfaced, write "None.".

## What NOT to do

- **Don't implement more than one phase per invocation.** If the user asks "do phases 2 and 3", implement only the lowest-numbered phase and **hard-stop** with an explicit instruction to re-invoke for the next phase. Do not chain phases internally.
- **Don't fight the codebase.** If the project is OOP-heavy or in an OOP-native language, FP-discipline still applies inside functions (pure helpers, immutability, no hidden state) but do not rip out the surrounding class structure. See [FP.md](FP.md).
- **Don't bake in implementation details that the plan deliberately left abstract.** Routes / schema / model names are stable; concrete file paths and function names are not — match the codebase's actual layout, don't invent.
- **Don't skip preconditions.** Especially loading `<cwd>/.plans/UI-RULES.md` + `<cwd>/.plans/DESIGN.md` for UI work — they exist to keep output off the AI-slop axis.
- **Don't `git add -A`** or commit unrelated working-tree changes. Stage only the files that satisfy the current AC.
- **Don't amend, force-push, or use `--no-verify`** without explicit user authorization. "Explicit" means the user types something unambiguous like `yes, bypass hooks` or `use --no-verify` — a generic "ok" or "go ahead" mid-conversation does **not** qualify. Always create a new commit when fixing a hook failure.
- **In TDD mode, don't skip red.** Production code without a preceding failing test for the same AC violates the cycle — even if "the test is obvious." Don't write green and refactor in the same commit either. See [TDD.md](TDD.md).
