---
name: oss-implement
description: "Implement an OSS contribution (bug fix, docs fix, typo fix, or test addition) using deep-comprehension workflow. For bugs: trace root cause, reproduce-first, comprehensive fix. For docs/typos: verify correctness. For tests: meaningful coverage. REJECT feature requests."
user-invocable: true
---

# OSS Implementation — Deep Comprehension Workflow

We contribute **deeply and comprehensively**. No surface-level patches. Understand the codebase before you touch it. Every PR must fully resolve the reported issue — no partial fixes.

**Contribution types (in order of merge probability):**
1. Documentation/typo fixes — near-guaranteed merge
2. Test additions — high merge rate
3. Bug fixes — standard merge rate (use reproduce-first workflow)

## Prerequisites
- Issue selected and CONFIRMED as actionable (bug, docs fix, typo, or test addition)
- Repo cloned+analyzed
- Branch: clawoss/{type}/<issue>-<desc> (type = fix, docs, test, or typo)

## Workflow (in order, no skipping)

### 0. CONFIRM ACTIONABLE + NOT SUPERSEDED (mandatory first step)
Before any coding, verify this is a valid contribution AND no one else is already on it:
- **Bug fix**: Does the issue describe broken/incorrect behavior? Error messages, stack traces?
- **Docs fix**: Is the documentation factually incorrect or outdated? Can you verify against code?
- **Typo fix**: Is there a clear typo in code, docs, comments, or error messages?
- **Test addition**: Is there an untested code path or a bug scenario lacking a test?
- **If this is a large feature request, enhancement, or refactor: ABANDON IMMEDIATELY.**
- **Supersession check**: Does the issue have linked open PRs from other contributors? Is it assigned to someone? If yes, ABANDON with reason `superseded` or `issue_assigned`.
- Write "ABANDONED: not actionable" or "ABANDONED: superseded" in the result file and stop.

### 1. DEEP COMPREHENSION (mandatory for bugs — scaled for other types)
For bug fixes: build a full mental model of the relevant codebase. Do NOT jump to writing code.
For docs/typos: verify the fix is correct by reading relevant source code.
For test additions: understand the code path being tested.

**1a. Understand the repo architecture:**
- Read the project README, directory structure, and key configuration files
- Read CONTRIBUTING.md if it exists — follow its style/process requirements
- Read AGENTS.md if it exists — it may contain agent-specific instructions that override defaults
- Identify the module/package structure and how components relate
- Understand the data flow and execution model (sync/async, event-driven, etc.)

**1b. Trace the relevant code path (bugs: mandatory; docs/typos/tests: read relevant modules):**
- **Bugs**: Start from the entry point, follow the code path to the error, read EVERY function in the call chain
- **Docs/typos**: Read the source code the documentation describes — verify what the actual behavior is
- **Tests**: Read the module being tested, understand its public API and edge cases

**1c. Identify what needs to change:**
- **Bugs**: Why does the bug exist? Logic error, edge case, race condition, missing validation?
  Could the same root cause affect other parts of the codebase? Check for similar patterns.
- **Docs/typos**: What is the correct text? Verify against actual code behavior.
- **Tests**: What code paths are untested? What edge cases matter?

**1d. Plan the complete fix:**
- What needs to change to fully resolve the issue?
- If the fix requires touching multiple files across the codebase, that's fine — do it right
- **If the issue is too complex to fully resolve: ABANDON rather than submit a partial fix**

### 2. REPRODUCE (mandatory for bugs — adapted for other types)
**For bug fixes:**
- Run existing tests for baseline
- Write a FAILING test that demonstrates the exact bug reported
- The test should cover the root cause, not just the surface symptom
- Record failure output as evidence — this proves the bug exists
- Cannot reproduce after 10 min? Abandon with note. Already fixed upstream? Remove from queue.

**For docs/typos:**
- Verify the current text is incorrect by checking actual code behavior
- No reproduction test needed — the fix is the documentation itself

**For test additions:**
- Run existing tests to establish baseline
- Write the new test targeting the identified code path
- The test should pass with current code (unless it's a test for a known bug)

### 3. IMPLEMENT (type-appropriate fix)
**For bug fixes:** Fix the ROOT CAUSE identified in Step 1, not just the surface symptom.
**For docs/typos:** Apply the minimal correct change. Cross-check against actual code behavior.
**For test additions:** Write tests following repo conventions. Ensure meaningful coverage.

For all types:
- If the fix correctly requires changes across multiple files, do it — do it right
- Match existing code style exactly
- **No "while I'm here" improvements** — do not refactor surrounding code
- **No feature additions** — do not add new functionality even if it seems related
- **No scope creep** — if you discover other issues, file them separately, do NOT fix them here
- **DO resolve the reported issue completely** — a partial fix is worse than no fix

### 4. VERIFY — FULL CI MATRIX (a broken CI is WORSE than no PR)
**4a. Read `.github/workflows/` FIRST** to understand the full CI matrix:
- Which OS? (ubuntu, macos, windows, multiple?)
- Which language versions? (Python 3.8-3.12, Node 16/18/20, etc.)
- Which build configs? (debug/release, with/without optional deps)
- What test suites beyond unit tests? (linting, type checking, formatting)

**4b. Run ALL test suites**, not just `make test` or `pytest`:
- Unit tests, linting, type checking, formatters (check mode), integration tests
- Any custom test scripts in Makefile, package.json, etc.

**4c. Cross-platform check** (C/C++, Rust, embedded, etc.):
- Does the fix touch platform-specific code? Check ALL target platforms.
- Does it use APIs that differ across OS/architectures?
- Example: micropython builds for stm32, esp32, rp2, unix — a fix that works on unix but breaks stm32 is a BAD PR.

**4d. Verify results:**
- Failing test MUST now pass. Full test suite — no regressions.
- Fix failures (max 2 tries) or abandon.
- Record passing output as evidence.
- Verify the fix addresses the root cause, not just the symptom.
- **Hypothesis check**: If your fix relies on a specific API/library behavior (e.g., "escaping chars will make function X treat them as literals"), verify that assumption with a minimal test. If you cannot verify the assumption, state this clearly in the PR description: "Note: I was unable to verify that [specific assumption] holds in all cases." Do NOT submit fixes based on unverified assumptions about third-party API behavior.
- **If tests don't pass, ABANDON. Do not submit untested PRs — a broken CI wastes maintainer time and gets us blocked.**

### 5. REVIEW (contribution-type-aware checks)
Self-check diff with these questions:
1. **Does this fully resolve the reported issue?** Partial fixes are not acceptable.
2. **For bugs: does the fix address the root cause?** If just the symptom, go back to Step 1.
3. **For docs/typos: is the corrected text factually accurate?** Verify against actual code behavior.
4. **Is every change directly related to the issue?** Revert unrelated changes.
5. **Did I accidentally add a feature or refactor code?** If yes, strip it out.
6. **Is the commit type correct?** `fix` for bugs, `docs` for documentation, `test` for tests.
7. Scoped to issue only? Matches style? No secrets/debug/AI-slop? 25-100 LOC target.
8. **HARD SIZE GATE: if total insertions + deletions > 200, ABANDON.** Large PRs = scope creep.
9. If 3+ checks fail, abandon.

### 6. SUBMIT
Commit with appropriate type: `fix(scope): desc`, `docs(scope): desc`, or `test(scope): desc`. Create PR:
- Title clearly indicates the contribution type
- **Check for PR template first**: `ls .github/PULL_REQUEST_TEMPLATE.md .github/PULL_REQUEST_TEMPLATE/ 2>/dev/null` — use it if present.
- PR body: write like a human developer, not an AI. Be terse (3-5 sentences). No "This PR addresses...", "Upon investigation...", or other AI tells.
  - **Bug fixes**: what broke + why (root cause) + what you changed + test evidence. Fixes #N.
  - **Docs/typo fixes**: what was wrong + what's correct now. Fixes #N.
  - **Test additions**: what's tested + why it matters. Fixes #N.
- Push to fork.

## Constraints
- Target 25-100 LOC. HARD MAX 200 — abort if exceeded. Match repo style. No new deps unless essential.
- No AI-slop, no single-use helpers, variable names match repo conventions.
- **Commit type must match contribution**: `fix` for bugs, `docs` for docs/typos, `test` for tests. NEVER use `feat:` — if you're committing a feature, ABANDON.
- **Every line changed must be necessary to resolve the reported issue.**
- **The contribution must COMPLETELY resolve the issue** — no partial work. If you can't fully complete it, ABANDON.
- Multi-file changes are fine if the scope demands it — do it right, not minimal for minimal's sake.

## Related Skills
systematic-debugging, test-driven-development, verification-before-completion
