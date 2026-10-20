---
name: engineering-checklist
description: >
  Mandatory principles and checklist for ALL engineers (frontend & backend) when writing or modifying code.
  MUST be loaded when: implementing tasks, fixing bugs, refactoring code, or reviewing code.
  Covers rename completeness, import integrity, dead code cleanup, test hygiene, lock-file
  regeneration after a dependency manifest edit, and where a validation check belongs.
user-invocable: false
---

# Engineering Checklist

**Derived from real-world production bugs. Applies to ALL engineers — frontend, backend, Electron, and reviewers.**

## Principles — follow these while writing code

1. **Match existing patterns over "best practice"** — per `agent-guidelines` → *Match Existing Code Before Writing*; deviations are stated up front, never silently introduced.
2. **Run the linter** — if the project has a linter configured, run it after every change and fix errors before committing; no lint rules disabled without justification
3. **Every rename must be total** — grep the entire codebase for the old name; string literals, dynamic refs, and config keys are easy to miss
4. **Delete, don't comment out** — removed features = delete ALL related code (components, routes, tests, styles, configs)
5. **Imports are a contract** — after deleting/moving an export, update all importers yourself
6. **Tests must stay clean** — delete old test files when replacements exist; fix the type instead of `as any`; remove a `@ts-expect-error` / `@ts-ignore` once the issue under it is fixed
7. **One bug means many bugs** — grep the full codebase for the same pattern; fix all occurrences, not just the one you found
8. **Bulk changes require bulk verification** — glob/grep for remaining instances; "it compiled" is not proof of correctness
9. **Guard at the trust boundary, nowhere else** — a check belongs where the value *enters*, and only when its source can actually send something wrong. Three sources, three answers:
   - **Written into the code** (a const, a timeout on a model, a factory default) → **no check at all.** The only "input" is the next engineer editing that line, and the type plus the diff already cover it; a branch that can never be true just makes the next reader ask whether it can. Observed: a hardcoded timeout gained a negative-value check on the consuming side, three lines below the literal it guards, where the framework would have thrown anyway.
   - **Config / env** → validate **once at startup and fail fast**, never on each use, and validate what actually breaks: a unit mismatch (`30` read as ms when seconds were meant) passes every sign and range check ever written.
   - **A request from outside the trust boundary** → validate, using the project's existing contract mechanism.

   **A developer-facing API is not a trust boundary because it has a form in front of it.** A Swagger-driven internal/admin endpoint does not need field-shape validation on its inputs — a max length, a format regex, a numeric range — beyond what the type already enforces; authn/authz is what keeps the wrong caller out, and whoever can reach that form can read the code. Full field validation is for an actual end-user-facing form (marketing, customer input). **A library's or plugin's public API is the opposite case, developer-facing though it is** — a JS caller or an `as`-casted TS one sends whatever it likes and the type never runs, so that entry point IS a boundary and keeps its runtime guards; `frontend-checklist` principle 11 owns the shape they take. **This governs the check you are about to write, never one already in the code** — an existing guard stays, since it may be load-bearing for a reason no longer visible (`agents/review-engineer.md` treats removing one as a finding in its own right), and where the surrounding code guards these values by convention, **principle 1 outranks this one**: match the convention and note the divergence in your report instead of breaking the pattern. **This binds reviewing as much as writing, wherever this file is loaded: a missing guard on a non-boundary value is not a finding** — raising it spends a fix round adding dead code. Two things it does not touch: a genuine boundary, injection, or resource-exhaustion finding, and a bound that exists because the **sink** is bounded — an open-ended field (a remark, a note, a description) written to a fixed-width column is a correctness concern at any exposure, with no attacker required (`agents/security-engineer.md` routes exactly that case to review-engineer).

10. **A dependency manifest edit is only half the change — its lock file is the other half.** Adding, removing, or version-bumping a dependency in `package.json` / `*.csproj` / `pyproject.toml` / `go.mod` leaves the lock file (`package-lock.json`, `pnpm-lock.yaml`, `packages.lock.json`, `uv.lock`, `go.sum`) still describing the old tree. Run the project's own install command so the lock regenerates, and commit it in the **same** commit as the manifest — a manifest-only commit fails CI's frozen-lockfile install and hands the next person an unrelated lock diff on their first build. Where the install cannot run (no registry access, no toolchain), say so in your report instead of committing the manifest alone.
