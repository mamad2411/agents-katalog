---
name: codecrafters-stage
description: >-
  Work through a single stage of the CodeCrafters Build your own Shell challenge
  in Go. Use when starting a new stage, when the user invokes /next-stage, or
  when continuing codecrafters-shell-go work after a stage is marked complete.
---

# CodeCrafters Stage Workflow

Follow these steps in order for each challenge stage.

## 1. Understand the task

Run `codecrafters task` and read the full stage instructions.

- Identify the expected behavior, inputs, outputs, and edge cases.
- Skim existing code under `app/` to see what is already implemented.
- Classify complexity:
  - **Trivial**: a small, localized change (e.g. print a prompt, handle one builtin).
  - **Non-trivial**: new packages/modules, parsing logic, state management, or unclear requirements.

Proceed directly to step 3 for trivial tasks. For non-trivial tasks, go to step 2.

## 2. Plan changes (optional)

Required only for **non-trivial** tasks or when requirements are ambiguous.

1. Switch to **Plan mode** (`SwitchMode` → `plan`).
2. Draft a concise plan: files to add or change, key functions/types, and test approach.
3. List any clarifying questions for the user.
4. Present the plan and questions, then **stop and wait for approval**.

Do **not** implement, test, or commit until the user approves the plan or answers your questions.

## 3. Implement the code

Write clean, readable, maintainable Go that satisfies the stage requirements.

- Keep `app/main.go` thin: wire up the REPL and delegate to other packages/files.
- Put reusable logic in separate files or packages under `app/` (e.g. `app/shell/`, `app/parser/`).
- Follow project rules: [Effective Go](https://go.dev/doc/effective_go) and existing code style.
- Run `gofmt` on changed files before testing.
- Prefer extending existing abstractions over duplicating logic.

## 4. Write local tests

Add table-driven tests in `*_test.go` files alongside the code they exercise.

- Cover the behavior introduced or changed in this stage, including edge cases from the task description.
- Follow the project [table-driven tests](https://go.dev/wiki/TableDrivenTests) rule.
- Test pure logic directly; use `os/exec` or similar only when integration-style coverage is needed.

## 5. Run local tests

```bash
go test ./...
```

- If tests fail, fix the code or tests and re-run until all pass.
- Do not proceed to step 6 while local tests are failing.

## 6. Run codecrafters test

```bash
codecrafters test
```

- If tests fail, read the failure output, fix issues, re-run local tests (step 5), then re-run `codecrafters test`.
- Do not proceed to step 7 while codecrafters tests are failing.

## 7. Hand off for review

When both test suites pass, stop coding and report:

- Brief summary of what was implemented.
- Files changed.
- Test results (`go test ./...` and `codecrafters test`).
- A suggested **Conventional Commits** message (see project commit rule). Example:

  ```
  feat(shell): print prompt on startup
  ```

Do **not** commit or push yet. Wait for human review (step 8).

## 8. Human review

The user reviews the code and either:

- Requests changes → address feedback, then repeat steps 4–7 as needed.
- Approves and asks to commit → proceed to step 9.

Only create a git commit when the user explicitly requests it.

## 9. Commit and push

After explicit user approval to commit:

1. Stage only the relevant files (exclude unrelated changes).
2. Commit with the agreed message from step 7 (updated if the user requested changes).
3. Push to `master`:

```bash
git add <files>
git commit -m "<conventional-commit-message>"
git push origin master
```

CodeCrafters runs tests automatically on push. Do not use `codecrafters submit`.

## 10. Mark stage as completed

The user marks the stage complete in the CodeCrafters browser UI.

When the user invokes **/next-stage** (or `/codecrafters-stage`), start again at **step 1** for the next stage.

## Project layout reference

| Path | Purpose |
|------|---------|
| `app/main.go` | Entry point; keep minimal |
| `app/**/*.go` | Shell implementation |
| `app/**/*_test.go` | Local tests |
| `codecrafters.yml` | Buildpack and debug settings |

## Commands quick reference

| Action | Command |
|--------|---------|
| View current stage | `codecrafters task` |
| Local tests | `go test ./...` |
| Challenge tests | `codecrafters test` |
| Commit and push stage | `git commit` + `git push origin master` |
