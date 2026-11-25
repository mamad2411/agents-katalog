---
name: git-iris
description: Use this skill when generating commit messages, pull request descriptions, release notes, changelogs, or code reviews in a repository where git-iris is available. Activates on requests like "commit this", "write a commit message", "draft a PR", "generate release notes", "write a changelog", or "review my changes" when git-iris is on PATH.
---

# Git-Iris

Delegate commit messages, PR descriptions, reviews, changelogs, and release notes to `git-iris`. Iris reads the diff herself, follows project style (gitmoji, presets, project-config), and produces structured output. Your job is to pass the _why_, then commit or post the result.

## When to use

If the repo has `git-iris` on PATH and the user asks for any of:

| Intent                           | Subcommand               |
| -------------------------------- | ------------------------ |
| Write a commit message           | `git-iris gen`           |
| Draft or update a PR description | `git-iris pr`            |
| Generate release notes           | `git-iris release-notes` |
| Generate a changelog             | `git-iris changelog`     |
| Code review of staged changes    | `git-iris review`        |

Check first: `command -v git-iris`. If it's missing, fall through to writing the message yourself.
If the installed `git-iris` is stale for the current branch, use the branch binary instead:
`cargo run --quiet -- -q gen -p -i "<why>"` or `target/debug/git-iris -q gen -p -i "<why>"`.
The `-q` flag still belongs to `git-iris`, after Cargo's `--`.

## The core pattern

```bash
git-iris -q gen -p -i "<one tight paragraph explaining why>"
```

- `-q` suppresses iris's startup banner. **Always pass `-q` when capturing stdout** or the version banner will pollute the captured message.
- `-p` prints to stdout without committing. Capture, inspect, then commit yourself with `git commit -F-`.
- `-i` is the _why_. Iris already reads the diff, so don't paste it. Pass intent: what user request triggered this, what constraint shaped the choice, what tone applies.
- Drop `-p` and add `-a` to auto-commit when the user is fine with iris's output as-is. `-q` is optional in auto-commit mode (the banner just goes to your terminal, not into the message).

## What goes in `-i`

Good context (one paragraph, roughly 3-5 sentences):

- The user request that triggered the change ("user asked to fix the doubled gitmoji bug")
- Non-obvious constraints ("had to keep the public API unchanged for downstream callers")
- Tone or scope hints ("internal refactor only, no behavior change")
- Related ticket or issue if relevant

Bad context (skip these):

- The diff itself, iris reads it
- File-by-file enumeration, iris reads them
- Restating commit conventions, iris uses project presets
- Boilerplate praise or filler

## Per-capability flags

### Commit messages (`gen`)

| Flag                   | When                                                                                                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p` / `--print`       | Print to stdout, you commit yourself                                                                                                                                                  |
| `-a` / `--auto-commit` | Iris commits directly with the generated message                                                                                                                                      |
| `--amend`              | Amend the previous commit. Requires `-p` or `-a`; standalone `--amend` is a no-op with a warning                                                                                      |
| `--no-verify`          | Skip iris's auto-commit hooks. **Only affects iris's own commit (`-a` mode).** When you commit yourself with `git commit -F-`, pass `--no-verify` to git too if the user asked for it |
| `--critic` / `--no-critic` | Toggle the critic verification pass after generation. Commit messages default off; use `--critic` to opt in                                                                       |

### PR descriptions (`pr`)

| Flag                          | When                                                                         |
| ----------------------------- | ---------------------------------------------------------------------------- |
| `--update`                    | Push the description to the GitHub PR (requires `gh auth`)                   |
| `--pr <N>`                    | Target a specific PR number for `--update`. Has no effect without `--update` |
| `--from <ref>` / `--to <ref>` | Custom commit range                                                          |
| `-c` / `--copy`               | Copy raw markdown to clipboard                                               |
| `--critic` / `--no-critic`    | Toggle the critic verification pass after generation. Default on             |

### Changelog and release notes

Both subcommands **require `--from`**. `--to` defaults to `HEAD` if omitted.

| Flag                       | When                                                                    |
| -------------------------- | ----------------------------------------------------------------------- |
| `--from <ref>`             | **Required.** Starting reference (commit/tag/branch)                    |
| `--to <ref>`               | Ending reference. Defaults to `HEAD`                                    |
| `--version-name <X>`       | Explicit version label (works for both `changelog` and `release-notes`) |
| `--file <path>`            | Output file path (defaults to `CHANGELOG.md` / `RELEASE_NOTES.md`)      |
| `--critic` / `--no-critic` | Toggle the critic verification pass after generation. Default on        |

### Code review (`review`)

By default, reviews staged changes. Use the flags below for other scopes.

| Flag                          | When                                                                                      |
| ----------------------------- | ----------------------------------------------------------------------------------------- |
| `-p` / `--print`              | Print review to stdout instead of console-formatted display                               |
| `--raw`                       | Raw markdown (good for piping or saving to file)                                          |
| `--include-unstaged`          | Include unstaged working-tree changes alongside staged. Incompatible with `--from`/`--to` |
| `--commit <SHA>`              | Review a single commit. Mutually exclusive with `--from`/`--to`                           |
| `--from <ref>` / `--to <ref>` | Review a commit range. `--from` requires `--to`                                           |
| `--github-review`             | Post the review to the current GitHub PR (requires `gh auth`)                             |
| `--github-inline-comments`    | Add inline comments at flagged lines when posting                                         |
| `--github-review-event <E>`   | GitHub review action: `comment` (default), `request-changes`, `approve`                   |
| `--pr <N>`                    | Target a specific PR for `--github-review`                                                |
| `--critic` / `--no-critic`    | Toggle the critic verification pass after generation. Default on                          |

## Attributions and trailers

Iris doesn't manage `Co-Authored-By:` trailers. After capturing iris's output with `-p`, append trailers yourself when committing:

```bash
msg=$(git-iris -q gen -p -i "<why>")
git commit -F- <<EOF
$msg

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
```

For PR and release-notes markdown, attribution is optional and lives in the body if at all. Don't post-process iris's markdown unless the user asks for it.

## Print vs auto-commit

| Situation                               | Use                                      |
| --------------------------------------- | ---------------------------------------- |
| User wants to review before commit      | `-p`, show stdout, confirm, then commit  |
| User said "just commit it" or "ship it" | `-a`                                     |
| User is mid-flow and trusts the output  | `-p` and commit silently with trailers   |
| You need to add Co-Authored-By trailers | `-p` (auto-commit can't append trailers) |

## Things to know

- **Iris uses the repo's project-config.** Don't pass `--gitmoji` or `--preset` flags unless the user explicitly asks to override.
- **Iris re-runs cleanly.** If the first output isn't right, refine `-i` and call again rather than editing iris's output by hand.
- **Studio TUI exists.** If the user wants to iterate interactively, suggest `git-iris studio` instead of repeated CLI calls.
- **`--debug` is colorful.** When something looks wrong, `git-iris gen --debug -i "..."` shows tool calls and reasoning in color. Don't combine `--debug` with `-q -p` capture; debug output goes to stderr but the visual noise distracts from triage.

## Anti-patterns

- Don't write the commit message yourself when `git-iris` is on PATH and the user wanted iris to do it.
- Don't paste the diff into `-i`. Iris reads the diff.
- Don't chain `-i` with shell-escaped multi-paragraph prose. One paragraph, plain quotes.
- Don't override project style flags unless the user asked.
- Don't skip the user's review step on a non-trivial commit just because `-a` is faster.
