---
name: git-insight
description: Analyze git commit history and summarize recent activity from a mission or project perspective. Use for commit summaries, daily or weekly progress reviews, author-specific work summaries, team activity reviews, release-note prep, or understanding what changed in a repository over a time window.
license: MIT
metadata:
  version: "1.0.0"
  template: references/report-template.md
---

# Git Insight

Analyze git commit history over a specified period and produce a concise, mission-focused activity summary. The goal is to help users understand what changed, who contributed, how work grouped into meaningful themes, and what the practical progress was.

## When to use

Use this skill when the user asks for git history analysis, including:

- "git insight"
- "commit summary"
- "what did I work on?"
- "today's commits"
- "this week's work"
- "weekly progress review"
- "team activity"
- "summarize recent changes"
- "prepare release notes from commits"

Do not use this skill for code review or root-cause debugging unless the user specifically wants history analysis as part of that work.

## Inputs to resolve

If the user did not specify these, ask one concise clarifying question before running broad history analysis:

- **Repository**: current repo by default if already inside one.
- **Date range**: examples: `today`, `yesterday`, `this week`, `last week`, `last 7 days`, explicit dates.
- **Author scope**: `all`, `me`, or a named author/email.
- **Branch/ref scope**: current branch by default; ask if the user likely means `origin/main`, a release branch, or all branches.
- **Merge commits**: include by default; use `--no-merges` if the user wants implementation-only activity.

Default only when safe:

- If the user says "this week" or "weekly", use the last 7 days unless their workspace convention says otherwise.
- If the user says "my commits", identify the author carefully instead of assuming `git config user.name` is correct.

## Privacy and sharing

Git history from private repositories can reveal project names, incidents, customers, security fixes, or internal roadmap details. Do not send summaries outside the current conversation or publish them without explicit approval. When creating public examples, use fictional commit subjects and contributors.

## Procedure

### 1. Confirm repository context

Check that the working directory is a git repository:

```bash
git rev-parse --show-toplevel
git status --short
```

If the user expects fresh remote history, fetch before analysis:

```bash
git fetch origin --prune
```

Do not mutate repository state. Avoid checkout, rebase, reset, or clean operations for this skill unless the user separately asks for them.

### 2. Resolve time window

Use explicit `--since` and `--until` values where possible:

```bash
git log --since="<start>" --until="<end>" --date=iso --pretty=format:"%h|%ad|%an|%ae|%s"
```

Useful examples:

```bash
git log --since="today 00:00" --date=iso --pretty=format:"%h|%ad|%an|%ae|%s"
git log --since="7 days ago" --date=iso --pretty=format:"%h|%ad|%an|%ae|%s"
git log --since="2026-06-01" --until="2026-06-30 23:59" --date=iso --pretty=format:"%h|%ad|%an|%ae|%s"
```

### 3. Resolve author scope

For `all`, do not add an author filter.

For `me`, inspect likely author identities before filtering:

```bash
git config user.name || true
git config user.email || true
git shortlog -sn --since="<start>" --until="<end>" HEAD
```

If GitHub CLI is available and authenticated, it can help identify the current GitHub user, but do not require it:

```bash
gh api user --jq '{login: .login, email: .email}'
```

Filter by the most reliable author name or email:

```bash
git log --since="<start>" --until="<end>" --author="<name-or-email>" --date=iso --pretty=format:"%h|%ad|%an|%ae|%s"
```

If multiple identities may belong to the same person, either ask which to include or combine them with multiple logs and deduplicate by commit hash.

### 4. Extract commit details and stats

Basic commit list with short stats:

```bash
git log --since="<start>" --until="<end>" <author-filter> --date=iso --pretty=format:"%h|%ad|%an|%ae|%s" --shortstat
```

Machine-friendlier commit list:

```bash
git log --since="<start>" --until="<end>" <author-filter> --date=iso --pretty=format:"%H%x09%h%x09%ad%x09%an%x09%ae%x09%s"
```

Total line changes:

```bash
git log --since="<start>" --until="<end>" <author-filter> --pretty=tformat: --numstat \
  | awk 'NF==3 {add+=$1; del+=$2} END {print "+"add" -"del}'
```

Files touched, useful for mission grouping:

```bash
git log --since="<start>" --until="<end>" <author-filter> --name-only --pretty=format:"commit %h %s"
```

Optional implementation-only view:

```bash
git log --no-merges --since="<start>" --until="<end>" <author-filter> --date=iso --pretty=format:"%h|%ad|%an|%ae|%s" --shortstat
```

### 5. Group commits into missions

Group semantically related commits into mission-level themes. Good grouping signals include:

- Shared issue/PR number.
- Shared prefix, feature area, package, app, service, or directory.
- Similar intent in commit subjects, such as `auth`, `billing`, `cache`, `observability`, `refactor`, `test`, or `release`.
- File paths touched by the commits.
- Branch naming conventions if visible in the repository.

If no strong themes are visible, use functional categories:

- Features
- Bug fixes
- Refactoring
- Tests and validation
- Documentation
- Chores and releases

Avoid overclaiming. If commit messages are vague, say that grouping is inferred from subjects/files and may need confirmation.

### 6. Produce the report

Prefer a compact Markdown report with:

1. Header: repository, date range, branch/ref, author scope, commit count, total line changes.
2. Mission overview: grouped missions with contributors, commits, and line changes.
3. Mission details: concise work items per mission.
4. Optional highlight: one short interpretation of progress.
5. Caveats: missing remote fetch, ambiguous authors, merge commits included/excluded, or unreliable line stats.

Use Markdown tables when the target surface renders them well. If the target surface is likely to mangle tables, use bullet lists instead.

See `references/report-template.md` for a reusable report shape.

## Output guidelines

- Keep mission names specific but not too long.
- Use `@name` or plain names consistently for contributors.
- Include commit hashes only when useful for auditability.
- Use comma formatting for numbers at or above 1,000.
- Keep work item descriptions concise.
- Separate confirmed facts from inferred interpretation.
- For release-note prep, rephrase internal commit language into user-facing changes and omit purely internal chores unless relevant.

## Failure modes

- **No commits found**: report the exact range/ref/author filter checked and suggest broadening the range.
- **Not a git repo**: ask for the repository path.
- **Ambiguous author**: show likely authors from `git shortlog` and ask which to include.
- **Huge history**: narrow the date range, branch, author, or path scope before generating a detailed report.
- **Binary/generated file noise**: mention that line stats may be inflated and focus on commit intent.
