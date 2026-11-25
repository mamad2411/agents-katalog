---
name: loopmath-import-runs
description: "Bring agent runs the user already has as OCP files (*.ocp.json) into loopmath in one pass: validate all, import all, fit once, show the results page. Use when the user points at OCP files or a folder of finished runs, or at the output of an orchestrator or experiment harness that writes OCP, and wants loopmath to learn from them."
allowed-tools: Bash(loopmath:*), Bash(open:*), Bash(xdg-open:*)
---

# Bring existing runs into loopmath

The user has finished runs written as OCP v0.3 (or v0.1, v0.2) documents. Validate them all, import them all without refitting after each, fit once, and show the results page. Ask nothing unless the location of the files is unknown.

Use exactly the commands below. Flags and fields are in `reference.md` next to this file. Never run `--help`.

## 1. Find the files

Use the folder or files the user named. `DIR` below is that folder. If the user named nothing, ask once where the files are; that is the only question.

## 2. Validate all

```sh
loopmath ocp validate DIR/*.ocp.json --json
```

For files in subfolders, list them with `find DIR -name '*.ocp.json'` and pass them all.

Read `passed`, `failed`, `files[]` (`path`, `ok`, `findings[]` (`code`, `message`)). For each file with `ok` false, keep its `path` and first finding. Do not fix files by hand. When some fail, import the ones that passed and report the failures at the end. When all fail, stop and show the first three findings.

## 3. Import all, without a refit per file

```sh
loopmath run import DIR --finish --no-fit --json --brief
```

With only some files valid, pass those files instead of `DIR`. Read `imported`, `failed`, `failures[]` (`file`, `error`), `more_failures`, `overlap_note`, `next`. Report each failure with its file and error; when `more_failures` is above 0, say how many more failed. When `overlap_note` is not null, keep it for the summary, where it is said once, word for word (for example "44 of your runs are also in the shipped rq1 prior (same runs): fits use your copies"). `next` is the step after the import: here it is the fit below.

## 4. Fit once

```sh
loopmath fit --json
```

Read `fit.id`, `fit.n_runs.user`, `fit.n_runs.prior`, `runs_by_source`, `seconds`. The fit's `shipped_overlap` is the same overlap as `overlap_note`: do not name it a second time.

## 5. Show the results page

```sh
loopmath posterior --html
```

It prints the page path. Open it (`open PATH` on macOS, `xdg-open PATH` on Linux); if that fails, give the path.

## 6. Summary

End with at most 6 lines, then stop (the overlap line only when `overlap_note` is not null):

> Validated 44 files: 44 passed. Imported 44 runs (0 failed).
> 44 of your runs are also in the shipped rq1 prior (same runs): fits use your copies.
> Fit fit_20260924170512: 44 of your runs plus 1,469 shipped runs, 3.3 s.
> Results page: /Users/me/.loopmath/views/posterior-20260924-170515.html
> Next: plan a task with these runs ("plan this task: ...").

## Never

- Do not import with a refit per file (always `--no-fit`, then one `fit`).
- Do not edit the OCP files or the store by hand.
