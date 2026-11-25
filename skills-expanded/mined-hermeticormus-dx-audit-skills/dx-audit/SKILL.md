---
name: dx-audit
description: Audit and improve developer experience in a codebase by inspecting README, quickstart, scripts, contributing guide, env docs, error messages, and tooling, scoring onboarding friction, and reporting findings or implementing fixes. Use when a new contributor hits friction, when setup is undocumented, or when the README has not been run on a clean checkout since the stack changed.
license: MIT
---

# DX audit

A protocol for auditing and improving developer experience in a codebase. Developer experience is everything a contributor touches before their first useful line of code. High onboarding friction is silent: no one files a bug for it, every new contributor just pays the cost.

## Usage

```text
/dx-audit                 # full audit of the current project (report-only)
/dx-audit [path]          # audit a specific directory
/dx-audit --report-only   # inspect and report, change nothing (default)
/dx-audit --implement     # apply fixes with approval, verify each
```

## What to inspect

Walk the codebase as a new contributor would. For each dimension, record what exists, what is missing, and whether what exists is accurate.

1. README: first-paragraph clarity, a copy-pasteable quickstart, current commands, links to deeper docs.
2. Quickstart and setup: the path from clone to running app, in dependency order, with prerequisites listed. Run it on a clean checkout and count what fails.
3. Scripts: install / dev / build / test / lint / format entries in a task runner, with names that match the README and contributing guide.
4. Contributing guide: branch naming, commit format, PR expectations, how to run tests, checked against the actual workflow.
5. Environment docs: an `.env.example` listing every required variable, each annotated with what it is and where to get it.
6. Error messages: setup scripts fail loudly with actionable messages, so missing deps, wrong runtime version, or absent env vars produce a sentence, not a stack trace.
7. Tooling: linter, formatter, type-checker configured and wired to a pre-commit hook or CI so they run without being remembered.

## How to score friction

Assign each dimension a level. The goal is to find where the silent cost concentrates.

- None: present, accurate, discoverable. A new contributor succeeds without asking.
- Low: present but incomplete or stale. Costs a minute of guessing.
- Medium: present but wrong, or absent where it matters. Costs a question to a maintainer.
- High: absent or actively misleading. Blocks a new contributor until someone intervenes.

Anchor the score with two timings: time to first run (clone to running app or passing test) and time to first contribution (clone to a tested, formatted, ready-to-open PR).

## Report-only vs implement modes

State the active mode before producing output.

Report-only (default): inspect, score, and produce a prioritized findings list grouped by effort (quick wins, medium effort, larger work). Each finding names the dimension, the friction level, and the specific fix. Change nothing.

Implement: apply fixes with approval, highest-friction and lowest-effort first. Make surgical changes: add the missing section, create the `.env.example`, add the script, fix the message. Verify each fix on a clean checkout before claiming it done. Stop after each group and report what changed and what was verified.

Default to report-only when the mode is unstated, because applying changes a contributor never reviewed is itself a DX failure.

## Verify before claiming a fix

Run the quickstart on a clean checkout, not on your already-configured machine. Run each documented script. Trigger the missing-env-var and wrong-version paths and read the message a contributor would see. A README that has not been run on a clean checkout is a guess, not a fix.

---

See full content at https://github.com/HermeticOrmus/dx-audit-skills.
