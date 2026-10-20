---
name: phase-5-build
description: Phase 5 of the development cycle — the build loop. Implements one backlog task at a time with test-first development, then an independent code review (and security audit when relevant), then a clean commit and backlog update. Run it repeatedly until the milestone is done.
disable-model-invocation: true
argument-hint: "[task id, e.g. T-003 — omit to take the next one]"
---

# Phase 5 — Build one task

Task: $ARGUMENTS. If no task was given, take the first `[ ]` task in `docs/plan/BACKLOG.md` whose dependencies are done.

One run of this command = one task, finished to the definition of done. Then run it again for the next task.

## Steps

```
Task progress:
- [ ] 1. Understand the task
- [ ] 2. Branch and plan
- [ ] 3. Write failing tests from acceptance criteria
- [ ] 4. Implement until green
- [ ] 5. Clean up
- [ ] 6. Independent review
- [ ] 7. Commit and update the backlog
```

**1. Understand.**
- Read the task in BACKLOG.md.
- Read the acceptance criteria it covers in PRODUCT_SPEC.md.
- Read the related sections of ARCHITECTURE.md, DATA_MODEL.md, the API contract, and any relevant ADRs.
- If something is ambiguous, ask the user. Don't guess at product behavior.
- Mark the task `[~]`.

**2. Branch and plan.**
- Create the branch `feat/T-xxx-short-name`, or `fix/…` for a fix.
- If the task touches more than a few files, show the user a 3–6 line plan and wait for a go-ahead.

**3. Tests first** (`writing-tests`). Turn each acceptance criterion into at least one automated test. Run the tests and confirm they fail for the right reason.

**4. Implement.** Write the simplest code that makes the tests pass. Follow the conventions already in the codebase, and use the relevant skill:
- endpoints or contracts → `designing-apis`, and keep the API contract file in sync
- schema or migrations → `designing-data-models`
- UI → `building-frontends`
- something breaks along the way → `debugging-systematically`

**5. Clean up** (`refactoring-safely`).
- Remove duplication and unclear names while the tests are green.
- Run the full suite plus lint, format, and type checks. All must pass.

**6. Independent review.**
- Use the **code-reviewer** agent on the branch diff.
- If the task touches login, permissions, user input, file uploads, payments, or personal data, also use the **security-auditor** agent.
- Fix every Blocker and Major finding, then re-run the tests.
- List any Minor findings you didn't fix in the summary.

**7. Commit and record** (`writing-commits-and-prs`).
- Commit with a Conventional Commit message that references the task, for example `feat(auth): sign up with email (T-003)`.
- Mark the task `[x]` in BACKLOG.md.
- If a design decision changed, update the docs or add an ADR.
- Ask the user before pushing or opening a pull request.

## Report to the user

```markdown
**Done:** T-xxx <title>
**Acceptance criteria covered:** AC-…, AC-… (tests: <files>)
**Tests:** <command> → <N passed>
**Review:** <blockers/majors fixed; minors left>
**Next task:** T-yyy <title>  → run `/phase-5-build`
```

When all the tasks in a milestone are done, suggest `/phase-6-verify`.
