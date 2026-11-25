---
name: figlens-code-review
description: >-
  Review a figlens change before it becomes a pull request, or review an open
  pull request. Use whenever the user asks to review a diff, branch, commit
  range or PR, check a change before opening a PR, or find what a change
  missed. It checks correctness, the repository's documented rules, the
  originating issue or spec, every consumer of a changed concept, and cleanup,
  then verifies each finding against the code before reporting it. Read-only
  unless the user asks for fixes.
argument-hint: "[base ref | PR number | path] [fix]"
metadata:
  targets: [claude, universal, pi]
---

Review one change in five independent passes, verify every finding, and report them by pass. $ARGUMENTS names the target (a base ref, a PR number, or a path) and may end with `fix`.

Load `python3 scripts/ai-context.py review` for the pre-PR and AI-review follow-up procedure. After an authorized PR fix, push verified changes, request `@codex review` and inspect the completed review of that head; the topic owns this workflow.

**Scope**: read-only by default. With `fix`, apply only verified findings that do not change intended behavior, then run the checks in `AGENTS.md` Verification. Commit, push or comment on GitHub only within a PR workflow the user authorized.

## Step 1: Pin the diff

| $ARGUMENTS | Diff |
|---|---|
| empty | `git diff origin/main...HEAD` plus `git diff HEAD` (uncommitted work counts) |
| a ref | `git diff <ref>...HEAD` plus `git diff HEAD` |
| a PR number | check the PR out in a new scratch worktree (`git worktree add`, then `gh pr checkout <n>` inside it) and review there with `git diff origin/<base>...HEAD`, so Step 4 reads the PR's code, not the current branch |
| a path | that file or directory, reviewed whole |

Run `git fetch origin` first so the base is current. Stop here if the ref does not resolve or the diff is empty. In a shared checkout, list files changed by another session (`git status`) and leave them out of scope.

## Step 2: Gather context once

1. **Spec**: in order, issue references in commit messages or the PR body (`gh issue view <n>`), a path in $ARGUMENTS, or the matching item in `wiki/direction.md`. If none exists, the Spec pass reports "no spec".
2. **Rules**: `AGENTS.md`, plus every topic whose `AGENTS.md` row matches a touched area (`python3 scripts/ai-context.py <topic>`); area rules live there, not in the kernel. For example: `src/` decoding, expansion, REST output, variables, rendering or bundles → `fig-format` (plus `instances` for expansion, and `accuracy` when the change claims closer output); `.github/`, `scripts/install*`, `scripts/*dist*`, `npm/`, `Dockerfile.dist` or a version → `release`; `wiki/`, `AGENTS.md`, `scripts/ai-context.py` → `ai-context`.
3. **Concepts**: name each command, flag, MCP tool or parameter, emitted REST field, bundle file, error message, or behavior the diff adds or alters. The Consumers pass sweeps these.

## Step 3: Run five passes in parallel

Launch one subagent per pass in a single message, using your tool's default subagent model; do not name a model the tool may not have. If your tool has no subagents, run the passes yourself one after another. Give each the diff command, the context from Step 2, and its brief below. Each returns findings as `file:line`, a one-sentence claim, and a concrete scenario (input or state → wrong result). A finding without a scenario is not reported.

1. **Correctness**: bugs the change introduces. Wrong output, panics or stack overflows on unusual `.fig` input, broken error paths, anything written to stdout that corrupts JSON or the MCP protocol, path escapes when writing bundles or exports, and unchecked downloads in install or update paths. When an emitted field is read from another node (a page's map, a document table, a main component), check every scope below that node: `diff --node`, change tracking, `inspect` depth and node budgets, and bundles. Ignore style.
2. **Rules**: breaches of `AGENTS.md` and the loaded topics, such as a format change without measured evidence, Rust run outside Docker, a stale doc left behind, a design file committed, or versions out of step. Cite the file and rule.
3. **Spec**: requirements missing or partial, behavior nobody asked for, and requirements implemented wrongly. Quote the spec line for each.
4. **Consumers**: for each concept from Step 2, grep every place that describes or exposes it and report each one the diff did not update: the CLI `USAGE` text in `src/main.rs`, the MCP `TOOLS` table in `src/contract.rs`, the Pi tools and commands in `pi/index.ts`, the OpenCode (`opencode/`) and OMP (`omp/`) entries, `docs/README.md` and every `docs/README-*.md` locale (Commands table, `What the agent gets`), the lead of `README.md` and every root `README-*.md` (feature bullets and setup line) and its Limitations, the site landing page (`site/src/data.ts`, `site/src/pages/index.astro`), the preview viewer's handoff `context()` in `src/preview/viewer.js`, `skills/figlens/SKILL.md`, the wiki topics, `npm/` and `scripts/install*`, and the tests beside the changed code. Also report a new branch in decoding or rendering with no test.
5. **Cleanup**: code that re-implements an existing helper (name it), complexity a simpler form would remove, wasted work on hot paths (decoding, expansion, rendering per node), and fixes applied as a special case where the shared mechanism should change. Labelled as judgement calls.

## Step 4: Verify

For every finding, read the cited code yourself and decide:

- **CONFIRMED**: the scenario happens; you can name the line where it goes wrong.
- **PLAUSIBLE**: the code allows it, but it depends on state you could not check (often a `.fig` you do not have). Say which.
- **Dropped**: the code prevents it, the scenario is unsupported, or it duplicates another finding. Count drops; do not list them.

When a `.fig` in `samples/` can show the scenario, run it in Docker (`docker compose run --rm dev figlens ...`) instead of reasoning about it.

## Step 5: Report

Use the user's language. Keep the passes separate and do not rerank across them: a change can pass the spec and still break a rule.

```
## Correctness (n)
1. CONFIRMED path:line: claim. Scenario: ...
## Rules (n)
## Spec (n)   or: no spec
## Consumers (n)
## Cleanup (n)

Dropped: n. Not checked: <passes or areas skipped, and why>.
```

End with the single most severe confirmed finding per pass, or "clean".

With `fix`: apply the CONFIRMED findings, add a failing test first for each correctness fix, rerun the narrowest check that proves it, and report each finding as fixed, skipped (why), or no change needed.

## Rules

- Run no Rust toolchain on the host; checks run with `docker compose run --rm dev ...`.
- A finding is a claim until Step 4 confirms it. Never report an unverified finding as fact.
- Review the diff, not the whole crate. Pre-existing problems go in one line under "Not checked" as follow-ups.
