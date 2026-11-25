---
name: todo-capture
description: "Frictionless capture of a TODO into the current project's TODO.md, plus an optional triage pass that proposes what each open item should become. Use when the user wants to park an idea, follow-up, or future task mid-session without pivoting away from the work in progress, or asks to review and triage their TODO list."
user-invocable: false
---

# Todo capture

> Park a thought in `TODO.md` and return to whatever was happening. Capture only: do not execute, plan, or expand the todo.

The skill is meant to be invisible. The user drops a todo and the session continues the prior task in the same response.

Two modes:

| Invocation | Mode |
|---|---|
| `/todo <text>` | Capture (default) |
| `/todo triage` | Triage the open items (proposal only) |
| `/todo` with no text | Ask in one line: "What's the todo?" and wait |

## Capture

### Step 1: take the text verbatim

Everything after `/todo` is the todo, verbatim. Strip surrounding whitespace only. Do not rewrite, expand, or interpret it.

### Step 2: locate TODO.md

Find the project root: `git rev-parse --show-toplevel 2>/dev/null`. If that fails, walk up from the working directory looking for the first folder that contains `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or `CLAUDE.md` (stop after six levels). If nothing matches, use the working directory.

Target: `<project_root>/TODO.md`.

If the working directory is your home folder or the Claude Code config folder, write to `~/TODO.md` instead of creating project files there.

### Step 3: append

Get today's date in the machine's local time zone: `date +%Y-%m-%d`.

- **No TODO.md yet**: create it:

  ```markdown
  # TODO

  ## YYYY-MM-DD

  - [ ] <todo text>
  ```

- **TODO.md has a `## YYYY-MM-DD` heading for today**: append `- [ ] <todo text>` as the last bullet of that section (insert before the next `## ` heading, or at the end of the file).
- **TODO.md has no heading for today**: insert a new `## YYYY-MM-DD` section directly under the `# TODO` title, above older dates, with the new bullet. Newest dates stay on top.
- **No `# TODO` title**: prepend it.

### Step 4: confirm in one line, then resume

Print exactly one line:

```
TODO captured: <path>:L<line>
```

Then continue whatever the user was doing before `/todo`. If there was no active task, stop after the confirmation line.

Do not:

- suggest next steps or ask whether to act on the todo now
- expand the todo into subtasks
- move it into the session task list (this is a long-lived, file-based capture, not a session task)

### Edge cases

- **Multi-line text**: keep it as one bullet; indent continuation lines by four spaces.
- **Duplicate-looking todo on the same day**: append anyway. The user may be re-flagging it on purpose.
- **TODO.md is a directory, or a link to one**: print `TODO.md is not a regular file at <path>, skipped.` and resume.
- **No write permission**: print `TODO.md is not writable at <path>, skipped.` and resume.

### File shape over time

```markdown
# TODO

## 2026-05-03

- [ ] refactor the auth flow once the deploy is done
- [ ] check why webhook retries spike after midnight

## 2026-05-02

- [ ] move the nightly job to the build server
- [x] migrate the worker to systemd
```

The user owns completion (`- [x]`), pruning, and grooming. Capture mode only appends.

## Triage (`/todo triage`)

A review pass for when the list has grown. It proposes; it does not change anything until the user agrees.

1. Read `TODO.md`. Collect the open items (`- [ ]`) with their dates.
2. For each item, propose one destination:

   | Destination | When |
   |---|---|
   | **keep** | Still a small, personal follow-up that fits the list |
   | **ticket** | Needs tracking, an owner, or discussion (an issue in the project's tracker) |
   | **memory** | Not a task at all but a fact or preference worth keeping (hand it to the absorb plugin) |
   | **done** | The repo already shows it finished; cite the evidence (a commit, a file) |
   | **drop** | Obsolete; say why |

3. Show the proposal as a table: item, date, destination, one-line reason.
4. Apply only what the user approves: tick `done` items, remove `drop` items, and for `ticket` items print a ready-to-paste title and body (or create the issue with `gh issue create` if the user asks for it). Never delete an item the user did not approve.
