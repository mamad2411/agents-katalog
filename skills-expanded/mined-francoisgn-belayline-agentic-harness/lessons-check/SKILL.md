---
name: lessons-check
description: Self-review of the current diff against the lessons table of the Belayline harness (and the project's) before a PR or a review fix; returns a verdict per applicable lesson. Use before pushing or before moving a PR to review.
argument-hint: "[base, default: integration branch]"
---

# Self-review against the lessons

1. Diff: `git diff origin/<base>...HEAD`, where `<base>` is "$ARGUMENTS" if given, otherwise the integration branch
   (`.harness/config.json` → `integration_branch`).
2. Tables: `.harness/docs/LESSONS.md` (otherwise `${CLAUDE_PLUGIN_ROOT}/docs/LESSONS.md`) **and** the project's own
   lessons if it has any (e.g. `docs/agents/LESSONS.md`). Keep the relevant scopes: `general`, `docs`, `ci` always;
   `swift`, `ios`, `linux-cloud` depending on the project and the environment. Keep only the rows whose **Class**
   column is `judgment` or `mechanical, check to write`: a row `mechanical, enforced by <check>` is verified by that
   check (unless the project has switched it off: then read it), a `one-off` row is not re-read, nor is the
   **Archive** section. A project table without a Class column is read whole.
3. For **each** lesson that applies to the diff, one line: `L..: ✅ followed | ⚠️ to verify | ❌ broken: where
   (file:line) and why`. Do not list unrelated lessons.
4. Concrete checks, not impressions: run the announced tests, show that a new test fails without the change (L01),
   find the caller of a function "called at launch" (L82), check save compatibility if a persisted type changes
   (L80).
5. Fix the ❌ before pushing; unresolved ⚠️ go into "Watch points / not tested" in the PR.
6. **Candidates** to leave the table (exit rule in the header of `LESSONS.md`), listed after the verdicts, never
   moved by you: rows `mechanical, enforced by` or `one-off`; a row this review found to duplicate, or be a special
   case of, another (`Lnn → merge into Lmm`); a `judgment` row cited by no review or correction for six months
   (`git log --since=6.months --grep='Lnn'` empty, nor in the latest review rounds). One line each, with the reason;
   the operator decides.
