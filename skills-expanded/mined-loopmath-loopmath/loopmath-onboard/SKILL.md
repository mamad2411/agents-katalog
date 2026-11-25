---
name: loopmath-onboard
description: "Set the user up with loopmath from their own Claude Code and Codex history, in one pass: one question (which model labels their sessions, with its cost), then onboarding, the first fit and the results page. Use when the user asks to onboard, set up, start or try loopmath, or when loopmath has no runs yet."
allowed-tools: Bash(loopmath:*), Bash(open:*), Bash(xdg-open:*)
---

# Onboard the user with loopmath

Onboarding reads the user's past Claude Code and Codex sessions (read only), groups them into tasks, has a model the user chooses name each task's type, records one run per task, finds the usual workflow per task type and repo, and fits. You ask one question, the labeller with its cost, and do the rest without stopping.

Use exactly the commands below. Flags and fields are in `reference.md` next to this file. Never run `--help`.

## 1. Look first (no question yet)

Tell the user in one line: "Reading your Claude Code and Codex history, read only. A long history takes a few minutes." Then:

```sh
loopmath onboard --dry-run --json
```

Read `prior.line`, `groups.total`, `groups.to_label`, `window.from`, `window.to`, `sessions`, `cost_in_logs.usd`, `labeler.chosen`, `labeler.spec`, `labeler.expected.usd`, `labeler.options[]` (`spec`, `title`, `expected.usd`).

Show the user `prior.line` once, word for word. It says what the answers start from before any of their runs, the prior that ships inside loopmath: its version, its runs per source, the published benchmarks it holds and the date it was built. Do not repeat it later, and do not write the numbers yourself: they change with each release. `loopmath prior show` lists the same prior source by source.

If `groups.to_label` is 0, there is nothing to label. Do not ask anything. Say what was found (`groups.total` groups, none with a prompt to label, or no sessions in the window), run `loopmath fit --json`, and go to step 4. Suggest `loopmath-import-runs` if the user has OCP files.

## 2. Ask one question

Ask exactly one question. It names what was found, the labeller options with their cost, and says that the answer approves the cost. Build the options from `labeler.options`, in its order, and always add "your own command". Example:

> loopmath found 1,204 sessions (Claude Code 900, Codex 304) from 2026-06-26 to 2026-09-24: 312 tasks, $1,480.20 of agent spend in your logs.
> To learn your task types, a model labels a short summary of each task. Which labeller?
> 1. `claude:claude-haiku-4-5`, through your claude CLI: about $0.42
> 2. `codex:gpt-6-luna`, through your codex CLI: about $0.31
> 3. `none`: a keyword guess, free, less accurate
> 4. your own command, for example a local model: tell me the command
>
> Your answer also approves that cost.

If `labeler.chosen` is true (the user chose one before), ask only: "Label 312 tasks with SPEC for about $X?" with `labeler.spec` and `labeler.expected.usd`.

Never pick the labeller yourself, even when one is much cheaper. If the user names another model, use `claude:MODEL` or `codex:MODEL`; for their own command, `command:CMD`.

## 3. Onboard

Tell the user in one line that labelling and recording has started. Then:

```sh
loopmath onboard --labeler SPEC --yes --json
```

Read `runs.written`, `classified.by_type`, `unclassified.total`, `unclassified.by_reason`, `usual[]` (`type`, `repo`, `label`, `runs`, `total`), `fit.id`, `fit.error`, `labeler.actual.usd`, `labeler.failed_chunks`.

- If `fit.error` is set, run `loopmath fit --json` once.
- If the command exits 1 saying a CLI is not on PATH, tell the user which one and ask for another labeller (the only case for a second question).

## 4. Show the results page

```sh
loopmath posterior --html
```

It prints the page path. Open it (`open PATH` on macOS, `xdg-open PATH` on Linux); if that fails, give the path.

## 5. Summary

End with at most 8 lines, then stop:

> Onboarded: 287 runs recorded (bug_fix 120, feature 90, refactor 40, docs 37). 25 tasks not classified (still running 3, no prompt 22).
> Usual workflow per task type:
> - bug_fix, acme/api: implement_review: opus-5-5/high, gpt-6-astra/xhigh (40 of 52 runs)
> - feature, acme/web: solo: opus-5-5/high (31 of 44 runs)
> Labelling cost $0.39. First fit fit_20260924163012.
> Results page: /Users/me/.loopmath/views/posterior-20260924-163015.html
> Next: tell me a task ("plan this task: ...") and I will pick its workflow with loopmath.

Take the usual lines from `usual[]`: at most 4, most runs first, and skip rows whose `repo` is `*` when the same type has a repo row.

## Never

- Do not run `onboard` without `--dry-run` before the user answered.
- Do not edit files under `~/.loopmath` or `$LOOPMATH_HOME` by hand.
- Do not read or quote the user's session contents; loopmath does the reading.
