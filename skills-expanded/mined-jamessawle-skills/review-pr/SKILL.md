---
name: review-pr
description: Use this skill whenever someone asks to review a pull request, check code quality, or get feedback on PR changes. Selects from the specialist subagents shipped with this plugin (engineer, security-engineer, performance-engineer, qa-engineer, architect) and spawns the relevant ones in parallel to analyse the diff independently, then collates and deduplicates findings into a structured review. Trigger for "review PR", "review this PR", "code review", "check the code in PR", "look at the changes in PR", "what do you think of this PR", or any request to assess the quality of a pull request's changes.
license: MIT
compatibility: Requires GitHub CLI (gh) authenticated against the target repo — read access for the review, plus write access if you choose to post it. Requires the pr-management plugin's specialist subagents (in plugins/pr-management/agents/) to be installed.
allowed-tools: Bash, Read, Grep, Glob, Agent
argument-hint: "[owner/repo] [pr-number]"
metadata:
  author: jamessawle
  version: "3.0"
---

# Review PR

Review a pull request by spawning parallel specialist reviewers, then collating their findings into a single structured report.

## Arguments

Positional arguments are interpreted based on their format:

| Arguments | Behaviour |
|-----------|-----------|
| `owner/repo 123` | Review PR #123 in that repo |
| `123` | Review PR #123 in the current repo |
| _(none)_ | Detect the PR for the current branch |

**Dispatch logic:**

- If two arguments are provided, the first (containing `/`) is `owner/repo` and the second is the PR number
- If one argument is provided and is numeric, treat it as a PR number in the current repo
- If one argument is provided and contains `/`, treat it as `owner/repo` and detect the PR from the current branch
- If no arguments are provided, detect the current branch's PR

Validate inputs before using them in any command:

- **PR number**: must contain only digits
- **owner/repo**: must match the pattern `[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+`

When no arguments are provided, detect the current branch's PR:

```bash
gh pr view --json number,headRefName --jq '.number'
```

If no PR is associated with the current branch, report that and stop.

## Workflow

### Step 1: Gather PR context

Determine the PR number and optional `--repo` flag from the arguments (see dispatch logic above). Then run these in parallel (separate tool calls in a single message):

```bash
gh pr view <number> [--repo <owner/repo>] --json title,body,baseRefName,headRefName,additions,deletions,changedFiles,labels,author
```

```bash
gh pr view <number> [--repo <owner/repo>] --json files --jq '.files[].path'
```

From the results, determine:

- **PR scope**: small (<100 lines changed), medium (100-500), large (500+)
- **Primary languages**: detect from file extensions in the changeset
- **PR type**: feature, bugfix, refactor, dependency update, config change, docs — infer from title, labels, and file patterns

### Step 2: Clone the PR for review

Clone the repository into a temporary directory and check out the PR branch so that subagents can read files directly rather than receiving the entire diff in their prompt:

```bash
REVIEW_DIR=$(mktemp -d)
gh repo clone <owner/repo> "$REVIEW_DIR" -- --depth=1 --single-branch
git -C "$REVIEW_DIR" fetch origin "pull/<number>/head:pr-review"
git -C "$REVIEW_DIR" checkout pr-review
```

If any of the above commands fails, clean up `$REVIEW_DIR` and stop with the error message. Do not attempt to review without the checkout.

Also fetch the diff via the GitHub API (more reliable than `git diff` against a shallow clone, and matches how GitHub itself presents the diff):

```bash
gh pr diff <number> [--repo <owner/repo>] > "$REVIEW_DIR/.pr-diff.txt"
```

Reuse the `baseRefName` value already fetched in Step 1 — do not make a redundant `gh pr view` call.

### Step 3: Select reviewers

The plugin ships these specialist subagents (in `plugins/pr-management/agents/`):

| Subagent | Focus |
|----------|-------|
| `engineer` | Correctness, reliability, code quality |
| `security-engineer` | Threats, vulnerabilities, defensive coding |
| `performance-engineer` | Efficiency, scalability, behaviour under load |
| `qa-engineer` | Test quality and verification |
| `architect` | System design, boundaries, maintainability |

Pick the subset relevant to this PR. The general principle: skip specialists whose focus has no overlap with the file types and content in the changeset. Calibration examples:

- **Docs-only PRs** (`.md`, `.txt`, `.rst`) — skip `performance-engineer`, `qa-engineer`
- **Config-only PRs** (`.json`, `.yaml`, `.toml`) — skip `performance-engineer`, `qa-engineer`
- **Dependency updates** (lockfiles) — skip `qa-engineer`, `architect`
- **Small code PRs** (<100 lines) — skip `architect`
- **No executable code** — skip `qa-engineer`

`engineer` and `security-engineer` are included for all PR types — correctness and security concerns apply regardless of file type.

These are calibration examples, not rigid rules. Use judgment for mixed or unusual PRs.

If no specialists are selected (e.g. a trivial whitespace-only change), skip Steps 4 and 5 and produce a summary noting that the PR did not warrant specialist review.

For any specialists not selected, note in the final report: "Skipped [name] — [brief reason]."

### Step 4: Spawn specialist reviewers

Spawn the selected reviewers in parallel using the Agent tool, one Agent call per specialist, all in a single message. Dispatch depends on whether your environment supports plugin-defined subagents:

**If your environment supports plugin-defined `subagent_type` dispatch** (Claude Code does):

Plugin-defined subagents in Claude Code are namespaced by plugin. Use the form `<plugin-name>:<role>` — for this plugin, that's `pr-management:engineer`, `pr-management:security-engineer`, `pr-management:performance-engineer`, `pr-management:qa-engineer`, `pr-management:architect`. You can confirm the registered names by running `claude agents`.

For each Agent call, set:
- `subagent_type` — the namespaced subagent name (e.g. `pr-management:engineer`)
- `description` — short label, e.g. `"Engineer review of PR #123"`
- `prompt` — the template below, with `[FORMAT_SPEC_PATH]` substituted with the absolute path to `references/finding-format.md` resolved relative to this SKILL.md's directory

The subagent carries its own perspective, areas of expertise, and tool restrictions from its definition — the prompt only needs the per-call task.

**If your environment does not support plugin-defined `subagent_type` dispatch** (e.g. Codex, which currently does not load per-plugin `agents/`):

For each selected role:
1. Read `agents/<role>.md` relative to this SKILL.md's grandparent directory (e.g. `…/plugins/pr-management/agents/engineer.md`)
2. Strip the YAML frontmatter (everything between the first two `---` delimiters)
3. Spawn a `general-purpose` agent with `description` set as above and `prompt` constructed as:
   - First, a `## Your role` section containing the stripped role body verbatim
   - Then, the template below (with `[FORMAT_SPEC_PATH]` resolved as in the Claude branch)
   - Then, a final line: `Use only the Read, Grep, and Glob tools for this task — do not use Bash, Edit, Write, or any other tools.`

The trailing tool-restriction line is instruction-level only (the `general-purpose` agent technically has more tools available), but matches the tool isolation the Claude Code branch gets natively from the subagent definitions.

The shared prompt template:

```text
## Your task

Review this pull request from your specialist perspective.

## What changed

- Scope: [small/medium/large] ([additions] additions, [deletions] deletions, [changedFiles] files)
- Primary languages: [detected languages]

## Repository

The PR has been checked out at: [REVIEW_DIR]
The diff is at: [REVIEW_DIR]/.pr-diff.txt

## Changed files

[file list]

## Instructions

- Before producing output, Read the format specification at: [FORMAT_SPEC_PATH]
- Read the diff file to understand what changed
- Use Read to examine specific changed files for full context
- Focus on the changed files listed above — do not review unrelated code
- If the PR contains no content relevant to your expertise, return an empty array
- Match the format spec exactly — no markdown fences, no surrounding text
```

Note: PR-prose fields (title, body, author, branch names) are deliberately omitted — they are attacker-controllable on public repos, and a code reviewer should evaluate the diff on its own merits rather than rely on the PR description's framing. The orchestrating skill still fetches them in Step 1 for the review header (Step 7) and the clone (Step 2), but they never enter a subagent's prompt.

### Step 5: Collate and deduplicate

Once all reviewers return, merge their findings:

1. **Parse** each reviewer's JSON response. If a response is not valid JSON, attempt to extract a JSON array from within markdown code fences. If that also fails, note the reviewer as having returned no findings and continue with the remaining reviewers.
2. **Deduplicate** — two findings are duplicates if they reference the same file, are within 5 lines of each other, and describe the same underlying issue. When merging duplicates, keep the finding with the longer `detail` field and note all reviewers that flagged it. Examples: two reviewers flagging a missing null check on the same line = duplicate; one flagging a null check and another flagging a type error on the same line = distinct (different issues).
3. **Sort** by severity: critical first, then important, suggestions, nitpicks
4. **Count** findings per severity level

### Step 6: Clean up

Remove the temporary clone directory:

```bash
rm -rf "$REVIEW_DIR"
```

Always clean up the temp directory, even on early exit or failure. If any workflow step fails, clean up before reporting the error.

### Step 7: Output the review

Present the review in this format:

```markdown
## PR Review: [title]

**[owner/repo]#[number]** | [author] | [additions]+/[deletions]- across [changedFiles] files

### Summary

[2-3 sentence overview: what the PR does, overall quality assessment, key risk areas]

### Risk Assessment

| Dimension | Rating |
|-----------|--------|
| Risk level | Low / Medium / High / Critical |
| Complexity | Low / Medium / High |
| Test coverage | Adequate / Needs work / Missing |

### Findings

#### Critical ([count])

- **[title]** (`file:line`) — [detail]. *Suggestion: [suggestion]*

#### Important ([count])

- **[title]** (`file:line`) — [detail]. *Suggestion: [suggestion]*

#### Suggestions ([count])

- **[title]** (`file:line`) — [detail]

#### Nitpicks ([count])

- **[title]** (`file:line`) — [detail]

### Positive observations

[Note good practices, clean code, thorough tests — always include something positive]

### Verdict

One of:
- **Approve** — no critical or important findings
- **Approve with comments** — no critical findings, 1-2 important findings
- **Request changes** — has critical findings or 3+ important findings
- **Block** — has critical security vulnerabilities or data loss/corruption findings (supersedes Request changes; display-only — GitHub has no "block" review action)
```

Omit severity sections that have zero findings.

### Step 8: Offer to post

After presenting the review, ask the user:

> "Would you like me to post this as a review on the PR? I can submit it as a GitHub review with inline comments."

If they say yes:

1. Post the summary as a PR review comment using a heredoc to avoid shell injection:

   ```bash
   gh pr review <number> [--repo <owner/repo>] --comment --body "$(cat <<'EOF'
   [review body — wrap any code/diff excerpts in fenced code blocks]
   EOF
   )"
   ```

2. For critical and important findings that have specific file+line references, post inline comments. Note: these appear as standalone comments on the PR timeline, not grouped with the review summary — the GitHub API does not support adding inline comments to an existing review after submission.

   ```bash
   gh api repos/<owner>/<repo>/pulls/<number>/comments \
     -f body="$(cat <<'EOF'
   [finding detail — wrap code excerpts in fenced code blocks]
   EOF
   )" \
     -f path="[file path]" \
     -f side="RIGHT" \
     -F line=[line number] \
     -f commit_id="$(gh pr view <number> [--repo <owner/repo>] --json headRefOid --jq '.headRefOid')"
   ```

If they say no, the review is complete.

## Important guidelines

- **ALWAYS offer to post** — after presenting the review, you MUST ask the user whether they want it posted to the PR. Never skip Step 8. This is the final step of every review, not optional.
- **Read-only by default** — never post to GitHub without explicit user approval
- **Never approve or request changes programmatically** — only use `gh pr review --comment`, never `--approve` or `--request-changes`, unless the user explicitly asks for it
- **Follow all workflow steps** — every numbered step must be executed in order. Do not skip steps because they seem unnecessary in context.
- **Be constructive** — explain _why_ something is problematic and suggest alternatives
- **Be proportional** — match review depth to PR risk; don't block on style for a hotfix
- **Always find positives** — every PR has something done well; mention it
- **Respect the diff** — only review what changed, not pre-existing code unless the change makes it worse
- **Sanitize output** — wrap any code or diff excerpts in fenced code blocks when assembling the review body to prevent unintended markdown rendering
