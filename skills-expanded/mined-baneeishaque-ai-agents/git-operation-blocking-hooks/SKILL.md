---
name: git-operation-blocking-hooks
description: Mechanism composer — integrates global hook bootstrap +
    repo hook chain + alias preflight into a gate that blocks git
    operations (commit/push/merge/rebase) when a check script fails.
category: Git-Composer
---

# Git Operation Blocking Hooks — Mechanism Composer

> **Skill ID:** `git-operation-blocking-hooks`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

This is a **prose-only composer skill** — it ships no scripts of its
own. It defines how to integrate three general infrastructure skills
into a complete git operation blocking gate:

| Layer | Skill | Role |
| --- | --- | --- |
| Layer 1 | [`git-global-hook-bootstrap`](../git-global-hook-bootstrap/SKILL.md) | One-time machine setup: `~/.git-hooks/` symlink + `post-checkout` |
| Layer 1 | [`git-repo-hook-chain`](../git-repo-hook-chain/SKILL.md) | Repo-level hooks: `core.hooksPath`, `lib.bash` dispatch, `pre-*` wrappers |
| Layer 1 | [`git-alias-preflight`](../git-alias-preflight/SKILL.md) | Alias chaining: `git status` → check + real status |

The composer answers: "which hooks block, which aliases run checks,
what is the bootstrap flow, how does any repo self-wire, how to bypass
and recover."

## Composition Rationale

This skill is a **mechanism composer**. It does NOT re-implement any
of the three general skills. Instead, it defines their orchestration:

1. **Bootstrap flow:** machine setup → global hook → repo bootstrap →
   hook dispatch → check execution.
2. **Blocking semantics:** which hooks block on check failure.
3. **Self-wire contract:** how any repository opts into the gate.
4. **Bypass protocols:** how to temporarily skip the gate.
5. **Recovery:** how to fix a broken check.

### End-to-End Bootstrap Chain

```text
┌────────────────────────────────────────────────────────────────┐
│ MACHINE SETUP (one-time, per developer):                       │
│ setup-global-hooks.bash (from git-global-hook-bootstrap)       │
│   1. ln -sf <repo>/dotfiles/git-hooks/  ~/.git-hooks/         │
│   2. git config --global core.hooksPath ~/.git-hooks           │
│                                                                │
│ Now ~/.git-hooks/ contains exactly one file: post-checkout     │
└────────────────────────────────────────────────────────────────┘
         │
         │ On EVERY checkout / clone of ANY repo:
         ▼
┌────────────────────────────────────────────────────────────────┐
│ GLOBAL HOOK: ~/.git-hooks/post-checkout                        │
│   REPO_ROOT=$(git rev-parse --show-toplevel)                   │
│   if [ -x "$REPO_ROOT/scripts/setup-hooks.bash" ]; then        │
│     exec bash "$REPO_ROOT/scripts/setup-hooks.bash"            │
│   fi                                                           │
│   exit 0  (no hooks == fine)                                   │
└────────────────────────────────────────────────────────────────┘
         │
         │ If the repo has scripts/setup-hooks.bash:
         ▼
┌────────────────────────────────────────────────────────────────┐
│ REPO BOOTSTRAP: scripts/setup-hooks.bash (idempotent)          │
│   1. bash .../setup-repo-hooks.bash   (from git-repo-hook-chain)│
│      → git config core.hooksPath scripts/githooks              │
│   2. bash .../register-alias.bash     (from git-alias-preflight)│
│      → git config alias.status "...lib.bash status"            │
│   3. export GATE_CHECK_SCRIPT="$PWD/scripts/<check>.bash"      │
│   4. Seed snapshot from reference/ if missing                  │
└────────────────────────────────────────────────────────────────┘
         │
         │ On every commit / push / status:
         ▼
┌────────────────────────────────────────────────────────────────┐
│ REPO HOOK or ALIAS → lib.bash dispatch:                        │
│   CALLER=$(basename "$1")                                      │
│   Run GATE_CHECK_SCRIPT                                        │
│   case "$CALLER" in                                            │
│     pre-*)  if check fails → BLOCK (exit 1)                    │
│     status) print result → exec git status                     │
│   esac                                                         │
└────────────────────────────────────────────────────────────────┘
```

### How Any Repository Self-Wires

Create a single executable file at the repo root:

**`scripts/setup-hooks.bash`**

```bash
#!/bin/bash
set -euo pipefail

# 1. Activate repo hooks
bash scripts/setup-repo-hooks.bash

# 2. Register pre-flight alias
bash scripts/register-alias.bash

# 3. Wire the check script
export GATE_CHECK_SCRIPT="$PWD/scripts/check-claude-trivial.bash"

# 4. Seed baseline snapshot if first time
if [ ! -f "scripts/.claude-trivial-snapshot" ]; then
  cp scripts/reference/known_marketplaces.json \
     scripts/.claude-trivial-snapshot
fi
```

That is the entire contract. The global `post-checkout` discovers this
file automatically on every checkout. No per-repo manual configuration
is needed beyond creating this file.

## Environment

| Requirement | Minimum |
| --- | --- |
| Shell | Bash 4+ |
| Git | 2.x+ |

**Dependencies:** This skill has no script files. It composes the three
Layer-1 skills above. Ensure those skills are available in the same
`.agents/skills/` tree.

## Operational Logic

### Phase 1 — Machine Setup (one-time per developer)

Follow [`git-global-hook-bootstrap`](../git-global-hook-bootstrap/SKILL.md#31--machine-setup-one-time)
section 3.1.

### Phase 2 — Clone / First Checkout (automatic)

Nothing to do. The global `post-checkout` hook fires on every checkout
and discovers `scripts/setup-hooks.bash`. See the End-to-End Bootstrap
Chain above.

### Phase 3 — Normal Operation

All git operations (commit, push, merge, rebase, status) run through
the check. On `pre-*` hooks, failure blocks the operation. On `status`,
failure is displayed but status output still appears.

### Phase 4 — Check Failure & Diagnosis

When a check fails (exit != 0):

1. **`pre-commit`/`pre-push`/`pre-merge-commit`/`pre-rebase`**: the
   operation is blocked. The user sees:

```text
[gate] BLOCKED: meaningful change detected (pre-commit)
[gate] Use --no-verify (commit) or SKIP_GATE=1 (push) to bypass
```

- **`git status`**: the check failure is displayed but `git status`
   still runs, so the user can see what changed:

```text
--- [gate preflight check] ---
[gate] BLOCKED: meaningful change detected (pre-commit)
--- gate exit: 1 ---

On branch main
Changes not staged for commit:
...
```

### Phase 5 — Bypass

Sometimes the check is a false positive or the user intentionally wants
to commit a partial change. Bypass mechanisms:

| Bypass | Effect |
| --- | --- |
| `git commit --no-verify` | Skips `pre-commit` and `pre-merge-commit` hooks |
| `SKIP_GATE=1 git push` | Skips `pre-push` hook (check the env var in lib.bash) |
| `git -c core.hooksPath=/dev/null commit` | Skips ALL hooks (global override) |

### Phase 6 — Recovery

If the check script itself is broken (syntax error, missing dependency):

1. Fix the check script.
2. The bypass mechanisms above allow operations in the meantime.
3. Re-seed the snapshot if corrupted:

   ```bash
   rm -f scripts/.claude-trivial-snapshot
   bash scripts/setup-hooks.bash   # re-seeds from reference
   ```

4. Verify the fix:

   ```bash
   GATE_CHECK_SCRIPT="$PWD/scripts/check-claude-trivial.bash"
   export GATE_CHECK_SCRIPT
   bash scripts/githooks/lib.bash pre-commit
   ```

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`claude-config-change-gate`](../claude-config-change-gate/SKILL.md) | Domain composer — composes this mechanism with the JSON-compare-ignore-keys base primitive for claude config files. Provides the concrete `check-claude-trivial.bash` script. |

## Related Skills

| Skill | Relationship | Layer |
| --- | --- | --- |
| [`git-global-hook-bootstrap`](../git-global-hook-bootstrap/SKILL.md) | Composed — provides machine-level hook setup | Layer 1 |
| [`git-repo-hook-chain`](../git-repo-hook-chain/SKILL.md) | Composed — provides repo-level hook dispatch | Layer 1 |
| [`git-alias-preflight`](../git-alias-preflight/SKILL.md) | Composed — provides pre-flight alias pattern | Layer 1 |
| [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) | Complementary — run this composer FIRST to verify the gate passes, then run atomic commit construction for the actual commit workflow. | — |

## Verification

```bash
# 1. Confirm the bootstrap chain is documented
#    (this file — the End-to-End Bootstrap Chain section above)

# 2. Simulate a full bootstrap in a test repo
mkdir -p /tmp/_gate-test/scripts/githooks /tmp/_gate-test/dotfiles/git-hooks
cp scripts/setup-repo-hooks.bash /tmp/_gate-test/scripts/
cp scripts/register-alias.bash /tmp/_gate-test/scripts/
cp scripts/githooks/lib.bash /tmp/_gate-test/scripts/githooks/
for h in pre-commit pre-push pre-merge-commit pre-rebase; do
  cp "scripts/githooks/$h" "/tmp/_gate-test/scripts/githooks/$h"
done

# Create minimal setup-hooks.bash
cat > /tmp/_gate-test/scripts/setup-hooks.bash << 'EOF'
#!/bin/bash
set -euo pipefail
bash scripts/setup-repo-hooks.bash
bash scripts/register-alias.bash
EOF
chmod +x /tmp/_gate-test/scripts/setup-hooks.bash

# Verify the chain works
cd /tmp/_gate-test
git init
bash scripts/setup-hooks.bash
git config core.hooksPath
git config alias.status

# Cleanup
rm -rf /tmp/_gate-test
```
