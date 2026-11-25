---
name: claude-config-change-gate
description: Domain composer — gates git operations when claude auto-
    timestamped files (known_marketplaces.json, .last-cleanup) contain
    only trivial timestamp changes.
category: Git-Composer
---

# Claude Config Change Gate — Domain Composer

> **Skill ID:** `claude-config-change-gate`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A domain-specific git operation gate for repositories containing claude
auto-timestamped configuration files. It detects whether the only changes
to claude config files are trivial timestamp updates, and blocks git
operations (commit, push, merge, rebase) when a meaningful structural
change is detected.

**Files monitored:**

| File | Check Method | Ignored Keys |
| --- | --- | --- |
| `claude/plugins/known_marketplaces.json` | JSON structural comparison via base comparator | `lastUpdated` |
| `claude/.last-cleanup` | Regex: must contain only a valid ISO 8601 timestamp | N/A |

## Composition Rationale

This skill is a **domain composer at Layer 3** — the most specific layer
in the stacking. It composes:

| Layer | Skill | How |
| --- | --- | --- |
| Layer 0 | [`json-content-compare-ignore-keys`](../json-content-compare-ignore-keys/SKILL.md) | **Base primitive** — shells out to its Python script with `--ignore-keys lastUpdated` for JSON file comparison |
| Layer 2 | [`git-operation-blocking-hooks`](../git-operation-blocking-hooks/SKILL.md) | **Mechanism composer** — provides the global→repo hook chain, `lib.bash` dispatch, `git status` alias, blocking/bypass protocols |

Domain-specific additions owned by this skill:

- Concrete `scripts/check-claude-trivial.bash` (the `GATE_CHECK_SCRIPT`)
- Concrete `scripts/setup-hooks.bash` template (how to bootstrap this gate)
- Reference copy of `known_marketplaces.json` for snapshot seeding
- `.last-cleanup` ISO-timestamp regex validation

## Environment

| Requirement | Minimum |
| --- | --- |
| Python | 3.12+ (for base JSON comparator) |
| Shell | Bash 4+ (for check script and hooks) |
| Git | 2.x+ |

## Operational Logic

### 7.1 — Phase 1: Machine Setup

Follow [`git-operation-blocking-hooks` §Phase 1](../git-operation-blocking-hooks/SKILL.md#phase-1--machine-setup-one-time-per-developer).

Additionally, ensure the base Python script is accessible. The check
script discovers it via `JSON_COMPARE_SCRIPT` env var or a path anchored
on its own location:

### 7.2 — Phase 2: Repo Bootstrap

Create `scripts/setup-hooks.bash` at the repo root:

```bash
#!/bin/bash
set -euo pipefail

# 1. Activate repo hooks
bash scripts/setup-repo-hooks.bash

# 2. Register pre-flight alias
bash scripts/register-alias.bash

# 3. Wire the claude config check
export GATE_CHECK_SCRIPT="$PWD/scripts/check-claude-trivial.bash"

# 4. Seed baseline snapshot if first time
SNAPSHOT_FILE="scripts/.claude-trivial-snapshot"
if [ ! -f "$SNAPSHOT_FILE" ]; then
  cp scripts/reference/known_marketplaces.json "$SNAPSHOT_FILE"
  echo "[claude-gate] Snapshot seeded from reference"
fi
```

Place this file at the repo root and make it executable. The global
`post-checkout` hook discovers and execs it on every checkout.

### 7.3 — Phase 3: Normal Operation

All git operations flow through the check dispatch:

```text
git commit    → pre-commit  → lib.bash → check-claude-trivial.bash
git push      → pre-push    → lib.bash → check-claude-trivial.bash
git merge     → pre-merge-commit → lib.bash → check-claude-trivial.bash
git rebase    → pre-rebase  → lib.bash → check-claude-trivial.bash
git status    → alias       → lib.bash status → check + real status
```

### 7.4 — Phase 4: Check Logic Detail

The `check-claude-trivial.bash` script performs two checks:

**Check A — `claude/.last-cleanup`**

If the file exists, read its content. If the content matches the regex
`^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}` (ISO 8601 datetime prefix),
the change is trivial. If the content is anything else (empty, multiple
lines, non-timestamp text), the check blocks.

**Check B — `claude/plugins/known_marketplaces.json`**

If the file exists, shell out to the base Python script:

```bash
python3 json-content-compare-ignore-keys.py \
  --file claude/plugins/known_marketplaces.json \
  --ignore-keys lastUpdated
```

- First run: creates snapshot, exits 0 (allow).
- Subsequent runs: compare structural hash, excluding `lastUpdated`:
    - Hash matches → only timestamp changed → update snapshot → exit 0 (allow)
    - Hash differs → structural change detected → exit 1 (block)

### 7.5 — Phase 5: Bypass

When the gate incorrectly blocks (false positive) or a partial change
is intentional:

| Method | Effect |
| --- | --- |
| `git commit --no-verify` | Skips `pre-commit` and `pre-merge-commit` |
| `SKIP_GATE=1 git push` | Skips `pre-push` |
| `GATE_CHECK_SCRIPT="" git commit` | Disables the check entirely for one invocation |

### 7.6 — Phase 6: Recovery

**Snapshot corruption or mismatch:**

```bash
# Re-seed from reference
cp scripts/reference/known_marketplaces.json scripts/.claude-trivial-snapshot

# Verify the gate passes
bash scripts/check-claude-trivial.bash
echo $?   # should be 0
```

**Check script broken:**

```bash
# Temporarily disable
GATE_CHECK_SCRIPT="" bash scripts/githooks/lib.bash pre-commit

# Fix the script and retest
bash scripts/check-claude-trivial.bash
```

## Script Reference

| Script | Purpose | Invocation |
| --- | --- | --- |
| [`scripts/check-claude-trivial.bash`](scripts/check-claude-trivial.bash) | Main check — discover claude files, run JSON comparison + timestamp regex | Set as `GATE_CHECK_SCRIPT` in `setup-hooks.bash` |
| [`scripts/reference/known_marketplaces.json`](scripts/reference/known_marketplaces.json) | Clean-state reference for snapshot seeding | Referenced by `setup-hooks.bash` |

## Related Skills

| Skill | Relationship | Layer |
| --- | --- | --- |
| [`json-content-compare-ignore-keys`](../json-content-compare-ignore-keys/SKILL.md) | Composed — base JSON comparator | Layer 0 |
| [`git-operation-blocking-hooks`](../git-operation-blocking-hooks/SKILL.md) | Composed — blocking hook mechanism (which itself composes 3 Layer-1 skills) | Layer 2 |
| [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) | Complementary — after the gate passes, use this for the actual commit workflow | — |
| [`git-post-gitignore-untrack`](../git-post-gitignore-untrack/SKILL.md) | Complementary — after untracking auto-timestamped files, set up this gate | — |
| [`gitignore-rules`](../gitignore-rules/SKILL.md) | Complementary — `.gitignore` blocks untracked; this gate also blocks tracked-file commits | — |

## Verification

```bash
# 1. Test .last-cleanup regex
echo "2024-06-13T12:00:00Z" > /tmp/_cleanup_ok
echo "not a timestamp" > /tmp/_cleanup_bad

grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}' /tmp/_cleanup_ok \
  && echo "OK pass" || echo "OK fail"
grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}' /tmp/_cleanup_bad \
  && echo "BAD pass" || echo "BAD fail"

rm /tmp/_cleanup_ok /tmp/_cleanup_bad

# 2. Test JSON comparison (see json-content-compare-ignore-keys verification)
# 3. Run the check script in a test repo
cd /tmp && mkdir _claude_test && cd _claude_test
git init
mkdir -p claude/plugins
echo '{"lastUpdated":"2024-01-01T00:00:00Z","marketplaces":[]}' \
  > claude/plugins/known_marketplaces.json
echo "2024-01-01T00:00:00Z" > claude/.last-cleanup

export JSON_COMPARE_SCRIPT="$PWD/../json-content-compare-ignore-keys.py"
mkdir -p scripts && cp .../check-claude-trivial.bash scripts/
bash scripts/check-claude-trivial.bash
echo $?   # should be 0 (first run creates snapshot)

# Modify only the timestamp
echo '{"lastUpdated":"2024-06-13T12:00:00Z","marketplaces":[]}' \
  > claude/plugins/known_marketplaces.json
bash scripts/check-claude-trivial.bash
echo $?   # should be 0 (only timestamp changed)

# Modify structure
echo '{"lastUpdated":"2024-06-13T12:00:00Z","marketplaces":[{"id":"new"}]}' \
  > claude/plugins/known_marketplaces.json
bash scripts/check-claude-trivial.bash
echo $?   # should be 1 (structural change)

rm -rf /tmp/_claude_test
```
