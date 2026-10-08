---
name: rca
description: Root-cause analysis and QA review for a PR, branch, or stack trace. Detects bugfix vs feature, then for a bugfix finds the commit that introduced the bug (the suspect set, via git blame/log), the bug's life story (intent, releases it shipped in, hotspot recurrence, fix completeness), and explains why it broke; for a feature maps the blast radius. Also yields a QA risk score, the tests to run, co-change ("did you forget X?"), and suggested reviewers. Use when the user asks "why did this break", "what introduced this bug", "root cause", "rca", "what does this PR affect", "what's the risk of this change", "which tests should I run", "did I forget to change anything", or "find the culprit from this stack trace".
---

<!--
  TEMPLATE - copy this into your repo at .claude/skills/rca/SKILL.md and replace the
  placeholders below. culprit is a standalone CLI; this skill is just one frontend over it.

    <REPO_PATH>     absolute path to the repo to analyze (often "." / the current repo)
    <BASE_BRANCH>   the branch your work is cut from (e.g. origin/main, origin/develop)
    <RCA>           how you invoke culprit (see "Invoking culprit" below)

  Pin <BASE_BRANCH> once in a `.culprit.toml` at the repo root (`base = "origin/main"`)
  so you can drop --base entirely. The engine is read-only - it only runs git
  (diff/blame/log) and, when available, gh pr (read-only). It never modifies the repo or PR.

  NOTE: On Claude Code, the one-command plugin bundles this skill AND the MCP server:
      /plugin marketplace add noordeen123/culprit
      /plugin install culprit@culprit
  This template is for a non-plugin setup or another agent.

  If your agent supports MCP (Claude Code, Cursor, Windsurf, VS Code, Codex CLI,
  Zed, Continue, Cline, Amazon Q, Goose, or any MCP SDK client), the MCP server
  integration is simpler and more capable than this skill. Install with:
      pip install "culprit[mcp]"
  Then add to your client's MCP config:
      { "mcpServers": { "culprit": { "command": "culprit-mcp" } } }
  All 11 culprit tools (including verify_fix) then appear natively without needing this file.
  See https://github.com/noordeen123/culprit#use-in-claude-code-or-any-agent
-->

# RCA (Root Cause Analysis) + QA review

Runs the deterministic **culprit** engine to produce a structured analysis +
markdown skeleton, then **you** write the "why it broke" / risk narrative by
reading the actual diffs of the suspect commits.

## Invoking culprit (`<RCA>`)

- Installed (`pip install culprit`): `rca` (or `culprit`).
- From a checkout, no install: `PYTHONPATH=/path/to/culprit python3 -m culprit.cli`.

The examples below write `<RCA>` for whichever form you use, and `--repo <REPO_PATH>`
(omit it when running from inside the repo - it defaults to the current directory).

## When to use

- "Why did this break / what introduced this regression / root cause" → bugfix RCA.
- "What does this PR affect / blast radius / what should I test" → feature analysis.
- "How risky is this change / is it safe to merge" → the QA risk score (+ `--fail-on` gate).
- "Which tests should I run for this change" → `--select-tests`.
- "Find the culprit from this crash / stack trace" → `--trace` (no fix or PR needed).
- Given a PR number, the current branch, or a pasted stack trace.

## Workflow

### 1. Run the engine (get structured result + skeleton)

```bash
<RCA> --repo <REPO_PATH> --no-save --json                       # current branch vs the configured/base branch
<RCA> --repo <REPO_PATH> --last --no-save --json                # just the latest commit ("the change I just made")
<RCA> --repo <REPO_PATH> --pr 123 --no-save --json              # a specific PR (uses the PR's own base)
<RCA> --repo <REPO_PATH> --base <BASE_BRANCH> --no-save --json  # override the base explicitly
```

Pick the scope to the user's intent: `--last` for "why did my latest change break
X"; the default (vs base) for "what does this whole branch affect". A long-lived
branch can be many commits ahead of the base - the engine caps blame at 150 files
and notes it.

- `--json` gives the structured result; drop it for the markdown skeleton.
- **Always use `--mode harness`** (the default) inside Claude Code - you do the
  reasoning. `--mode api` is for the standalone CLI (needs `ANTHROPIC_API_KEY`).

### 2. Read the structured result

- `classification.verdict` is **advisory** (`bugfix` / `feature` / `unknown`) with
  `evidence` - make the final call yourself from the diff.
- `risk` (always present): `{score 0-100, level, factors[]}` - the headline QA score
  over test gap, completeness, hotspot, blast radius, churn. Each factor has a `detail`.
- `test_impact.tests`: existing tests that reach the change (what to re-run).
- `coupling.missed`: files that usually change **with** the touched ones but aren't in
  this diff ("did you forget X?"). `owners`: suggested reviewers.

- **Bugfix** → `bugfix.suspects`: ranked commits that last touched the changed lines
  (`hash`, `author`, `subject`, `pr_number`, `weight`, `in_base`). Plus the life story:
  - `suspects[0].intent`: the introducing commit's `body`, its `pr` (title/body), and
    `linked_issues` - *what the author was trying to do*.
  - `lifecycle`: `releases` the bug shipped in, `commits_span`, `recurrence` (`is_hotspot`).
  - `completeness`: `untouched_count` (other references the fix missed), `adds_test`, `is_revert`.

  > **⚠ Self-suspect guard - check this first.** If `bugfix.origin_on_branch` is `true`,
  > the prime suspect is a commit **on the current branch** (part of this very change -
  > e.g. `--last` over your own previous commit). It is **not** the bug's origin. Do not
  > present it as "when it broke"; say so and re-run against the target branch:
  > `--base <bugfix.trunk>`. A suspect with `in_base: true` is a real origin in the
  > target history; `in_base: false` is branch-local.

- **Feature** → `feature.dependents`, `covering_tests`, `high_risk`.

### 3. Write the narrative (only you can do this)

For the top 1-2 suspects, inspect the introducing change:

```bash
git -C <REPO_PATH> show <suspect_hash> -- <file>
git -C <REPO_PATH> log -L <start>,<end>:<file> <base_sha>   # evolution of the buggy lines
```

Produce the bug's life story: **symptom → introduced (quote `intent`; how that change
broke it) → lived (how long / which `releases`; is it a `hotspot`?) → root cause (the
commit, hash + why; contrast stated intent vs effect) → fixed (does it fully address the
cause, or does `completeness.untouched_count` leave call sites unpatched? `adds_test`?)
→ prevent (the test gap).** Cite hashes/paths from the data; never invent commits or files.

For a **feature**: the real affected areas, a risk ranking (lean on `high_risk` +
dependent counts), and the test surface to exercise (`covering_tests` + dependents).

### 4. Present

Lead with the verdict and **QA risk** (level + the factors that drove it), then the prime
suspect (or top affected areas) and the "why", then next steps: what to re-test
(`test_impact.tests`), fix completeness, co-change you may have missed (`coupling.missed`),
and reviewers (`owners`).

### 5. (Optional) Visual HTML report

```bash
# write your step-3 narrative to a markdown file, then embed it:
<RCA> --repo <REPO_PATH> --pr 123 --force bugfix --no-save \
  --html /tmp/rca-123.html --narrative-file /tmp/rca-narrative.md --open
```

One self-contained file (no CDN, opens offline). It opens with a pinned **Summary**
(verdict, when-it-broke, risk, do-next) and a **risk banner**; the timeline collapses
earlier history by default. The narrative fills the "Analysis" section.

### 6. (Optional) QA mode - gate, test selection, stack-trace RCA

```bash
<RCA> --repo <REPO_PATH> --last --fail-on high                 # CI gate: non-zero exit when risk is high
<RCA> --repo <REPO_PATH> --last --select-tests                 # tests to run for this change
<RCA> --repo <REPO_PATH> --last --coverage coverage/lcov.info --json   # pinpoint uncovered changed lines
<RCA> --repo <REPO_PATH> --trace /tmp/crash.txt --html /tmp/rca.html --open   # RCA from a stack trace
```

For an interactive run (branch/base picker, same report in-page):
`<RCA> serve --repo <REPO_PATH>` → http://127.0.0.1:8722.

## Notes / gotchas

- **Self-suspect / `origin_on_branch`:** common with `--last` (the base is your own
  previous commit). Don't report a branch-local commit as "when it broke" - re-run
  against `--base <BASE_BRANCH>`.
- **Base branch:** pin it in `.culprit.toml` (`base = "..."`) or `CULPRIT_BASE`. Don't
  use a branch that's thousands of commits behind your line.
- **Big divergence:** a branch far ahead of base yields a large changeset; the engine
  caps blame at 150 files. Use `--last` or `--pr N` for a focused analysis.
- **Pure-addition fixes** (a guard added, nothing removed): the engine blames the
  surrounding context and notes it - treat those as "where the gap was".
- **`unknown` classification** falls through to the bugfix path; override with
  `--force bugfix|feature` if you already know.
