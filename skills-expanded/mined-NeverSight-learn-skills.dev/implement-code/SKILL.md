---
name: implement-code
version: 4
description: >-
  Implement a **non-UI** phase — backend, library, CLI, infra, data pipeline — from a plan at `.plans/<feature>/plan.md`; the phase must have no UI work (components, pages, styling, interactions). Triggers on "implement phase X", "do phase N", "build phase 2 of <feature>". Prefers FP idioms (pure functions, immutability, composition); falls back to OOP for class-based languages or OOP-heavy codebases (`FP.md`). Optional **TDD mode** (red→green→refactor) on "tdd" / "test-first" — see `TDD.md`.
---

# Implement-code (FP-first, no UI)

Execute exactly **one phase** of a plan for non-UI code (backend services, libraries, CLIs, scripts, infra, data pipelines, etc.). Output is real production code plus an implementation report. The skill leaves the working tree on a clean series of atomic commits — one per acceptance criterion — and never amends.

## Inputs and outputs
- **Code output:** edits to project source.
- **Report output:** `<cwd>/.plans/<feature>/implementations/code/{feat,fix,refactor}/<phase_number>.md` — what was built, decisions made (FP choices, complexity), and any deviations from the plan. Subdirectory choice (`feat` / `fix` / `refactor`) follows the dominant intent of the phase: new behaviour → `feat`, bug-fix → `fix`, internal restructure with no behaviour change → `refactor`. If mixed, default to `feat`.

This skill **does not** read `<cwd>/.plans/DESIGN.md` and **does not** invoke any other skill. If the chosen phase touches a UI surface, hard-stop and tell the user to use a UI-oriented implementation skill instead — one that reads `.plans/DESIGN.md` and `.plans/UI-RULES.md`.

## Modes

Two modes — **default** and **TDD**. Pick once at the start of the invocation; do not switch mid-phase.

- **Default mode** — write code, then run the narrowest automated check that proves the AC, then commit. One commit per AC.
- **TDD mode** — strict red → green → refactor per AC. Activated when the user's prompt contains "tdd", "use tdd", "tdd mode", or "test-first", **or** when (during preconditions) the user explicitly opts in. In TDD mode, each AC produces 2–3 commits (`[red]` failing test, `[green]` passing code, optional `refactor`). Full discipline in [TDD.md](TDD.md).

If the prompt contains a near-trigger that doesn't match the list exactly (e.g. "write tests as you go", "test everything"), ask once with AskUserQuestion during preconditions; default to non-TDD if they decline to choose. Do **not** ask when no trigger phrase appeared — silence means default mode.

## Mandatory preconditions

Run **before** writing any code, in this order:

1. **Discover the plan.** Glob `<cwd>/.plans/*/plan.md`. If multiple, AskUserQuestion which `<feature>`. If zero, hard-stop and tell the user a plan file must exist at `.plans/<feature>/plan.md` first.
2. **Pick the phase.** Read the plan and list every phase title with its count of unchecked ACs. AskUserQuestion which phase number. If the user already supplied "phase N" in the prompt, use it directly. **Hard-stops:**
   - Plan has no phases (malformed) → tell the user the plan file at `.plans/<feature>/plan.md` needs phases before this skill can run.
   - Requested phase number does not exist → list the valid numbers and stop.
   - Every AC in the chosen phase is already `[x]` → tell the user the phase is complete; suggest the next phase with unchecked ACs, or ask them to explicitly re-open an AC.
3. **Reject UI phases.** Scan the chosen phase's ACs for UI markers and **hard-stop** if any apply, telling the user: *"This phase touches a UI surface — use a UI-oriented implementation skill instead, one that reads `.plans/DESIGN.md` and `.plans/UI-RULES.md`."* Do not silently fall through.

   **UI markers (any one triggers rejection):**
   - **Frameworks / tooling:** React / Vue / Svelte / Solid / Angular / Next.js / Nuxt / SvelteKit / Remix / Astro / Qwik / shadcn / Tailwind / Radix / Framer Motion / Storybook / a design-token reference (`DESIGN.md`, `colors`, `typography`, `rounded`, `spacing`).
   - **File extensions in changed files:** `.tsx`, `.jsx`, `.vue`, `.svelte`, `.astro`, `.css`, `.scss`, `.sass`, `.module.css`.
   - **Concept words in AC text:** `component`, `page`, `layout`, `screen`, `view` (when paired with a UI framework or route), `modal`, `dialog`, `dropdown`, `toast`, `interaction`, `animation`, `transition`, `theme`, `responsive`, `breakpoint`, `viewport`, `aria-*`, `dark mode`, `hover state`, `focus ring`, `JSX`, `DOM`.

   **Not UI (do not reject):** PDF rendering, server-side template rendering for emails (Jinja, Handlebars, MJML — when the AC is "send the email", not "design the template"), gRPC server-streaming, graphics-engine renderers, JSON-rendering/serialization. The literal word `render` is **not** a marker on its own — only flag it when paired with a UI framework, the DOM, or a UI surface.
4. **Research third-party patterns.** Confirm versions from `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / etc. before assuming APIs. **Source order:** check `<cwd>/.library/` first — if a directory matching the library name (or close variant) exists, treat it as the authoritative local cache and read it directly. If absent or clearly stale relative to the manifest version, fall back to Exa (`get_code_context_exa` for fresh code examples, `web_search_exa` for recent docs/tutorials). Use Context7 (`resolve-library-id` + `query-docs`) as a final fallback for canonical API reference when Exa results are insufficient. Note in the implementation report which source was used per library.

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
3. **Run the narrowest automated check that proves the AC.** Pick by type: **unit test** for pure functions, parsers, mappers, validators; **integration / contract test** for HTTP handlers, DB queries, message-bus interactions, CLI invocations; **end-to-end test** only when narrower levels can't capture the AC. If the AC is purely operational (a script that runs once, a migration with no domain logic), document the verification step you ran (the command, the observed output) in the implementation report instead of synthesizing a hollow assertion.
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

If an AC genuinely cannot be tested first, document the carve-out in the implementation report and fall back to the default-mode loop for that AC only — see [TDD.md](TDD.md) for the catalogue of legitimate cases.

## Implementation report

Write to `<cwd>/.plans/<feature>/implementations/code/{feat,fix,refactor}/<phase_number>.md`. Include:

- **Summary** — one paragraph: what the phase delivered end-to-end.
- **Acceptance criteria** — copy each AC verbatim with its commit SHA. In TDD mode, list the red / green / (optional) refactor SHAs per AC, plus any "Don't test" carve-outs with reasoning.
- **FP decisions** — which FP idioms were used and why; any place OOP was unavoidable (with the language/codebase reason).
- **Complexity notes** — Big-O for any non-trivial loop, recursion, or data-structure choice.
- **Deviations from the plan** — any AC reinterpreted or split, with reasoning.
- **Open follow-ups** — anything surfaced during implementation that belongs in the next phase or a new plan. Always include this section; if nothing surfaced, write "None.".

## What NOT to do

- **Don't implement more than one phase per invocation.** If the user asks "do phases 2 and 3", implement only the lowest-numbered phase and **hard-stop** with an explicit instruction to re-invoke for the next phase. Do not chain phases internally.
- **Don't accept UI phases.** This skill is for non-UI code only. If the phase touches components, pages, layouts, styling, or interactions, hard-stop and tell the user to use a UI-oriented implementation skill instead. Do not attempt UI work without the design preconditions such a skill enforces.
- **Don't read `DESIGN.md` or invoke any other skill.** This skill is intentionally self-contained — no design loading, no discussion loops, no requirement-clarification side-quests. If the plan's ACs are ambiguous, surface the ambiguity to the user and stop; do not invoke another skill to resolve it.
- **Don't fight the codebase.** If the project is OOP-heavy or in an OOP-native language, FP-discipline still applies inside functions (pure helpers, immutability, no hidden state) but do not rip out the surrounding class structure. See [FP.md](FP.md).
- **Don't bake in implementation details that the plan deliberately left abstract.** Routes / schema / model names are stable; concrete file paths and function names are not — match the codebase's actual layout, don't invent.
- **Don't `git add -A`** or commit unrelated working-tree changes. Stage only the files that satisfy the current AC.
- **Don't amend, force-push, or use `--no-verify`** without explicit user authorization. "Explicit" means the user types something unambiguous like `yes, bypass hooks` or `use --no-verify` — a generic "ok" or "go ahead" mid-conversation does **not** qualify. Always create a new commit when fixing a hook failure.
- **In TDD mode, don't skip red.** Production code without a preceding failing test for the same AC violates the cycle — even if "the test is obvious." Don't write green and refactor in the same commit either. See [TDD.md](TDD.md).
