---
name: implement-with-instructions
version: 4
description: >-
  Implement freeform user instructions as acceptance criteria (ACs), one atomic commit per AC — no plan file or design rulebook required. Triggers: "implement <thing>", "build <feature> end-to-end", "just implement <description>", "ship <X> end-to-end". For phases of an existing plan at `<cwd>/.plans/<feature>/plan.md`, don't fire. Writes a report at `<cwd>/.plans/<slug>/implementations/with-instructions/{feat,fix,refactor}/run.md` with open follow-ups. FP-first; optional TDD mode.
---

# Implement-with-instructions

Execute the user's instructions as a list of **acceptance criteria (ACs)** — small, end-to-end behaviours that each compile, run, and demonstrate an observable signal. Output is real production code committed atomically. No plan file, no UI rulebook, no design tokens file required.

## Inputs and outputs

- **Input:** the user's freeform instructions in the conversation. Optional: pasted sketches, file pointers, screenshots.
- **Code output:** edits to project source.
- **Commits:** one atomic commit per AC (or per red/green/refactor step in TDD mode).
- **Report output:** `<cwd>/.plans/<slug>/implementations/with-instructions/{feat,fix,refactor}/run.md` — what was built, decisions made (FP choices, complexity), and any open follow-ups. Subdirectory choice (`feat` / `fix` / `refactor`) follows the dominant intent of the work: new behaviour → `feat`, bug-fix → `fix`, internal restructure with no behaviour change → `refactor`. If mixed, default to `feat`. If `run.md` already exists at that path, write `run-2.md`, `run-3.md`, etc. — never overwrite.

## What an AC means

An acceptance criterion (AC) is the smallest end-to-end piece that is **observable** — something a caller, a test, or a user can run and see. Examples: an HTTP endpoint returning a hardcoded response; a pure function plus the test that pins its first behaviour; a button that opens a modal with placeholder content; a migration plus the model field it backs.

ACs are **not** "create the file", "add the import", "write the docstring". If a unit cannot be exercised on its own, fold it into the next observable step.

**Source of ACs.** Dynamic — if the user's instructions already enumerate acceptance criteria (numbered list, checklist, pasted plan content), take those verbatim. Otherwise, derive the AC list from the freeform instructions during preconditions step 1.

## Modes

Two modes — **default** and **TDD**. Pick once at the start of the invocation; do not switch mid-run.

- **Default mode** — write code, run the narrowest automated check that proves the AC, commit.
- **TDD mode** — strict red → green → refactor per AC. Activated when the user's prompt contains "tdd", "use tdd", "tdd mode", or "test-first", **or** when (during preconditions) the user explicitly opts in. Full discipline in [TDD.md](TDD.md).

If the prompt contains a near-trigger that doesn't match the list exactly (e.g. "write tests as you go"), ask once with AskUserQuestion during preconditions; default to non-TDD if the user declines to choose. Do **not** ask when no trigger phrase appeared — silence means default mode.

## Mandatory preconditions

Run **before** writing any code, in this order:

1. **Derive the AC list and pick a slug.** If the user's instructions already enumerate acceptance criteria (numbered list, checklist, pasted plan content), take them verbatim. Otherwise, translate the freeform instructions into a numbered list of ACs — each with a verb-led title and the observable signal that proves it (test, endpoint behaviour, visible UI state, CLI output). Propose a short kebab-case `<slug>` derived from the instructions (e.g. `add-jwt-auth`, `fix-cache-eviction`) — this names the report directory under `<cwd>/.plans/<slug>/`. Surface the AC list **and** the proposed slug together with AskUserQuestion: "Proceed with these ACs and slug `<slug>`, edit either, or change scope?" Do not start implementation until the user confirms both. **Hard-stop** if the instructions are too vague to produce ACs — ask one round of clarifying questions, then stop if still ambiguous. Once confirmed, register each AC in the task list via TaskCreate (status `pending`) so progress is visible throughout the run.
2. **Research third-party patterns.** Confirm versions from `package.json` / `pyproject.toml` / `Cargo.toml` / equivalent before assuming APIs. **Source order:** check `<cwd>/.library/` first — if a directory matching the library name (or close variant) exists, treat it as the authoritative local cache. If absent or stale, fall back to Exa (`get_code_context_exa` for fresh code examples, `web_search_exa` for recent docs). Use Context7 (`resolve-library-id` + `query-docs`) as a final fallback for canonical API reference. Note in the final summary which source was used per library.

   **Before installing or upgrading any third-party package**, run the package manager's view command first to confirm the latest published version, then pin explicitly. Pick the command that matches the project's manager: `npm view <pkg> version`, `pnpm view <pkg> version`, `yarn info <pkg> version`, `bun pm view <pkg> version`, `pip index versions <pkg>` (or `uv pip index versions <pkg>`), `poetry show <pkg> --latest`, `cargo info <pkg>`, `go list -m -versions <module>`, `gem search -e <pkg>`, `composer show <pkg> --available`. Surface major-version jumps to the user before adopting.
3. **Detect language paradigm.** Determine whether the target language is OOP-native (Java, C#, Kotlin/JVM, Swift, Dart, Objective-C, Smalltalk family) or whether the existing codebase already uses OOP heavily. Ruby and PHP are FP-default but flip to OOP when the codebase is class-heavy. See [FP.md](FP.md) for the full classification — it drives the FP discipline applied during implementation.
4. **Verify the working tree is clean.** Run `git status --short`. If anything is staged, modified, or untracked-and-relevant, surface the diff and **hard-stop** — do not absorb the user's unrelated work into AC commits.

Only proceed to implementation after 1–4 are complete.

## Implementation loop (default mode)

For each AC in the agreed list, run this loop:

1. **Re-confirm the tree is clean** before staging — formatters, generated files, or hooks between ACs can dirty it. If unexpectedly dirty, stop and surface to the user. Mark the current AC's task as `in_progress` (TaskUpdate).
2. **Write the code.** Apply FP discipline (see [FP.md](FP.md)): pure functions over methods on classes, immutable data, composition over inheritance, exhaustive matching where the language supports it. Optimise for readability first; flag any non-trivial Big-O choice in the final summary.
3. **Prove the AC.** Run the narrowest automated check that demonstrates the observable signal: unit test for pure functions, integration / contract test for API endpoints, end-to-end test or a manual run for UI / CLI surfaces. If the AC is purely visual, invite the user to look before committing.
4. **Commit atomically.** Stage only the files that changed for this AC (never `git add -A`). Message format: `AC<i>: <verb-led summary>` where `<i>` is the AC's 1-based ordinal in the agreed list (fixed across re-runs). Include the AC description verbatim in the commit body. After the commit lands, mark the AC's task as `completed` (TaskUpdate).
5. **Never amend.** If a pre-commit hook fails, fix the underlying issue and create a **new** commit. Do not use `--no-verify` to bypass hooks unless the user explicitly authorises it (see What NOT to do).

When all ACs are committed, write the implementation report (see below). Do not push — leave that to the user.

## Implementation loop (TDD mode)

When TDD mode is active, replace steps 2–4 with the **red → green → refactor** cycle per AC. Full discipline (triangulation, multi-behaviour AC handling, carve-out catalogue) in [TDD.md](TDD.md). Commit messages use TDD prefixes so the cycle is machine-distinguishable in `git log`:

- `test: AC<i> [red]: <summary>` — failing test only, production code unstaged.
- `feat: AC<i> [green]: <summary>` — minimum production code to pass.
- `refactor: AC<i>: <what changed>` — optional, only if cleanup is warranted and tests stay green throughout.

Mark the AC's task as `in_progress` before the red commit and `completed` after the green commit (or after the final green in a multi-behaviour AC). A subsequent refactor commit does not require re-opening the task.

If an AC genuinely cannot be tested first, document the carve-out in the implementation report and fall back to the default-mode loop **for that AC only**.

## Implementation report

Write to `<cwd>/.plans/<slug>/implementations/with-instructions/{feat,fix,refactor}/run.md` (or `run-2.md`, `run-3.md`, … if a prior run file exists at that path — never overwrite). Pick the subdirectory by dominant intent: new behaviour → `feat`, bug-fix → `fix`, internal restructure with no behaviour change → `refactor`. If mixed, default to `feat`. Create parent directories as needed.

Include:

- **Summary** — one paragraph: what the run delivered end-to-end.
- **Acceptance criteria** — copy each AC verbatim with its commit SHA. In TDD mode, list the red / green / (optional) refactor SHAs per AC, plus any "Don't test" carve-outs with reasoning.
- **FP decisions** — which FP idioms were used and why; any place OOP was unavoidable (with the language/codebase reason).
- **Complexity notes** — Big-O for any non-trivial loop, recursion, or data-structure choice.
- **Third-party sources** — `<cwd>/.library/`, Exa, or Context7 — per library touched.
- **Open follow-ups** — anything surfaced during implementation that was out of scope for the agreed AC list, or worth tackling next. Always include this section; if nothing surfaced, write "None.".

After writing the report, post a one-line pointer to its path in the conversation so the user knows where it landed.

## What NOT to do

- **Don't expand scope silently.** If during implementation you spot work that wasn't in the agreed AC list, surface it in the final summary as an open follow-up; do not just add an AC.
- **Don't fight the codebase.** If the project is OOP-heavy or in an OOP-native language, FP-discipline still applies inside functions (pure helpers, immutability, no hidden state) but do not rip out the surrounding class structure. See [FP.md](FP.md).
- **Don't `git add -A`** or commit unrelated working-tree changes. Stage only the files that satisfy the current AC.
- **Don't amend, force-push, or use `--no-verify`** without explicit user authorisation. "Explicit" means the user types something unambiguous like `yes, bypass hooks` or `use --no-verify` — a generic "ok" or "go ahead" mid-conversation does **not** qualify. Always create a new commit when fixing a hook failure.
- **Don't invent a plan file or `<cwd>/.plans/` artefacts.** This skill deliberately operates without them. If the user wants persistent planning artefacts, they need a plan file at `<cwd>/.plans/<feature>/plan.md` and a plan-driven implementer instead.
- **In TDD mode, don't skip red.** Production code without a preceding failing test for the same AC violates the cycle — even if "the test is obvious." Don't write green and refactor in the same commit either. See [TDD.md](TDD.md).
