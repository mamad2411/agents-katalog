---
name: git-change-intelligence
description: >-
  Return structured Git working-tree status, recent commit metadata, and changed paths using a read-only JavaScript Git implementation. Use when an agent needs a quick repository-change inventory or history sample for a code review, handoff, debugging session, or pre-edit check. It can distinguish staged, unstaged, deleted, and untracked paths where supported. This tool does not return patch hunks, stage files, or create commits.
---

# Git change intelligence

Use for a compact inventory before reviewing a change or when a caller needs machine-readable status/history. It reads the repository and emits one JSON object to stdout; errors go to stderr as JSON with exit code 1.

```sh
node scripts/index.js status .
node scripts/index.js diff .
node scripts/index.js commits . --limit 8
```

Run it against the repository root. It uses `isomorphic-git` and does not call the system `git` executable. Repositories that depend on Git features not supported by that library may produce incomplete results or an error; use the project's Git tooling for authoritative patch review.

## Commands

`status <repo>` returns the status matrix for tracked and untracked files. Each entry includes the path, numeric HEAD/worktree/stage status values from isomorphic-git, and a simplified state (`untracked`, `deleted`, `staged`, `modified`, or `clean`). Paths are relative to the repository.

`diff <repo>` filters that same status inventory to paths whose simplified state is not `clean`. It is a changed-path summary, not a textual diff: it has no patch hunks, rename detection, or whitespace analysis. Inspect actual diffs with Git when reviewing line-level changes.

`commits <repo> [--limit N]` returns newest-first commit objects with object ID, message, author, and committer metadata. The limit defaults to 10, must be a positive integer, and is capped at 100. It does not include file-level commit stats or guarantee the complete history.

Example response:

```json
{"data":{"repo":"/workspace/project","files":[{"file":"src/app.js","head":1,"worktree":2,"stage":1,"state":"modified"}]}}
```

## Review workflow

1. Run `status` to see whether the tree is clean and note staged versus unstaged work before editing.
2. Use `diff` for the changed-path list, then inspect the relevant patch with the repository's normal Git interface.
3. Use `commits` as orientation only; check commit details directly when the exact patch or parent relationship matters.
4. Preserve all existing user changes. This utility is read-only; do not interpret a clean report as proof that generated, ignored, or untracked material outside its view does not exist.

## Choose the command

- Use `status` before editing or when you need to understand staged versus unstaged work.
- Use `diff` when another tool already provides the actual patch and you only need the changed-path inventory.
- Use `commits` to orient yourself to recent history; use the repository's normal Git tooling to inspect exact changes, renames, authorship, or ancestry.

For a pull request or release review, compare the paths reported here with the requested scope, then inspect the real patch. Do not infer that a path is safe or correct from its state label alone. If the result conflicts with `git` output, trust the repository's Git implementation and treat this library's result as incomplete for that repository.

## Detailed change-review procedure

### Establish the repository and baseline

Pass the repository root explicitly. Before making edits, capture the status and note staged, unstaged, untracked, and deleted paths. A “clean” simplified state does not mean the file is safe to overwrite: inspect the status matrix and use the project's normal Git tooling if a distinction matters. Preserve the current state as the user's work, not as disposable noise.

### Use history as context, not proof

Use `commits` to learn recent messages and authorship context when it helps orient a review. A commit message is a claim about intent, not a description of the exact patch. The returned list is limited and newest-first; it does not include diffs, rename detection, file statistics, branch comparison, or complete history guarantees. Open the relevant commit with normal Git tooling before attributing a behavior change to it.

### Turn path inventory into a review

1. Run `status` and record the working-tree context.
2. Run `diff` to get the changed paths (or use the same status result if no separate filter is needed).
3. Compare those paths with the user's requested scope. Look for unexpected files such as generated output, local config, build artifacts, or unrelated edits.
4. Inspect patch hunks using the repository's authoritative Git interface.
5. Review relevant callers, tests, and configuration before judging impact.

For a handoff, report only the path inventory and status distinctions that the recipient needs. For a code review, never use this tool's path list as a substitute for reading the patch. For a cleanup request, do not remove or reset files just because they are untracked or unexpected.

## Interpreting status entries

`head`, `worktree`, and `stage` are numeric status codes from isomorphic-git; the simplified `state` is intended for quick scanning. If both staged and working-tree changes exist, inspect each layer with full Git tooling before describing what will enter a commit. A deleted path, untracked path, or partially staged file can have different implications even if a consumer only uses the simplified label.

When reporting, include the repository path, command used, number and names of relevant changed paths, and any limitation caused by unsupported Git features. Do not include unrelated local filenames or sensitive paths unless they matter to the request.
