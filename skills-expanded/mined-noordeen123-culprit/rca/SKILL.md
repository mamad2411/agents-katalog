---
name: rca
description: Root-cause analysis and pre-commit fix verification for a PR, branch, commit, or stack trace. Detects bugfix vs feature; for a bugfix finds the commit that introduced it (the suspect set, via git blame/log), its intent, the releases it shipped in, and whether a proposed fix is complete; for a feature maps the blast radius. Also yields a QA risk score, the tests to run, co-change gaps, and reviewers. Use when the user (or you, mid-task) asks "why did this break", "what introduced this bug", "root cause", "rca", "what does this change affect", "what's the risk", "which tests should I run", "did I forget to change anything", "is this fix complete", "verify my fix before I commit", or "find the culprit from this stack trace".
---

# Root-cause analysis + fix verification (culprit)

culprit is a deterministic, offline, read-only engine that does the git forensics
so you can reason about the result. This plugin installs its MCP server, so **prefer
the `culprit` MCP tools** below — they return structured JSON. If they are not
available, fall back to the `rca` / `culprit` CLI (same analysis, `--json` output).

The engine only runs `git` (diff/blame/log) and, when present, read-only `gh`. It
never modifies the repo or the PR.

## When to use

- "Why did this break / what introduced this regression" -> bugfix RCA (`analyze`).
- "Is this fix complete / verify my fix before committing" -> `verify_fix` on the diff.
- "What does this change affect / blast radius / what should I test" -> feature analysis.
- "How risky is this / safe to merge" -> `get_risk_score`.
- "Find the culprit from this crash" -> `from_trace` on the stack trace.

## MCP tools

- `analyze(repo, base?, head?, pr?)` — one-call analysis: bugfix vs feature, suspect
  set, intent, lifecycle, completeness, risk. Start here.
- `verify_fix(repo, proposed_diff, base?)` — check a not-yet-committed diff. Returns
  `verdict` (`complete` | `partial` | `risky`), `untouched_references`,
  `skipped_symbols`, `risk_level`, `adds_test`, `notes`.
- `find_suspects`, `classify_change`, `get_evolution`, `get_intent`,
  `check_completeness`, `get_test_impact`, `get_blast_radius`, `get_risk_score`,
  `from_trace` — drill into one signal.

## Workflow

### Bugfix RCA
1. `analyze` (or `find_suspects`) to rank the introducing commits.
2. Read the suspect commits' **actual diffs** and write the "why it broke"
   narrative. The engine gives you structure; you supply the reasoning.
3. `get_intent` / `get_evolution` when you need the author's original goal or the
   line-by-line history of the buggy range.

### Verify a fix before committing (yours or a subagent's)
1. `verify_fix` on the staged/proposed diff.
2. If `verdict` is `partial`, patch the `untouched_references` it names, then re-run.
3. If `risk_level` is not `low`: add the missing test (see `notes`), or review the
   `skipped_symbols` by hand if their contract changed.
4. Iterate until `verdict == complete`. Treat this as the gate before you commit.

## CLI fallback

If the MCP tools are absent:

```bash
rca --repo <path> --json          # current branch vs the configured/base branch
rca --last --json                 # just the latest commit ("the change I just made")
rca --pr 123 --json               # a specific PR (uses the PR's own base)
rca --trace - --json              # RCA from a stack trace on stdin
rca --verify-fix patch.diff       # check a diff; exits 0 if complete, 1 otherwise
```

Add `--base <ref>` to override the base branch (or pin it once in `.culprit.toml`).
