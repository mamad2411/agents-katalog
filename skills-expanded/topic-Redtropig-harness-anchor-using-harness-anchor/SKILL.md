---
name: using-harness-anchor
description: Use whenever working in a project. Establishes state/scope/verification discipline. Auto-loaded at session start. Complements superpowers.
---

# Using harness-anchor

You have the **harness-anchor** runtime layer, companion to `superpowers` (process methodology): it anchors **state persistence, scope boundaries, verification gates, and C/C++ engineering**.

<!-- os-windows-start -->
**Windows session (Git-Bash):** plugin scripts already handle path and JSON-engine portability — do not hand-"fix" MSYS paths or shell out to PowerShell. C/C++ caveat: TSan/LSan are unavailable on this platform; read the `cpp-sanitizers` skill's Windows platform notes before trusting sanitizer coverage.
<!-- os-windows-end -->

## Priority Order

1. **User's explicit instructions** (CLAUDE.md, direct requests) — highest
2. **superpowers skills** (process)
3. **harness-anchor skills** (state/scope/verification/cpp)
4. Default system prompt — lowest

On apparent conflict, prefer superpowers' process and use harness-anchor to **anchor** state/evidence around it.

## Project Navigation (read these BEFORE acting)

If they exist in the project root, read in this order:

1. `AGENTS.md` or `CLAUDE.md` — operating manual
2. `feature_list.json` — active feature + scope + done criteria
3. `PROJECT-TOC.md` — file-level index, one line per file
4. `golden-rules.md` — project taste / anti-pattern rules to honor
5. `session-handoff.md` — what previous session left

If none exist, the project is **un-anchored**. Suggest the user run `/anchor` to scaffold.

## Sibling Skills (load when triggered)

- `project-indexing` — need to find files; PROJECT-TOC.md before Glob
- `feature-state-keeper` — feature work starts/finishes; updates feature_list.json + progress.md
- `init-verification` — at start of work; run `init.sh` health check
- `self-correction-loop` — after edits that fail lint/build; iterate with evidence
- `anti-hallucination-gates` — before claiming "done"; Default-FAIL evidence contract
- `test-coverage-design` — what to test / is coverage real before "done"; dispatches `coverage-analyst`
- `capturing-golden-rules` — a mistake recurs / a review comment is really a convention; encode it in golden-rules.md
- `context-budget-discipline` — context fills up; SELECT/WRITE/COMPRESS/ISOLATE
- `docs-lookup` — unfamiliar tools/APIs/errors; Context7 → WebSearch → calibrated-uncertainty chain
<!-- cpp-only-start -->
- `cpp-build-systems` — CMake/Meson/Make/Bazel project
- `cpp-static-analysis` — clang-tidy / cppcheck / IWYU
- `cpp-formatting` — clang-format
- `cpp-sanitizers` — ASan / UBSan / TSan / valgrind
<!-- cpp-only-end -->

## Hard Rules

1. **No "done" without evidence — and no "absent" without scope.** "pass" requires compile + tests + lint with concrete output paths; lacking evidence → status stays `in-progress`. The same rule runs in reverse: a claim that something is missing (tool not installed, no such function) must state what you searched and when — `searched <scope>, not found (as of <date>)`. Express uncertainty: *"I am uncertain whether X passes because <reason>."*
2. **One active feature at a time** unless explicit multi-feature plan. Unrelated mid-feature request → surface the scope-jump and confirm before pivoting.
3. **State lives on disk, not in chat.** Update `feature_list.json` / `progress.md` / `session-handoff.md`.
4. **PROJECT-TOC.md before Glob.**
5. **Subagents are single-level.** Never invoke a subagent from within a subagent — a dispatched worker must not run the subagent-backed gates `/verify` · `/test-plan` · `/gc`; the parent runs them after workers integrate.
6. **When stuck, follow `docs-lookup`.** Never guess at unfamiliar tools/APIs/errors.

**Interop seams with superpowers** (contract in the named skill): parallel/subagent dispatch → `feature-state-keeper`; worktree setup → `init-verification`; sensor-finding triage → `self-correction-loop` (+ `receiving-code-review`).

## Commands — recommend them at the right moment

Commands never auto-trigger (unlike skills). Surfacing the right one — with a one-line why — is your job.

- `/anchor` — project un-anchored (no `feature_list.json`): scaffolds the state files.
<!-- cpp-only-start -->
- `/cpp-init` — C/C++ project with no `.clang-format`/`.clang-tidy` (right after `/anchor`): drops C/C++ config + sanitizer build.
<!-- cpp-only-end -->
- `/index-project` — `PROJECT-TOC.md` absent or stale, or before a broad file search: (re)builds the index.
- `/verify` — before claiming a feature passes or flipping status to `pass`: build + lint + tests in a fresh-context subagent (`--fix` = bounded ≤2-cycle auto-fix).
- `/test-plan` — after implementing, before marking `pass`: fresh-context coverage-gap analysis. Complements `/verify`.
- `/gc` — after a batch of generated code, before `/session-end`: fresh-context drift/entropy scan vs `golden-rules.md` + slop heuristics. Read-only (not `git gc`).
<!-- cpp-only-start -->
- `/sanitize` — after a C/C++ source change, or before merging C/C++: ASan+UBSan run (TSan separately) with an evidence log.
<!-- cpp-only-end -->
- `/status` — "where am I / what's the state": read-only snapshot, writes nothing.
- `/session-end` — at a stopping point: writes handoff, appends `progress.md`, offers over-budget state archival + a commit.

## When to NOT use this

- Inside a subagent dispatched for a narrow task (its own prompt governs)
- When the user has explicitly disabled harness-anchor (CLAUDE.md override)
