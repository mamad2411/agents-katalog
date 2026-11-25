---
name: github-repo-commit-fetch
description: Base skill — read-only fetch primitives for GitHub repo data via the `gh api` CLI. Owns four scripts (list recent commits, fetch one commit's details, fetch a file at a specific ref, fetch the latest release) that higher-level skills compose into auditing, archaeology, PR-review, supply-chain, and tool-version-freshness workflows. Pure stdlib Python, zero pip dependencies.
category: GitHub-Automation
---

# GitHub Repo Commit Fetch Skill (v1)

> **Skill ID:** `github-repo-commit-fetch`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base (per [`skill-factory` §2.0 Layering Decision](../skill-factory/SKILL.md))

## 1. When to Apply

Use this skill — or a higher-level composer of it — whenever the agent must
read GitHub repo data WITHOUT cloning the repo, via `gh api`. Specifically:

- "What are the N most recent commits on `<repo>`?"
- "What files did commit `<sha>` touch, and what was its message?"
- "Give me the file `<path>` exactly as it existed at ref `<sha>`."
- "What is the latest (non-prerelease) release tag for `<repo>`?"

**Anti-trigger:** If the agent already has a local clone and wants
hunk-level diffs, use plain `git log` / `git show` / `git cat-file` —
those are richer and offline. This skill exists for the no-clone case
(e.g., auditing a separate repository the workflow lives in).

## 2. Why `gh api` + Python (not `gh` flag soup, not raw curl)

| Option | Verdict | Reason |
| --- | --- | --- |
| `gh api ... --jq '...'` ad-hoc one-liners | ⚠️ Works | jq quoting across PowerShell / bash / inline-tool contexts is hostile; results not reusable |
| `gh repo view --json files` | ❌ Insufficient | No per-commit file list; cannot pin to a ref |
| Raw `curl https://api.github.com/...` | ⚠️ Possible | Requires manual auth-header plumbing; see [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md) for that path |
| Python wrapping `gh api` | ✅ Adopted | UTF-8 by default, structured JSON output, argparse, zero pip deps, matches sibling skill [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) precedent |

Language tier: **Python 3 (Tier 1)** per
[`scripting-language-selection-rules.md` §2](../../../ai-agent-rules/scripting-language-selection-rules.md).
Interpreter sourced via `mise` per workspace convention (see [`mise-tool-management`](../mise-tool-management/SKILL.md)).

## 3. Required Inputs

- `gh` CLI installed and authenticated (`gh auth status` clean). If absent,
  fall back to [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md).
- Python 3.10+ on PATH (or invoked directly via the mise-pinned path).

## 4. Operational Logic

### 4.1 Common invocation pattern

```bash
SCRIPTS_DIR=.agents/skills/github-repo-commit-fetch/scripts
```

### 4.2 Primitive scripts (catalogue)

| Script | Purpose | Required args | Output |
| --- | --- | --- | --- |
| [`scripts/list-commits.py`](scripts/list-commits.py) | List N most recent commits on the default (or specified) branch, with optional path filter. | `--repo owner/name` | JSON array of `{sha, short, date, author, message}` |
| [`scripts/commit-details.py`](scripts/commit-details.py) | Fetch one commit's full metadata: author, date, message, list of changed files with status + additions + deletions. `--files-only` reduces to a bare filename list. | `--repo`, `--sha` | JSON object (or filename lines with `--files-only`) |
| [`scripts/fetch-file-at-ref.py`](scripts/fetch-file-at-ref.py) | Resolve the contents API's `download_url` for `<path>@<ref>` and stream the body to `<out>` using `urllib` (no `curl` pipeline, no shell quoting). | `--repo`, `--ref`, `--path`, `--out` | `OK: <path> (N bytes) from <url>` on stdout |
| [`scripts/latest-release.py`](scripts/latest-release.py) | Fetch the latest published (non-prerelease) GitHub release for `<repo>` — the backend-native truth when auditing a tool pinned via a mise `github:` backend. | `--repo owner/name` | JSON object `{tag_name, name, published_at}` |

All scripts return exit code `0` on success, `1` on `gh`/API failure,
`2` on config error. All emit JSON to stdout (where applicable),
diagnostics to stderr — safe to pipe.

### 4.3 End-to-end example: did the latest scheduled backup include my schema change?

```bash
SCRIPTS_DIR=.agents/skills/github-repo-commit-fetch/scripts
REPO=owner/backup-repo

# 1. Find the most recent backup commit.
SHA=$(python3 "$SCRIPTS_DIR"/list-commits.py --repo $REPO --limit 1 | python3 -c 'import json,sys;print(json.load(sys.stdin)[0]["short"])')

# 2. What file did that commit touch?
python3 "$SCRIPTS_DIR"/commit-details.py --repo $REPO --sha $SHA --files-only
# -> db_backups/foo.sql

# 3. Download the file at that exact ref and verify a string is present.
python3 "$SCRIPTS_DIR"/fetch-file-at-ref.py --repo $REPO --ref $SHA \
    --path db_backups/foo.sql --out /tmp/backup.sql
grep -c "ENGINE=InnoDB" /tmp/backup.sql
```

## 5. Composition by Higher-Level Skills

| Composer | Uses (this skill's scripts) | Purpose |
| --- | --- | --- |
| [`github-actions-run-audit`](../github-actions-run-audit/SKILL.md) | `list-commits.py`, `commit-details.py`, `fetch-file-at-ref.py` | Verify that a workflow run actually committed the expected artifact (e.g., periodic mysqldump backup contains today's DDL change). |
| [`mise-tool-management`](../mise-tool-management/SKILL.md) | `latest-release.py` | Tier-2 backend-native freshness probe (§2.2.2): supplies the latest `github:` release tag to compare against `mise ls-remote` during tool install / update. |

When inlined by a composer, scripts MUST be invoked via a relative path
anchored to the composer's location, per
[`ai-rule-standardization-rules.md` §2 Layered Composition Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md).

## 6. Composition by This Skill (downstream)

This skill composes with:

- [`github-rest-api-fallback`](../github-rest-api-fallback/SKILL.md) — the
  REST-without-`gh` fallback if the `gh` CLI is unavailable or unauthenticated.
- [`mise-tool-management`](../mise-tool-management/SKILL.md) — interpreter pinning.
- [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) —
  for capturing fetched-file output to `scratch/`.

## 7. Prohibited Behaviors

- Inlining `jq` projections directly in agent prose / multi-shell heredocs
  when this skill's scripts already cover the case.
- Calling `curl` against `https://raw.githubusercontent.com/...` from prose
  when `fetch-file-at-ref.py` exists — the script handles redirect, error
  surfaces, byte-safe write, and parent-dir creation.
- Hard-coding GitHub tokens in scripts — `gh` already owns auth.
- Probing private repos without checking `gh auth status` first.
